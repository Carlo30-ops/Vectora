"""
Excepciones personalizadas para Vectora
Proporciona excepciones específicas del dominio para mejor manejo de errores
"""
from typing import Optional


class VectoraException(Exception):
    """Excepción base para todas las excepciones de Vectora"""


class PDFValidationError(VectoraException):
    """Error de validación de archivo PDF"""
    
    def __init__(self, message: str, file_path: Optional[str] = None):
        super().__init__(message)
        self.file_path = file_path


class PDFProcessingError(VectoraException):
    """Error durante el procesamiento de PDF"""
    
    def __init__(self, message: str, operation: Optional[str] = None):
        super().__init__(message)
        self.operation = operation


class ConfigurationError(VectoraException):
    """Error de configuración"""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(message)
        self.config_key = config_key


class FileAccessError(VectoraException):
    """Error de acceso a archivos (permisos, no existe, etc.)"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, error_type: Optional[str] = None):
        super().__init__(message)
        self.file_path = file_path
        self.error_type = error_type  # 'not_found', 'permission_denied', 'read_only', etc.
