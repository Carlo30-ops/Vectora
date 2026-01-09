import os
import requests

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

def download_icons():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Downloading icons to {OUTPUT_DIR}...")
    
    for name, icon_name in ICONS.items():
        url = f"{BASE_URL}{icon_name}.svg"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Customizing color to black/currentcolor is usually handled in Qt by QIcon/QPixmap mask or simpler: download as is (black stroke usually)
                with open(f"{OUTPUT_DIR}/{name}.svg", "wb") as f:
                    f.write(response.content)
                print(f"✅ Downloaded {name}.svg")
            else:
                print(f"❌ Failed to download {name} ({url})")
        except Exception as e:
            print(f"❌ Error downloading {name}: {e}")

if __name__ == "__main__":
    download_icons()
