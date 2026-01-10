@echo off
echo ==========================================
echo   Ejecutar Tests de Vectora
echo ==========================================
echo.

REM Verificar entorno virtual
if not exist venv\Scripts\python.exe (
    echo [ERROR] No se encontro el entorno virtual
    echo Ejecuta quick_setup.bat primero
    pause
    exit /b 1
)

REM Instalar pytest si no está instalado
echo [1/3] Verificando pytest...
venv\Scripts\pip.exe show pytest > nul 2>&1
if errorlevel 1 (
    echo    pytest no instalado, instalando...
    venv\Scripts\pip.exe install pytest pytest-cov --quiet
    echo    [OK] pytest instalado
) else (
    echo    [OK] pytest ya instalado
)

echo.
echo [2/3] Ejecutando tests...
echo ==========================================
venv\Scripts\python.exe -m pytest tests/ -v

echo.
echo [3/3] Generando reporte de coverage...
echo ==========================================
echo Reporte HTML guardado en: htmlcov\index.html
echo.

if exist htmlcov\index.html (
    echo ¿Quieres abrir el reporte de coverage en el navegador? (S/N)
    set /p OPEN_REPORT=
    if /i "%OPEN_REPORT%"=="S" (
        start htmlcov\index.html
    )
)

echo.
pause
