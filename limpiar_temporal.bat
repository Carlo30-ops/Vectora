@echo off
TITLE Limpiar Archivos Temporales - Vectora
cls

echo ========================================================
echo   LIMPIEZA DE ARCHIVOS TEMPORALES
echo ========================================================
echo.

echo Los siguientes archivos seran eliminados:
echo   - diagnostico_entorno.bat
echo   - diagnostico_entorno.log
echo.

if exist "diagnostico_entorno.bat" (
    echo Eliminando diagnostico_entorno.bat...
    del /q "diagnostico_entorno.bat"
    echo [OK] Eliminado
)

if exist "diagnostico_entorno.log" (
    echo Eliminando diagnostico_entorno.log...
    del /q "diagnostico_entorno.log"
    echo [OK] Eliminado
)

echo.
echo ========================================================
echo   LIMPIEZA COMPLETA
echo ========================================================
echo.
pause
