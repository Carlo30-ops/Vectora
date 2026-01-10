"""
Módulo de validaciones para Vectora
Centraliza lógica de validación de archivos y entradas de usuario
"""
import os
from pathlib import Path
from typing import List, Tuple, Optional
from PyPDF2 import PdfReader

# Constantes de validación
MAX_FILE_SIZE_MB = 100
MAX_BATCH_SIZE = 50
VALID_EXTENSIONS = ['.pdf']

def validate_file_size(file_path: str, max_mb: int = MAX_FILE_SIZE_MB) -> Tuple[bool, str]:
    """
    Valida que el archivo no exceda el tamaño máximo
    
    Args:
        file_path: Ruta del archivo
        max_mb: Tamaño máximo en MB
        
    Returns:
        (bool, str): (Es válido, Mensaje de error)
    """
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        
        if size_mb > max_mb:
            return False, f"El archivo excede el límite de {max_mb} MB (Tamaño actual: {size_mb:.2f} MB)"
        
        return True, ""
    except Exception as e:
        return False, f"Error al validar tamaño: {str(e)}"

def validate_pdf_file(file_path: str) -> Tuple[bool, str]:
    """
    Valida que el archivo sea un PDF válido y legible
    
    Args:
        file_path: Ruta del archivo
        
    Returns:
        (bool, str): (Es válido, Mensaje de error)
    """
    if not os.path.exists(file_path):
        return False, "El archivo no existe"
        
    if Path(file_path).suffix.lower() not in VALID_EXTENSIONS:
        return False, "La extensión del archivo no es .pdf"
        
    try:
        # Intentar leer el PDF
        reader = PdfReader(file_path)
        if len(reader.pages) == 0:
            return False, "El PDF está vacío"
        if reader.is_encrypted:
            # Nota: Algunos PDFs encriptados se pueden leer si no tienen user password,
            # pero para operaciones de escritura generalmente necesitamos decriptar.
            # Por ahora avisamos.
            return True, "Advertencia: El PDF está encriptado (podría requerir contraseña)"
            
        return True, ""
    except Exception as e:
        return False, f"El archivo PDF está corrupto o es inválido: {str(e)}"

def validate_batch_size(file_count: int, max_count: int = MAX_BATCH_SIZE) -> Tuple[bool, str]:
    """Valida el tamaño del lote"""
    if file_count > max_count:
        return False, f"Demasiados archivos. El límite es {max_count}."
    return True, ""

def format_size(size_bytes: int) -> str:
    """Formatea bytes a texto legible"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
