@echo off
echo ==========================================
echo   Vectora - Verificador de Salud del Proyecto
echo ==========================================
echo.

REM Verificar entorno virtual
echo [1] Verificando entorno virtual...
if exist venv\Scripts\python.exe (
    echo    [OK] Entorno virtual encontrado
) else (
    echo    [WARN] No se encontro el entorno virtual
    echo           Ejecuta: python -m venv venv
)
echo.

REM Verificar dependencias
echo [2] Verificando dependencias principales...
if exist venv\Scripts\pip.exe (
    venv\Scripts\pip.exe show PySide6 > nul 2>&1
    if errorlevel 1 (
        echo    [WARN] PySide6 no instalado
    ) else (
        echo    [OK] PySide6 instalado
    )
    
    venv\Scripts\pip.exe show PyPDF2 > nul 2>&1
    if errorlevel 1 (
        echo    [WARN] PyPDF2 no instalado
    ) else (
        echo    [OK] PyPDF2 instalado
    )
    
    venv\Scripts\pip.exe show pikepdf > nul 2>&1
    if errorlevel 1 (
        echo    [WARN] pikepdf no instalado
    ) else (
        echo    [OK] pikepdf instalado
    )
)
echo.

REM Verificar estructura de directorios
echo [3] Verificando estructura de directorios...
if exist backend\ (
    echo    [OK] backend/
) else (
    echo    [ERROR] Falta backend/
)

if exist ui\ (
    echo    [OK] ui/
) else (
    echo    [ERROR] Falta ui/
)

if exist config\ (
    echo    [OK] config/
) else (
    echo    [ERROR] Falta config/
)

if exist utils\ (
    echo    [OK] utils/
) else (
    echo    [ERROR] Falta utils/
)

if exist icons\ (
    echo    [OK] icons/
) else (
    echo    [WARN] Falta icons/
)
echo.

REM Verificar directorios de trabajo
echo [4] Verificando directorios de trabajo...
if exist temp\ (
    echo    [OK] temp/
) else (
    echo    [WARN] Creando temp/
    mkdir temp
)

if exist output\ (
    echo    [OK] output/
) else (
    echo    [WARN] Creando output/
    mkdir output
)
echo.

REM Verificar archivo de configuración
echo [5] Verificando configuracion...
if exist .env (
    echo    [OK] .env encontrado
) else (
    echo    [WARN] .env no encontrado
    echo           Copia .env.example a .env y configura las rutas
)
echo.

REM Verificar herramientas externas
echo [6] Verificando herramientas externas...
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo    [OK] Tesseract OCR encontrado
) else (
    echo    [WARN] Tesseract OCR no encontrado en la ruta por defecto
)

if exist "C:\Program Files\poppler-25.12.0\Library\bin" (
    echo    [OK] Poppler encontrado
) else (
    echo    [WARN] Poppler no encontrado en la ruta por defecto
)
echo.

REM Verificar carpeta duplicada
echo [7] Buscando carpeta Vectora duplicada...
if exist Vectora\Vectora\ (
    echo    [WARN] Carpeta duplicada Vectora\Vectora\ encontrada
    echo           Considera eliminarla o investigar su proposito
) else (
    echo    [OK] No se encontro duplicacion
)
echo.

REM Verificar archivos principales
echo [8] Verificando archivos principales...
if exist main.py (
    echo    [OK] main.py
) else (
    echo    [ERROR] main.py no encontrado
)

if exist requirements.txt (
    echo    [OK] requirements.txt
) else (
    echo    [WARN] requirements.txt no encontrado
)

if exist build_exe.bat (
    echo    [OK] build_exe.bat
) else (
    echo    [WARN] build_exe.bat no encontrado
)
echo.

echo ==========================================
echo Verificacion completada
echo ==========================================
echo.
echo Revisa los warnings y errores arriba para corregir problemas.
echo.
pause
