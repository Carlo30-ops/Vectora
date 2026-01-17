# 🎨 Generador de Iconos - LocalPDF v5

Este generador crea todos los iconos SVG necesarios para la aplicación LocalPDF v5.

## 📦 Contenido

- **generate_icons.py**: Script principal de generación
- **generar_iconos.bat**: Script de ejecución para Windows
- **generar_iconos.sh**: Script de ejecución para Linux/Mac

## 🚀 Uso Rápido

### Windows
Simplemente haz doble clic en:
```
generar_iconos.bat
```

### Linux/Mac
Ejecuta en la terminal:
```bash
chmod +x generar_iconos.sh
./generar_iconos.sh
```

### Manual (cualquier sistema)
```bash
python generate_icons.py
```

## 📁 Estructura Generada

Después de ejecutar el script, se creará la siguiente estructura:

```
icons/
├── archivo1.svg               # 30+ iconos base
├── archivo2.svg
├── ...
├── colored/                   # Variantes de color
│   ├── scissors-white.svg
│   ├── scissors-black.svg
│   ├── scissors-blue.svg
│   └── ...
├── sizes/                     # Diferentes tamaños
│   ├── file-text-16px.svg
│   ├── file-text-24px.svg
│   ├── file-text-32px.svg
│   └── ...
├── icons.py                   # Módulo Python
└── icons.qrc                  # Qt Resource file
```

## 📝 Iconos Disponibles

### Principales
- `file-text` - Logo principal de PDF
- `home` - Dashboard
- `wand-2` - Asistente inteligente
- `combine` - Combinar PDFs
- `scissors` - Dividir PDF
- `archive` - Comprimir PDF
- `refresh-cw` - Convertir
- `shield` - Seguridad
- `scan-text` - OCR
- `folder-clock` - Procesamiento por lotes

### Acciones
- `upload` - Subir archivos
- `download` - Descargar
- `x` - Cerrar
- `arrow-right` - Siguiente
- `chevron-right` - Expandir

### Estados
- `check-circle-2` - Completado
- `clock` - Pendiente
- `play` - Procesando
- `alert-circle` - Error

### Seguridad
- `lock` - Encriptar
- `unlock` - Desencriptar
- `eye` - Mostrar contraseña
- `eye-off` - Ocultar contraseña

### Conversión
- `image` - Imágenes
- `file-spreadsheet` - Word
- `file-search` - Búsqueda
- `languages` - Idiomas

### Otros
- `sparkles` - Características especiales
- `grip-vertical` - Arrastrar
- `help-circle` - Ayuda
- `folder` - Carpeta

## 🔧 Uso en PySide6

### Opción 1: Cargar desde archivo SVG

```python
from PySide6.QtGui import QIcon

# Cargar icono SVG
icon = QIcon('icons/scissors.svg')

# Usar en botón
button.setIcon(icon)
```

### Opción 2: Usar módulo Python

```python
from icons.icons import get_icon_qicon, get_icon_svg, ICONS

# Obtener QIcon directamente
icon = get_icon_qicon('scissors')
button.setIcon(icon)

# Obtener QIcon con color personalizado
white_icon = get_icon_qicon('scissors', color='#ffffff')

# Obtener SVG como string
svg_content = get_icon_svg('scissors')

# Listar todos los iconos
print(ICONS.keys())
```

### Opción 3: Usar Qt Resources (recomendado para distribución)

```bash
# 1. Compilar el archivo .qrc
pyside6-rcc icons/icons.qrc -o icons_rc.py

# 2. En tu aplicación
import icons_rc
from PySide6.QtGui import QIcon

# Usar con prefijo de recurso
icon = QIcon(':/icons/scissors.svg')
button.setIcon(icon)
```

## 🎨 Personalización de Colores

### En SVG directo
Los iconos usan `stroke="currentColor"`, lo que permite cambiar el color con CSS:

```python
from PySide6.QtSvg import QSvgWidget

svg_widget = QSvgWidget('icons/scissors.svg')
svg_widget.setStyleSheet('color: #ffffff;')  # Blanco
```

### Con el módulo Python
```python
from icons.icons import get_icon_qicon

# Crear icono blanco para fondo negro
white_icon = get_icon_qicon('scissors', color='#ffffff')

# Crear icono negro para fondo blanco
black_icon = get_icon_qicon('scissors', color='#000000')

# Crear icono gris
gray_icon = get_icon_qicon('scissors', color='#6b7280')
```

### Variantes pre-generadas
```python
# Usar iconos coloreados pre-generados
white_icon = QIcon('icons/colored/scissors-white.svg')
black_icon = QIcon('icons/colored/scissors-black.svg')
blue_icon = QIcon('icons/colored/scissors-blue.svg')
green_icon = QIcon('icons/colored/scissors-green.svg')
red_icon = QIcon('icons/colored/scissors-red.svg')
```

## 📏 Diferentes Tamaños

```python
# Usar tamaños pre-generados
small_icon = QIcon('icons/sizes/file-text-16px.svg')
medium_icon = QIcon('icons/sizes/file-text-24px.svg')
large_icon = QIcon('icons/sizes/file-text-48px.svg')
xlarge_icon = QIcon('icons/sizes/file-text-128px.svg')

# Tamaños disponibles: 16, 24, 32, 48, 64, 128 píxeles
```

## 🔍 Ejemplo Completo

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QPushButton
from PySide6.QtGui import QIcon, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Opción 1: Desde archivo
        self.merge_icon = QIcon('icons/combine.svg')
        self.split_icon = QIcon('icons/scissors.svg')
        
        # Opción 2: Desde módulo Python
        from icons.icons import get_icon_qicon
        self.compress_icon = get_icon_qicon('archive')
        self.convert_icon = get_icon_qicon('refresh-cw')
        
        # Crear toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Agregar acciones con iconos
        merge_action = QAction(self.merge_icon, "Combinar", self)
        split_action = QAction(self.split_icon, "Dividir", self)
        compress_action = QAction(self.compress_icon, "Comprimir", self)
        convert_action = QAction(self.convert_icon, "Convertir", self)
        
        toolbar.addAction(merge_action)
        toolbar.addAction(split_action)
        toolbar.addAction(compress_action)
        toolbar.addAction(convert_action)
        
        # Botones con iconos
        button = QPushButton("Procesar")
        button.setIcon(get_icon_qicon('play'))
        
        # Cambiar color del icono según estado
        button_dark = QPushButton("Procesar")
        button_dark.setIcon(get_icon_qicon('play', color='#ffffff'))  # Blanco para fondo negro

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
```

## 📦 Distribución

### Para desarrollo
Usa los archivos SVG directamente desde la carpeta `icons/`

### Para producción
1. Compila el archivo .qrc:
   ```bash
   pyside6-rcc icons/icons.qrc -o icons_rc.py
   ```

2. Importa el módulo compilado:
   ```python
   import icons_rc
   ```

3. Usa los iconos con el prefijo `:/icons/`:
   ```python
   icon = QIcon(':/icons/scissors.svg')
   ```

### Ventajas de Qt Resources
- ✅ Los iconos se embeben en el ejecutable
- ✅ No necesitas distribuir archivos SVG separados
- ✅ Carga más rápida
- ✅ Menos problemas con rutas

## 🛠️ Requisitos

- Python 3.6+
- PySide6 (para usar los iconos)

```bash
pip install PySide6
```

## 📄 Licencia

Los iconos están basados en [Lucide Icons](https://lucide.dev/), que usa la licencia ISC (permisiva, similar a MIT).

---

**Creado para LocalPDF v5** 🚀
