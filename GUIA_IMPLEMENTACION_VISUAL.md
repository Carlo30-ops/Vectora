# LocalPDF v5 - Guía de Implementación Visual

## 📋 Estado de Aplicación de Diseño

Fecha: 17 de Enero de 2026
Estado: **En Progreso** ✅

### ✅ Completado

- [x] Paleta de colores actualizada en `themes.py`
- [x] Estilos QSS expandidos en `style_content.py`
- [x] Sistema de variables de tema completado
- [x] Definiciones de colores de estado (Success, Error, Warning, Info)

### ⏳ Próximos Pasos

1. **Implementar Iconos Dinámicos**
   - Asegurar que los iconos en "Acciones Rápidas" se cargan correctamente
   - Verificar rutas de `assets/icons/`

2. **Refinar Layout del Sidebar**
   - Ajustar ancho a 256px (w-64)
   - Implementar header con logo y versión
   - Implementar footer con indicador offline

3. **Mejorar Dashboard**
   - Grid de acciones rápidas (3 columnas)
   - Card del Asistente (fondo negro)
   - Sección de características avanzadas

4. **Animaciones**
   - Fade in desde arriba/abajo
   - Scale animations para cards
   - Transiciones suaves en hover

---

## 🎨 Paleta de Colores - Actualizada

### Colores Principales (Light Theme)

```
APP_BG:           #f9fafb (gray-50)     - Fondo global
SURFACE_BG:       #ffffff (white)        - Fondos principales
TEXT_PRIMARY:     #111827 (gray-900)     - Textos principales
TEXT_SECONDARY:   #6b7280 (gray-500)     - Textos secundarios
ACCENT:           #000000 (black)        - Botones y elementos destacados
ACCENT_TEXT:      #ffffff (white)        - Texto en elementos oscuros
BORDER:           #e5e7eb (gray-200)     - Bordes normales
BORDER_DASHED:    #d1d5db (gray-300)     - Bordes punteados
HOVER:            #f3f4f6 (gray-100)     - Estados hover
ICON_COLOR:       #4b5563 (gray-600)     - Iconos
```

### Colores de Estado

```
SUCCESS:          #10b981 (emerald-500)  - Operaciones completadas ✓
SUCCESS_LIGHT:    #d1fae5 (emerald-100)  - Fondo de success
ERROR:            #ef4444 (red-500)      - Errores ✗
ERROR_LIGHT:      #fee2e2 (red-100)      - Fondo de error
WARNING:          #f59e0b (amber-500)    - Advertencias ⚠
WARNING_LIGHT:    #fef3c7 (amber-100)    - Fondo de warning
INFO:             #8b5cf6 (violet-500)   - Información ℹ
INFO_LIGHT:       #ede9fe (violet-100)   - Fondo de info
```

---

## 🔧 Componentes QSS Disponibles

Cada componente usa una id específica que se puede aplicar en el código:

### Sidebar
```python
# Aplicar en main_window.py
sidebar_widget.setObjectName("sidebar")
sidebar_header.setObjectName("sidebarHeader")
nav_button.setObjectName("sidebarButton")
sidebar_footer.setObjectName("sidebarFooter")
```

### Dashboard
```python
dashboard_title.setObjectName("dashboardTitle")
dashboard_subtitle.setObjectName("dashboardSubtitle")
card.setObjectName("dashboardCard")
assistant_card.setObjectName("assistantCard")
```

### Botones
```python
button.setObjectName("primaryButton")
secondary_btn.setObjectName("secondaryButton")
```

### Inputs
```python
input_field.setObjectName("QLineEdit")  # Automático
combo_box.setObjectName("QComboBox")    # Automático
```

### Drop Zone
```python
drop_area.setObjectName("dropZone")
```

### Progress
```python
progress_bar.setObjectName("QProgressBar")  # Automático
```

---

## 📐 Especificaciones de Tamaños

### Sidebar
- Ancho: 256px (w-64)
- Padding header: 24px
- Padding footer: 16px
- Altura botón nav: 48px (padding 12px vertical)

### Dashboard
- Padding contenedor: 32px (p-8)
- Max ancho contenido: 896px (max-w-4xl)
- Radio cards: 20px (rounded-2xl)
- Padding cards: 24px (p-6)

### Botones
- Alto: 48px (h-12)
- Padding horizontal: 24px (px-6)
- Padding vertical: 12px (py-3)
- Radio: 12px (rounded-xl)

