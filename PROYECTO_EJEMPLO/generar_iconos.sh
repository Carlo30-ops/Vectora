#!/bin/bash
# Generador de Iconos para LocalPDF v5
# Este script genera todos los iconos SVG necesarios

echo ""
echo "============================================================"
echo "  Generador de Iconos - LocalPDF v5"
echo "============================================================"
echo ""

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python no está instalado"
    echo "Por favor instala Python 3:"
    echo "  - Ubuntu/Debian: sudo apt-get install python3"
    echo "  - macOS: brew install python3"
    exit 1
fi

echo "[INFO] Python encontrado. Generando iconos..."
echo ""

# Ejecutar el script de generación
python3 generate_icons.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Hubo un problema al generar los iconos"
    exit 1
fi

echo ""
echo "============================================================"
echo "  Generación completada exitosamente!"
echo "============================================================"
echo ""
echo "Los iconos se encuentran en la carpeta: icons/"
echo ""

# Abrir la carpeta de iconos (dependiendo del sistema)
if [ -d "icons" ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open icons
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open icons 2>/dev/null || echo "Carpeta: $(pwd)/icons"
    fi
fi

exit 0
