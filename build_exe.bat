@echo off
echo ==========================================
echo   Vectora (LocalPDF v5) Builder
echo ==========================================

echo 1. Instalando dependencias de build...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo.
echo 2. Instalando dependencias adicionales...
pip install PySide6 PySide6-Addons
pip install pikepdf PyPDF2 python-dotenv
pip install pytesseract pdf2image Pillow

echo.
echo 3. Asegurando sistema de iconos...
python setup_icons.py

echo.
echo 4. Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo 5. Creando directorios de salida...
if not exist output mkdir output
if not exist temp mkdir temp

echo.
echo 6. Generando ejecutable...
pyinstaller Vectora.spec --noconfirm

echo.
echo ==========================================
if exist dist\Vectora\Vectora.exe (
    echo [EXITO] Ejecutable generado correctamente:
    echo dist\Vectora\Vectora.exe
    echo.
    echo Copiando directorios de salida...
    xcopy /E /I /Y output dist\Vectora\output
    mkdir dist\Vectora\temp
) else (
    echo [ERROR] Fallo la generacion.
)
echo ==========================================
pause
