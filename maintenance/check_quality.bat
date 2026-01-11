@echo off
setlocal
echo ===================================================
echo   VECTORA - VERIFICACION DE CALIDAD (QUALITY CHECK)
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
echo [1/5] Verificando formato (Black)...
black --check backend ui utils
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] El formato de codigo no es correcto. Ejecuta clean_code.bat
) else (
    echo [OK] Formato correcto.
)

echo.
echo [2/5] Verificando imports (Isort)...
isort --check-only backend ui utils
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Los imports no estan ordenados. Ejecuta clean_code.bat
) else (
    echo [OK] Imports ordenados.
)

echo.
echo [3/5] Verificando tipos (Mypy)...
mypy backend ui utils
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Se encontraron problemas de tipado.
) else (
    echo [OK] Tipado correcto.
)

echo.
echo [4/5] Analizando codigo (Pylint)...
pylint backend ui utils --exit-zero
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Pylint encontro problemas.
) else (
    echo [OK] Analisis completado.
)

echo.
echo [5/5] Ejecutando Tests (Pytest)...
pytest
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Los tests fallaron.
) else (
    echo [OK] Tests pasaron exitosamente.
)

echo.
echo ===================================================
echo   VERIFICACION COMPLETADA
echo ===================================================
pause
