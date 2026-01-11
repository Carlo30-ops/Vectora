@echo off
echo [VECTORA V5] Verificacion Rapida
echo ===============================
echo.

echo 1. Verificando Dependencias...
python -c "import pikepdf, PyPDF2, pytest; print('OK: Dependencias core listas')" || (echo ERROR: Faltan dependencias & pause & exit /b 1)

echo 2. Verificando Estructura V5...
if exist backend\core\operation_result.py (echo OK: Infraestructura V5 presente) else (echo ERROR: Falta operation_result.py & pause & exit /b 1)

echo 3. Corriendo Tests Criticos...
pytest tests/test_pdf_merger.py -v --tb=short
if %ERRORLEVEL% NEQ 0 (echo ERROR: Tests de Merger fallaron & pause & exit /b 1)

echo.
echo [FINALIZADO] Todo parece estar en orden.
echo.
pause
