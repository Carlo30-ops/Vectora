@echo off
setlocal
title Vectora Widget Tester

:: 1. Define Root (One level up from maintenance)
set "PROJECT_ROOT=%~dp0.."
set "PYTHONPATH=%PROJECT_ROOT%"
cd /d "%PROJECT_ROOT%"

:MENU
cls
echo ==================================================
echo   VECTORA WIDGET DEBUGGER
echo ==================================================
echo.
echo  [1] Security Widget (Encriptar/Desencriptar)
echo  [2] Merge Widget    (Unir PDFs)
echo  [3] Split Widget    (Dividir PDFs)
echo  [4] OCR Widget      (Texto a PDF)
echo  [5] PDF Compressor  (Reducir tamanio)
echo.
echo  [0] Salir
echo.
echo ==================================================
set /p "op=Selecciona una opcion: "

if "%op%"=="1" goto RUN_SECURITY
if "%op%"=="2" goto RUN_MERGE
if "%op%"=="3" goto RUN_SPLIT
if "%op%"=="4" goto RUN_OCR
if "%op%"=="5" goto RUN_COMPRESS
if "%op%"=="0" goto END

echo Opcion invalida.
pause
goto MENU

:RUN_SECURITY
echo Lanzando Security Widget...
python maintenance/debug_runner.py security
pause
goto MENU

:RUN_MERGE
echo Lanzando Merge Widget...
python maintenance/debug_runner.py merge
pause
goto MENU

:RUN_SPLIT
echo Lanzando Split Widget...
python maintenance/debug_runner.py split
pause
goto MENU

:RUN_OCR
echo Lanzando OCR Widget...
python maintenance/debug_runner.py ocr
pause
goto MENU

:RUN_COMPRESS
echo Lanzando Compressor Widget...
python maintenance/debug_runner.py compress
pause
goto MENU

:END
exit /b 0
