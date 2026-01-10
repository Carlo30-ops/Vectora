"""
Ejecutor de Flujos de Trabajo
Orquesta la ejecución de pasos definidos en un Workflow utilizando los servicios reales.
"""
import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
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
        
        # Inicializar servicios
        self.merger = PDFMerger(self.logger)
        self.splitter = PDFSplitter(self.logger)
        self.converter = PDFConverter(self.logger)
        self.compressor = PDFCompressor(self.logger)
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
        
        # Asegurar directorio base
        base_path = Path(base_output_dir) / str(workflow.id)
        try:
            settings.ensure_directories()
            base_path.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            self.logger.error(f"Error creando directorio de workflow: {e}")
            raise

        for i, step in enumerate(workflow.steps):
            if step.status == StepStatus.COMPLETED:
                continue
                
            self.logger.info(f"Ejecutando paso {i+1}/{total_steps}: {step.action.value}")
            step.status = StepStatus.PENDING 
            
            try:
                # 1. Resolver Inputs
                input_path = self._resolve_input(step.params, context)
                
                # Fallback a params directos si no se resolvió
                if not input_path:
                    input_path = step.params.get('input_path')
                    
                # Validación específica para MERGE (que requiere lista)
                if step.action == ActionType.MERGE:
                    # Para merge, input_path podría ser una lista si viene de params
                    # O si viene de context, podría ser un solo archivo (que no tiene sentido para merge unario, pero bueno)
                    # Aquí asumiremos que si viene de context, es UN archivo que se quiere unir con algo más?
                    # Simplificación: Merge suele ser el inicio. Checkear 'input_paths' list.
                    if not input_path:
                        input_path = step.params.get('input_paths')

                if not input_path: 
                    raise ValueError(f"No se pudo determinar el archivo de entrada para el paso {step.id}")

                # 2. Preparar Output
                output_filename = f"step_{i+1}_{step.action.value}"
                
                # Determinar extensión y si es directorio
                is_dir_output = False
                ext = ".pdf"
                
                if step.action == ActionType.CONVERT:
                    fmt = step.params.get('format', 'docx')
                    if fmt == 'docx': ext = '.docx'
                    elif fmt in ['jpg', 'png']: 
                        ext = '' 
                        is_dir_output = True
                
                if is_dir_output:
                    output_path = base_path / f"{output_filename}_images"
                    # Limpiar si existe para evitar mezcla de runs anteriores
                    if output_path.exists():
                        shutil.rmtree(output_path)
                    output_path.mkdir()
                else:
                    output_path = base_path / f"{output_filename}{ext}"

                # 3. Ejecutar Acción
                # Convertimos paths a string para compatibilidad con servicios legacy
                step_result = self._execute_step_action(
                    step, 
                    str(input_path) if not isinstance(input_path, list) else [str(p) for p in input_path], 
                    str(output_path)
                )
                
                # 4. Actualizar Estado y Contexto
                step.status = StepStatus.COMPLETED
                
                # Guardar el path resultante para el siguiente paso
                final_output = step_result.get('output_path', str(output_path))
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

    def _resolve_input(self, params: Dict, context: Dict) -> Optional[str]:
        """Resuelve referencias dinámicas a pasos anteriores"""
        source = params.get('input_source')
        if source and isinstance(source, str) and source.startswith("step_ref:"):
            ref_id = source.split(":")[1]
            if ref_id in context:
                return context[ref_id]
        return None

    def _execute_step_action(self, step: WorkflowStep, input_path: Any, output_path: str) -> Dict:
        """Despacha la ejecución al servicio correspondiente"""
        
        params = step.params
        
        if step.action == ActionType.MERGE:
            # input_path debe ser lista
            if not isinstance(input_path, list):
                 raise ValueError("Action MERGE requiere una lista de 'input_paths'")
            
            return self.merger.merge_pdfs(input_path, output_path)
            
        elif step.action == ActionType.SPLIT:
            return self.splitter.split_by_range(input_path, output_path, params.get('range', 'all'))
            
        elif step.action == ActionType.CONVERT:
            target_fmt = params.get('format', 'docx')
            if target_fmt == 'docx':
                return self.converter.pdf_to_word(input_path, output_path)
            elif target_fmt in ['jpg', 'png']:
                return self.converter.pdf_to_images(
                    input_path, 
                    output_path, # Aquí output_path ya es un directorio
                    image_format=target_fmt.upper()
                )
            elif target_fmt == 'pdf':
                 return self.converter.word_to_pdf(input_path, output_path)
                 
        elif step.action == ActionType.COMPRESS:
            level = params.get('level', 'medium')
            return self.compressor.compress_pdf(input_path, output_path, level)
            
        elif step.action == ActionType.SECURITY:
            mode = params.get('mode', 'encrypt')
            pwd = params.get('password', 'default123')
            if mode == 'encrypt':
                return self.security.encrypt_pdf(input_path, output_path, pwd)
            else:
                return self.security.decrypt_pdf(input_path, output_path, pwd)
                
        else:
            raise NotImplementedError(f"Acción {step.action} no implementada en Executor")
