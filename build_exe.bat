@echo off
echo ==========================================
echo   Vectora (LocalPDF v5) Builder
echo ==========================================

echo 1. Instalando dependencias de build...
pip install -r requirements.txt
pip install pyinstaller

echo 1.5. Asegurando iconos...
python setup_icons.py
echo 2. Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo 3. Generando ejecutable...
pyinstaller Vectora.spec --noconfirm

echo ==========================================
if exist dist\Vectora\Vectora.exe (
    echo [EXITO] Ejecutable generado correctamente:
    echo dist\Vectora\Vectora.exe
) else (
    echo [ERROR] Fallo la generacion.
)
echo ==========================================
pause
