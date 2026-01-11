"""
Servicio de procesamiento por lotes
Aplica una operación a múltiples archivos de manera robusta y centralizada
"""

import traceback
from dataclasses import dataclass, field
from logging import Logger
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from utils.logger import get_logger


@dataclass
class BatchResult:
    """Estructura de datos para el resultado de un lote"""

    success: bool
    total_files: int
    successful_count: int
    failed_count: int
    results: List[Dict[str, Any]] = field(default_factory=list)
    message: str = ""


class BatchProcessor:
    """Servicio para procesamiento por lotes de PDFs"""

    def __init__(self, logger: Optional[Logger] = None):
        """
        Inicializa el procesador por lotes
        Args:
            logger: Logger personalizado (opcional)
        """
        self.logger = logger or get_logger(__name__)

    def process_batch(
        self,
        file_paths: List[str],
        operation_func: Callable[..., Dict[str, Any]],
        operation_config: Dict[str, Any],
        output_dir: str,
        progress_callback: Optional[Callable[[int, str, Dict], None]] = None,
    ) -> BatchResult:
        """
        Procesa múltiples archivos con una operación específica

        Args:
            file_paths: Lista de rutas de archivos a procesar
            operation_func: Función ejecutable (bound method de un servicio instanciado)
            operation_config: Argumentos extra para la operación
            output_dir: Directorio de salida
            progress_callback: Función para reportar progreso (percent, message, result)

        Returns:
            BatchResult object
        """
        if not file_paths:
            self.logger.warning("Intento de procesamiento por lotes sin archivos")
            raise ValueError("No hay archivos para procesar")

        # Crear directorio de salida
        try:
            Path(output_dir).mkdir(exist_ok=True, parents=True)
        except Exception as e:
            self.logger.error(f"No se pudo crear directorio de salida {output_dir}: {e}")
            raise Exception(f"Error creando directorio de salida: {e}")

        total_files = len(file_paths)
        results = []
        successful = 0
        failed = 0

        self.logger.info(f"Iniciando lote de {total_files} archivos. Salida: {output_dir}")

        # Procesar cada archivo
        for i, file_path in enumerate(file_paths):
            file_name = Path(file_path).name
            result = {
                "file": file_name,
                "file_path": file_path,
                "success": False,
                "output_path": None,
                "error": None,
                "details": None,
            }

            # Reportar inicio de archivo
            if progress_callback:
                progress = int((i) / total_files * 100)
                message = f"Iniciando: {file_name}"
                progress_callback(progress, message, {})

            try:
                # Generar ruta de salida automática
                output_path = str(Path(output_dir) / f"processed_{file_name}")

                self.logger.debug(f"Procesando archivo {i+1}/{total_files}: {file_name}")

                # Ejecutar operación
                operation_result = operation_func(file_path, output_path, **operation_config)

                result["success"] = True
                result["output_path"] = output_path
                result["details"] = operation_result
                successful += 1

            except Exception as e:
                self.logger.error(f"Fallo al procesar {file_name}: {e}", exc_info=True)
                result["error"] = str(e)
                result["traceback"] = traceback.format_exc()
                failed += 1

            results.append(result)

            # Reportar finalización de archivo
            if progress_callback:
                progress = int((i + 1) / total_files * 100)
                msg_status = "OK" if result["success"] else "ERROR"
                message = f"[{msg_status}] {i+1}/{total_files}: {file_name}"
                progress_callback(progress, message, result)

        summary_msg = (
            f"Completado: {successful} exitosos, {failed} fallidos de {total_files} archivos"
        )
        self.logger.info(summary_msg)

        return BatchResult(
            success=failed == 0,
            total_files=total_files,
            successful_count=successful,
            failed_count=failed,
            results=results,
            message=summary_msg,
        )

    def validate_batch_files(
        self,
        file_paths: List[str],
        required_extension: Optional[str] = None,
        max_files: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Valida los archivos para procesamiento por lotes"""
        errors = []
        warnings = []

        # Validar que hay archivos
        if not file_paths:
            errors.append("No se seleccionaron archivos")
            return {"valid": False, "errors": errors, "warnings": warnings}

        # Validar número máximo
        if max_files and len(file_paths) > max_files:
            errors.append(
                f"Máximo {max_files} archivos permitidos (seleccionaste {len(file_paths)})"
            )

        # Validar consistencia
        missing_files = []
        invalid_ext_files = []

        for path in file_paths:
            p = Path(path)
            if not p.exists():
                missing_files.append(p.name)
            elif required_extension and p.suffix.lower() != required_extension.lower():
                invalid_ext_files.append(p.name)

        if missing_files:
            errors.append(f"Archivos no encontrados: {', '.join(missing_files)}")
        if invalid_ext_files:
            errors.append(
                f"Extensión incorrecta (se requiere {required_extension}): {', '.join(invalid_ext_files)}"
            )

        # Advertencias
        if len(file_paths) > 20:
            warnings.append(f"Lote grande ({len(file_paths)} archivos). Esto puede tomar tiempo.")

        is_valid = len(errors) == 0
        if not is_valid:
            self.logger.warning(f"Validación de lote fallida: {errors}")

        return {"valid": is_valid, "errors": errors, "warnings": warnings}
