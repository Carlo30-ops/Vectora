"""
Servicio de conversión de formatos
Convierte entre PDF, Word e Imágenes
"""

import os
from logging import Logger
from pathlib import Path
from typing import Callable, List, Optional

from pdf2docx import Converter
from pdf2image import convert_from_path
from PIL import Image

from backend.core.operation_result import OperationResult
from config.settings import settings as default_settings
from utils.logger import get_logger


class PDFConverter:
    """Servicio para conversión entre formatos"""

    def __init__(self, logger: Optional[Logger] = None, settings=None):
        """
        Inicializa el servicio de conversión
        Args:
            logger: Logger personalizado
            settings: Configuración (opcional)
        """
        self.logger = logger or get_logger(__name__)
        self.settings = settings or default_settings

    def pdf_to_word(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> OperationResult:
        """Convierte PDF a Word preservando el layout"""
        try:
            self.logger.info(f"Convirtiendo PDF a Word: {input_path}")
            cv = Converter(input_path)

            def progress_wrapper(current, total):
                if progress_callback and total > 0:
                    percent = int((current / total) * 100)
                    msg = "Procesando..."
                    if percent <= 25:
                        msg = "Analizando estructura..."
                    elif percent <= 50:
                        msg = "Aplicando layout..."
                    elif percent <= 75:
                        msg = "Generando documento..."
                    progress_callback(percent, msg)

            # Convertir
            cv.convert(output_path, start=0, end=None)
            cv.close()

            if progress_callback:
                progress_callback(100, "Conversión completada")

            return OperationResult(
                success=True,
                message="PDF convertido a Word exitosamente",
                data={"output_path": output_path},
            )

        except Exception as e:
            self.logger.error(f"Error PDF->Word: {e}", exc_info=True)
            raise Exception(f"Error al convertir PDF a Word: {str(e)}")

    def pdf_to_images(
        self,
        input_path: str,
        output_dir: str,
        dpi: int = 300,
        image_format: str = "PNG",
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> OperationResult:
        """Convierte cada página del PDF en una imagen"""
        try:
            self.logger.info(f"Convirtiendo PDF a Imágenes: {input_path}")
            Path(output_dir).mkdir(exist_ok=True, parents=True)

            images = convert_from_path(input_path, dpi=dpi, poppler_path=self.settings.POPPLER_PATH)

            output_files = []
            total_pages = len(images)
            base_name = Path(input_path).stem

            for i, image in enumerate(images):
                output_path = os.path.join(
                    output_dir, f"{base_name}_pagina_{i+1}.{image_format.lower()}"
                )
                image.save(output_path, image_format)
                output_files.append(output_path)

                if progress_callback:
                    progress = int((i + 1) / total_pages * 100)
                    progress_callback(progress)

            return OperationResult(
                success=True,
                message=f"Se generaron {len(output_files)} imágenes",
                data={"output_files": output_files, "total_images": len(output_files)},
            )

        except Exception as e:
            self.logger.error(f"Error PDF->Imágenes: {e}", exc_info=True)
            raise Exception(f"Error al convertir PDF a imágenes: {str(e)}")

    def images_to_pdf(
        self,
        image_paths: List[str],
        output_path: str,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> OperationResult:
        """Combina múltiples imágenes en un PDF"""
        if not image_paths:
            raise ValueError("Se necesita al menos una imagen")

        try:
            self.logger.info(f"Convirtiendo {len(image_paths)} imágenes a PDF")
            images = []
            total_images = len(image_paths)

            for i, path in enumerate(image_paths):
                img = Image.open(path)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                images.append(img)

                if progress_callback:
                    progress = int((i + 1) / total_images * 50)
                    progress_callback(progress)

            if images:
                images[0].save(
                    output_path,
                    save_all=True,
                    append_images=images[1:] if len(images) > 1 else [],
                    resolution=100.0,
                )
                if progress_callback:
                    progress_callback(100)

            return OperationResult(
                success=True,
                message=f"Se combinaron {len(images)} imágenes en PDF",
                data={"output_path": output_path, "total_images": len(images)},
            )

        except Exception as e:
            self.logger.error(f"Error Imágenes->PDF: {e}", exc_info=True)
            raise Exception(f"Error al convertir imágenes a PDF: {str(e)}")

    def word_to_pdf(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> OperationResult:
        """Convierte Word a PDF (Requiere MS Word)"""
        if not self.settings.WORD_CONVERSION_AVAILABLE:
            raise Exception("La conversión Word → PDF no está disponible.")

        try:
            self.logger.info(f"Convirtiendo Word a PDF: {input_path}")
            from docx2pdf import convert

            if progress_callback:
                progress_callback(50)

            convert(input_path, output_path)

            if progress_callback:
                progress_callback(100)

            return OperationResult(
                success=True,
                message="Word convertido a PDF exitosamente",
                data={"output_path": output_path},
            )

        except ImportError:
            self.logger.warning("docx2pdf no instalado")
            raise Exception("docx2pdf no está instalado")
        except Exception as e:
            self.logger.error(f"Error Word->PDF: {e}", exc_info=True)
            raise Exception(f"Error al convertir Word a PDF: {str(e)}")
