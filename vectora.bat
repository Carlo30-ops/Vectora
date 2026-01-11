@echo off
setlocal enabledelayedexpansion
title Vectora - Panel de Control
color 0A

:menu
cls
echo ==========================================
echo     VECTORA v5.0.0 - Panel de Control
echo ==========================================
echo.
echo Seleccione una opcion:
echo.
echo   [1] SETUP - Configurar entorno inicial
echo   [2] RUN   - Ejecutar aplicacion (desarrollo)
echo   [3] TEST  - Ejecutar suite de tests
echo   [4] BUILD - Generar ejecutable (.exe)
echo   [5] VERIFY- Verificar entorno y salud del proyecto
echo   [6] TOOLS - Herramientas adicionales
echo   [7] CLEAN - Limpiar archivos temporales
echo   [0] SALIR
echo.
set /p opcion="Opcion: "

if "%opcion%"=="1" goto setup
if "%opcion%"=="2" goto run
if "%opcion%"=="3" goto test
if "%opcion%"=="4" goto build
if "%opcion%"=="5" goto verify
if "%opcion%"=="6" goto tools
if "%opcion%"=="7" goto clean
if "%opcion%"=="0" goto end
goto menu

:setup
cls
echo ==========================================
echo   CONFIGURAR ENTORNO INICIAL
echo ==========================================
echo.

REM 1. Crear entorno virtual
echo [1/5] Verificando entorno virtual...
if not exist venv\ (
    echo    Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo    [ERROR] Fallo al crear entorno virtual
        pause
        goto menu
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
    echo    [ERROR] requirements.txt no encontrado
    pause
    goto menu
)
echo.

REM 4. Crear directorios necesarios
echo [4/5] Creando directorios necesarios...
if not exist temp\ mkdir temp
if not exist output\ mkdir output
if not exist assets\ mkdir assets
if not exist logs\ mkdir logs
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
pause
goto menu

:run
cls
echo ==========================================
echo   EJECUTAR APLICACION
echo ==========================================
echo.

if not exist venv\Scripts\python.exe (
    echo [ERROR] No se encontro el entorno virtual
    echo Ejecuta la opcion [1] SETUP primero
    pause
    goto menu
)

echo Iniciando Vectora...
echo.
venv\Scripts\python.exe main.py

if errorlevel 1 (
    echo.
    echo [ERROR] La aplicacion fallo al ejecutarse
    pause
)
goto menu

:test
cls
echo ==========================================
echo   EJECUTAR TESTS
echo ==========================================
echo.

if not exist venv\Scripts\python.exe (
    echo [ERROR] No se encontro el entorno virtual
    echo Ejecuta la opcion [1] SETUP primero
    pause
    goto menu
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
venv\Scripts\python.exe -m pytest tests/ --cov=backend --cov=utils --cov-report=html --quiet

if exist htmlcov\index.html (
    echo Reporte HTML guardado en: htmlcov\index.html
    echo.
    set /p OPEN_REPORT="¿Abrir reporte de coverage? (S/N): "
    if /i "!OPEN_REPORT!"=="S" (
        start htmlcov\index.html
    )
)
echo.
pause
goto menu

:build
cls
echo ==========================================
echo   GENERAR EJECUTABLE
echo ==========================================
echo.

if not exist venv\Scripts\python.exe (
    echo [ERROR] No se encontro el entorno virtual
    echo Ejecuta la opcion [1] SETUP primero
    pause
    goto menu
)

echo [1/6] Actualizando pip...
venv\Scripts\python.exe -m pip install --upgrade pip --quiet

echo.
echo [2/6] Verificando PyInstaller...
venv\Scripts\pip.exe show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo    PyInstaller no instalado, instalando...
    venv\Scripts\pip.exe install pyinstaller --quiet
    echo    [OK] PyInstaller instalado
) else (
    echo    [OK] PyInstaller ya instalado
)

echo.
echo [3/6] Asegurando sistema de iconos...
if exist setup_icons.py (
    venv\Scripts\python.exe setup_icons.py
)

