@echo off
echo ==========================================
echo   Generador de Requirements con Versiones
echo ==========================================
echo.
echo Este script genera requirements.txt con versiones exactas
echo usando pip freeze del entorno virtual.
echo.

REM Verificar si existe el entorno virtual
if not exist venv\Scripts\pip.exe (
    echo [ERROR] No se encontro el entorno virtual en venv\
    echo Por favor, crea el entorno virtual primero:
    echo    python -m venv venv
    pause
    exit /b 1
)

echo [1/3] Generando requirements.txt con pip freeze...
venv\Scripts\pip.exe freeze > requirements_frozen.txt

if errorlevel 1 (
    echo [ERROR] Fallo al ejecutar pip freeze
    pause
    exit /b 1
)

echo [2/3] Filtrando solo dependencias principales...
REM Crear requirements.txt limpio con solo las dependencias principales
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
echo ==========================================
echo [EXITO] requirements.txt generado correctamente
echo ==========================================
echo.
type requirements.txt
echo.
pause
