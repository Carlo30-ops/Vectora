@echo off
TITLE Plan de Correccion - Vectora
cls

echo ========================================================
echo   PLAN DE CORRECCION DE CODIGO
echo ========================================================
echo.

> plan_correccion.md (
    echo # Plan de Correccion - Vectora
    echo.
    echo Generado: %date% %time%
    echo.
    echo ## Resumen Ejecutivo
    echo.
    echo - **Tests**: 22/36 pasando ^(61%%^) - **14 fallidos**
    echo - **Cobertura**: 11.87%%
    echo - **Formato**: ✅ Correcto
    echo - **Imports**: ✅ Ordenados
    echo - **MyPy**: 203 errores ^(~150 son falsos positivos de PySide6^)
    echo. 
    echo ---
    echo.
    echo ## Fase 1: Correcciones Criticas ^(Tests^)
    echo.
    echo ### 1.1 Actualizar Tests de OperationResult
    echo.
    echo **Archivos a modificar:**
    echo - `tests/test_pdf_merger.py`
    echo - `tests/test_pdf_splitter.py`
    echo.
    echo **Cambios:**
    echo ```python
    echo # Antes:
    echo assert result['success'] is True
    echo.
    echo # Despues:
    echo assert result.success is True
    echo ```
    echo.
    echo **Razon:** Los servicios ahora devuelven objetos `OperationResult` en lugar de diccionarios.
    echo.
    echo ---
    echo.
    echo ### 1.2 Corregir OCR Service
    echo.
    echo **Archivo:** `backend/services/ocr_service.py`
    echo.
    echo **Problema:** PyMuPDF devuelve `fitz.Pixmap` que pytesseract no reconoce.
    echo.
    echo **Solucion:** Convertir Pixmap a PIL Image:
    echo ```python
    echo from PIL import Image
    echo import io
    echo.
    echo # Convertir pixmap a imagen PIL
    echo img_data = pix.tobytes^(^)
    echo image = Image.frombytes^("RGB", [pix.width, pix.height], img_data^)
    echo ```
    echo.
    echo ---
    echo.
    echo ### 1.3 Corregir PDF Compressor
    echo.
    echo **Archivo:** `backend/services/pdf_compressor.py`
    echo.
    echo **Problema:** El archivo comprimido no se esta guardando.
    echo.
    echo **Solucion:** Asegurar que `doc.save^(output_path^)` se ejecute correctamente.
    echo.
    echo ---
    echo.
    echo ## Fase 2: Configuracion MyPy
    echo.
    echo **Archivo:** `pyproject.toml`
    echo.
    echo **Agregar:** echo ```toml
    echo [[tool.mypy.overrides]]
    echo module = "PySide6.*"
    echo ignore_errors = true
    echo ```
    echo.
    echo Esto eliminara ~150 errores falsos positivos.
    echo.
    echo ---
    echo.
    echo ## Fase 3: Mejoras de Codigo ^(Opcional^)
    echo.
    echo - Limpiar imports no usados
    echo - Refactorizar codigo duplicado de drag-drop
    echo - Cambiar f-strings por lazy logging
    echo.
    echo ---
    echo.
    echo ## Comandos para Ejecutar
    echo.
    echo 1. `analizar_problemas.bat` - Ver reporte detallado
    echo 2. `corregir_tests.bat` - Actualizar tests ^(generare este^)
    echo 3. `corregir_ocr.bat` - Corregir servicio OCR ^(generare este^)
    echo 4. `ejecutar_tests.bat` - Verificar correcciones
    echo.
)

echo [OK] Plan generado: plan_correccion.md
echo.
type plan_correccion.md
echo.
pause
