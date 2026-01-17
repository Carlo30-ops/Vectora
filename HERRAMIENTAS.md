# 🛠️ Herramientas de Desarrollo - Vectora

Sistema de scripts `.bat` para verificación, diagnóstico y corrección de código.

---

## 📋 Scripts Disponibles

### 🎯 **Menu Principal**

```cmd
menu_herramientas.bat
```

Menu interactivo con acceso a todas las herramientas.

---

### 🔍 **Diagnóstico y Análisis**

#### `resumen_estado.bat`

Muestra un resumen ejecutivo del estado del código:

- Estado de tests (22/36 pasando)
- Formato y estilo
- Errores de tipado
- Cobertura

#### `analizar_problemas.bat`

Genera reporte detallado categorizando todos los problemas detectados.

- Output: `problemas_detectados.txt`

#### `generar_plan.bat`

Crea un plan de corrección con pasos específicos.

- Output: `plan_correccion.md`

---

### ✅ **Verificación**

#### `analisis_rapido.bat` ⚡

Verificación rápida sin detalles:

- ✓ Formato (Black)
- ✓ Imports (isort)
- ✓ Estructura del proyecto
- ✓ Conteo de archivos

#### `verificar_codigo.bat` 🔬

Verificación completa paso a paso:

1. Tests (pytest)
2. Tipado (mypy)
3. Formato (black)
4. Imports (isort)
5. Análisis estático (pylint)

Genera reporte de cobertura en `htmlcov/index.html`

#### `ejecutar_tests.bat` 🧪

Solo ejecuta tests con pytest

- Más rápido que verificación completa
- Genera reporte de cobertura

---

### 🔧 **Corrección**

#### `corregir_codigo.bat` 🛠️

Auto-corrige problemas de formato:

- ✓ Aplica Black (formateo)
- ✓ Aplica isort (ordenar imports)
- ⚠️ Pide confirmación antes de modificar

---

### 🐍 **Entorno Virtual**

#### `verificar_venv.bat`

Verifica que el entorno virtual está funcionando:

- Info de Python
- Paquetes instalados

#### `recrear_venv.bat`

Elimina y recrea completamente el venv:

- ⚠️ Elimina venv corrupto
- ✓ Crea venv nuevo limpio
- ✓ Instala dependencias

#### `reparar_entorno.bat`

Analiza y repara el venv sin eliminarlo:

- Verifica integridad
- Recrea solo si es necesario
- Actualiza dependencias

---

### 🧹 **Utilidades**

#### `limpiar_temporal.bat`

Limpia archivos de diagnóstico temporales:

- `diagnostico_entorno.bat`
- `diagnostico_entorno.log`

---

## 🚀 Flujo de Trabajo Recomendado

### Primera Vez

```cmd
1. recrear_venv.bat          # Crear entorno limpio
2. verificar_venv.bat         # Confirmar que funciona
3. resumen_estado.bat         # Ver estado general
```

### Desarrollo Diario

```cmd
1. analisis_rapido.bat        # Check rápido
2. verificar_codigo.bat       # Análisis completo
3. corregir_codigo.bat        # Auto-fix formato
4. ejecutar_tests.bat         # Verificar tests
```

### Solución de Problemas

```cmd
1. resumen_estado.bat         # Ver qué falla
2. analizar_problemas.bat     # Detalles completos
3. generar_plan.bat           # Plan de acción
```

---

## 📊 Estado Actual del Código

**Tests:** 22/36 pasando (61%)

- 14 tests fallidos por corregir

**Formato:** ✅ Correcto (Black)

**Imports:** ✅ Ordenados (isort)

**Tipado:** ⚠️ 203 errores MyPy

- ~150 falsos positivos (PySide6)
- ~30 OperationResult
- ~23 type annotations

**Cobertura:** 11.87%

---

## 🔥 Problemas Críticos

### 1. Tests de OperationResult

Los servicios devuelven objetos `OperationResult` pero los tests esperan diccionarios.

**Archivos afectados:**

- `tests/test_pdf_merger.py`
- `tests/test_pdf_splitter.py`

**Fix:** Cambiar `result['success']` por `result.success`

### 2. Servicio OCR

Error: "Unsupported image object"

**Archivo:** `backend/services/ocr_service.py`

**Causa:** PyMuPDF devuelve `fitz.Pixmap` incompatible con pytesseract

**Fix:** Convertir Pixmap a PIL Image

### 3. PDF Compressor

El archivo comprimido no se genera.

**Archivo:** `backend/services/pdf_compressor.py`

**Fix:** Asegurar que `doc.save(output_path)` se ejecute correctamente

---

## 📝 Notas

- **Ejecuta siempre los scripts desde la raíz del proyecto**
- **Los `.bat` NO ejecutan comandos destructivos sin confirmación**
- **Los reportes se guardan como `.txt` o `.md` para fácil revisión**

---

## 🆘 Ayuda

Si encuentras problemas:

1. Ejecuta `resumen_estado.bat` para ver el estado general
2. Ejecuta `analizar_problemas.bat` para detalles
3. Si el entorno virtual falla, ejecuta `recrear_venv.bat`

---

**Generado:** 2026-01-12  
**Proyecto:** Vectora v5.0.0