echo.
echo [4/6] Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [5/6] Creando directorios necesarios...
if not exist output mkdir output
if not exist temp mkdir temp
if not exist logs mkdir logs

echo.
echo [6/6] Generando ejecutable con PyInstaller...
venv\Scripts\pyinstaller.exe Vectora.spec --noconfirm

echo.
echo ==========================================
if exist dist\Vectora\Vectora.exe (
    echo [EXITO] Ejecutable generado correctamente:
    echo    dist\Vectora\Vectora.exe
    echo.
    
    REM Copiar directorios necesarios
    if not exist dist\Vectora\output mkdir dist\Vectora\output
    if not exist dist\Vectora\temp mkdir dist\Vectora\temp
    if not exist dist\Vectora\logs mkdir dist\Vectora\logs
    
    REM Copiar .env si existe
    if exist .env (
        copy /Y .env dist\Vectora\.env > nul
        echo    [OK] Archivo .env copiado
    )
    
    REM Crear README en dist
    (
    echo Vectora v5.0.0 - Editor de PDFs
    echo.
    echo Ubicaciones importantes:
    echo - Logs: %%USERPROFILE%%\Documents\Vectora\logs\
    echo - Salida: output\
    echo - Temporales: temp\
    echo.
    echo Ejecuta: Vectora.exe
    ) > dist\Vectora\README.txt
    
    echo    [OK] Estructura completa
    echo.
    echo ==========================================
    echo Build completado exitosamente!
) else (
    echo [ERROR] Fallo la generacion del ejecutable.
    echo Revisa los errores arriba.
)
echo.
pause
goto menu

:verify
cls
echo ==========================================
echo   VERIFICAR ENTORNO Y SALUD
echo ==========================================
echo.

echo [1/4] Verificando Python...
python --version
if errorlevel 1 (
    echo    [ERROR] Python no encontrado
) else (
    echo    [OK] Python instalado
)
echo.

echo [2/4] Verificando entorno virtual...
if exist venv\Scripts\python.exe (
    echo    [OK] Entorno virtual existe
    echo.
    echo [3/4] Dependencias instaladas:
    venv\Scripts\pip.exe list
) else (
    echo    [WARN] Entorno virtual no existe
    echo    Ejecuta la opcion [1] SETUP para crearlo
)
echo.

echo [4/4] Verificando estructura del proyecto...
set ERRORS=0
if not exist main.py set /a ERRORS+=1
if not exist backend\services set /a ERRORS+=1
if not exist ui\components set /a ERRORS+=1
if not exist config\settings.py set /a ERRORS+=1

if %ERRORS% EQU 0 (
    echo    [OK] Estructura del proyecto correcta
) else (
    echo    [ERROR] Faltan archivos o directorios importantes
)

echo.
echo ==========================================
if %ERRORS% EQU 0 (
    echo Proyecto en buen estado
) else (
    echo Se encontraron problemas
)
echo ==========================================
pause
goto menu

:tools
cls
echo ==========================================
echo   HERRAMIENTAS ADICIONALES
echo ==========================================
echo.
echo   [1] Generar requirements.txt
echo   [2] Instalar/actualizar PyInstaller
echo   [3] Verificar entorno Python
echo   [4] Generar iconos
echo   [0] Volver al menu principal
echo.
set /p tool_opcion="Opcion: "

if "%tool_opcion%"=="1" goto gen_requirements
if "%tool_opcion%"=="2" goto install_pyinstaller
if "%tool_opcion%"=="3" goto check_env
if "%tool_opcion%"=="4" goto gen_icons
if "%tool_opcion%"=="0" goto menu
goto tools

:gen_requirements
cls
echo ==========================================
echo   GENERAR REQUIREMENTS.TXT
echo ==========================================
echo.

if not exist venv\Scripts\pip.exe (
    echo [ERROR] No se encontro el entorno virtual
    pause
    goto tools
)

echo [1/3] Generando requirements.txt con pip freeze...
venv\Scripts\pip.exe freeze > requirements_frozen.txt

if errorlevel 1 (
    echo [ERROR] Fallo al ejecutar pip freeze
    pause
    goto tools
)

