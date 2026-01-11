@echo off
setlocal enabledelayedexpansion
title Vectora V5 Migration Master

echo ===================================================
echo    VECTORA V5 - MIGRATION MASTER SCRIPT
echo ===================================================
echo.

:menu
echo Seleccione el paso a ejecutar:
echo 1. Aplicar Estandarizacion Backend (Fase 1) [YA APLICADO]
echo 2. Verificar Entorno y Dependencias
echo 3. Correr Tests de Integracion (Backend)
echo 4. Salir
echo.

set /p choice=Ingrese su opcion (1-4): 

if "%choice%"=="1" goto phase1
if "%choice%"=="2" goto verify_env
if "%choice%"=="3" goto run_tests
if "%choice%"=="4" goto exit

:phase1
echo.
echo [INFO] Aplicando Fase 1: Estandarizacion Backend...
python apply_phase1.py
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Fase 1 aplicada exitosamente.
) else (
    echo [ERROR] Hubo un fallo al aplicar la Fase 1.
)
pause
goto menu

:verify_env
echo.
echo [INFO] Verificando entorno...
call check_env.bat
pause
goto menu

:run_tests
echo.
echo [INFO] Ejecutando tests de backend...
pytest tests/test_pdf_merger.py tests/test_pdf_splitter.py
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Todos los tests pasaron.
) else (
    echo [ERROR] Algunos tests fallaron.
)
pause
goto menu

:exit
echo.
echo Saliendo de Migration Master.
exit /b 0
