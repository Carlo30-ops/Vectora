@echo off
echo ==========================================
echo   Vectora - Configuracion Rapida
echo ==========================================
echo.
echo Este script realiza la configuracion inicial del proyecto.
echo.

REM 1. Crear entorno virtual si no existe
echo [1/5] Verificando entorno virtual...
if not exist venv\ (
    echo    Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo    [ERROR] Fallo al crear entorno virtual
        pause
        exit /b 1
    )
    echo    [OK] Entorno virtual creado
) else (
    echo    [OK] Entorno virtual ya existe
)
echo.

REM 2. Actualizar pip
echo [2/5] Actualizando pip...
venv\Scripts\python.exe -m pip install --upgrade pip --quiet
echo    [OK] pip actualizado
echo.

REM 3. Instalar dependencias
echo [3/5] Instalando dependencias...
if exist requirements.txt (
    echo    Instalando desde requirements.txt...
    venv\Scripts\pip.exe install -r requirements.txt
    if errorlevel 1 (
        echo    [WARN] Algunas dependencias fallaron
    ) else (
        echo    [OK] Dependencias instaladas
    )
) else (
    echo    [WARN] requirements.txt no encontrado
    echo    Instalando dependencias basicas...
    venv\Scripts\pip.exe install PySide6 PyPDF2 pikepdf pdf2docx pdf2image Pillow pytesseract python-dotenv
)
echo.

REM 4. Crear directorios necesarios
echo [4/5] Creando directorios necesarios...
if not exist temp\ mkdir temp
if not exist output\ mkdir output
if not exist assets\ mkdir assets
echo    [OK] Directorios creados
echo.

REM 5. Verificar archivo .env
echo [5/5] Verificando configuracion...
if not exist .env (
    echo    [WARN] Archivo .env no encontrado
    echo    Creando .env basico...
    (
    echo # Vectora - Configuracion
    echo.
    echo # Rutas de software externo
    echo TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
    echo POPPLER_PATH=C:\Program Files\poppler-25.12.0\Library\bin
    echo.
    echo # Configuracion de OCR
    echo TESSERACT_LANG=spa+eng
    echo OCR_DPI=300
    echo.
    echo # Configuracion de conversion
    echo PDF_TO_IMAGE_DPI=300
    echo IMAGE_FORMAT=PNG
    echo.
    echo # Directorios
    echo TEMP_DIR=./temp
    echo OUTPUT_DIR=./output
    echo.
    echo # Limites
    echo MAX_FILE_SIZE_MB=100
    echo MAX_BATCH_FILES=50
    ) > .env
    echo    [OK] .env creado - REVISA Y AJUSTA LAS RUTAS
) else (
    echo    [OK] .env ya existe
)
echo.

echo ==========================================
echo [EXITO] Configuracion completada
echo ==========================================
echo.
echo Proximos pasos:
echo 1. Revisa y ajusta el archivo .env con las rutas correctas
echo 2. Instala Tesseract OCR si aun no lo tienes
echo 3. Descarga y descomprime Poppler
echo 4. Ejecuta: venv\Scripts\python.exe main.py
echo.
pause
