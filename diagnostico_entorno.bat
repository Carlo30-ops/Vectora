@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
TITLE Diagnostico de Entorno Virtual Python - Vectora

set LOG_FILE=diagnostico_entorno.log
echo. > %LOG_FILE%

echo ================================================ >> %LOG_FILE%
echo DIAGNOSTICO DE ENTORNO VIRTUAL >> %LOG_FILE%
echo Fecha: %date% %time% >> %LOG_FILE%
echo ================================================ >> %LOG_FILE%
echo. >> %LOG_FILE%

echo [DIAGNOSTICO] Iniciando analisis... 
echo [DIAGNOSTICO] Iniciando analisis... >> %LOG_FILE%

:: Test 1: Verificar Python
echo. >> %LOG_FILE%
echo [TEST 1] Verificando Python... >> %LOG_FILE%
python --version >> %LOG_FILE% 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado >> %LOG_FILE%
    echo [ERROR] Python no encontrado en PATH
    goto :END
) else (
    echo [OK] Python encontrado >> %LOG_FILE%
    echo [OK] Python encontrado
)

:: Test 2: Verificar carpeta venv
echo. >> %LOG_FILE%
echo [TEST 2] Verificando carpeta venv... >> %LOG_FILE%
if exist "venv" (
    echo [OK] Carpeta venv existe >> %LOG_FILE%
    echo [OK] Carpeta venv existe
    
    if exist "venv\Scripts\python.exe" (
        echo [OK] venv\Scripts\python.exe existe >> %LOG_FILE%
        echo [OK] venv\Scripts\python.exe existe
    ) else (
        echo [ERROR] venv\Scripts\python.exe NO existe >> %LOG_FILE%
        echo [ERROR] venv\Scripts\python.exe NO existe
    )
    
    if exist "venv\Scripts\activate.bat" (
        echo [OK] venv\Scripts\activate.bat existe >> %LOG_FILE%
        echo [OK] venv\Scripts\activate.bat existe
    ) else (
        echo [ERROR] venv\Scripts\activate.bat NO existe >> %LOG_FILE%
        echo [ERROR] venv\Scripts\activate.bat NO existe
    )
) else (
    echo [INFO] Carpeta venv NO existe (se necesita crear) >> %LOG_FILE%
    echo [INFO] Carpeta venv NO existe (se necesita crear)
)

:: Test 3: Intentar activar venv (si existe)
if exist "venv\Scripts\activate.bat" (
    echo. >> %LOG_FILE%
    echo [TEST 3] Intentando activar entorno virtual... >> %LOG_FILE%
    echo [TEST 3] Intentando activar entorno virtual...
    
    ENDLOCAL
    call venv\Scripts\activate.bat >> %LOG_FILE% 2>&1
    set ACTIVATE_ERROR=%errorlevel%
    SETLOCAL ENABLEDELAYEDEXPANSION
    
    if !ACTIVATE_ERROR! equ 0 (
        echo [OK] Entorno activado correctamente >> %LOG_FILE%
        echo [OK] Entorno activado correctamente
    ) else (
        echo [ERROR] No se pudo activar (errorlevel: !ACTIVATE_ERROR!) >> %LOG_FILE%
        echo [ERROR] No se pudo activar (errorlevel: !ACTIVATE_ERROR!)
    )
)

:: Test 4: Verificar requirements.txt
echo. >> %LOG_FILE%
echo [TEST 4] Verificando requirements.txt... >> %LOG_FILE%
if exist "requirements.txt" (
    echo [OK] requirements.txt encontrado >> %LOG_FILE%
    echo [OK] requirements.txt encontrado
    echo Contenido: >> %LOG_FILE%
    type requirements.txt >> %LOG_FILE%
) else (
    echo [WARNING] requirements.txt NO encontrado >> %LOG_FILE%
    echo [WARNING] requirements.txt NO encontrado
)

:END
echo. >> %LOG_FILE%
echo ================================================ >> %LOG_FILE%
echo FIN DEL DIAGNOSTICO >> %LOG_FILE%
echo ================================================ >> %LOG_FILE%

echo.
echo [COMPLETO] Diagnostico finalizado. Revisa el archivo: %LOG_FILE%
echo.
type %LOG_FILE%
echo.
echo Presiona cualquier tecla para salir...
pause >nul
