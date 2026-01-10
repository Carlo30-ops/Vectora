"""
Script de refactorización automática del backend de Vectora.
Este script actualiza los archivos de servicio para usar inyección de dependencias y mejores prácticas.
"""
import os
from pathlib import Path

# Nuevos contenidos de los archivos

PDF_MERGER_CONTENT = '''"""
Servicio de combinación de PDFs
Combina múltiples archivos PDF en uno solo preservando el orden
"""
from PyPDF2 import PdfMerger as PyPDFMerger
from pathlib import Path
from typing import List, Callable, Optional
from logging import Logger
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
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """
        Combina múltiples PDFs en uno solo
        """
        self.logger.info(f"Iniciando combinación de {len(input_paths)} archivos PDF")
        
        if len(input_paths) < 2:
            self.logger.error("Validación fallida: se necesitan al menos 2 archivos")
            raise ValueError("Se necesitan al menos 2 archivos PDF para combinar")
        
        for path in input_paths:
            if not Path(path).exists():
                self.logger.error(f"Archivo no encontrado: {path}")
                raise FileNotFoundError(f"El archivo no existe: {path}")
        
        merger = PyPDFMerger()
        total_files = len(input_paths)
        
        try:
            for i, pdf_path in enumerate(input_paths):
                try:
                    file_name = Path(pdf_path).name
                    self.logger.debug(f"Procesando archivo {i+1}/{total_files}: {file_name}")
                    merger.append(pdf_path)
                    
                    if progress_callback:
                        progress = int((i + 1) / total_files * 100)
                        progress_callback(progress)
                        
                except Exception as e:
                    self.logger.error(f"Error al procesar {Path(pdf_path).name}: {e}", exc_info=True)
                    raise Exception(f"Error al procesar {Path(pdf_path).name}: {str(e)}")
            
            self.logger.info(f"Guardando archivo combinado: {output_path}")
            merger.write(output_path)
            merger.close()
            
            output_size = Path(output_path).stat().st_size / (1024 * 1024)
            self.logger.info(f"Combinación completada exitosamente - Tamaño: {output_size:.2f} MB")
            
            return {
                "success": True,
                "output_path": output_path,
                "total_files": total_files,
                "message": f"Se combinaron {total_files} archivos exitosamente"
            }
            
        except Exception as e:
            self.logger.error(f"Error durante la combinación: {e}", exc_info=True)
            merger.close()
            raise e
'''

PDF_SPLITTER_CONTENT = '''"""
Servicio de división de PDFs
Divide PDFs por rangos, páginas específicas o cada N páginas
"""
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from typing import List, Callable, Optional
from logging import Logger
from utils.logger import get_logger
import os

class PDFSplitter:
    """Servicio para dividir PDFs de diferentes maneras"""
    
    def __init__(self, logger: Optional[Logger] = None):
        """
        Inicializa el servicio de división
        Args:
            logger: Logger personalizado (opcional)
        """
        self.logger = logger or get_logger(__name__)
    
    def parse_page_specification(self, spec: str) -> List[int]:
        """Parsea especificación de páginas como '1, 3, 5-8, 12'"""
        pages = set()
        parts = spec.split(',')
        
        for part in parts:
            part = part.strip()
            if '-' in part:
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
                try:
                    pages.add(int(part))
                except ValueError:
                    raise ValueError(f"Número de página inválido: {part}")
        
        return sorted(list(pages))
    
    def split_by_range(
        self,
        input_path: str,
        output_path: str,
        start_page: int,
        end_page: int,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """Extrae un rango de páginas de un PDF"""
        self.logger.info(f"Dividiendo por rango {start_page}-{end_page}: {input_path}")
        
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        
        if start_page < 1 or end_page > total_pages:
            raise ValueError(f"El rango debe estar entre 1 y {total_pages}")
        
        writer = PdfWriter()
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])
            if progress_callback:
                progress = int((page_num - start_page + 2) / (end_page - start_page + 1) * 100)
                progress_callback(progress)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
            
        return {
            "success": True,
            "output_path": output_path,
            "pages_extracted": end_page - start_page + 1,
            "message": f"Se extrajeron las páginas {start_page}-{end_page}"
        }

    def split_by_pages(
        self,
        input_path: str,
        output_path: str,
        page_specification: str,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """Extrae páginas específicas de un PDF"""
        self.logger.info(f"Dividiendo páginas específicas '{page_specification}': {input_path}")
        
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        pages = self.parse_page_specification(page_specification)
        
        if any(p < 1 or p > total_pages for p in pages):
            raise ValueError(f"Todas las páginas deben estar entre 1 y {total_pages}")
        
        writer = PdfWriter()
        for i, page_num in enumerate(pages):
            writer.add_page(reader.pages[page_num - 1])
            if progress_callback:
                progress = int((i + 1) / len(pages) * 100)
                progress_callback(progress)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
            
        return {
            "success": True,
            "output_path": output_path,
            "pages_extracted": len(pages),
            "message": f"Se extrajeron {len(pages)} páginas"
        }
    
    def split_every_n_pages(
        self,
        input_path: str,
        output_dir: str,
        n_pages: int,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """Divide el PDF cada N páginas"""
        self.logger.info(f"Dividiendo cada {n_pages} páginas: {input_path}")
        
        if n_pages < 1:
            raise ValueError("Debe dividir cada 1 o más páginas")
        
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        output_files = []
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        base_name = Path(input_path).stem
        
        for i in range(0, total_pages, n_pages):
            writer = PdfWriter()
            end = min(i + n_pages, total_pages)
            
            for page_num in range(i, end):
                writer.add_page(reader.pages[page_num])
            
            part_num = i // n_pages + 1
            out_path = os.path.join(output_dir, f"{base_name}_parte_{part_num}.pdf")
            
            with open(out_path, 'wb') as output_file:
                writer.write(output_file)
            
            output_files.append(out_path)
            if progress_callback:
                progress = int((i + n_pages) / total_pages * 100)
                progress_callback(min(progress, 100))
                
        return {
            "success": True,
            "output_files": output_files,
            "total_parts": len(output_files),
            "message": f"Se crearon {len(output_files)} archivos"
        }
'''

def update_file(path, content):
    full_path = Path(__file__).parent.parent / path
    print(f"Actualizando {full_path}...")
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("OK")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    print("Iniciando refactorización del backend...")
    update_file("backend/services/pdf_merger.py", PDF_MERGER_CONTENT)
    update_file("backend/services/pdf_splitter.py", PDF_SPLITTER_CONTENT)
    print("Refactorización completada.")
