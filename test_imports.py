"""
Script de prueba rápida de imports
Verifica que todos los módulos modificados se importen correctamente
"""
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path si no está
if __name__ == "__main__":
    root_dir = Path(__file__).parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))

print("=" * 60)
print("PRUEBA DE IMPORTS - Vectora v5.0.0")
print("=" * 60)
print(f"Python: {sys.version}")
print(f"Directorio: {Path(__file__).parent}")
print()

errors = []
success = []

# Test 1: Settings
try:
    from config.settings import settings
    assert hasattr(settings, 'get_output_directory'), "settings.get_output_directory() no existe"
    result = settings.get_output_directory()
    assert isinstance(result, Path), "get_output_directory() debe retornar Path"
    success.append("✓ Settings - get_output_directory()")
except Exception as e:
    errors.append(f"✗ Settings: {e}")

# Test 2: Widgets con drag & drop
widgets_to_test = [
    ("SplitWidget", "ui.components.operation_widgets.split_widget"),
    ("CompressWidget", "ui.components.operation_widgets.compress_widget"),
    ("SecurityWidget", "ui.components.operation_widgets.security_widget"),
    ("OCRWidget", "ui.components.operation_widgets.ocr_widget"),
    ("ConvertWidget", "ui.components.operation_widgets.convert_widget"),
    ("BatchWidget", "ui.components.operation_widgets.batch_widget"),
    ("MergeWidget", "ui.components.operation_widgets.merge_widget"),
]

for widget_name, module_path in widgets_to_test:
    try:
        module = __import__(module_path, fromlist=[widget_name])
        widget_class = getattr(module, widget_name)
        success.append(f"✓ {widget_name}")
    except Exception as e:
        errors.append(f"✗ {widget_name}: {e}")

# Test 3: Verificar que drag & drop está implementado
print("\n[3/3] Verificando implementación de drag & drop...")
try:
    from ui.components.operation_widgets.split_widget import SplitWidget
    # Verificar que tiene método _setup_drag_drop
    assert hasattr(SplitWidget, '_setup_drag_drop'), "SplitWidget no tiene _setup_drag_drop"
    success.append("✓ SplitWidget._setup_drag_drop")
except Exception as e:
    errors.append(f"✗ Verificación drag & drop: {e}")

# Resumen
print()
print("=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"✓ Exitosos: {len(success)}")
if errors:
    print(f"✗ Errores: {len(errors)}")
    for error in errors:
        print(f"  {error}")
    sys.exit(1)
else:
    print("✓ Todos los imports funcionan correctamente")
    print("=" * 60)
    sys.exit(0)
