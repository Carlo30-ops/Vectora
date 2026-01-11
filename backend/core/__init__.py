"""
Módulo core de Vectora
Contiene componentes centrales del sistema
"""

from .exceptions import (
    ConfigurationError,
    FileAccessError,
    PDFProcessingError,
    PDFValidationError,
    VectoraException,
)
from .operation_result import OperationResult

__all__ = [
    "OperationResult",
    "VectoraException",
    "PDFValidationError",
    "PDFProcessingError",
    "ConfigurationError",
    "FileAccessError",
]