echo [2/3] Filtrando dependencias principales...
(
echo # Vectora v5 - Dependencias con Versiones Exactas
echo # Generado automaticamente - NO editar manualmente
echo.
echo # === GUI Framework ===
findstr /i "PySide6==" requirements_frozen.txt
echo.
echo # === PDF Processing ===
findstr /i "PyPDF2==" requirements_frozen.txt
findstr /i "pikepdf==" requirements_frozen.txt
findstr /i "pdf2docx==" requirements_frozen.txt
findstr /i "docx2pdf==" requirements_frozen.txt
findstr /i "pdf2image==" requirements_frozen.txt
findstr /i "pymupdf==" requirements_frozen.txt 2>nul
echo.
echo # === Image Processing ===
findstr /i "Pillow==" requirements_frozen.txt
findstr /i "opencv-python==" requirements_frozen.txt
echo.
echo # === OCR ===
findstr /i "pytesseract==" requirements_frozen.txt
echo.
echo # === Utilities ===
findstr /i "python-dotenv==" requirements_frozen.txt
findstr /i "watchdog==" requirements_frozen.txt
echo.
echo # === Build Tools ===
findstr /i "pyinstaller==" requirements_frozen.txt
) > requirements.txt

echo [3/3] Limpiando archivos temporales...
del requirements_frozen.txt

echo.
echo [EXITO] requirements.txt generado correctamente
echo.
type requirements.txt
pause
goto tools

:install_pyinstaller
cls
echo ==========================================
echo   INSTALAR/ACTUALIZAR PYINSTALLER
echo ==========================================
echo.

if not exist venv\Scripts\pip.exe (
    echo [ERROR] No se encontro el entorno virtual
    pause
    goto tools
)

echo Instalando/actualizando PyInstaller...
venv\Scripts\pip.exe install --upgrade pyinstaller

if errorlevel 1 (
    echo [ERROR] Fallo la instalacion
) else (
    echo [EXITO] PyInstaller instalado/actualizado
)
pause
goto tools

:check_env
cls
echo ==========================================
echo   VERIFICAR ENTORNO PYTHON
echo ==========================================
echo.
python --version
echo.
echo PIP LIST:
pip list
echo.
pause
goto tools

:gen_icons
cls
echo ==========================================
echo   GENERAR ICONOS
echo ==========================================
echo.

if not exist venv\Scripts\python.exe (
    echo [ERROR] No se encontro el entorno virtual
    pause
    goto tools
)

if exist setup_icons.py (
    echo Generando iconos...
    venv\Scripts\python.exe setup_icons.py
    echo [EXITO] Iconos generados
) else (
    echo [ERROR] setup_icons.py no encontrado
)
pause
goto tools

:clean
cls
echo ==========================================
echo   LIMPIAR ARCHIVOS TEMPORALES
echo ==========================================
echo.

echo Se eliminaran los siguientes:
echo   - build/
echo   - dist/
echo   - __pycache__/
echo   - *.pyc
echo   - .pytest_cache/
echo   - htmlcov/
echo   - .coverage
echo.
set /p confirm="¿Continuar? (S/N): "

if /i not "%confirm%"=="S" goto menu

echo.
echo [1/4] Limpiando build y dist...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo    [OK] Build y dist eliminados

echo.
echo [2/4] Limpiando cache de Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
echo    [OK] Cache de Python limpiado

echo.
echo [3/4] Limpiando cache de pytest...
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist htmlcov rmdir /s /q htmlcov
if exist .coverage del /q .coverage 2>nul
echo    [OK] Cache de pytest limpiado

echo.
echo [4/4] Limpiando logs antiguos...
REM Mantener logs de los ultimos 7 dias
forfiles /p logs /m *.log /d -7 /c "cmd /c del @path" 2>nul
echo    [OK] Logs antiguos eliminados

echo.
echo ==========================================
echo [EXITO] Limpieza completada
echo ==========================================
pause
goto menu

:end
cls
echo.
echo Gracias por usar Vectora!
echo.
exit /b 0
