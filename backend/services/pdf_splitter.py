"""
Servicio de división de PDFs
Divide PDFs por rangos, páginas específicas o cada N páginas
"""
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from typing import List, Callable, Optional, Union
import os


class PDFSplitter:
    """Servicio para dividir PDFs de diferentes maneras"""
    
    @staticmethod
    def parse_page_specification(spec: str) -> List[int]:
        """
        Parsea especificación de páginas como "1, 3, 5-8, 12"
        
        Args:
            spec: Especificación de páginas (ej: "1,3,5-8,12")
            
        Returns:
            Lista de números de página (ordenada, sin duplicados)
            
        Raises:
            ValueError: Si el formato es inválido
        """
        pages = set()
        parts = spec.split(',')
        
        for part in parts:
            part = part.strip()
            
            if '-' in part:
                # Rango: "5-8"
                try:
                    start, end = part.split('-')
                    start_num = int(start.strip())
                    end_num = int(end.strip())
                    
                    if start_num > end_num:
                        raise ValueError(f"Rango inválido: {part} (inicio > fin)")
                    
                    pages.update(range(start_num, end_num + 1))
                except ValueError as e:
                    raise ValueError(f"Error al parsear rango '{part}': {str(e)}")
            else:
                # Página individual: "3"
                try:
                    pages.add(int(part))
                except ValueError:
                    raise ValueError(f"Número de página inválido: {part}")
        
        return sorted(list(pages))
    
    @staticmethod
    def split_by_range(
        input_path: str,
        output_path: str,
        start_page: int,
        end_page: int,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """
        Extrae un rango de páginas de un PDF
        
        Args:
            input_path: Ruta del PDF original
            output_path: Ruta del PDF resultante
            start_page: Página inicial (1-indexed)
            end_page: Página final (1-indexed)
            progress_callback: Función para reportar progreso
            
        Returns:
            Diccionario con información del resultado
        """
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        
        # Validaciones
        if start_page < 1 or end_page > total_pages:
            raise ValueError(f"El rango debe estar entre 1 y {total_pages}")
        
        if start_page > end_page:
            raise ValueError("La página inicial debe ser menor o igual que la final")
        
        writer = PdfWriter()
        
        # Agregar páginas (convertir a 0-indexed)
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])
            
            if progress_callback:
                progress = int((page_num - start_page + 2) / (end_page - start_page + 1) * 100)
                progress_callback(progress)
        
        # Guardar resultado
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return {
            'success': True,
            'output_path': output_path,
            'pages_extracted': end_page - start_page + 1,
            'message': f'Se extrajeron las páginas {start_page}-{end_page}'
        }
    
    @staticmethod
    def split_by_pages(
        input_path: str,
        output_path: str,
        page_specification: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """
        Extrae páginas específicas de un PDF
        
        Args:
            input_path: Ruta del PDF original
            output_path: Ruta del PDF resultante
            page_specification: Especificación de páginas (ej: "1,3,5-8,12")
            progress_callback: Función para reportar progreso
            
        Returns:
            Diccionario con información del resultado
        """
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        
        # Parsear especificación
        pages = PDFSplitter.parse_page_specification(page_specification)
        
        # Validar que todas las páginas existen
        if any(p < 1 or p > total_pages for p in pages):
            raise ValueError(f"Todas las páginas deben estar entre 1 y {total_pages}")
        
        writer = PdfWriter()
        
        # Agregar páginas especificadas
        for i, page_num in enumerate(pages):
            writer.add_page(reader.pages[page_num - 1])  # Convertir a 0-indexed
            
            if progress_callback:
                progress = int((i + 1) / len(pages) * 100)
                progress_callback(progress)
        
        # Guardar resultado
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return {
            'success': True,
            'output_path': output_path,
            'pages_extracted': len(pages),
            'message': f'Se extrajeron {len(pages)} páginas'
        }
    
    @staticmethod
    def split_every_n_pages(
        input_path: str,
        output_dir: str,
        n_pages: int,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """
        Divide el PDF cada N páginas
        
        Args:
            input_path: Ruta del PDF original
            output_dir: Directorio donde guardar los archivos resultantes
            n_pages: Número de páginas por archivo
            progress_callback: Función para reportar progreso
            
        Returns:
            Diccionario con información del resultado
        """
        if n_pages < 1:
            raise ValueError("Debe dividir cada 1 o más páginas")
        
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        output_files = []
        
        # Crear directorio si no existe
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        
        # Obtener nombre base del archivo
        base_name = Path(input_path).stem
        
        # Dividir en chunks
        for i in range(0, total_pages, n_pages):
            writer = PdfWriter()
            end = min(i + n_pages, total_pages)
            
            # Agregar páginas del chunk actual
            for page_num in range(i, end):
                writer.add_page(reader.pages[page_num])
            
            # Guardar archivo
            part_num = i // n_pages + 1
            output_path = os.path.join(output_dir, f"{base_name}_parte_{part_num}.pdf")
            
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            output_files.append(output_path)
            
            # Reportar progreso
            if progress_callback:
                progress = int((i + n_pages) / total_pages * 100)
                progress_callback(min(progress, 100))
        
        return {
            'success': True,
            'output_files': output_files,
            'total_parts': len(output_files),
            'message': f'Se crearon {len(output_files)} archivos'
        }
