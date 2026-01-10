@echo off
echo ==========================================
echo   Test del Sistema de Logging
echo ==========================================
echo.
echo Este script ejecuta las pruebas del sistema de logging.
echo.

REM Verificar entorno virtual
if not exist venv\Scripts\python.exe (
    echo [ERROR] No se encontro el entorno virtual
    pause
    exit /b 1
)

echo Ejecutando tests de logging...
echo.
venv\Scripts\python.exe test_logging.py

echo.
echo ==========================================
echo Test completado
echo ==========================================
echo.
echo Para ver los logs:
if exist logs (
    echo    logs\vectora_*.log
) else (
    echo    %USERPROFILE%\Documents\Vectora\logs\vectora_*.log
)
echo.
pause
