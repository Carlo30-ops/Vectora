"""
Servicio de combinación de PDFs
Combina múltiples archivos PDF en uno solo preservando el orden
"""

from logging import Logger
from pathlib import Path
from typing import Callable, List, Optional

import pikepdf

from backend.core.operation_result import OperationResult
from utils.logger import get_logger


class PDFMerger:
    """Servicio para combinar múltiples PDFs en uno solo"""

    def __init__(self, logger: Optional[Logger] = None):
        """
        Inicializa el servicio de combinación
        Args:
            logger: Logger personalizado (opcional)
        """
        self.logger = logger or get_logger(__name__)

    def merge_pdfs(
        self,
        input_paths: List[str],
        output_path: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> OperationResult:
        """
        Combina múltiples PDFs en uno solo usando pikepdf (High Performance)
        """
        self.logger.info(f"Iniciando combinación de {len(input_paths)} archivos PDF")

        if len(input_paths) < 2:
            self.logger.error("Validación fallida: se necesitan al menos 2 archivos")
            raise ValueError("Se necesitan al menos 2 archivos PDF para combinar")

        # Validar existencia
        for path in input_paths:
            if not Path(path).exists():
                self.logger.error(f"Archivo no encontrado: {path}")
                raise FileNotFoundError(f"El archivo no existe: {path}")

        try:
            # Crear nuevo PDF destino
            with pikepdf.new() as merged_pdf:
                total_files = len(input_paths)

                for i, pdf_path in enumerate(input_paths):
                    try:
                        file_name = Path(pdf_path).name
                        self.logger.debug(f"Procesando archivo {i+1}/{total_files}: {file_name}")

                        # Abrir PDF origen y copiar páginas
                        with pikepdf.open(pdf_path) as src_pdf:
                            merged_pdf.pages.extend(src_pdf.pages)

                        if progress_callback:
                            progress = int((i + 1) / total_files * 100)
                            progress_callback(progress, f"Procesando {file_name}...")

                    except Exception as e:
                        msg = f"Error al procesar {Path(pdf_path).name}: {str(e)}"
                        self.logger.error(msg, exc_info=True)
                        raise Exception(msg)

                # Guardar el resultado
                self.logger.info(f"Guardando archivo combinado: {output_path}")
                merged_pdf.save(output_path)

            output_size = Path(output_path).stat().st_size / (1024 * 1024)
            self.logger.info(f"Combinación completada exitosamente - Tamaño: {output_size:.2f} MB")

            return OperationResult(
                success=True,
                message=f"Se combinaron {total_files} archivos exitosamente",
                data={"output_path": output_path, "total_files": total_files},
                metrics={"output_size_mb": round(output_size, 2)},
            )

        except Exception as e:
            self.logger.error(f"Error durante la combinación: {e}", exc_info=True)
            raise e