### Inputs
- Alto: 40px
- Padding: 10px 12px
- Radio: 10px (rounded-lg)
- Borde: 1px

### Drop Zone
- Radio: 24px (rounded-3xl)
- Padding: 48px (p-12)
- Borde: 2px dashed

---

## 🎬 Animaciones Implementadas

### En Style Content (CSS)

Disponibles para widgets que soporten transiciones:

1. **Hover Effects**
   - Buttons: opacity 0.9 en hover
   - Cards: cambio de hover background

2. **Transiciones**
   - Border color on focus (inputs)
   - Background color on state change

### Próximas a Implementar (QPropertyAnimation)

1. **Fade In**
   - Opacity: 0 → 1
   - Duración: 300ms

2. **Slide In**
   - Position: -20px → 0px
   - Duración: 300ms

3. **Scale**
   - Scale: 0.98 → 1
   - Duración: 200ms

---

## 📋 Checklist de Implementación

### Sidebar
- [ ] Ancho fijo a 256px
- [ ] Header con logo (icono negro 40x40px)
- [ ] Versión mostrada
- [ ] Botones nav con estado activo/inactivo
- [ ] Footer con indicador offline
- [ ] Badge "Nuevo" en Asistente

### Dashboard
- [ ] Título "Bienvenido a LocalPDF" (36px, bold)
- [ ] Card grande del Asistente (fondo negro, icono blanco)
- [ ] Grid 3 columnas de "Acciones Rápidas"
- [ ] Iconos en cada card (48x48px, fondo negro)
- [ ] Grid 2 columnas de "Características Avanzadas"

### General
- [ ] Todos los cards con border-gray-200
- [ ] Todos los botones primarios con bg-black
- [ ] Scroll areas con tema consistente
- [ ] Hover effects en todos los elementos interactivos

---

## 🔗 Archivos Modificados

### ✅ themes.py
- Actualizado con paleta completa de LocalPDF v5
- Añadidos colores de estado (Success, Error, Warning, Info)
- Mantiene compatibilidad con dark theme

### ✅ style_content.py
- Expandido a 200+ líneas de QSS
- Definiciones completas para todos los componentes
- Variables {{VARIABLE}} para tema dinámico
- Documentación inline completa

### ⏳ main_window.py
- Próxima a revisar/actualizar para usar nuevas clases

### ⏳ Widgets específicos
- Próximos a aplicar objectName para custom styling

---

## 💡 Notas de Desarrollo

### Para Aplicar Estilos a Nuevos Widgets

```python
# En el constructor del widget
widget.setObjectName("dashboardCard")
# Automáticamente aplicará los estilos de #dashboardCard del QSS
```

### Para Crear Nuevos Estilos

```python
# Agregar a STYLES_QSS en style_content.py
QFrame#myCustomWidget {
    background-color: {{ACCENT}};
    border-radius: 12px;
    padding: 16px;
}

# Luego usar en el código
my_widget.setObjectName("myCustomWidget")
```

### Colores Dinámicos

Todos los colores usan variables {{VARIABLE}} que se reemplazan automáticamente:

```python
# En theme_manager.py (ya implementado)
for key, value in palette.items():
    qss_content = qss_content.replace(f"{{{{{key}}}}}", value)
```

---

## 🎯 Próximas Acciones

1. **Verificar Iconos**
   - Revisar que los iconos en "Acciones Rápidas" se cargan desde `assets/icons/`
   - Asegurar que tienen el tamaño correcto (48x48px)

2. **Refinar Main Window**
   - Aplicar objectName a todos los widgets principales
   - Asegurar que los ids coinciden con el QSS

3. **Pruebas Visuales**
   - Ejecutar `python main.py`
   - Verificar que los colores y espaciados son correctos
   - Revisar hover effects y transiciones

4. **Animaciones**
   - Si es necesario, implementar QPropertyAnimation para efectos más complejos
   - Fade in, slide in, scale effects

---

## 📞 Referencia Rápida

**Documento Original**: LocalPDF v5 - Documentación Completa de Diseño y Funcionalidad
**Basado en**: Diseño minimalista iOS, paleta blanco/gris/negro
**Framework**: Qt/PySide6
**Tipografía**: Segoe UI, Helvetica Neue, sans-serif
**Colores**: Grises de Tailwind + Negro principal
**Estados**: Success (verde), Error (rojo), Warning (ámbar), Info (violeta)

---

*Documento generado: 17 de Enero de 2026*
*Proyecto: LocalPDF v5 (Vectora) - PySide6 Implementation*
