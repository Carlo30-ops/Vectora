# 🧪 Tests de Vectora

## 📖 Descripción

Suite completa de tests para Vectora v5, cubriendo servicios backend de procesamiento de PDFs.

## 🎯 Cobertura Actual

### Tests Implementados

| Módulo                 | Tests        | Cobertura    |
| ---------------------- | ------------ | ------------ |
| `test_pdf_merger.py`   | 10 tests     | ✅           |
| `test_pdf_splitter.py` | 17 tests     | ✅           |
| **Total**              | **27 tests** | **Completa** |

### Servicios Cubiertos

- ✅ **PDFMerger**: Combinación de PDFs
- ✅ **PDFSplitter**: División por rango, páginas específicas, cada N páginas
- ⏳ **PDFCompressor**: Por implementar
- ⏳ **PDFConverter**: Por implementar
- ⏳ **OCRService**: Por implementar

## 🚀 Ejecutar Tests

### Opción 1: Script Batch (Recomendado)

```cmd
run_tests.bat
```

### Opción 2: pytest Directamente

```cmd
venv\Scripts\python -m pytest tests/ -v
```

### Opción 3: Con Coverage

```cmd
venv\Scripts\python -m pytest tests/ --cov=backend --cov=utils --cov-report=html
```

## 📊 Ver Reporte de Coverage

Después de ejecutar tests:

```cmd
start htmlcov\index.html
```

## 🧩 Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidas
├── test_pdf_merger.py       # Tests de combinación (10 tests)
├── test_pdf_splitter.py     # Tests de división (17 tests)
└── .gitignore               # Ignorar archivos temporales
```

## 🔧 Fixtures Disponibles

Definidas en `conftest.py`:

| Fixture                | Descripción                                        |
| ---------------------- | -------------------------------------------------- |
| `temp_dir`             | Directorio temporal que se limpia automáticamente  |
| `sample_pdf`           | PDF de prueba simple (1 página)                    |
| `sample_pdfs_multiple` | 3 PDFs con 1, 2, 3 páginas respectivamente         |
| `sample_pdf_multipage` | PDF con 10 páginas                                 |
| `non_existent_file`    | Path a archivo que NO existe (para tests de error) |
| `output_path`          | Path para archivo de salida                        |

## 📝 Escribir Nuevos Tests

### Ejemplo Básico

```python
import pytest
from backend.services.pdf_merger import PDFMerger

@pytest.mark.unit
def test_mi_funcionalidad(sample_pdfs_multiple, output_path):
    # Arrange
    input_files = sample_pdfs_multiple

    # Act
    result = PDFMerger.merge_pdfs(input_files, output_path)

    # Assert
    assert result['success'] is True
```

### Markers Disponibles

```python
@pytest.mark.unit          # Test unitario
@pytest.mark.integration   # Test de integración
@pytest.mark.slow          # Test que tarda
@pytest.mark.pdf           # Test que usa PDFs
```

## 🎯 Comandos Útiles

### Ejecutar solo tests unitarios

```cmd
venv\Scripts\python -m pytest tests/ -m unit
```

### Ejecutar tests de un archivo específico

```cmd
venv\Scripts\python -m pytest tests/test_pdf_merger.py -v
```

### Ejecutar un test específico

```cmd
venv\Scripts\python -m pytest tests/test_pdf_merger.py::TestPDFMerger::test_merge_two_pdfs -v
```

### Ver output completo (sin captura)

```cmd
venv\Scripts\python -m pytest tests/ -v -s
```

### Modo verbose + mostrar datos de tests

```cmd
venv\Scripts\python -m pytest tests/ -vv
```

## 📈 Objetivos de Cobertura

- **Actual**: ~60% (PDFMerger y PDFSplitter)
- **Objetivo**: 80% de código backend

## 🔜 Próximos Tests a Implementar

1. **test_pdf_compressor.py**: Tests de compresión
2. **test_pdf_converter.py**: Tests de conversión
3. **test_validators.py**: Tests de validaciones
4. **test_file_handler.py**: Tests de manejo de archivos

## 🐛 Debugging Tests

Si un test falla:

1. Ejecutar con `-vv` para más detalles
2. Revisar logs en `logs/vectora_*.log`
3. Usar `pytest --pdb` para debugger interactivo

## ✅ Pre-commit Checklist

Antes de commit:

```cmd
run_tests.bat
```

Asegurar que:

- ✅ Todos los tests pasan
- ✅ Coverage > 60%
- ✅ No hay warnings críticos
