"""
Servicio de procesamiento por lotes
Aplica una operación a múltiples archivos
"""
from typing import List, Callable, Optional, Dict, Any
from pathlib import Path
import traceback


class BatchProcessor:
    """Servicio para procesamiento por lotes de PDFs"""
    
    @staticmethod
    def process_batch(
        file_paths: List[str],
        operation_func: Callable,
        operation_config: Dict[str, Any],
        output_dir: str,
        progress_callback: Optional[Callable[[int, str, Dict], None]] = None
    ) -> dict:
        """
        Procesa múltiples archivos con una operación específica
        
        Args:
            file_paths: Lista de rutas de archivos a procesar
            operation_func: Función de la operación (ej: PDFMerger.merge_pdfs)
            operation_config: Configuración de la operación
            output_dir: Directorio de salida
            progress_callback: Función para reportar progreso (percent, message, result)
            
        Returns:
            Diccionario con resultados:
            {
                'success': bool,
                'total_files': int,
                'successful': int,
                'failed': int,
                'results': List[Dict],
                'message': str
            }
        """
        if not file_paths:
            raise ValueError("No hay archivos para procesar")
        
        # Crear directorio de salida
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        
        total_files = len(file_paths)
        results = []
        successful = 0
        failed = 0
        
        # Procesar cada archivo
        for i, file_path in enumerate(file_paths):
            file_name = Path(file_path).name
            result = {
                'file': file_name,
                'file_path': file_path,
                'success': False,
                'output_path': None,
                'error': None
            }
            
            try:
                # Generar ruta de salida
                output_path = str(Path(output_dir) / f"processed_{file_name}")
                
                # Ejecutar operación
                operation_result = operation_func(
                    file_path,
                    output_path,
                    **operation_config
                )
                
                result['success'] = True
                result['output_path'] = output_path
                result['details'] = operation_result
                successful += 1
                
            except Exception as e:
                result['error'] = str(e)
                result['traceback'] = traceback.format_exc()
                failed += 1
            
            results.append(result)
            
            # Reportar progreso
            if progress_callback:
                progress = int((i + 1) / total_files * 100)
                message = f"Procesando {i+1}/{total_files}: {file_name}"
                progress_callback(progress, message, result)
        
        return {
            'success': failed == 0,
            'total_files': total_files,
            'successful': successful,
            'failed': failed,
            'results': results,
            'message': f'Completado: {successful} exitosos, {failed} fallidos de {total_files} archivos'
        }
    
    @staticmethod
    def validate_batch_files(
        file_paths: List[str],
        required_extension: Optional[str] = None,
        max_files: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Valida los archivos para procesamiento por lotes
        
        Args:
            file_paths: Lista de rutas de archivos
            required_extension: Extensión requerida (ej: '.pdf')
            max_files: Número máximo de archivos permitidos
            
        Returns:
            Diccionario con resultado de validación:
            {
                'valid': bool,
                'errors': List[str],
                'warnings': List[str]
            }
        """
        errors = []
        warnings = []
        
        # Validar que hay archivos
        if not file_paths:
            errors.append("No se seleccionaron archivos")
        
        # Validar número máximo
        if max_files and len(file_paths) > max_files:
            errors.append(f"Máximo {max_files} archivos permitidos (seleccionaste {len(file_paths)})")
        
        # Validar que existen
        missing_files = []
        for path in file_paths:
            if not Path(path).exists():
                missing_files.append(Path(path).name)
        
        if missing_files:
            errors.append(f"Archivos no encontrados: {', '.join(missing_files)}")
        
        # Validar extensión
        if required_extension:
            invalid_files = []
            for path in file_paths:
                if Path(path).suffix.lower() != required_extension.lower():
                    invalid_files.append(Path(path).name)
            
            if invalid_files:
                errors.append(f"Archivos con extensión incorrecta: {', '.join(invalid_files)}")
        
        # Advertencia si hay muchos archivos
        if len(file_paths) > 20:
            warnings.append(f"Procesando {len(file_paths)} archivos, esto puede tomar varios minutos")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
