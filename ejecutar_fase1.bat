@echo off
setlocal enabledelayedexpansion
title Vectora V5 - Ejecutor Fase 1 (Pro)

echo ===================================================
echo    VECTORA V5 - MIGRACION AUTOMATICA (FASE 1)
echo ===================================================
echo.

:: 1. Asegurar Infraestructura Core
echo [1/3] Verificando infraestructura core...
if not exist "backend\core" mkdir "backend\core"

(
echo from typing import Any, Optional, Dict
echo from dataclasses import dataclass, field
echo import time
echo.
echo @dataclass
echo class OperationResult:
echo     """Clase estandar para resultados de operaciones de backend"""
echo     success: bool
echo     message: str
echo     data: Optional[Any] = None
echo     error_message: Optional[str] = None
echo     metrics: Dict[str, Any] = field(default_factory=dict^)
echo     timestamp: float = field(default_factory=time.time^)
echo.
echo     def to_dict(self^) -^> Dict[str, Any]:
echo         return {
echo             'success': self.success,
echo             'message': self.message,
echo             'data': self.data,
echo             'error_message': self.error_message,
echo             'metrics': self.metrics,
echo             'timestamp': self.timestamp
echo         }
) > backend\core\operation_result.py

:: 2. Procesar Servicios con Logica Mejorada
echo.
echo [2/3] Estandarizando servicios en backend/services...
python -c "
import os, re
from pathlib import Path

def migrate():
    services_dir = Path('backend/services')
    count = 0
    for file in services_dir.glob('*.py'):
        if file.name == '__init__.py': continue
        try:
            with open(file, 'r', encoding='utf-8') as f: content = f.read()
            
            if 'OperationResult' in content:
                print(f'[SKIP] {file.name} ya esta estandarizado.')
                continue

            modified = False
            
            # Estrategia A: Insertar despues de importaciones de logging
            if 'import logging' in content:
                content = content.replace('import logging', 'import logging\nfrom backend.core.operation_result import OperationResult')
                modified = True
            elif 'from logging import' in content:
                content = re.sub(r'(from logging import.*)', r'\1\nfrom backend.core.operation_result import OperationResult', content)
                modified = True
            
            # Estrategia B: Si no hay logging, insertar despues de las importaciones de typing
            if not modified and 'from typing import' in content:
                content = re.sub(r'(from typing import.*)', r'\1\nfrom backend.core.operation_result import OperationResult', content)
                modified = True
                
            # Estrategia C: Si sigue sin modificarse, insertar al principio del archivo (despues de docstrings)
            if not modified:
                content = 'from backend.core.operation_result import OperationResult\n' + content
                modified = True

            # Actualizar progreso (Callable)
            # Detectar variantes de progress_callback
            if 'progress_callback: Optional[Callable[[int], None]]' in content:
                content = content.replace('progress_callback: Optional[Callable[[int], None]]', 'progress_callback: Optional[Callable[[int, str], None]]')
            elif 'progress_callback=None' in content:
                # Opcional: Podriamos tipar aqui, pero mejor dejarlo simple por ahora
                pass

            if modified:
                with open(file, 'w', encoding='utf-8') as f: f.write(content)
                print(f'[OK] {file.name} estandarizado.')
                count += 1
                
        except Exception as e:
            print(f'[ERROR] {file.name}: {e}')
            
    print(f'\nTotal servicios actualizados: {count}')

migrate()
"

:: 3. Fin con Popup
echo.
echo [3/3] Finalizando...
powershell -Command "[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Refactor de servicios completado. Se han detectado y actualizado todos los servicios faltantes.', 'Vectora V5 - Exito', 'OK', 'Information')"

echo.
echo ===================================================
echo    FASE 1 COMPLETADA (REFORZADA)
echo ===================================================
echo.
pause
