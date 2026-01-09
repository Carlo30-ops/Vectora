"""
Servicio de conversión de formatos
Convierte entre PDF, Word e Imágenes
"""
from pdf2docx import Converter
from pdf2image import convert_from_path
from PIL import Image
from pathlib import Path
from typing import List, Callable, Optional
import os
from config.settings import settings


class PDFConverter:
    """Servicio para conversión entre formatos"""
    
    @staticmethod
    def pdf_to_word(
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> dict:
        """
        Convierte PDF a Word preservando el layout
        
        Args:
            input_path: Ruta del PDF
            output_path: Ruta del archivo DOCX resultante
            progress_callback: Función para reportar progreso (progress, message)
            
        Returns:
            Diccionario con información del resultado
        """
        try:
            cv = Converter(input_path)
            
            def progress_wrapper(current, total):
                if progress_callback and total > 0:
                    percent = int((current / total) * 100)
                    
                    # Mensajes según fase
                    if percent <= 25:
                        progress_callback(percent, "Analizando estructura del documento...")
                    elif percent <= 50:
                        progress_callback(percent, "Aplicando Layout Engine...")
                    elif percent <= 75:
                        progress_callback(percent, "Generando archivo final...")
                    else:
                        progress_callback(percent, f"Procesando... {percent}%")
            
            # Convertir
            cv.convert(output_path, start=0, end=None)
            cv.close()
            
            if progress_callback:
                progress_callback(100, "Conversión completada")
            
            return {
                'success': True,
                'output_path': output_path,
                'message': 'PDF convertido a Word exitosamente'
            }
            
        except Exception as e:
            raise Exception(f"Error al convertir PDF a Word: {str(e)}")
    
    @staticmethod
    def pdf_to_images(
        input_path: str,
        output_dir: str,
        dpi: int = 300,
        image_format: str = 'PNG',
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """
        Convierte cada página del PDF en una imagen
        
        Args:
            input_path: Ruta del PDF
            output_dir: Directorio donde guardar las imágenes
            dpi: Resolución (150=baja, 300=alta, 600=muy alta)
            image_format: 'PNG' o 'JPEG'
            progress_callback: Función para reportar progreso
            
        Returns:
            Diccionario con información del resultado
        """
        try:
            # Crear directorio si no existe
            Path(output_dir).mkdir(exist_ok=True, parents=True)
            
            # Convertir PDF a imágenes usando Poppler
            images = convert_from_path(
                input_path,
                dpi=dpi,
                poppler_path=settings.POPPLER_PATH
            )
            
            output_files = []
            total_pages = len(images)
            base_name = Path(input_path).stem
            
            # Guardar cada imagen
            for i, image in enumerate(images):
                output_path = os.path.join(
                    output_dir,
                    f'{base_name}_pagina_{i+1}.{image_format.lower()}'
                )
                image.save(output_path, image_format)
                output_files.append(output_path)
                
                if progress_callback:
                    progress = int((i + 1) / total_pages * 100)
                    progress_callback(progress)
            
            return {
                'success': True,
                'output_files': output_files,
                'total_images': len(output_files),
                'message': f'Se generaron {len(output_files)} imágenes'
            }
            
        except Exception as e:
            raise Exception(f"Error al convertir PDF a imágenes: {str(e)}")
    
    @staticmethod
    def images_to_pdf(
        image_paths: List[str],
        output_path: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """
        Combina múltiples imágenes en un PDF
        
        Args:
            image_paths: Lista de rutas de imágenes
            output_path: Ruta del PDF resultante
            progress_callback: Función para reportar progreso
            
        Returns:
            Diccionario con información del resultado
        """
        if not image_paths:
            raise ValueError("Se necesita al menos una imagen")
        
        try:
            images = []
            total_images = len(image_paths)
            
            # Cargar todas las imágenes
            for i, path in enumerate(image_paths):
                img = Image.open(path)
                
                # Convertir a RGB si es necesario (PNG con transparencia)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                images.append(img)
                
                if progress_callback:
                    # Primera mitad del progreso: cargando imágenes
                    progress = int((i + 1) / total_images * 50)
                    progress_callback(progress)
            
            # Guardar como PDF
            if images:
                images[0].save(
                    output_path,
                    save_all=True,
                    append_images=images[1:] if len(images) > 1 else [],
                    resolution=100.0
                )
                
                if progress_callback:
                    progress_callback(100)
            
            return {
                'success': True,
                'output_path': output_path,
                'total_images': len(images),
                'message': f'Se combinaron {len(images)} imágenes en PDF'
            }
            
        except Exception as e:
            raise Exception(f"Error al convertir imágenes a PDF: {str(e)}")
    
    @staticmethod
    def word_to_pdf(
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """
        Convierte Word a PDF
        
        NOTA: Requiere Microsoft Word instalado (Windows) o LibreOffice (Linux)
        
        Args:
            input_path: Ruta del archivo DOCX
            output_path: Ruta del PDF resultante
            progress_callback: Función para reportar progreso
            
        Returns:
            Diccionario con información del resultado
        """
        if not settings.WORD_CONVERSION_AVAILABLE:
            raise Exception("La conversión Word → PDF no está disponible. Requiere Microsoft Word instalado.")
        
        try:
            from docx2pdf import convert
            
            if progress_callback:
                progress_callback(50)
            
            convert(input_path, output_path)
            
            if progress_callback:
                progress_callback(100)
            
            return {
                'success': True,
                'output_path': output_path,
                'message': 'Word convertido a PDF exitosamente'
            }
            
        except ImportError:
            raise Exception("docx2pdf no está instalado")
        except Exception as e:
            raise Exception(f"Error al convertir Word a PDF: {str(e)}")
