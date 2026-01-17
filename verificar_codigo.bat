@echo off
TITLE Verificacion Completa de Codigo - Vectora
cls

echo ========================================================
echo   VERIFICACION COMPLETA DE CODIGO - VECTORA
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

set ERROR_COUNT=0

echo ========================================================
echo [1/5] EJECUTANDO TESTS CON PYTEST
echo ========================================================
echo.
pytest
if %errorlevel% neq 0 (
    echo [WARNING] Algunos tests fallaron
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Todos los tests pasaron
)
echo.
pause

echo ========================================================
echo [2/5] VERIFICANDO TIPOS CON MYPY
echo ========================================================
echo.
mypy backend ui utils --ignore-missing-imports
if %errorlevel% neq 0 (
    echo [WARNING] Se encontraron errores de tipado
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Verificacion de tipos exitosa
)
echo.
pause

echo ========================================================
echo [3/5] VERIFICANDO FORMATO CON BLACK
echo ========================================================
echo.
black --check backend ui utils main.py
if %errorlevel% neq 0 (
    echo [WARNING] Algunos archivos necesitan formateo
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Formato correcto
)
echo.
pause

echo ========================================================
echo [4/5] VERIFICANDO IMPORTS CON ISORT
echo ========================================================
echo.
isort --check-only backend ui utils main.py
if %errorlevel% neq 0 (
    echo [WARNING] Algunos imports necesitan ordenamiento
    set /a ERROR_COUNT+=1
) else (
    echo [OK] Imports ordenados correctamente
)
echo.
pause

echo ========================================================
echo [5/5] ANALISIS ESTATICO CON PYLINT
echo ========================================================
echo.
pylint backend ui utils main.py --exit-zero
echo.
echo [INFO] Pylint completado (revisa los warnings arriba)
echo.
pause

echo ========================================================
echo   RESUMEN DE VERIFICACION
echo ========================================================
if %ERROR_COUNT% equ 0 (
    echo [EXCELENTE] No se encontraron problemas criticos
) else (
    echo [ATENCION] Se encontraron %ERROR_COUNT% categorias con problemas
    echo Revisa los mensajes arriba para mas detalles
)
echo.
echo Reporte de cobertura HTML generado en: htmlcov\index.html
echo.
pause
