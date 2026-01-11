@echo off
title Vectora - Reinstalacion de Entorno
color 0E

echo ==========================================
echo   REPARACION DE ENTORNO VIRTUAL
echo ==========================================
echo.
echo Detectamos un problema con tu entorno Python (Python314 no encontrado).
echo Vamos a eliminar 'venv' y crerlo desde cero usando tu Python actual.
echo.

echo [1/5] Eliminando entorno corrupto (puede tardar)...
if exist venv (
    rmdir /s /q venv
    if exist venv (
        echo [ERROR] No se pudo eliminar 'venv'. Cierra cualquier terminal o programa que lo use.
        pause
        exit /b 1
    )
)
echo    [OK] Entorno eliminado.

echo.
echo [2/5] Detectando Python...
REM Intentar con py (Python Launcher) primero, luego python
set PYTHON_CMD=
py -3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3
    echo    [OK] Python detectado via 'py -3'
) else (
    python --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=python
        echo    [OK] Python detectado via 'python'
    ) else (
        echo [ERROR] No se encontro Python instalado.
        echo.
        echo Soluciones:
        echo   1. Instala Python desde python.org
        echo   2. O habilita Python desde Microsoft Store
        echo   3. Verifica que Python este en el PATH del sistema
        pause
        exit /b 1
    )
)

echo.
echo [3/5] Creando nuevo entorno virtual...
%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual.
    echo Python encontrado pero fallo al crear venv.
    pause
    exit /b 1
)
echo    [OK] Entorno creado.

echo.
echo [4/5] Actualizando herramientas base...
venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel --quiet
if errorlevel 1 (
    echo [WARN] Algunos problemas al actualizar herramientas, pero continuando...
)

echo.
echo [5/5] Instalando dependencias (esto tomara un momento)...
if exist requirements.txt (
    venv\Scripts\pip.exe install -r requirements.txt
) else (
    echo [WARN] No se encontro requirements.txt, instalando paquetes minimos...
    venv\Scripts\pip.exe install PySide6 pikepdf pytesseract pdf2image watchdog python-dotenv pyinstaller
)

echo.
echo ==========================================
echo   REPARACION COMPLETADA
echo ==========================================
echo.
echo Ahora puedes intentar ejecutar el BUILD nuevamente.
echo.
pause
