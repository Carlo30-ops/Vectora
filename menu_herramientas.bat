@echo off
TITLE Menu de Herramientas - Vectora
cls

:MENU
echo ========================================================
echo   MENU DE HERRAMIENTAS - VECTORA
echo ========================================================
echo.

echo [DIAGNOSTICO Y ANALISIS]
echo   1. Resumen de Estado
echo   2. Analisis Detallado de Problemas
echo   3. Generar Plan de Correccion
echo.

echo [VERIFICACION]
echo   4. Verificacion Rapida
echo   5. Verificacion Completa
echo   6. Ejecutar Solo Tests
echo.

echo [CORRECCION]
echo   7. Auto-Corregir Codigo ^(Black + isort^)
echo.

echo [ENTORNO]
echo   8. Verificar Entorno Virtual
echo   9. Recrear Entorno Virtual
echo.

echo [UTILIDADES]
echo   A. Abrir Reporte de Cobertura
echo   B. Limpiar Archivos Temporales
echo.

echo   0. Salir
echo.

echo ========================================================
set /p opcion="Selecciona una opcion: "

if "%opcion%"=="1" goto RESUMEN
if "%opcion%"=="2" goto ANALISIS
if "%opcion%"=="3" goto PLAN
if "%opcion%"=="4" goto VER_RAPIDA
if "%opcion%"=="5" goto VER_COMPLETA
if "%opcion%"=="6" goto TESTS
if "%opcion%"=="7" goto CORREGIR
if "%opcion%"=="8" goto VER_VENV
if "%opcion%"=="9" goto RECREAR_VENV
if /i "%opcion%"=="A" goto COBERTURA
if /i "%opcion%"=="B" goto LIMPIAR
if "%opcion%"=="0" goto FIN

echo Opcion invalida
timeout /t 2 >nul
goto MENU

:RESUMEN
cls
call resumen_estado.bat
goto MENU

:ANALISIS
cls
call analizar_problemas.bat
goto MENU

:PLAN
cls
call generar_plan.bat
goto MENU

:VER_RAPIDA
cls
call analisis_rapido.bat
goto MENU

:VER_COMPLETA
cls
call verificar_codigo.bat
goto MENU

:TESTS
cls
call ejecutar_tests.bat
goto MENU

:CORREGIR
cls
call corregir_codigo.bat
goto MENU

:VER_VENV
cls
call verificar_venv.bat
goto MENU

:RECREAR_VENV
cls
call recrear_venv.bat
goto MENU

:COBERTURA
cls
echo Abriendo reporte de cobertura...
if exist "htmlcov\index.html" (
    start htmlcov\index.html
    echo [OK] Reporte abierto en navegador
) else (
    echo [ERROR] No se encuentra el reporte de cobertura
    echo Ejecuta 'ejecutar_tests.bat' primero
)
timeout /t 3 >nul
goto MENU

:LIMPIAR
cls
call limpiar_temporal.bat
goto MENU

:FIN
echo.
echo Saliendo...
exit /b 0
