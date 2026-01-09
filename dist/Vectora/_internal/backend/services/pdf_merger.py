"""
Servicio de combinación de PDFs
Combina múltiples archivos PDF en uno solo preservando el orden
"""
from PyPDF2 import PdfMerger
from pathlib import Path
from typing import List, Callable, Optional


class PDFMerger:
    """Servicio para combinar múltiples PDFs en uno solo"""
    
    @staticmethod
    def merge_pdfs(
        input_paths: List[str],
        output_path: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """
        Combina múltiples PDFs en uno solo
        
        Args:
            input_paths: Lista de rutas de archivos PDF en el orden deseado
            output_path: Ruta del archivo PDF resultante
            progress_callback: Función para reportar progreso (0-100)
            
        Returns:
            Diccionario con información del resultado:
            {
                'success': bool,
                'output_path': str,
                'total_files': int,
                'message': str
            }
            
        Raises:
            ValueError: Si hay menos de 2 archivos
            FileNotFoundError: Si algún archivo no existe
            Exception: Si hay error al procesar algún PDF
        """
        # Validación: mínimo 2 archivos
        if len(input_paths) < 2:
            raise ValueError("Se necesitan al menos 2 archivos PDF para combinar")
        
        # Validación: todos los archivos existen
        for path in input_paths:
            if not Path(path).exists():
                raise FileNotFoundError(f"El archivo no existe: {path}")
        
        merger = PdfMerger()
        total_files = len(input_paths)
        
        try:
            # Procesar cada archivo
            for i, pdf_path in enumerate(input_paths):
                try:
                    merger.append(pdf_path)
                    
                    # Reportar progreso
                    if progress_callback:
                        progress = int((i + 1) / total_files * 100)
                        progress_callback(progress)
                        
                except Exception as e:
                    raise Exception(f"Error al procesar {Path(pdf_path).name}: {str(e)}")
            
            # Guardar el resultado
            merger.write(output_path)
            merger.close()
            
            return {
                'success': True,
                'output_path': output_path,
                'total_files': total_files,
                'message': f'Se combinaron {total_files} archivos exitosamente'
            }
            
        except Exception as e:
            merger.close()
            raise e
