import os
import re

def fix_tests_operation_result():
    files = [
        'tests/test_pdf_merger.py',
        'tests/test_pdf_splitter.py'
    ]
    
    replacements = [
        (r"\['success'\]", ".success"),
        (r"\['message'\]", ".message"),
        (r"\['data'\]", ".data"),
        (r"\['error_message'\]", ".error_message"),
        (r"\['metrics'\]", ".metrics"),
        (r"assert 'success' in result", "assert hasattr(result, 'success')"),
    ]
    
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"Archivo no encontrado: {file_path}")
            continue
            
        print(f"Corrigiendo {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, new_content)
            
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  -> Corregido")
        else:
            print(f"  -> Sin cambios necesarios")

def fix_ocr_service():
    file_path = 'backend/services/ocr_service.py'
    if not os.path.exists(file_path):
        return

    print(f"Corrigiendo {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    imports_added = False
    
    for line in lines:
        if not imports_added and line.startswith('import'):
            new_lines.append("from PIL import Image\n")
            new_lines.append("import io\n")
            imports_added = True
            
        if "pytesseract.image_to_string(image, lang=language)" in line:
            # Reemplazar la linea problematica con bloque de conversion
            indent = line[:line.find("pytesseract")]
            block = [
                f"{indent}# Convertir Pixmap a PIL Image\n",
                f"{indent}img_data = image.tobytes()\n",
                f"{indent}pil_image = Image.frombytes('RGB', [image.width, image.height], img_data)\n",
                f"{indent}text = pytesseract.image_to_string(pil_image, lang=language)\n"
            ]
            new_lines.extend(block)
        else:
            new_lines.append(line)
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"  -> Logica de imagen PIL agregada")

def fix_pdf_compressor():
    file_path = 'backend/services/pdf_compressor.py'
    if not os.path.exists(file_path):
        return

    print(f"Corrigiendo {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar donde falta el guardado
    # Esta es una insercion especifica basada en el error conocido
    if "doc.save(output_path," not in content:
        # Intentar insertar antes de calcular el size
        target = "compressed_size = os.path.getsize(output_path)"
        if target in content:
            new_content = content.replace(
                target,
                f"doc.save(output_path, garbage=4, deflate=True)\n        {target}"
            )
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  -> Guardado de archivo agregado")
        else:
            print("  [WARNING] No se encontro punto de insercion para fix de compresor")
    else:
        print("  -> Ya contiene logica de guardado")

def fix_mypy_config():
    file_path = 'pyproject.toml'
    if not os.path.exists(file_path):
        return

    print(f"Corrigiendo {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "module = \"PySide6.*\"" not in content:
        append_config = """

[[tool.mypy.overrides]]
module = "PySide6.*"
ignore_errors = true
"""
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(append_config)
        print(f"  -> Configuracion de ignorar PySide6 agregada")
    else:
        print("  -> Configuracion ya existe")

if __name__ == "__main__":
    print("Iniciando correcciones automaticas...")
    try:
        fix_tests_operation_result()
        fix_ocr_service()
        fix_pdf_compressor()
        fix_mypy_config()
        print("\n[EXITO] Todas las correcciones se aplicaron.")
    except Exception as e:
        print(f"\n[ERROR] Fallo al aplicar correcciones: {e}")
