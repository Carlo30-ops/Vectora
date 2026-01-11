import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class OperationResult:
    """Clase estandar para resultados de operaciones de backend"""

    success: bool
    message: str
    data: Optional[Any] = None
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "error_message": self.error_message,
            "metrics": self.metrics,
            "timestamp": self.timestamp,
        }
