@echo off
setlocal enabledelayedexpansion
title Vectora V5 - Auto-Repair Utility

echo ===================================================
echo    VECTORA V5 - SISTEMA DE AUTO-REPARACION
echo ===================================================
echo.

:: 1. Corregir config/settings.py (Agregar APP_AUTHOR)
echo [1/3] Corrigiendo config/settings.py...
set PYTHON_CMD=import os; path = 'config/settings.py'; f = open(path, 'r', encoding='utf-8'); content = f.read(); f.close(); 
set PYTHON_CMD=%PYTHON_CMD%if 'self.APP_AUTHOR' not in content: content = content.replace('self.APP_VERSION = \"5.0.0\"', 'self.APP_VERSION = \"5.0.0\"\\n        self.APP_AUTHOR = \"Vectora Team\"'); f = open(path, 'w', encoding='utf-8'); f.write(content); f.close(); print('   -^> APP_AUTHOR agregado exitosamente.')
set PYTHON_CMD=%PYTHON_CMD%else: print('   -^> APP_AUTHOR ya existe.')

python -c "%PYTHON_CMD%"

:: 2. Corregir error de Icono en PyInstaller
echo [2/3] Verificando iconos para compilacion...
if not exist "assets" mkdir assets
python -c "import os; spec_path = 'Vectora.spec'; content = open(spec_path, 'r', encoding='utf-8').read(); icon_exists = os.path.exists('assets/vectora.ico'); \
if (not icon_exists) and ('icon=''assets/vectora.ico''' in content): \
    print('   -^> assets/vectora.ico no existe. Deshabilitando icono en .spec.'); \
    new_content = content.replace('icon=''assets/vectora.ico''', 'icon=None # assets/vectora.ico no encontrado'); \
    open(spec_path, 'w', encoding='utf-8').write(new_content)" 2>nul

:: 3. Limpiar caches de Python y PyInstaller
echo [3/3] Limpiando temporales...
if exist "build" rd /s /q build
if exist "dist" rd /s /q dist
echo.
echo ===================================================
echo    REPARACION COMPLETADA
echo ===================================================
echo Ahora puedes volver a ejecutar v5_smart_control.bat
echo.
pause
