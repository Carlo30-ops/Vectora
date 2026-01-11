"""
Módulo core de Vectora
Contiene componentes centrales del sistema
"""
from .operation_result import OperationResult
from .exceptions import (
    VectoraException,
    PDFValidationError,
    PDFProcessingError,
    ConfigurationError,
    FileAccessError
)

__all__ = [
    'OperationResult',
    'VectoraException',
    'PDFValidationError',
    'PDFProcessingError',
    'ConfigurationError',
    'FileAccessError'
]
