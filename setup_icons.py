"""
Setup de iconos para Vectora
Este script descarga iconos SVG de Lucide Icons (opcional)
Si ya existen los iconos, no hace nada
"""
import os
import sys

ICONS = {
    "dashboard": "layout-dashboard",
    "wizard": "wand-2",
    "merge": "combine",
    "split": "scissors",
    "compress": "minimize-2",
    "convert": "refresh-cw",
    "security": "shield",
    "ocr": "scan-text",
    "batch": "layers",
    "logo": "file-text",
    "check": "check",
    "chevron-right": "chevron-right",
    "arrow-right": "arrow-right",
    "file": "file",
    "folder": "folder",
    "upload": "upload",
    "x": "x",
    "loader": "loader-2"
}

BASE_URL = "https://unpkg.com/lucide-static@latest/icons/"
OUTPUT_DIR = "assets/icons"

def check_icons_exist():
    """Verifica si los iconos ya existen"""
    if not os.path.exists(OUTPUT_DIR):
        return False
    
    # Verificar si al menos algunos iconos existen
    existing_icons = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.svg')]
    return len(existing_icons) > 0

def download_icons():
    """Descarga iconos desde Lucide Icons (requiere requests)"""
    # Verificar si ya existen iconos
    if check_icons_exist():
        print(f"✅ Iconos ya existen en {OUTPUT_DIR}/")
        print("   No es necesario descargar")
        return True
    
    # Intentar importar requests
    try:
        import requests
    except ImportError:
        print("⚠️  Módulo 'requests' no encontrado")
        print("   Los iconos se descargarán automáticamente al ejecutar la app")
        print("   O instala requests si quieres descargarlos ahora:")
        print("   pip install requests")
        return False
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"📥 Descargando iconos a {OUTPUT_DIR}...")
    
    success_count = 0
    for name, icon_name in ICONS.items():
        url = f"{BASE_URL}{icon_name}.svg"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                with open(f"{OUTPUT_DIR}/{name}.svg", "wb") as f:
                    f.write(response.content)
                print(f"✅ {name}.svg")
                success_count += 1
            else:
                print(f"❌ Fallo {name} (HTTP {response.status_code})")
        except Exception as e:
            print(f"❌ Error {name}: {e}")
    
    print(f"\n✅ Descargados {success_count}/{len(ICONS)} iconos")
    return success_count > 0

if __name__ == "__main__":
    print("="*50)
    print("  Setup de Iconos para Vectora")
    print("="*50)
    download_icons()
    print("="*50)

