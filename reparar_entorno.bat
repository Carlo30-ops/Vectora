@echo off
TITLE Analisis y Reparacion de Entorno Virtual Python - Vectora

echo ========================================================
echo      ANALISIS Y REPARACION DE ENTORNO VIRTUAL
echo ========================================================
echo.

:: 1. Verificar si Python esta instalado en el sistema
echo [1/5] Buscando instalacion de Python en el sistema...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] No se detecto 'python' en el PATH.
    echo Por favor instala Python 3.10+ y asegurate de marcar "Add Python to PATH".
    pause
    exit /b 1
)
python --version
echo [OK] Python detectado.
echo.

:: 2. Analizar estado de la carpeta venv
echo [2/5] Analizando entorno virtual 'venv'...
set RECREATE_VENV=0
set VENV_PATH=venv

if exist "%VENV_PATH%" (
    if exist "%VENV_PATH%\Scripts\python.exe" (
        echo      - La carpeta '%VENV_PATH%' existe.
        echo      - Verificando integridad...
        "%VENV_PATH%\Scripts\python.exe" --version >nul 2>&1
        if %errorlevel% equ 0 (
            echo [OK] El entorno virtual parece valido.
        ) else (
            echo [ALERTA] El entorno virtual esta corrupto (python no responde).
            set RECREATE_VENV=1
        )
    ) else (
        echo [ALERTA] Carpeta 'venv' existe pero falta Scripts\python.exe.
        set RECREATE_VENV=1
    )
) else (
    echo [INFO] No se encontro carpeta '%VENV_PATH%'. Se creara una nueva.
    set RECREATE_VENV=1
)

:: 3. Recrear venv si es necesario
if %RECREATE_VENV% equ 1 (
    echo.
    echo [3/5] Reconstruyendo entorno virtual...
    if exist "%VENV_PATH%" (
        echo      - Eliminando entorno corrupto/incompleto...
        rmdir /s /q "%VENV_PATH%"
    )
    echo      - Creando nuevo entorno virtual (esto puede tardar unos segundos)...
    python -m venv %VENV_PATH%
    if %errorlevel% neq 0 (
        echo [ERROR] Fallo al crear el entorno virtual usando 'python -m venv %VENV_PATH%'.
        pause
        exit /b 1
    )
    echo [OK] Entorno creado exitosamente.
) else (
    echo [SKIP] Paso 3 omitido (el entorno ya existe y funciona).
)
echo.

:: 4. Configurar e Instalar Dependencias
echo [4/5] Configurando dependencias...
echo      - Activando entorno...
call "%VENV_PATH%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo activar el entorno virtual.
    pause
    exit /b 1
)

echo      - Actualizando pip...
python -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo [WARNING] No se pudo actualizar pip, continuando...
)

if exist "requirements.txt" (
    echo      - Instalando librerias desde requirements.txt...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Hubo un error instalando las dependencias.
        echo Revisa los mensajes de error arriba.
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas/verificadas.
) else (
    echo [WARNING] No se encontro 'requirements.txt'. No se instalaron librerias.
)
echo.

:: 5. Verificacion Final
echo [5/5] Verificacion final...
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} corriendo en: {sys.prefix}')"
echo.

echo ========================================================
echo      PROCESO COMPLETADO EXITOSAMENTE
echo ========================================================
echo Tu entorno virtual esta listo y configurado.
echo Para usarlo manualmente ejecuta: call venv\Scripts\activate
echo.
pause
