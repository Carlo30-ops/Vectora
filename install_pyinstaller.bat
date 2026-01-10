@echo off
echo ==========================================
echo   Instalador de PyInstaller
echo ==========================================
echo.

REM Verificar entorno virtual
if not exist venv\Scripts\pip.exe (
    echo [ERROR] No se encontro el entorno virtual
    echo Por favor, ejecuta quick_setup.bat primero
    pause
    exit /b 1
)

echo [1/3] Verificando si PyInstaller esta instalado...
venv\Scripts\pip.exe show pyinstaller > nul 2>&1

if errorlevel 1 (
    echo    [INFO] PyInstaller NO esta instalado
    echo.
    echo [2/3] Instalando PyInstaller...
    venv\Scripts\pip.exe install pyinstaller
    
    if errorlevel 1 (
        echo    [ERROR] Fallo la instalacion
        pause
        exit /b 1
    )
    echo    [OK] PyInstaller instalado correctamente
) else (
    echo    [OK] PyInstaller ya esta instalado
    echo.
    echo [2/3] Actualizando PyInstaller a la ultima version...
    venv\Scripts\pip.exe install --upgrade pyinstaller
)

echo.
echo [3/3] Verificando instalacion...
venv\Scripts\pip.exe show pyinstaller

echo.
echo ==========================================
echo [EXITO] PyInstaller configurado
echo ==========================================
echo.
echo Ahora ejecuta generate_requirements.bat para actualizar
echo el archivo requirements.txt con PyInstaller incluido.
echo.
pause
