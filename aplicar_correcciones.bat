@echo off
TITLE Aplicar Correcciones Criticas - Vectora
cls

echo ========================================================
echo   APLICANDO CORRECCIONES AUTOMATICAS
echo ========================================================
echo.

:: Verificar que existe el venv
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] No se encuentra el entorno virtual
    echo Ejecuta 'recrear_venv.bat' primero
    pause
    exit /b 1
)

:: Activar entorno
call venv\Scripts\activate

echo Ejecutando script de correcciones (tools/fix_code.py)...
python tools/fix_code.py

if %errorlevel% neq 0 (
    echo [ERROR] Fallo al aplicar correcciones
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   PROCESO COMPLETADO
echo ========================================================
echo Ahora ejecuta 'ejecutar_tests.bat' para verificar.
echo.
pause
