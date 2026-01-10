@echo off
echo ==========================================
echo   Fix Build - Solucion Rapida
echo ==========================================
echo.
echo Este script corrige los problemas de build:
echo 1. Carpeta libs/ inexistente
echo 2. setup_icons.py requiriendo requests
echo.

echo [1/2] Verificando estructura de directorios...

REM Crear directorios necesarios si no existen
if not exist assets mkdir assets
if not exist assets\icons mkdir assets\icons
if not exist icons mkdir icons
if not exist logs mkdir logs

echo    [OK] Directorios verificados

echo.
echo [2/2] Ejecutando build corregido...
echo.

REM Ejecutar build con las correcciones
call build_exe.bat

echo.
echo ==========================================
echo Fix completado
echo ==========================================
pause
