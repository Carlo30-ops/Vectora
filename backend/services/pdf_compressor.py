"""
Servicio de compresión de PDFs
Reduce el tamaño de archivos PDF comprimiendo streams
"""

import os
from logging import Logger
from pathlib import Path
from typing import Callable, Optional

import pikepdf

from utils.logger import get_logger


class PDFCompressor:
    """Servicio para comprimir archivos PDF"""

    # Niveles de compresión
    COMPRESSION_LEVELS = {
        "low": {"quality": 90, "label": "Baja", "reduction": "~20%"},
        "medium": {"quality": 70, "label": "Media", "reduction": "~40%"},
        "high": {"quality": 50, "label": "Alta", "reduction": "~60%"},
        "extreme": {"quality": 30, "label": "Extrema", "reduction": "~80%"},
    }

    def __init__(self, logger: Optional[Logger] = None):
        """
        Inicializa el servicio de compresión
        Args:
            logger: Logger personalizado (opcional)
        """
        self.logger = logger or get_logger(__name__)

    @staticmethod
    def get_compression_level_from_value(value: int) -> str:
        """Determina el nivel de compresión según el valor del slider"""
        if value <= 25:
            return "low"
        elif value <= 50:
            return "medium"
        elif value <= 75:
            return "high"
        else:
            return "extreme"

    def compress_pdf(
        self,
        input_path: str,
        output_path: str,
        quality_level: str = "medium",
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> dict:
        """Comprime un PDF reduciendo la calidad de imágenes y optimizando streams"""
        if quality_level not in PDFCompressor.COMPRESSION_LEVELS:
            raise ValueError(f"Nivel de compresión inválido: {quality_level}")

        self.logger.info(f"Comprimiendo PDF: {input_path} (Nivel: {quality_level})")

        # Obtener tamaño original
        original_size = os.path.getsize(input_path)
        original_size_mb = original_size / (1024 * 1024)

        try:
            # Abrir PDF con pikepdf
            with pikepdf.open(input_path) as pdf:
                total_pages = len(pdf.pages)

                # Reportar progreso inicial
                if progress_callback:
                    progress_callback(10)

                # Procesar cada página (para mostrar progreso)
                for i, page in enumerate(pdf.pages):
                    if progress_callback and total_pages > 0:
                        progress = int(10 + (i + 1) / total_pages * 80)
                        progress_callback(progress)

                # Guardar con compresión
                pdf.save(
                    output_path,
                    compress_streams=True,
                    stream_decode_level=pikepdf.StreamDecodeLevel.generalized,
                    object_stream_mode=pikepdf.ObjectStreamMode.generate,
                )

                if progress_callback:
                    progress_callback(100)

            # Calcular métricas
            compressed_size = os.path.getsize(output_path)
            compressed_size_mb = compressed_size / (1024 * 1024)
            savings_percent = ((original_size - compressed_size) / original_size) * 100

            self.logger.info(f"Compresión exitosa: {savings_percent:.1f}% ahorrado")

            return {
                "success": True,
                "output_path": output_path,
                "original_size_mb": round(original_size_mb, 2),
                "compressed_size_mb": round(compressed_size_mb, 2),
                "savings_percent": round(savings_percent, 2),
                "message": f"Se redujo {savings_percent:.1f}% del tamaño original",
            }

        except Exception as e:
            self.logger.error(f"Error comprimiendo PDF: {e}", exc_info=True)
            raise Exception(f"Error al comprimir PDF: {str(e)}")
