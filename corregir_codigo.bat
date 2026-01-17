@echo off
TITLE Auto-Correccion de Codigo - Vectora
cls

echo ========================================================
echo   AUTO-CORRECCION DE CODIGO - VECTORA
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

echo ATENCION: Este script modificara archivos automaticamente
echo.
echo Cambios que se aplicaran:
echo   1. Formatear codigo con BLACK
echo   2. Ordenar imports con ISORT
echo.
choice /C SN /M "Continuar con las correcciones"
if %errorlevel% equ 2 (
    echo Operacion cancelada
    pause
    exit /b 0
)

echo.
echo ========================================================
echo [1/2] FORMATEANDO CODIGO CON BLACK
echo ========================================================
echo.
black backend ui utils main.py
if %errorlevel% neq 0 (
    echo [ERROR] Hubo problemas con el formateo
    pause
    exit /b 1
)
echo [OK] Formateo completado
echo.

echo ========================================================
echo [2/2] ORDENANDO IMPORTS CON ISORT
echo ========================================================
echo.
isort backend ui utils main.py
if %errorlevel% neq 0 (
    echo [ERROR] Hubo problemas ordenando imports
    pause
    exit /b 1
)
echo [OK] Imports ordenados
echo.

echo ========================================================
echo   CORRECCIONES APLICADAS EXITOSAMENTE
echo ========================================================
echo.
echo Los siguientes cambios se aplicaron:
echo   - Codigo formateado segun estandar Black
echo   - Imports ordenados segun estandar isort
echo.
echo RECOMENDACION: Ejecuta 'verificar_codigo.bat' para confirmar
echo.
pause
