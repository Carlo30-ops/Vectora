"""
Configuración de fixtures y utilidades para tests de Vectora
"""
import pytest
from pathlib import Path
from PyPDF2 import PdfWriter
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """
    Crea un directorio temporal para tests
    Se limpia automáticamente después del test
    """
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_pdf(temp_dir):
    """
    Crea un PDF de prueba simple de 1 página
    """
    pdf_path = temp_dir / "sample.pdf"
    
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)  # Tamaño carta
    
    with open(pdf_path, 'wb') as f:
        writer.write(f)
    
    return pdf_path


@pytest.fixture
def sample_pdfs_multiple(temp_dir):
    """
    Crea múltiples PDFs de prueba (3 archivos)
    Retorna lista de paths
    """
    pdf_paths = []
    
    for i in range(1, 4):
        pdf_path = temp_dir / f"sample_{i}.pdf"
        writer = PdfWriter()
        
        # Agregar páginas (1, 2, 3 páginas respectivamente)
        for _ in range(i):
            writer.add_blank_page(width=612, height=792)
        
        with open(pdf_path, 'wb') as f:
            writer.write(f)
        
        pdf_paths.append(str(pdf_path))
    
    return pdf_paths


@pytest.fixture
def sample_pdf_multipage(temp_dir):
    """
    Crea un PDF de prueba con 10 páginas
    Para tests de splitting
    """
    pdf_path = temp_dir / "multipage.pdf"
    
    writer = PdfWriter()
    for i in range(10):
        writer.add_blank_page(width=612, height=792)
    
    with open(pdf_path, 'wb') as f:
        writer.write(f)
    
    return pdf_path


@pytest.fixture
def non_existent_file(temp_dir):
    """
    Retorna path a un archivo que NO existe
    Para tests de validación de errores
    """
    return str(temp_dir / "non_existent.pdf")


@pytest.fixture
def output_path(temp_dir):
    """
    Retorna path para archivo de salida
    """
    return str(temp_dir / "output.pdf")


# Helpers para assertions
def assert_pdf_exists(path):
    """Verifica que el PDF existe"""
    assert Path(path).exists(), f"PDF no existe: {path}"


def assert_pdf_pages(path, expected_pages):
    """Verifica el número de páginas de un PDF"""
    from PyPDF2 import PdfReader
    reader = PdfReader(path)
    actual_pages = len(reader.pages)
    assert actual_pages == expected_pages, f"Esperado {expected_pages} páginas, encontrado {actual_pages}"


def assert_file_size_greater_than(path, min_bytes):
    """Verifica que el archivo sea mayor a cierto tamaño"""
    size = Path(path).stat().st_size
    assert size > min_bytes, f"Archivo muy pequeño: {size} bytes"
