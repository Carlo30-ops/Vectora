@echo off
setlocal
echo ===================================================
echo   VECTORA - AUTO FIX AND VERIFY (ALL-IN-ONE)
echo ===================================================

:: Ensure we are starting from the script's directory (maintenance)
pushd "%~dp0"
:: Move up one level to Project Root
cd ..

:: Check/Activate Virtual Environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] No se encontro el entorno virtual en venv\
    echo Asegurate de estar ejecutando este script desde la carpeta maintenance o que venv exista en la raiz del proyecto.
    pause
    exit /b 1
)

echo.
echo [1/5] Running Auto-Fixes (Isort and Black)...
echo -------------------------------------------
echo Running isort...
isort backend ui utils
echo.
echo Running black...
black backend ui utils


echo.
echo [2/5] Checking Static Types (Mypy)...
echo -------------------------------------------
mypy backend ui utils

echo.
echo [3/5] Linting Code (Pylint)...
echo -------------------------------------------
pylint backend ui utils --exit-zero

echo.
echo [4/5] Running Tests (Pytest)...
echo -------------------------------------------
pytest

echo.
echo ===================================================
echo   PROCESS COMPLETED
echo ===================================================
pause
