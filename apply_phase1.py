import os
import sys
from pathlib import Path

def print_step(step):
    print(f"\n[STEP] {step}")

def create_operation_result():
    print_step("Creando backend/core/operation_result.py")
    path = Path("backend/core/operation_result.py")
    content = """from typing import Any, Optional, Dict
from dataclasses import dataclass, field
import time

@dataclass
class OperationResult:
    \"\"\"Clase estándar para resultados de operaciones de backend\"\"\"
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
            "timestamp": self.timestamp
        }
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def update_pdf_merger():
    print_step("Actualizando backend/services/pdf_merger.py")
    path = Path("backend/services/pdf_merger.py")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Reemplazar imports
    if "from backend.core.operation_result import OperationResult" not in content:
        content = content.replace("from logging import Logger", "from logging import Logger\\nfrom backend.core.operation_result import OperationResult")

    # Reemplazar firma y lógica de progreso
    old_call = "progress_callback: Optional[Callable[[int], None]] = None"
    new_call = "progress_callback: Optional[Callable[[int, str], None]] = None"
    content = content.replace(old_call, new_call)

    # Actualizar llamadas al callback
    content = content.replace(
        "progress_callback(progress)",
        "progress_callback(progress, f'Procesando {file_name}...')"
    )

    # Reemplazar retorno
    old_return = """            return {
                "success": True,
                "output_path": output_path,
                "total_files": total_files,
                "message": f"Se combinaron {total_files} archivos exitosamente"
            }"""
    
    new_return = """            return OperationResult(
                success=True,
                message=f"Se combinaron {total_files} archivos exitosamente",
                data={"output_path": output_path, "total_files": total_files},
                metrics={"output_size_mb": round(output_size, 2)}
            ).to_dict()"""
    
    content = content.replace(old_return, new_return)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content.replace("\\n", "\n"))

def update_pdf_splitter():
    print_step("Actualizando backend/services/pdf_splitter.py")
    path = Path("backend/services/pdf_splitter.py")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "from backend.core.operation_result import OperationResult" not in content:
        content = content.replace("from logging import Logger", "from logging import Logger\\nfrom backend.core.operation_result import OperationResult")

    # Cambiar callbacks
    content = content.replace("progress_callback: Optional[Callable[[int], None]] = None", "progress_callback: Optional[Callable[[int, str], None]] = None")
    
    # Actualizar llamadas de progreso
    content = content.replace("progress_callback(progress)", "progress_callback(progress, f'Extrayendo página {page_num+1}...')")
    content = content.replace("progress_callback(min(progress, 100))", "progress_callback(min(progress, 100), f'Generando parte {part_num}...')")

    # Cambiar retornos (Split by range)
    content = content.replace(
        """        return {
            "success": True,
            "output_path": output_path,
            "pages_extracted": end_page - start_page + 1,
            "message": f"Se extrajeron las páginas {start_page}-{end_page}"
        }""",
        """        return OperationResult(
            success=True,
            message=f"Se extrajeron las páginas {start_page}-{end_page}",
            data={"output_path": output_path, "pages_extracted": end_page - start_page + 1}
        ).to_dict()"""
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content.replace("\\n", "\n"))

def main():
    print("=== APLICANDO FASE 1: ESTANDARIZACIÓN BACKEND ===")
    create_operation_result()
    update_pdf_merger()
    update_pdf_splitter()
    print("\\n[SUCCESS] Fase 1 aplicada correctamente.")

if __name__ == "__main__":
    main()
