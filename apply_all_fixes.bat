@echo off
setlocal
echo ==========================================
echo Vectora Maintenance & Refactor Tool
echo ==========================================

echo [1/2] Limpiando directorios duplicados...
call cleanup_structure.bat
if %ERRORLEVEL% NEQ 0 (
    echo [ADVERTENCIA] La limpieza de directorios reporto errores.
    echo Es posible que ya se haya ejecutado anteriormente.
    echo Continuando...
)

echo.
echo [2/2] Aplicando refactorizacion de codigo backend...
python tools/apply_backend_refactor.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo al ejecutar el script de Python.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Mantenimiento Completado Exitosamente
echo ==========================================
pause
