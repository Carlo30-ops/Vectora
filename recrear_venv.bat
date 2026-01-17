@echo off
TITLE Recreacion Completa de Entorno Virtual - Vectora
cls

echo ========================================================
echo   RECREACION COMPLETA DE ENTORNO VIRTUAL
echo ========================================================
echo.

:: Paso 1: Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado en PATH
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python detectado.
echo.

:: Paso 2: Eliminar venv corrupto
echo [2/4] Eliminando entorno virtual corrupto...
if exist "venv" (
    echo      Eliminando carpeta 'venv'...
    rmdir /s /q "venv"
    if exist "venv" (
        echo [ERROR] No se pudo eliminar la carpeta venv
        echo      Asegurate de que no este en uso y vuelve a intentar
        echo.
        pause
        exit /b 1
    )
    echo [OK] Entorno anterior eliminado.
) else (
    echo [INFO] No habia entorno previo.
)
echo.

:: Paso 3: Crear nuevo venv
echo [3/4] Creando nuevo entorno virtual limpio...
echo      Ejecutando: python -m venv venv
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Fallo al crear el entorno virtual
    echo.
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] El entorno se creo pero falta python.exe
    echo.
    pause
    exit /b 1
)

echo [OK] Entorno virtual creado exitosamente.
echo.

:: Paso 4: Instalar dependencias
echo [4/4] Instalando dependencias...

:: Activar entorno (sin delayed expansion)
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo activar el entorno virtual
    echo.
    pause
    exit /b 1
)

echo [OK] Entorno activado.
echo.

echo      Actualizando pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip actualizado.
echo.

if exist "requirements.txt" (
    echo      Instalando desde requirements.txt...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Hubo problemas instalando dependencias
        echo      Revisa los mensajes arriba
        echo.
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas.
) else (
    echo [WARNING] No se encontro requirements.txt
)

echo.
echo ========================================================
echo   ENTORNO RECREADO EXITOSAMENTE
echo ========================================================
echo.
echo Informacion del entorno:
python -c "import sys; print(f'Python {sys.version}')"
python -c "import sys; print(f'Ubicacion: {sys.prefix}')"
echo.
echo Para activar manualmente: call venv\Scripts\activate
echo.
pause
