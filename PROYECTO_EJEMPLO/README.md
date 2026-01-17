# LocalPDF - Interfaz Web Profesional tipo iOS

Esta es una implementación web completa de LocalPDF con un diseño profesional inspirado en iOS. Está construida con React, TypeScript, Tailwind CSS y Motion (Framer Motion).

## 🎨 Características Visuales

### Estilo iOS Profesional
- **Glassmorphism**: Efectos de vidrio translúcido con backdrop-blur
- **Gradientes suaves**: Degradados modernos en tarjetas y botones
- **Animaciones fluidas**: Transiciones suaves con Motion/React
- **Bordes redondeados**: Esquinas curvas al estilo iOS
- **Sombras elevadas**: Profundidad visual con shadow-lg
- **Colores vibrantes**: Paleta de colores moderna y accesible

## 📁 Estructura del Proyecto

```
src/
├── app/
│   ├── App.tsx                          # Componente principal con routing
│   ├── components/
│   │   ├── Sidebar.tsx                  # Navegación lateral con animaciones
│   │   ├── Dashboard.tsx                # Panel principal con accesos rápidos
│   │   ├── FileDropzone.tsx             # Componente de drag & drop reutilizable
│   │   ├── Wizard.tsx                   # Asistente inteligente guiado
│   │   └── operations/                  # Operaciones PDF
│   │       ├── MergePDF.tsx             # Combinar PDFs con reordenamiento
│   │       ├── SplitPDF.tsx             # Dividir PDFs (rango/páginas/cada N)
│   │       ├── CompressPDF.tsx          # Comprimir con niveles ajustables
│   │       ├── ConvertPDF.tsx           # Conversiones múltiples formatos
│   │       ├── SecurityPDF.tsx          # Encriptar/Desencriptar/Permisos
│   │       ├── OCRPdf.tsx               # Reconocimiento de texto
│   │       └── BatchProcessing.tsx      # Procesamiento por lotes
│   └── components/ui/                   # Componentes UI base (shadcn)
└── styles/
    ├── index.css
    ├── theme.css                        # Variables de tema
    └── tailwind.css
```

## 🚀 Funcionalidades Implementadas

### 1. Dashboard
- Tarjeta destacada del Asistente Inteligente
- Grid de acciones rápidas con iconos coloridos
- Características avanzadas (Lotes, Layout Engine)
- Animaciones de entrada escalonadas

### 2. Combinar PDFs (Merge)
- Drag & drop múltiple
- Lista reordenable con Reorder de Motion
- Vista previa del orden de combinación
- Barra de progreso en tiempo real
- Descarga del archivo combinado

### 3. Dividir PDF (Split)
- Tres modos: Por rango, Páginas específicas, Cada N páginas
- Tabs para alternar entre modos
- Validación de inputs
- Visualización del resultado

### 4. Comprimir PDF
- Slider de nivel de compresión
- 4 niveles predefinidos: Baja, Media, Alta, Extrema
- Comparación de tamaños (original vs comprimido)
- Porcentaje de ahorro calculado

### 5. Convertir Archivos
- 4 tipos de conversión:
  - PDF → Word (con Layout Engine)
  - Word → PDF
  - PDF → Imágenes
  - Imágenes → PDF
- Tarjeta informativa sobre Layout Engine
- Selección visual de tipo de conversión

### 6. Seguridad PDF
- Tres modos: Encriptar, Desencriptar, Permisos
- Campos de contraseña con show/hide
- Switches para permisos individuales:
  - Permitir impresión
  - Permitir copiar texto
  - Permitir modificar
  - Permitir anotaciones

### 7. OCR
- Detección automática de páginas escaneadas
- Selector de idioma (6 idiomas)
- Información sobre Tesseract OCR
- Progreso por página
- Vista previa de capacidades del PDF resultante

### 8. Procesamiento por Lotes
- Selección de operación batch
- Hasta 50 archivos simultáneos
- Toggle de "Carpeta vigilada"
- Lista de estado por archivo:
  - Pendiente (gris)
  - Procesando (azul con spinner)
  - Completado (verde con check)
- Barra de progreso general

### 9. Asistente Inteligente (Wizard)
- Sistema de preguntas interactivas
- Breadcrumb de selección
- Recomendación personalizada
- Navegación directa a la función sugerida
- Animaciones de transición entre pasos

## 🎨 Paleta de Colores

Cada operación tiene su propio esquema de colores:

