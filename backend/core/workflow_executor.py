"""
Ejecutor de Flujos de Trabajo
Orquesta la ejecución de pasos definidos en un Workflow utilizando los servicios reales.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from logging import Logger

from backend.core.workflow_engine import Workflow, WorkflowStep, ActionType, StepStatus
from backend.services.pdf_merger import PDFMerger
from backend.services.pdf_splitter import PDFSplitter
from backend.services.pdf_converter import PDFConverter
from backend.services.pdf_compressor import PDFCompressor
from backend.services.pdf_security import PDFSecurity
from utils.logger import get_logger
from config.settings import settings

class WorkflowExecutor:
    """
    Ejecuta un Workflow paso a paso, gestionando el flujo de datos entre operaciones.
    """
    
    def __init__(self, logger: Optional[Logger] = None):
        self.logger = logger or get_logger(__name__)
        
        # Inicializar servicios (Lazy instantiation podría ser mejor si son pesados, 
        # pero para estos servicios ligeros está bien)
        self.merger = PDFMerger(self.logger)
        self.splitter = PDFSplitter(self.logger)
        self.converter = PDFConverter(self.logger) # Converter ya no inyecta settings en init, usa global o params
        self.compressor = PDFCompressor(self.logger) # Compressor no inyecta settings en init
        self.security = PDFSecurity(self.logger)

    def execute_workflow(
        self, 
        workflow: Workflow, 
        base_output_dir: str,
        progress_callback: Optional[Callable[[str, int], None]] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta todos los pasos pendientes en el workflow.
        
        Args:
            workflow: Objeto Workflow con los pasos a ejecutar.
            base_output_dir: Directorio raíz para guardar resultados.
            progress_callback: Función(step_id, percent) para feedback.
            
        Returns:
            Review de la ejecución.
        """
        self.logger.info(f"Iniciando ejecución de Workflow ID: {workflow.id}")
        
        context = {} # Almacena resultados intermedios {step_id: output_path}
        results = []
        
        total_steps = len(workflow.steps)
        
        for i, step in enumerate(workflow.steps):
            if step.status == StepStatus.COMPLETED:
                continue
                
            self.logger.info(f"Ejecutando paso {i+1}/{total_steps}: {step.action.value}")
            step.status = StepStatus.PENDING # Marcar en proceso si tuviéramos ese estado
            
            try:
                # 1. Resolver Inputs
                # Si el step tiene 'input_source' apuntando a un paso anterior, lo resolvemos
                input_path = self._resolve_input(step.params, context)
                if not input_path:
                     # Si no hay input resuelto por contexto, debe venir en params['input_path']
                     # o ser manejado por la lógica específica del paso
                     input_path = step.params.get('input_path')

                if not input_path and step.action != ActionType.MERGE: 
                    # Merge toma una lista, manejado distinto
                    raise ValueError(f"No se pudo determinar el archivo de entrada para el paso {step.id}")

                # 2. Preparar Output
                output_dir = os.path.join(base_output_dir, str(workflow.id))
                settings.ensure_directories() # Asegurar que la estructura base existe
                Path(output_dir).mkdir(exist_ok=True, parents=True)
                
                # Nombre de salida genérico
                output_filename = f"step_{i+1}_{step.action.value}"
                # Intentar mantener extensión o adivinarla
                ext = ".pdf"
                if step.action == ActionType.CONVERT:
                    fmt = step.params.get('format', 'docx')
                    if fmt == 'docx': ext = '.docx'
                    elif fmt in ['jpg', 'png']: ext = '' # Es un directorio para imágenes
                
                output_path = os.path.join(output_dir, f"{output_filename}{ext}")

                # 3. Ejecutar Acción
                step_result = self._execute_step_action(step, input_path, output_path)
                
                # 4. Actualizar Estado y Contexto
                step.status = StepStatus.COMPLETED
                
                # Guardar el path resultante para el siguiente paso
                # Nota: Algunos pasos devuelven un dict con 'output_path'
                final_output = step_result.get('output_path', output_path)
                context[step.id] = final_output
                
                results.append({
                    "step_id": step.id,
                    "status": "success",
                    "output": final_output
                })
                
                if progress_callback:
                    progress_callback(step.id, 100)
                    
            except Exception as e:
                self.logger.error(f"Error en paso {step.id}: {e}", exc_info=True)
                step.status = StepStatus.FAILED
                results.append({
                    "step_id": step.id,
                    "status": "failed",
                    "error": str(e)
                })
                # Detener ejecución en cascada
                raise e

        return {
            "workflow_id": workflow.id,
            "results": results,
            "final_output": context.get(workflow.steps[-1].id) if workflow.steps else None
        }

    def _resolve_input(self, params: Dict, context: Dict) -> str:
        """Resuelve referencias dinámicas a pasos anteriores"""
        source = params.get('input_source')
        if source and isinstance(source, str) and source.startswith("step_ref:"):
            ref_id = source.split(":")[1]
            if ref_id in context:
                return context[ref_id]
        return None

    def _execute_step_action(self, step: WorkflowStep, input_path: str, output_path: str) -> Dict:
        """Despacha la ejecución al servicio correspondiente"""
        
        params = step.params
        
        if step.action == ActionType.MERGE:
            # Merge es especial, requiere lista de inputs
            # Si viene de un paso anterior, asumimos que ese paso produjo una lista O 
            # que queremos unir el resultado anterior con algo más.
            # Por simplicidad en v5: Merge suele ser el primer paso, tomando lista explícita.
            inputs = params.get('input_paths')
            if not inputs:
                 raise ValueError("Action MERGE requiere 'input_paths'")
            
            return self.merger.merge_pdfs(inputs, output_path)
            
        elif step.action == ActionType.SPLIT:
            # Requiere modo de split
            # Por defecto simple split o range
            return self.splitter.split_by_range(input_path, output_path, params.get('range', 'all'))
            
        elif step.action == ActionType.CONVERT:
            target_fmt = params.get('format', 'docx')
            if target_fmt == 'docx':
                return self.converter.pdf_to_word(input_path, output_path)
            elif target_fmt in ['jpg', 'png']:
                # Output path para imágenes debe ser un directorio
                out_dir = output_path + "_images" # Hack simple par evitar colisión archivo/dir
                return self.converter.pdf_to_images(
                    input_path, 
                    out_dir, 
                    image_format=target_fmt.upper()
                )
            elif target_fmt == 'pdf':
                 # Word a PDF
                 return self.converter.word_to_pdf(input_path, output_path)
                 
        elif step.action == ActionType.COMPRESS:
            level = params.get('level', 'medium')
            return self.compressor.compress_pdf(input_path, output_path, level)
            
        elif step.action == ActionType.SECURITY:
            mode = params.get('mode', 'encrypt')
            pwd = params.get('password', 'default123') # ! Inseguro, solo prototipo
            if mode == 'encrypt':
                return self.security.encrypt_pdf(input_path, output_path, pwd)
            else:
                return self.security.decrypt_pdf(input_path, output_path, pwd)
                
        else:
            raise NotImplementedError(f"Acción {step.action} no implementada en Executor")
