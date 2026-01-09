@echo off
REM Generador de Iconos para LocalPDF v5
REM Este script genera todos los iconos SVG necesarios

echo.
echo ============================================================
echo   Generador de Iconos - LocalPDF v5
echo ============================================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Por favor instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python encontrado. Generando iconos...
echo.

REM Ejecutar el script de generación
python generate_icons.py

if errorlevel 1 (
    echo.
    echo [ERROR] Hubo un problema al generar los iconos
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Generacion completada exitosamente!
echo ============================================================
echo.
echo Los iconos se encuentran en la carpeta: icons/
echo.
echo Presiona cualquier tecla para abrir la carpeta...
pause >nul

REM Abrir la carpeta de iconos
if exist "icons" (
    explorer "icons"
)

exit /b 0
