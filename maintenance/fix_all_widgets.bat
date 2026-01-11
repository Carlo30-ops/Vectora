@echo off
setlocal EnableDelayedExpansion

echo ===========================================
echo   Vectora Widget Fixer (ALL Widgets)
echo ===========================================

:: Define directories
set "WIDGETS_DIR=%~dp0..\ui\components\operation_widgets"
set "PYTHON_SCRIPT=%TEMP%\fix_widgets_temp.py"

:: Check if directory exists
if not exist "%WIDGETS_DIR%" (
    echo [ERROR] No se encuentra el directorio:
    echo %WIDGETS_DIR%
    pause
    exit /b 1
)

:: Generate Python script for batch processing
echo import sys > "%PYTHON_SCRIPT%"
echo import os >> "%PYTHON_SCRIPT%"
echo import glob >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo widgets_dir = sys.argv[1] >> "%PYTHON_SCRIPT%"
echo print(f"Analizando widgets en: {widgets_dir}") >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo files = glob.glob(os.path.join(widgets_dir, "*.py")) >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo replacements = [ >> "%PYTHON_SCRIPT%"
echo     ('from icons.icons import IconHelper', 'from ui.components.ui_helpers import IconHelper'), >> "%PYTHON_SCRIPT%"
echo     ('self.finished.emit(result)', 'self.finished.emit(result.to_dict())') >> "%PYTHON_SCRIPT%"
echo ] >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo total_fixes = 0 >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo for file_path in files: >> "%PYTHON_SCRIPT%"
echo     filename = os.path.basename(file_path) >> "%PYTHON_SCRIPT%"
echo     if filename == "__init__.py" or filename == "base_operation.py": >> "%PYTHON_SCRIPT%"
echo         continue >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo     try: >> "%PYTHON_SCRIPT%"
echo         with open(file_path, 'r', encoding='utf-8') as f: >> "%PYTHON_SCRIPT%"
echo             content = f.read() >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo         file_changes = 0 >> "%PYTHON_SCRIPT%"
echo         for old, new in replacements: >> "%PYTHON_SCRIPT%"
echo             if old in content: >> "%PYTHON_SCRIPT%"
echo                 content = content.replace(old, new) >> "%PYTHON_SCRIPT%"
echo                 file_changes += 1 >> "%PYTHON_SCRIPT%"
echo                 print(f"  [FIX] {filename}: {old[:20]}...") >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo         if file_changes ^> 0: >> "%PYTHON_SCRIPT%"
echo             with open(file_path, 'w', encoding='utf-8') as f: >> "%PYTHON_SCRIPT%"
echo                 f.write(content) >> "%PYTHON_SCRIPT%"
echo             total_fixes += file_changes >> "%PYTHON_SCRIPT%"
echo     except Exception as e: >> "%PYTHON_SCRIPT%"
echo         print(f"  [ERR] {filename}: {e}") >> "%PYTHON_SCRIPT%"
echo. >> "%PYTHON_SCRIPT%"
echo print(f"\nResumen: {total_fixes} correcciones aplicadas en total.") >> "%PYTHON_SCRIPT%"

:: Run Python script
echo Ejecutando correcciones masivas...
python "%PYTHON_SCRIPT%" "%WIDGETS_DIR%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Hubo un problema ejecutando el script.
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
