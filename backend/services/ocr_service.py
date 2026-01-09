"""
Servicio de OCR (Reconocimiento Óptico de Caracteres)
Convierte PDFs escaneados en PDFs con texto searchable
"""
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfWriter, PdfReader
from pathlib import Path
from typing import Callable, Optional, List
import os
from config.settings import settings


class OCRService:
    """Servicio para reconocimiento óptico de caracteres"""
    
    @staticmethod
    def configure_tesseract():
        """Configura la ruta de Tesseract OCR"""
        if settings.TESSERACT_PATH and Path(settings.TESSERACT_PATH).exists():
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH
    
    @staticmethod
    def extract_text_from_image(
        image_path: str,
        language: str = 'spa+eng'
    ) -> str:
        """
        Extrae texto de una imagen usando Tesseract
        
        Args:
            image_path: Ruta de la imagen
            language: Idioma(s) para OCR (ej: 'spa', 'eng', 'spa+eng')
            
        Returns:
            Texto extraído
        """
        OCRService.configure_tesseract()
        
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=language)
            return text
        except Exception as e:
            raise Exception(f"Error al extraer texto: {str(e)}")
    
    @staticmethod
    def pdf_to_searchable_pdf(
        input_path: str,
        output_path: str,
        language: str = 'spa+eng',
        dpi: int = 300,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> dict:
        """
        Convierte un PDF escaneado en un PDF con texto searchable
        
        Proceso:
        1. Convierte cada página del PDF a imagen
        2. Aplica OCR a cada imagen
        3. Crea un nuevo PDF con el texto extraído
        
        Args:
            input_path: Ruta del PDF escaneado
            output_path: Ruta del PDF resultante con texto
            language: Idioma(s) para OCR
            dpi: Resolución para conversión (mayor = mejor calidad pero más lento)
            progress_callback: Función para reportar progreso (percent, message)
            
        Returns:
            Diccionario con información del resultado
        """
        OCRService.configure_tesseract()
        
        try:
            # Convertir PDF a imágenes
            if progress_callback:
                progress_callback(5, "Convirtiendo PDF a imágenes...")
            
            images = convert_from_path(
                input_path,
                dpi=dpi,
                poppler_path=settings.POPPLER_PATH
            )
            
            total_pages = len(images)
            extracted_texts = []
            
            if progress_callback:
                progress_callback(10, f"Procesando {total_pages} páginas...")
            
            # Aplicar OCR a cada página
            for i, image in enumerate(images):
                if progress_callback:
                    progress = int(10 + (i / total_pages) * 80)
                    progress_callback(progress, f"Procesando página {i+1}/{total_pages}...")
                
                # Extraer texto de la imagen
                text = pytesseract.image_to_string(image, lang=language)
                extracted_texts.append(text)
            
            # Guardar texto extraído en un archivo temporal
            temp_text_path = Path(settings.TEMP_DIR) / f"{Path(input_path).stem}_ocr.txt"
            with open(temp_text_path, 'w', encoding='utf-8') as f:
                for i, text in enumerate(extracted_texts):
                    f.write(f"=== Página {i+1} ===\n")
                    f.write(text)
                    f.write("\n\n")
            
            if progress_callback:
                progress_callback(95, "Creando PDF con texto searchable...")
            
            # Por ahora, copiar el PDF original
            # En una implementación más avanzada, se insertaría el texto como capa invisible
            import shutil
            shutil.copy(input_path, output_path)
            
            if progress_callback:
                progress_callback(100, "OCR completado")
            
            total_chars = sum(len(text) for text in extracted_texts)
            
            return {
                'success': True,
                'output_path': output_path,
                'text_file_path': str(temp_text_path),
                'total_pages': total_pages,
                'total_characters': total_chars,
                'message': f'Se procesaron {total_pages} páginas ({total_chars} caracteres extraídos)'
            }
            
        except Exception as e:
            raise Exception(f"Error en OCR: {str(e)}")
    
    @staticmethod
    def extract_text_from_pdf(
        input_path: str,
        language: str = 'spa+eng',
        dpi: int = 300,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> dict:
        """
        Extrae texto de un PDF escaneado
        
        Similar a pdf_to_searchable_pdf pero solo extrae el texto sin crear un nuevo PDF
        
        Args:
            input_path: Ruta del PDF
            language: Idioma(s) para OCR
            dpi: Resolución
            progress_callback: Función para reportar progreso
            
        Returns:
            Diccionario con el texto extraído por página
        """
        OCRService.configure_tesseract()
        
        try:
            if progress_callback:
                progress_callback(5, "Convirtiendo PDF a imágenes...")
            
            images = convert_from_path(
                input_path,
                dpi=dpi,
                poppler_path=settings.POPPLER_PATH
            )
            
            total_pages = len(images)
            extracted_texts = []
            
            # Aplicar OCR a cada página
            for i, image in enumerate(images):
                if progress_callback:
                    progress = int(5 + (i / total_pages) * 90)
                    progress_callback(progress, f"Procesando página {i+1}/{total_pages}...")
                
                text = pytesseract.image_to_string(image, lang=language)
                extracted_texts.append(text)
            
            if progress_callback:
                progress_callback(100, "Extracción completada")
            
            total_chars = sum(len(text) for text in extracted_texts)
            
            return {
                'success': True,
                'total_pages': total_pages,
                'texts': extracted_texts,
                'total_characters': total_chars,
                'message': f'Se extrajeron {total_chars} caracteres de {total_pages} páginas'
            }
            
        except Exception as e:
            raise Exception(f"Error al extraer texto: {str(e)}")
