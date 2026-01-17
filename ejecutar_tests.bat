@echo off
TITLE Ejecutar Tests - Vectora
cls

echo ========================================================
echo   EJECUTAR TESTS - VECTORA
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

echo Ejecutando tests con pytest...
echo.
pytest
echo.

if %errorlevel% equ 0 (
    echo ========================================================
    echo   TODOS LOS TESTS PASARON
    echo ========================================================
) else (
    echo ========================================================
    echo   ALGUNOS TESTS FALLARON
    echo ========================================================
    echo Revisa los mensajes arriba para mas detalles
)

echo.
echo Reporte de cobertura: htmlcov\index.html
echo.
pause
