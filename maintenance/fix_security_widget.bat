@echo off
setlocal EnableDelayedExpansion

echo ===========================================
echo   Vectora Security Widget Fixer
echo ===========================================

:: Define paths
set "TARGET_FILE=%~dp0..\ui\components\operation_widgets\security_widget.py"
set "PYTHON_SCRIPT=%TEMP%\fix_security_temp.py"

:: Check if target exists
if not exist "%TARGET_FILE%" (
    echo [ERROR] No se encuentra el archivo:
    echo %TARGET_FILE%
    echo Asegurate de ejecutar este archivo desde la carpeta maintenance.
    echo.
    echo Carpeta actual: %CD%
    echo Buscando en: %~dp0..\ui\components\operation_widgets\
    echo.
    pause
    exit /b 1
)

:: Generate Python script line by line to avoid batch syntax errors
echo Generando script de correcciones...

echo import sys > "%PYTHON_SCRIPT%"
echo import os >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo target = os.path.normpath(sys.argv[1]) >> "%PYTHON_SCRIPT%"
echo print(f"Procesando: {target}") >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo try: >> "%PYTHON_SCRIPT%"
echo     with open(target, 'r', encoding='utf-8') as f: >> "%PYTHON_SCRIPT%"
echo         content = f.read() >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo     replacements = [ >> "%PYTHON_SCRIPT%"
echo         ('from icons.icons import IconHelper', 'from ui.components.ui_helpers import IconHelper'), >> "%PYTHON_SCRIPT%"
echo         ('self.finished.emit(result)', 'self.finished.emit(result.to_dict())'), >> "%PYTHON_SCRIPT%"
echo         ('self.perm_group.setVisible(is_encrypt)', 'self.perm_box.setVisible(is_encrypt)') >> "%PYTHON_SCRIPT%"
echo     ] >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo     count = 0 >> "%PYTHON_SCRIPT%"
echo     for old, new in replacements: >> "%PYTHON_SCRIPT%"
echo         if old in content: >> "%PYTHON_SCRIPT%"
echo             content = content.replace(old, new) >> "%PYTHON_SCRIPT%"
echo             count += 1 >> "%PYTHON_SCRIPT%"
echo             print(f" [OK] Corregido: {old[:30]}...") >> "%PYTHON_SCRIPT%"
echo         else: >> "%PYTHON_SCRIPT%"
echo             if new in content: >> "%PYTHON_SCRIPT%"
echo                 print(f" [SKIP] Ya estaba corregido: {old[:30]}...") >> "%PYTHON_SCRIPT%"
echo             else: >> "%PYTHON_SCRIPT%"
echo                 print(f" [WARN] No se encontro el texto: {old[:30]}...") >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo     if count ^> 0: >> "%PYTHON_SCRIPT%"
echo         with open(target, 'w', encoding='utf-8') as f: >> "%PYTHON_SCRIPT%"
echo             f.write(content) >> "%PYTHON_SCRIPT%"
echo         print(f"\nExito: Se aplicaron {count} correcciones.") >> "%PYTHON_SCRIPT%"
echo     else: >> "%PYTHON_SCRIPT%"
echo         print("\nNinguna correccion fue necesaria.") >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo except Exception as e: >> "%PYTHON_SCRIPT%"
echo     print(f"Error: {e}") >> "%PYTHON_SCRIPT%"
echo     sys.exit(1) >> "%PYTHON_SCRIPT%"

:: Run Python script
echo Aplicando correcciones...
python "%PYTHON_SCRIPT%" "%TARGET_FILE%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Hubo un problema ejecutando el script de correccion.
    del "%PYTHON_SCRIPT%"
    pause
    exit /b 1
)

:: Cleanup
del "%PYTHON_SCRIPT%"

echo.
echo ===========================================
echo   PROCESO COMPLETADO
echo ===========================================
echo.
pause
