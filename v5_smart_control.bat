@echo off
setlocal enabledelayedexpansion
title Vectora V5 - Master Control

:: Colores (Opcional, solo si soporta ANSI)
echo ===================================================
echo    VECTORA V5 - SMART AUTOMATION TOOLBOX
echo ===================================================
echo.

:menu
echo Seleccione una accion para continuar:
echo 1. [MIGRACION] Estandarizar Backend Completo (Fase 1 Profesional)
echo 2. [SETUP] Preparar Entorno (Requirements + Iconos)
echo 3. [RUN] Ejecutar Aplicacion (Modo Desarrollo)
echo 4. [COMPILE] Generar Ejecutable (.EXE con PyInstaller)
echo 5. [DEBUG] Ejecutar Suite de Tests (PyTest)
echo 6. Salir
echo.
set /p opt="Opcion (1-6): "

if "%opt%"=="1" goto phase1
if "%opt%"=="2" goto prepare
if "%opt%"=="3" goto run
if "%opt%"=="4" goto build
if "%opt%"=="5" goto test
if "%opt%"=="6" exit
goto menu

:phase1
echo.
echo [INFO] Aplicando estandarizacion en todos los servicios de backend...
echo.
python -c "
import os, re
from pathlib import Path

def standardize():
    # 1. Crear o actualizar Infraestructura Core
    core_dir = Path('backend/core')
    core_dir.mkdir(parents=True, exist_ok=True)
    op_res_path = core_dir / 'operation_result.py'
    op_res_content = '''from typing import Any, Optional, Dict
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
            'success': self.success,
            'message': self.message,
            'data': self.data,
            'error_message': self.error_message,
            'metrics': self.metrics,
            'timestamp': self.timestamp
        }
'''
    with open(op_res_path, 'w', encoding='utf-8') as f: f.write(op_res_content)
    print(f'[CORE] Infraestructura de resultados creada en {op_res_path}')

    # 2. Procesar todos los archivos en backend/services
    services_dir = Path('backend/services')
    updated_count = 0
    
    for file in services_dir.glob('*.py'):
        if file.name == '__init__.py': continue
        
        try:
            with open(file, 'r', encoding='utf-8') as f: 
                content = f.read()
            
            modified = False
            
            # A. Agregar importación de OperationResult si falta
            if 'OperationResult' not in content:
                if 'from logging import Logger' in content:
                    content = content.replace('from logging import Logger', 'from logging import Logger\nfrom backend.core.operation_result import OperationResult')
                    modified = True
                elif 'import logging' in content:
                    content = content.replace('import logging', 'import logging\nfrom backend.core.operation_result import OperationResult')
                    modified = True
            
            # B. Actualizar firma de progress_callback a (progress, message)
            if 'progress_callback: Optional[Callable[[int], None]]' in content:
                content = content.replace('progress_callback: Optional[Callable[[int], None]]', 'progress_callback: Optional[Callable[[int, str], None]]')
                modified = True
            
            # C. Actualizar llamadas simples a progress_callback
            # Busca progress_callback(valor) y lo cambia a progress_callback(valor, 'Procesando...')
            # Solo si no tiene ya el segundo argumento
            new_content = re.sub(r'progress_callback\(([^,\)]+)\)', r'progress_callback(\1, \"Procesando...\")', content)
            if new_content != content:
                content = new_content
                modified = True
            
            if modified:
                with open(file, 'w', encoding='utf-8') as f: 
                    f.write(content)
                print(f'[SERVICE] {file.name} actualizado.')
                updated_count += 1
            else:
                print(f'[SKIP] {file.name} ya esta estandarizado o no requiere cambios.')
                
        except Exception as e:
            print(f'[ERROR] Fallo al procesar {file.name}: {e}')

    print(f'\n[RESUMEN] Se actualizaron {updated_count} servicios.')

standardize()
"
echo.
echo [SUCCESS] Fase 1 completada. Los servicios ahora usan el protocolo V5.
pause
goto menu

:prepare
echo.
echo [INFO] Generando requirements y recursos...
call generate_requirements.bat
call generar_iconos.bat
echo.
echo [SUCCESS] Recursos preparados.
pause
goto menu

:run
echo.
echo [INFO] Iniciando Vectora en modo desarrollo...
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] La aplicacion se cerro con errores.
    pause
)
goto menu

:build
echo.
echo [INFO] Iniciando proceso de compilacion con PyInstaller...
call build_exe.bat
pause
goto menu

:test
echo.
echo [INFO] Ejecutando suite de pruebas basicas...
pytest tests/test_pdf_merger.py tests/test_pdf_splitter.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Todas las pruebas pasaron exitosamente.
) else (
    echo.
    echo [WARNING] Algunas pruebas fallaron. Verifique los logs.
)
pause
goto menu
