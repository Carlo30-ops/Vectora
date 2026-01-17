@echo off
TITLE Verificacion de Entorno Virtual - Vectora
cls

echo ========================================================
echo   VERIFICACION DE ENTORNO VIRTUAL
echo ========================================================
echo.

:: Verificar que existe el venv
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] No se encuentra el entorno virtual
    echo.
    echo Ejecuta 'recrear_venv.bat' primero
    echo.
    pause
    exit /b 1
)

echo [1/3] Activando entorno virtual...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo activar el entorno
    pause
    exit /b 1
)
echo [OK] Entorno activado
echo.

echo [2/3] Informacion del sistema:
echo ----------------------------------------
python -c "import sys; print(f'Python Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
python -c "import sys; print(f'Ejecutable: {sys.executable}')"
python -c "import sys; print(f'Prefix: {sys.prefix}')"
echo.

echo [3/3] Verificando paquetes instalados:
echo ----------------------------------------
pip list
echo.

echo ========================================================
echo   VERIFICACION COMPLETA
echo ========================================================
echo El entorno esta funcionando correctamente
echo.
pause
