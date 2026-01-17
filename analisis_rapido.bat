@echo off
TITLE Analisis Rapido - Vectora
cls

echo ========================================================
echo   ANALISIS RAPIDO DE CODIGO - VECTORA
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
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo activar el entorno
    pause
    exit /b 1
)

echo [1/4] Verificando formato...
black --check backend ui utils main.py >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Formato correcto
) else (
    echo [!] Necesita formateo - ejecuta: corregir_codigo.bat
)

echo [2/4] Verificando imports...
isort --check-only backend ui utils main.py >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Imports ordenados
) else (
    echo [!] Necesita ordenar imports - ejecuta: corregir_codigo.bat
)

echo [3/4] Contando archivos Python...
set /a PY_FILES=0
for /r %%i in (*.py) do set /a PY_FILES+=1
echo [INFO] Total de archivos .py: %PY_FILES%

echo [4/4] Verificando estructura del proyecto...
if exist "backend" echo [OK] Carpeta backend/
if exist "ui" echo [OK] Carpeta ui/
if exist "utils" echo [OK] Carpeta utils/
if exist "tests" echo [OK] Carpeta tests/
if exist "main.py" echo [OK] Archivo main.py

echo.
echo ========================================================
echo   ANALISIS RAPIDO COMPLETADO
echo ========================================================
echo.
echo Para verificacion completa ejecuta: verificar_codigo.bat
echo Para auto-correccion ejecuta: corregir_codigo.bat
echo Para ejecutar tests: ejecutar_tests.bat
echo.
pause