- **Combinar**: Azul a Cyan (`from-blue-500 to-cyan-500`)
- **Dividir**: Morado a Rosa (`from-purple-500 to-pink-500`)
- **Comprimir**: Esmeralda a Teal (`from-emerald-500 to-teal-500`)
- **Convertir**: Naranja a Rojo (`from-orange-500 to-red-500`)
- **Seguridad**: Índigo a Azul (`from-indigo-500 to-blue-500`)
- **OCR**: Violeta a Morado (`from-violet-500 to-purple-500`)
- **Lotes**: Ámbar a Naranja (`from-amber-500 to-orange-500`)
- **Wizard**: Azul a Morado (`from-blue-500 via-indigo-500 to-purple-500`)

## 🔧 Componentes Reutilizables

### FileDropzone
Componente de drag & drop con:
- Soporte múltiple o single file
- Límite configurable de archivos
- Animaciones de hover/drag
- Lista de archivos seleccionados con preview
- Botón de eliminación individual

### Patrones de UI
- **Cards con glassmorphism**: `bg-white/60 backdrop-blur-xl`
- **Botones gradiente**: `bg-gradient-to-r from-{color} to-{color}`
- **Bordes suaves**: `rounded-2xl` o `rounded-3xl`
- **Sombras**: `shadow-lg` para elevación
- **Transiciones**: `transition-all duration-300`

## 🎭 Animaciones con Motion

### Tipos de animaciones usadas:

1. **Fade & Slide**: 
   ```tsx
   initial={{ opacity: 0, y: 20 }}
   animate={{ opacity: 1, y: 0 }}
   ```

2. **Scale**: 
   ```tsx
   whileHover={{ scale: 1.02 }}
   whileTap={{ scale: 0.98 }}
   ```

3. **Layout Animations**:
   ```tsx
   <motion.div layoutId="activeTab" />
   ```

4. **Reorder** (Drag & Drop):
   ```tsx
   <Reorder.Group values={items} onReorder={setItems}>
   ```

5. **AnimatePresence** (Enter/Exit):
   ```tsx
   <AnimatePresence>
     {condition && <motion.div exit={{ opacity: 0 }} />}
   </AnimatePresence>
   ```

## 📱 Responsive Design

- **Mobile-first**: Grid adaptable con `grid-cols-1 md:grid-cols-2`
- **Sidebar**: Colapsable en móviles (puede extenderse)
- **Cards**: Stack vertical en mobile, grid en desktop
- **Máximos anchos**: `max-w-4xl` o `max-w-5xl` para contenido

## 🎯 Para Implementar en Python/PySide6

### Conceptos traducibles:

1. **Glassmorphism** → QGraphicsBlurEffect + semi-transparencia
2. **Gradientes** → QLinearGradient en botones y fondos
3. **Animaciones** → QPropertyAnimation para transiciones
4. **Drag & Drop** → QDrag y eventos dragEnter/dropEvent
5. **Progress** → QProgressBar con estilos personalizados
6. **Tabs** → QTabWidget con estilos
7. **Wizard** → QWizard personalizado

### QSS Equivalentes:

```css
/* Glassmorphism en Qt */
QWidget#card {
    background-color: rgba(255, 255, 255, 150);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 80);
}

/* Gradiente en botón */
QPushButton {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #3b82f6,
        stop:1 #06b6d4
    );
    border-radius: 12px;
    color: white;
    padding: 12px 24px;
}

/* Hover effect */
QPushButton:hover {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #2563eb,
        stop:1 #0891b2
    );
}
```

## 📦 Dependencias Clave

- **React 18**: Framework base
- **Motion (Framer Motion)**: Animaciones fluidas
- **Tailwind CSS v4**: Utility-first CSS
- **Radix UI**: Componentes accesibles
- **Lucide React**: Iconos modernos
- **Sonner**: Notificaciones toast

## 🎨 Inspiración de Diseño

Esta interfaz está inspirada en:
- **iOS Design Guidelines**: Bordes redondeados, glassmorphism
- **macOS Big Sur**: Efectos de profundidad y translucidez
- **Material Design 3**: Uso de color y elevación
- **Figma**: Principios de diseño modernos

## 🚀 Cómo Usar

1. Cada operación tiene su propia vista
2. Todas usan el componente FileDropzone para selección
3. Las barras de progreso simulan procesamiento real
4. Los toasts (Sonner) muestran feedback al usuario
5. El Wizard guía a usuarios nuevos

## 💡 Mejoras Sugeridas

- [ ] Añadir vista previa de PDFs
- [ ] Implementar arrastrar archivos entre operaciones
- [ ] Modo oscuro completo
- [ ] Atajos de teclado
- [ ] Historial de operaciones
- [ ] Configuración de preferencias
- [ ] Exportar/Importar flujos de trabajo

---

**Nota**: Esta es una implementación de referencia visual. Para la versión Python/PySide6, 
adapta los conceptos de diseño usando QSS y las APIs de Qt equivalentes.
