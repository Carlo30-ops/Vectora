@echo off
setlocal
echo ===================================================
echo   VECTORA - LIMPIEZA DE CODIGO (AUTO-FORMAT)
echo ===================================================

cd ..
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] No se encontro el entorno virtual en venv\
    pause
    exit /b 1
)

echo.
echo [1/2] Reordenando imports (Isort)...
isort backend ui utils
echo [OK] Isort finalizado.

echo.
echo [2/2] Formateando codigo (Black)...
black backend ui utils
echo [OK] Black finalizado.

echo.
echo ===================================================
echo   CODIGO LIMPIO Y FORMATEADO
echo ===================================================
pause
