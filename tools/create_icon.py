"""
Script para generar el archivo .ico a partir del logo PNG
Requiere Pillow (Pillow ya está en requirements.txt)
"""
from PIL import Image
import os
import sys

def create_ico():
    source_png = "assets/logo.png"
    target_ico = "assets/vectora.ico"
    
    if not os.path.exists(source_png):
        print(f"Error: No se encuentra {source_png}")
        return False
        
    try:
        img = Image.open(source_png)
        
        # Guardar como .ico incluyendo varios tamaños estándar
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save(target_ico, sizes=icon_sizes)
        
        print(f"✅ Icono generado exitosamente: {target_ico}")
        return True
    except Exception as e:
        print(f"❌ Error al generar icono: {e}")
        return False

if __name__ == "__main__":
    create_ico()
