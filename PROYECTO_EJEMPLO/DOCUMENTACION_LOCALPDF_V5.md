# LocalPDF v5 - Documentación Completa de Diseño y Funcionalidad

## 📋 Índice

1. [Sistema de Diseño](#sistema-de-diseño)
2. [Estructura General](#estructura-general)
3. [Sidebar (Barra Lateral)](#sidebar-barra-lateral)
4. [Dashboard](#dashboard)
5. [Asistente Inteligente (Wizard)](#asistente-inteligente-wizard)
6. [Operaciones PDF](#operaciones-pdf)
7. [Componentes Reutilizables](#componentes-reutilizables)
8. [Animaciones y Transiciones](#animaciones-y-transiciones)

---

## Sistema de Diseño

### Paleta de Colores

LocalPDF v5 utiliza un **esquema minimalista** basado en blancos, negros y grises, inspirado en el diseño iOS:

#### Colores Principales

- **Negro Principal**: `#000000` / `rgb(0, 0, 0)` / Tailwind: `bg-black`
- **Gris Oscuro**: `#111827` / `gray-900` - Para textos principales
- **Gris Medio**: `#6b7280` / `gray-500` - Para textos secundarios
- **Gris Claro**: `#f9fafb` / `gray-50` - Para fondos secundarios
- **Blanco**: `#ffffff` / `bg-white` - Para fondos principales

#### Colores de Estado

- **Éxito**: Tonos verdes (`emerald`, `green`, `teal`)
- **Procesando**: Tonos azules (`blue`, `indigo`)
- **Advertencia**: Tonos ámbar (`amber`)
- **Información**: Tonos violeta (`violet`, `purple`)

### Tipografía

- **Familia de fuente**: Sistema nativo (sans-serif)
- **Tamaños principales**:
  - **Títulos principales (h1)**: `text-3xl` / `text-4xl` (30-36px)
  - **Subtítulos (h2)**: `text-2xl` / `text-xl` (20-24px)
  - **Encabezados (h3)**: `text-lg` (18px)
  - **Texto normal**: `text-base` (16px)
  - **Texto pequeño**: `text-sm` (14px)
  - **Texto extra pequeño**: `text-xs` (12px)

- **Pesos de fuente**:
  - **Normal**: `font-normal` (400)
  - **Medio**: `font-medium` (500)
  - **Semi-negrita**: `font-semibold` (600)
  - **Negrita**: `font-bold` (700)

### Espaciado y Layout

- **Padding de contenedor**: `p-8` (32px)
- **Espaciado entre secciones**: `space-y-6` (24px)
- **Máximo ancho de contenido**: `max-w-4xl` (896px) para operaciones estándar
- **Máximo ancho de contenido batch**: `max-w-5xl` (1024px)

### Bordes y Radios

- **Radio pequeño**: `rounded-xl` (12px) - Para iconos y elementos pequeños
- **Radio medio**: `rounded-2xl` (16px) - Para cards y contenedores principales
- **Radio grande**: `rounded-3xl` (24px) - Para elementos destacados
- **Bordes**: `border` / `border-2` con `border-gray-200` o `border-gray-300`

### Sombras

- **Sombra suave**: `shadow-sm` - Para elementos hover
- **Sombra media**: `shadow-md` - Para elementos activos
- **Sombra grande**: `shadow-xl` - Para elementos destacados

---

## Estructura General

### Layout Principal

```
┌─────────────────────────────────────────┐
│  [Sidebar]  │  [Contenido Principal]    │
│   264px     │     Resto del espacio      │
│             │                            │
│  Menú de    │  Dashboard / Operaciones   │
│  navegación │                            │
└─────────────────────────────────────────┘
```

#### Características del Layout

- **Fondo global**: `bg-gray-50`
- **Alto completo**: `h-screen` (100vh)
- **Sin scroll en layout**: `overflow-hidden` - El scroll está en cada vista individual
- **Flex layout**: Sidebar fijo + contenido flexible

---

## Sidebar (Barra Lateral)

### Dimensiones y Estructura

```
┌────────────────────────┐
│      [Header]          │ ← Logo y versión
├────────────────────────┤
│                        │
│    [Navegación]        │ ← Menú de opciones
│                        │
│  • Dashboard           │
│  • Asistente (Nuevo)   │
│  • Combinar            │
│  • Dividir             │
│  • Comprimir           │
│  • Convertir           │
│  • Seguridad           │
│  • OCR                 │
│  • Lotes               │
│                        │
├────────────────────────┤
│      [Footer]          │ ← Indicador offline
└────────────────────────┘
```

### Especificaciones Visuales

#### Contenedor Principal

- **Ancho**: `w-64` (256px)
- **Fondo**: `bg-white`
- **Borde derecho**: `border-r border-gray-200`
- **Display**: `flex flex-col` (columna flexible)

#### Header del Sidebar

**Padding**: `p-6` (24px)
**Borde inferior**: `border-b border-gray-200`

**Logo/Icono**:

- Contenedor: `w-10 h-10` (40x40px)
- Fondo: `bg-black`
- Radio: `rounded-2xl` (16px)
- Icono: FileText, `w-6 h-6` (24x24px), `text-white`

**Texto**:

- Título: "LocalPDF", `text-lg font-semibold text-gray-900`
- Versión: "v5.0", `text-xs text-gray-500`

#### Botones de Navegación

**Contenedor**: `p-4` (16px padding), `space-y-1` (4px entre items)

**Cada botón**:

- **Ancho completo**: `w-full`
- **Padding interno**: `px-4 py-3` (16px horizontal, 12px vertical)
- **Radio**: `rounded-xl` (12px)
- **Display**: `flex items-center gap-3`
- **Transición**: `transition-all duration-200`

**Estados del botón**:

1. **Estado Activo**:
   - Fondo: `bg-gray-900` (negro)
   - Texto: `text-white`
   - Icono: `text-white`
2. **Estado Inactivo**:
   - Fondo: transparente
   - Hover: `hover:bg-gray-100`
   - Texto: `text-gray-700`
   - Icono: `text-gray-600`

**Icono del botón**:

- Tamaño: `w-5 h-5` (20x20px)
- Alineación: Izquierda del texto

**Badge "Nuevo"** (en Asistente):

- Posición: `ml-auto` (extremo derecho)
- Padding: `px-2 py-0.5`
- Tamaño texto: `text-xs font-semibold`
- Fondo: `bg-black`
- Texto: `text-white`
- Radio: `rounded-full`

**Animaciones**:

- Hover: `scale: 1.02`
- Tap: `scale: 0.98`

#### Footer del Sidebar

**Padding**: `p-4` (16px)
**Borde superior**: `border-t border-gray-200`

**Card de estado**:

- Fondo: `bg-gray-100`
- Radio: `rounded-xl` (12px)
- Padding: `p-4` (16px)
- Texto principal: "100% Offline", `text-xs text-gray-900 font-medium`
- Texto secundario: "Sin conexión requerida", `text-xs text-gray-600`

---

## Dashboard

### Layout del Dashboard

```
┌─────────────────────────────────────────────┐
│  [Header con título de bienvenida]          │
├─────────────────────────────────────────────┤
│  [Card grande del Asistente - Negro]        │
├─────────────────────────────────────────────┤
│  [Grid de Acciones Rápidas - 3 columnas]    │
│  ┌──────┐  ┌──────┐  ┌──────┐              │
│  │Card 1│  │Card 2│  │Card 3│              │
│  └──────┘  └──────┘  └──────┘              │
│  ┌──────┐  ┌──────┐  ┌──────┐              │
│  │Card 4│  │Card 5│  │Card 6│              │
│  └──────┘  └──────┘  └──────┘              │
├─────────────────────────────────────────────┤
│  [Características Avanzadas - 2 columnas]   │
│  ┌───────────────┐  ┌───────────────┐      │
│  │  Lotes        │  │ Layout Engine │      │
│  └───────────────┘  └───────────────┘      │
└─────────────────────────────────────────────┘
```

### Especificaciones Visuales

#### Contenedor Principal

- **Fondo**: `bg-white`
- **Scroll**: `overflow-y-auto h-full`
- **Padding**: `p-8` (32px)
- **Max width**: `max-w-7xl mx-auto`

#### Header del Dashboard

**Animación entrada**: Fade in desde arriba

- `initial: opacity: 0, y: -20`
- `animate: opacity: 1, y: 0`

**Título**:

- Texto: "Bienvenido a LocalPDF"
- Estilo: `text-4xl font-bold text-gray-900`
- Margen inferior: `mb-2`

**Subtítulo**:

- Texto: "Herramienta profesional para manipulación de PDFs — 100% offline"
- Estilo: `text-gray-600`

#### Card del Asistente Inteligente

**Dimensiones y estilo**:

- Margen: `mb-8` (32px)
- Fondo: `bg-black`
- Radio: `rounded-3xl` (24px)
- Padding: `p-8` (32px)
- Cursor: `cursor-pointer`
- Hover: `hover:bg-gray-900`
- Transición: `transition-colors duration-300`

**Layout interno**: `flex items-center justify-between`

**Icono del asistente**:

- Contenedor: `w-16 h-16` (64x64px)
- Fondo: `bg-white`
- Radio: `rounded-2xl` (16px)
- Icono: Wand2, `w-8 h-8 text-black`

**Texto**:

- Título: "Asistente Inteligente", `text-2xl font-bold text-white mb-1`
- Descripción: "Déjanos ayudarte a elegir la mejor operación para tu documento", `text-gray-300`

**Flecha derecha**:

- Icono: ArrowRight, `w-6 h-6 text-white`
- Animación hover: `group-hover:translate-x-2 transition-transform duration-300`

#### Grid de Acciones Rápidas

**Título sección**: "Acciones Rápidas", `text-xl font-semibold text-gray-900 mb-4`

**Grid**:

- Layout: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4`
- Espacio entre cards: `gap-4` (16px)

**Cada Card de Acción**:

- Fondo: `bg-gray-50`
- Hover: `hover:bg-gray-100`
- Radio: `rounded-2xl` (16px)
- Padding: `p-6` (24px)
- Borde: `border border-gray-200`
- Transición: `transition-all duration-300`
- Cursor: `cursor-pointer`

**Icono de la acción**:

- Contenedor: `w-12 h-12` (48x48px)
- Fondo: `bg-black`
- Radio: `rounded-xl` (12px)
- Margen inferior: `mb-4`
- Animación hover: `group-hover:scale-110 transition-transform duration-300`
- Icono: `w-6 h-6 text-white`

**Texto del card**:

- Título: `font-semibold text-gray-900 mb-2`
- Descripción: `text-sm text-gray-600`

**Lista de acciones rápidas**:

1. **Combinar PDFs** (Icono: Combine)
2. **Dividir PDF** (Icono: Scissors)
3. **Comprimir** (Icono: Archive)
4. **Convertir** (Icono: RefreshCw)
5. **Seguridad** (Icono: Shield)
6. **OCR** (Icono: ScanText)

#### Sección Características Avanzadas

**Título**: "Características Avanzadas", `text-xl font-semibold text-gray-900 mb-4`

**Grid**: `grid grid-cols-1 md:grid-cols-2 gap-4`

**Card 1 - Procesamiento por Lotes** (Clickeable):

- Fondo: `bg-gray-50`
- Hover: `hover:bg-gray-100`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-gray-200`
- Layout: `flex items-center gap-4`

**Card 2 - Layout Engine** (No clickeable):

- Igual que Card 1 pero sin hover effects

**Iconos de características**:

- Contenedor: `w-12 h-12 bg-black rounded-xl`
- Icono: `w-6 h-6 text-white`

**Flecha en card clickeable**:

- Icono: ArrowRight, `w-5 h-5 text-gray-400`
- Animación: `group-hover:translate-x-2 transition-transform duration-300`

---

## Asistente Inteligente (Wizard)

### Layout del Wizard

```
┌─────────────────────────────────────────────┐
│  [Header con icono y título]                │
├─────────────────────────────────────────────┤
│  [Breadcrumb - Path de selección]           │
├─────────────────────────────────────────────┤
│  [Card de pregunta]                         │
│  ┌─────────────────────────────────────┐    │
│  │ ¿Qué quieres hacer con tus PDFs?   │    │
│  ├─────────────────────────────────────┤    │
│  │  [Grid de opciones - 2 columnas]   │    │
│  │  ┌──────────┐  ┌──────────┐        │    │
│  │  │ Opción 1 │  │ Opción 2 │        │    │
│  │  └──────────┘  └──────────┘        │    │
│  └─────────────────────────────────────┘    │
├─────────────────────────────────────────────┤
│  [Card de ayuda]                            │
└─────────────────────────────────────────────┘
```

### Especificaciones Visuales

#### Header del Wizard

**Layout**: `flex items-center gap-4 mb-4`

**Icono principal**:

- Contenedor: `w-14 h-14 bg-black rounded-2xl`
- Icono: Wand2, `w-7 h-7 text-white`

**Texto**:

- Título: "Asistente Inteligente", `text-3xl font-bold text-gray-900`
- Subtítulo: "Responde unas preguntas y te ayudaré a encontrar la función perfecta", `text-gray-600`

#### Breadcrumb (Path de Selección)

**Animación**: Fade in/out con `AnimatePresence`

- `initial: opacity: 0, y: -10`
- `animate: opacity: 1, y: 0`
- `exit: opacity: 0, y: -10`

**Layout**: `flex items-center gap-2 flex-wrap mb-6`

**Cada paso**:

- Fondo: `bg-white/60 backdrop-blur-xl`
- Padding: `px-3 py-1`
- Radio: `rounded-full`
- Texto: `text-sm text-gray-600`

**Separador**: ChevronRight, `w-4 h-4 text-gray-400`

#### Card de Pregunta

**Contenedor principal**:

- Fondo: `bg-gray-50`
- Radio: `rounded-2xl` (16px)
- Padding: `p-8` (32px)
- Borde: `border border-gray-200`
- Margen inferior: `mb-6`

**Encabezado de pregunta**:

- Layout: `flex items-start gap-3 mb-6`
- Icono: HelpCircle, `w-6 h-6 text-indigo-500`
- Texto: `text-2xl font-semibold text-gray-800`

**Grid de Opciones**: `grid grid-cols-1 md:grid-cols-2 gap-4`

#### Botones de Opción

**Estilo base**:

- Padding: `p-6` (24px)
- Fondo: `bg-white`
- Hover: `hover:bg-gray-50`
- Radio: `rounded-2xl` (16px)
- Borde: `border border-gray-200`
- Borde hover: `hover:border-gray-900`
- Sombra hover: `hover:shadow-md`
- Transición: `transition-all`
- Alineación: `text-left`

**Animaciones**:

- Hover: `scale: 1.02`
- Tap: `scale: 0.98`

**Layout interno**: `flex items-start gap-4`

**Icono de opción**:

- Contenedor: `w-12 h-12 bg-black rounded-xl`
- Animación hover: `group-hover:scale-110 transition-transform`
- Icono: `w-6 h-6 text-white`

**Texto de opción**:

- Texto principal: `font-medium text-gray-800 group-hover:text-indigo-900`

**Flecha indicadora**:

- Icono: ChevronRight, `w-5 h-5 text-gray-400`
- Hover: `group-hover:text-indigo-500 group-hover:translate-x-1`

#### Pantalla de Resultado

**Contenedor**:

- Fondo: `bg-gray-900`
- Radio: `rounded-2xl`
- Padding: `p-8`

**Icono de éxito**:

- Contenedor: `w-20 h-20 bg-white rounded-full` (centrado)
- Animación entrada: `scale: 0` → `scale: 1` con spring
- Icono: CheckCircle2, `w-10 h-10 text-black`

**Título**:

- Texto: "¡Perfecto! Te recomiendo:"
- Estilo: `text-2xl font-bold text-white mb-2`

**Subtítulo**:

- Texto: "Basándome en tus respuestas, esta es la mejor opción para ti"
- Estilo: `text-gray-300`

**Path de Selección**:

- Contenedor: `bg-white/10 backdrop-blur-xl rounded-xl p-6 mb-6`
- Título: "Tu selección:", `font-semibold text-white mb-3`

**Cada paso numerado**:

- Layout: `flex items-center gap-3`
- Número: `w-6 h-6 bg-white rounded-full`, texto: `text-black text-xs font-bold`
- Texto: `text-gray-300`

**Botones de acción**:

1. **Ir a la función**: `bg-white hover:bg-gray-100 text-black h-12 text-lg`
2. **Empezar de nuevo**: `variant-outline border-white text-white hover:bg-white/10`

#### Card de Ayuda

**Contenedor**:

- Fondo: `bg-gray-50`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-gray-200`
- Margen superior: `mt-8`

**Layout**: `flex items-start gap-3`

**Icono**: Sparkles, `w-6 h-6 text-gray-600`

**Contenido**:

- Título: "Sugerencia", `font-semibold text-gray-900 mb-2`
- Texto: `text-sm text-gray-600`

---

## Operaciones PDF

### Estructura Común de Todas las Operaciones

```
┌─────────────────────────────────────────────┐
│  [Header con icono y título]                │
├─────────────────────────────────────────────┤
│  [Dropzone para archivos]                  │
├─────────────────────────────────────────────┤
│  [Opciones específicas de la operación]    │
├─────────────────────────────────────────────┤
│  [Barra de progreso - cuando procesa]      │
├─────────────────────────────────────────────┤
│  [Card de éxito - cuando completa]         │
├─────────────────────────────────────────────┤
│  [Botón de acción principal]               │
└─────────────────────────────────────────────┘
```

### Header Estándar de Operaciones

**Layout**: `flex items-center gap-4 mb-4`

**Icono**:

- Contenedor: `w-14 h-14 bg-black rounded-2xl`
- Icono específico: `w-7 h-7 text-white`

**Texto**:

- Título: `text-3xl font-bold text-gray-900`
- Descripción: `text-gray-600`

### Botón de Acción Principal

**Estilo**:

- Ancho: `w-full` o `flex-1`
- Fondo: `bg-black`
- Hover: `hover:bg-gray-900`
- Texto: `text-white`
- Altura: `h-12` (48px)
- Tamaño texto: `text-lg`
- Disabled: `disabled:opacity-50 disabled:cursor-not-allowed`

**Icono del botón**: `w-5 h-5 mr-2`

### Card de Progreso

**Contenedor**:

- Fondo: `bg-gray-50`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-gray-200`

**Título**: "Procesando...", `text-lg font-semibold text-gray-800 mb-4`

**Barra de progreso**: Componente Progress con valor dinámico

**Porcentaje**: `text-sm text-gray-600 text-center`

### Card de Éxito

**Contenedor**:

- Fondo: `bg-gray-900`
- Radio: `rounded-2xl`
- Padding: `p-6`

**Layout**: `flex items-center justify-between`

**Texto**:

- Título: "¡Proceso completado!", `text-lg font-semibold text-white mb-1`
- Descripción: `text-sm text-gray-300`

**Botón descargar**:

- Fondo: `bg-white`
- Hover: `hover:bg-gray-100`
- Texto: `text-black`

---

## 1. Combinar PDFs (MergePDF)

### Elementos Únicos

#### Lista Reordenable de Archivos

**Contenedor**:

- Fondo: `bg-gray-50`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-gray-200`

**Título**: `text-lg font-semibold text-gray-900 mb-4`

- Icono: GripVertical, `w-5 h-5 text-gray-400`
- Texto: "Orden de combinación (arrastra para reordenar)"

**Cada archivo en la lista**:

- Layout: `flex items-center gap-3`
- Padding: `p-4`
- Fondo: `bg-white`
- Radio: `rounded-xl`
- Borde: `border border-gray-200`
- Hover: `hover:shadow-sm`
- Cursor: `cursor-move`

**Elementos del item**:

1. **Icono de arrastre**: GripVertical, `w-5 h-5 text-gray-400`
2. **Número de orden**:
   - Contenedor: `w-8 h-8 bg-gray-900 text-white rounded-lg`
   - Texto: `font-semibold text-sm`
3. **Info del archivo**:
   - Nombre: `font-medium text-gray-900`
   - Tamaño: `text-xs text-gray-500` (formato: X.XX MB)
4. **Flecha**: ArrowRight, `w-4 h-4 text-gray-400` (excepto último archivo)

---

## 2. Dividir PDF (SplitPDF)

### Elementos Únicos

#### Tabs de Modo de División

**Componente**: Tabs con 3 opciones

- "Por rango"
- "Páginas específicas"
- "Cada N páginas"

**TabsList**: `grid w-full grid-cols-3 mb-6`

#### Opción 1: Por Rango

**Grid de inputs**: `grid grid-cols-2 gap-4`

**Campos**:

1. **Página inicial**: Input numérico, placeholder "1"
2. **Página final**: Input numérico, placeholder "10"

**Descripción**: `text-sm text-gray-600`

- "Extrae un rango continuo de páginas del PDF"

#### Opción 2: Páginas Específicas

**Input de texto**:

- Placeholder: "1, 3, 5, 7-10"
- Label: "Páginas (separadas por coma)"

**Descripción**:

- 'Ejemplo: "1, 3, 5-8, 12" extraerá las páginas 1, 3, 5, 6, 7, 8 y 12'

#### Opción 3: Cada N Páginas

**Input numérico**:

- Label: "Dividir cada N páginas"
- Placeholder: "5"

**Descripción**:

- "Divide el PDF en múltiples archivos cada N páginas"

---

## 3. Comprimir PDF (CompressPDF)

### Elementos Únicos

#### Niveles de Compresión

**Datos de niveles**:

```
Baja:    25%  → ~20% reducción, Alta calidad
Media:   50%  → ~40% reducción, Calidad equilibrada
Alta:    75%  → ~60% reducción, Compresión fuerte
Extrema: 100% → ~80% reducción, Máxima compresión
```

#### Slider de Compresión

**Contenedor**:

- Fondo: `bg-gray-50`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-gray-200`

**Header del slider**: `flex items-center justify-between mb-4`

- Label izquierda: Nombre del nivel actual
- Label derecha:
  - Icono: Sparkles, `w-4 h-4 text-emerald-500`
  - Texto: Porcentaje de reducción, `text-sm font-medium text-emerald-600`

**Slider**: Rango de 0-100, paso de 1

**Descripción**: `text-sm text-gray-600` (calidad del nivel)

#### Grid de Niveles Rápidos

**Grid**: `grid grid-cols-4 gap-2`

**Cada botón de nivel**:

- Padding: `p-3`
- Radio: `rounded-xl`
- Alineación: `text-center`
- Transición: `transition-all`

**Estados**:

- **Activo**: `bg-black text-white shadow-md`
- **Inactivo**: `bg-gray-100 text-gray-600 hover:bg-gray-200`

**Contenido**:

- Nivel: `text-xs font-medium`
- Reducción: `text-xs opacity-80 mt-1`

#### Card de Resultado con Comparación

**Contenedor interior**: `grid grid-cols-3 gap-4 pt-4 border-t border-green-200`

**Cada columna de métrica**:

- Layout: `text-center`
- Icono: `w-8 h-8 mx-auto mb-2` con color específico
- Label: `text-xs mb-1`
- Valor: `text-lg font-bold`

**Métricas**:

1. **Tamaño original**:
   - Icono: FileText, color green-600
   - Texto: color green-800
2. **Nuevo tamaño**:
   - Icono: Archive, color emerald-600
   - Texto: color emerald-800
3. **Ahorro**:
   - Icono: Sparkles, color teal-600
   - Texto: color teal-800, formato "X%"

---

## 4. Convertir PDF (ConvertPDF)

### Elementos Únicos

#### Grid de Tipos de Conversión

**Grid**: `grid grid-cols-1 md:grid-cols-2 gap-4`

**Tipos disponibles**:

1. **PDF → Word**: `.pdf` → `.docx`, Icono FileText, gradiente azul-índigo
2. **Word → PDF**: `.doc,.docx` → `.pdf`, Icono FileSpreadsheet, gradiente púrpura-rosa
3. **PDF → Imágenes**: `.pdf` → `.png/.jpg`, Icono Image, gradiente esmeralda-teal
4. **Imágenes → PDF**: `.jpg,.jpeg,.png` → `.pdf`, Icono Image, gradiente naranja-rojo

#### Botón de Tipo de Conversión

**Estilo base**:

- Padding: `p-6`
- Radio: `rounded-2xl`
- Alineación: `text-left`
- Transición: `transition-all`

**Estados**:

- **Seleccionado**:
  - `bg-gray-900 text-white`
  - Borde: `border-2 border-gray-900`
  - Sombra: `shadow-md`
  - Layout ID animado: `layoutId="selectedConversion"`
- **No seleccionado**:
  - `bg-gray-50`
  - Borde: `border border-gray-200`
  - Hover: `hover:bg-gray-100`

**Animaciones**:

- Hover: `scale: 1.02`
- Tap: `scale: 0.98`

**Layout interno**: `flex items-start gap-4`

**Icono**:

- Contenedor: `w-12 h-12 rounded-xl shadow-md`
- Seleccionado: `bg-white`, icono `text-black`
- No seleccionado: `bg-black`, icono `text-white`

**Texto**:

- Título: `font-semibold mb-1`
- Descripción: `text-sm`

#### Card de Layout Engine

**Aparece solo cuando**: Archivos seleccionados Y tipo = 'pdf-to-word'

**Contenedor**:

- Fondo: `bg-gray-50`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-gray-200`

**Layout**: `flex items-start gap-3`

**Icono principal**:

- Contenedor: `w-10 h-10 bg-black rounded-lg`
- Icono: RefreshCw, `w-5 h-5 text-white`

**Contenido**:

- Título: "Layout Engine Avanzado", `font-semibold text-indigo-900 mb-2`
- Descripción: `text-sm text-indigo-700 mb-2`

**Lista de características** (ul):

- Espaciado: `space-y-1`
- Cada item: `flex items-center gap-2`
- Bullet: `w-1.5 h-1.5 bg-indigo-500 rounded-full`
- Texto: `text-sm text-indigo-700`

**Características**:

1. "Detectar y preservar la estructura del documento"
2. "Mantener el formato de tablas, columnas y listas"
3. "Reconocer imágenes y gráficos automáticamente"

#### Progreso con Mensajes

Durante el procesamiento, muestra mensajes en puntos específicos:

- 25%: "Analizando estructura del documento..."
- 50%: "Aplicando Layout Engine..."
- 75%: "Generando archivo final..."

---

## 5. Seguridad PDF (SecurityPDF)

### Elementos Únicos

#### Grid de Modos de Seguridad

**Grid**: `grid grid-cols-1 md:grid-cols-3 gap-4`

**Modos disponibles**:

1. **Encriptar**: Lock icon, "Protege tu PDF con contraseña"
2. **Desencriptar**: Unlock icon, "Remueve la protección del PDF"
3. **Permisos**: Shield icon, "Configura restricciones específicas"

#### Botón de Modo

**Estilo base**:

- Padding: `p-6`
- Radio: `rounded-2xl`
- Alineación: `text-left`
- Transición: `transition-all`

**Estados**:

- **Seleccionado**: `bg-gray-900 text-white border-2 border-gray-900 shadow-md`
- **No seleccionado**: `bg-gray-50 border border-gray-200 hover:bg-gray-100`

**Icono del modo**:

- Contenedor: `w-12 h-12 bg-black rounded-xl mb-3`
- Icono: `w-6 h-6 text-white`

#### Panel de Encriptar/Desencriptar

**Campos de contraseña**:

**Contenedor del input**:

- Posición: `relative`
- Input: `pr-10` (espacio para botón de ojo)

**Botón mostrar/ocultar**:

- Posición: `absolute right-3 top-1/2 -translate-y-1/2`
- Icono: Eye o EyeOff, `w-4 h-4`
- Color: `text-gray-500 hover:text-gray-700`

**Card de consejo**:

- Fondo: `bg-blue-50`
- Radio: `rounded-xl`
- Padding: `p-4`
- Texto: `text-sm text-blue-800`
- Formato: "💡 **Consejo:** Usa una contraseña de al menos 8 caracteres con letras, números y símbolos"

#### Panel de Permisos

**Cada switch de permiso**:

- Layout: `flex items-center justify-between`
- Padding: `p-4`
- Fondo: `bg-gray-50`
- Radio: `rounded-xl`

**Texto del permiso**:

- Label: `text-base`
- Descripción: `text-sm text-gray-600 mt-1`

**Permisos disponibles**:

1. **Permitir impresión**: Default ON
2. **Permitir copiar texto**: Default ON
3. **Permitir modificar**: Default OFF
4. **Permitir anotaciones**: Default ON

---

## 6. OCR - Reconocimiento de Texto (OCRPdf)

### Elementos Únicos

#### Card de Información Inicial

**Contenedor**:

- Fondo: `bg-gray-50`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-gray-200`

**Layout**: `flex items-start gap-3`

**Icono**:

- Contenedor: `w-10 h-10 bg-black rounded-lg`
- Icono: FileSearch, `w-5 h-5 text-white`

**Contenido**:

- Título: "Detección Automática", `font-semibold text-violet-900 mb-2`
- Descripción: `text-sm text-violet-700`

#### Selector de Idioma

**Contenedor**:

- Fondo: `bg-white/60 backdrop-blur-xl`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-white/50`

**Label**: `text-base flex items-center gap-2 mb-3`

- Icono: Languages, `w-5 h-5 text-violet-600`
- Texto: "Idioma del documento"

**Select**: Componente Select estándar, `w-full`

**Idiomas disponibles**:

1. Español (spa)
2. Inglés (eng)
3. Portugués (por)
4. Francés (fra)
5. Alemán (deu)
6. Italiano (ita)

#### Card de Tesseract

**Contenedor**:

- Fondo: `bg-gray-50`
- Radio: `rounded-xl`
- Padding: `p-4`

**Título**: "Powered by Tesseract OCR", `font-medium text-gray-800 mb-2`

**Lista de características**:

- Espaciado: `space-y-1`
- Cada item: `flex items-center gap-2`
- Bullet: `w-1.5 h-1.5 bg-violet-500 rounded-full`
- Texto: `text-sm text-gray-600`

**Características**:

1. "Reconocimiento de alta precisión"
2. "Soporte para múltiples idiomas"
3. "100% procesamiento offline"

#### Progreso de OCR con Páginas

**Contenedor**:

- Fondo: `bg-white/60 backdrop-blur-xl`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-white/50`

**Título**: "Procesando con OCR...", `text-lg font-semibold text-gray-800 mb-4`

**Barra de progreso**: Componente Progress

**Info adicional**: `flex items-center justify-between text-sm`

- Izquierda: "Procesando: X / Y páginas", `text-gray-600`
- Derecha: "X%", `text-gray-600 font-medium`

#### Card de Resultado OCR

**Sección de beneficios**:

- Contenedor: `bg-gray-50 rounded-xl p-4`
- Título: "✓ El PDF ahora incluye:", `font-medium text-green-800 mb-2`

**Lista de beneficios**:

- Espaciado: `space-y-1`
- Bullet: `w-1.5 h-1.5 bg-green-600 rounded-full`
- Texto: `text-sm text-green-700`

**Beneficios**:

1. "Capa de texto buscable"
2. "Texto seleccionable y copiable"
3. "Compatible con lectores de pantalla"

#### Mensajes de Progreso

- 10%: "Detectando páginas escaneadas..."
- 30%: "Aplicando OCR con Tesseract..."
- 60%: "Extrayendo texto..."
- 90%: "Generando PDF con capa de texto..."

---

## 7. Procesamiento por Lotes (BatchProcessing)

### Elementos Únicos

#### Selector de Operación por Lotes

**Contenedor**:

- Fondo: `bg-gray-50`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-gray-200`

**Label**: "Operación a realizar", `text-base mb-3 block`

**Select**: Componente Select con opciones complejas

**Operaciones disponibles**:

1. **Combinar todos**: "Une todos los archivos en uno"
2. **Comprimir cada uno**: "Reduce el tamaño de cada PDF"
3. **Convertir a Word**: "Convierte cada PDF a DOCX"
4. **Aplicar OCR**: "Reconocimiento de texto en todos"
5. **Encriptar todos**: "Protege con contraseña"

**Formato de cada opción en Select**:

```
<div className="flex flex-col items-start">
  <span className="font-medium">{nombre}</span>
  <span className="text-xs text-gray-500">{descripción}</span>
</div>
```

#### Switch de Carpeta Vigilada

**Contenedor**:

- Layout: `flex items-center justify-between`
- Padding: `p-4`
- Fondo: `bg-amber-50`
- Radio: `rounded-xl`

**Lado izquierdo**: `flex items-center gap-3`

- Icono: Folder, `w-5 h-5 text-amber-600`
- Label: "Carpeta vigilada", `text-base`
- Descripción: "Procesa automáticamente archivos nuevos", `text-sm text-gray-600 mt-1`

**Lado derecho**: Switch component

#### Lista de Estado de Archivos

**Contenedor principal**:

- Fondo: `bg-gray-50`
- Radio: `rounded-2xl`
- Padding: `p-6`
- Borde: `border border-gray-200`

**Título**: "Estado del procesamiento", `text-lg font-semibold text-gray-800 mb-4`

**Contenedor de lista**:

- Espaciado: `space-y-2`
- Max height: `max-h-96` (scroll cuando excede)
- Scroll: `overflow-y-auto`

#### Item de Archivo en Procesamiento

**Contenedor**:

- Layout: `flex items-center gap-3`
- Padding: `p-3`
- Fondo: `bg-white`
- Radio: `rounded-xl`

**Animación entrada**:

- `initial: opacity: 0, x: -20`
- `animate: opacity: 1, x: 0`
- Delay escalonado: `delay: index * 0.05`

#### Estados del Icono

**Layout**: `flex-shrink-0`

1. **Pendiente**:
   - Icono: Clock, `w-5 h-5 text-gray-400`

2. **Procesando**:
   - Icono: Play, `w-5 h-5 text-blue-500`
   - Animación: Rotación continua 360°, duración 2s

3. **Completado**:
   - Icono: CheckCircle2, `w-5 h-5 text-green-500`

#### Info del Archivo

**Contenedor**: `flex-1 min-w-0`

**Nombre**:

- Texto: `text-sm font-medium text-gray-800 truncate`

**Barra de progreso** (solo cuando status = 'processing'):

- Margen: `mt-2`
- Altura: `h-1`
- Valor: progreso del archivo individual (0-100)

#### Badge de Estado

**Contenedor**: `flex-shrink-0`

**Variantes**:

1. **Pendiente**:
   - Fondo: `bg-gray-100`
   - Texto: `text-gray-600`
   - Label: "Pendiente"

2. **Procesando**:
   - Fondo: `bg-blue-100`
   - Texto: `text-blue-600`
   - Label: "{progress}%"

3. **Completado**:
   - Fondo: `bg-green-100`
   - Texto: `text-green-600`
   - Label: "✓ Listo"

**Estilo común**: `text-xs px-2 py-1 rounded-full`

#### Barra de Progreso General

**Contenedor**:

- Margen: `mt-4 pt-4`
- Borde superior: `border-t border-gray-200`

**Header**: `flex items-center justify-between mb-2`

- Texto izquierda: "Progreso general", `text-sm font-medium text-gray-700`
- Texto derecha: "{X}%", `text-sm font-semibold text-amber-600`

**Barra**:

- Componente Progress
- Altura: `h-2`
- Valor: Porcentaje general (0-100)

---

## Componentes Reutilizables

### FileDropzone

#### Estructura Visual

```
┌─────────────────────────────────────────┐
│                                         │
│         [Icono de Upload]               │
│                                         │
│      {Título personalizable}            │
│      {Descripción}                      │
│      Máximo X archivos                  │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Archivos seleccionados (X)             │
├─────────────────────────────────────────┤
│  [📄] archivo1.pdf         2.5 MB  [×]  │
│  [📄] archivo2.pdf         1.8 MB  [×]  │
└─────────────────────────────────────────┘
```

#### Área de Drop

**Contenedor principal**:

- Borde: `border-2 border-dashed`
- Radio: `rounded-3xl` (24px)
- Padding: `p-12` (48px)
- Alineación: `text-center`
- Cursor: `cursor-pointer`
- Transición: `transition-all duration-300`

**Estados**:

1. **Normal**:
   - Borde: `border-gray-300`
   - Fondo: `bg-white`
   - Hover: `hover:bg-gray-50`

2. **Dragging** (arrastrando archivo encima):
   - Borde: `border-gray-900`
   - Fondo: `bg-gray-50`
   - Escala: `scale-105`

**Animación hover**: `scale: 1.01`

#### Input de Archivo

- Posición: `absolute inset-0`
- Tamaño: `w-full h-full`
- Opacidad: `opacity-0`
- Cursor: `cursor-pointer`

#### Icono de Upload

**Contenedor**:

- Tamaño: `w-16 h-16` (64x64px)
- Fondo: `bg-black`
- Radio: `rounded-2xl` (16px)
- Posición: Centrado con `mx-auto`
- Margen inferior: `mb-4`

**Icono**: Upload, `w-8 h-8 text-white`

**Animación cuando dragging**: `scale: 1.1` con spring

#### Textos

- **Título**: `text-lg font-semibold text-gray-900 mb-2`
- **Descripción**: `text-gray-600 text-sm mb-1`
- **Info máximo**: `text-gray-400 text-xs`

#### Lista de Archivos Seleccionados

**Título de sección**:

- Texto: "Archivos seleccionados ({count})"
- Estilo: `text-sm font-medium text-gray-900`

**Contenedor de lista**: `space-y-2`

**Cada archivo**:

- Layout: `flex items-center gap-3`
- Padding: `p-3`
- Fondo: `bg-gray-50`
- Radio: `rounded-xl`
- Borde: `border border-gray-200`
- Hover: `hover:bg-gray-100`
- Transición: `transition-colors`

**Animación entrada**:

- `initial: opacity: 0, x: -20`
- `animate: opacity: 1, x: 0`
- `exit: opacity: 0, x: 20`
- Delay: `delay: index * 0.05`

**Icono del archivo**:

- Contenedor: `w-10 h-10 bg-black rounded-lg`
- Icono: FileText, `w-5 h-5 text-white`

**Info del archivo**: `flex-1 min-w-0`

- Nombre: `text-sm font-medium text-gray-900 truncate`
- Tamaño: `text-xs text-gray-500`, formato: "X.XX MB"

**Botón eliminar**:

- Tamaño: `w-8 h-8`
- Radio: `rounded-lg`
- Fondo: `bg-gray-200`
- Texto: `text-gray-700`
- Opacidad: `opacity-0 group-hover:opacity-100`
- Hover: `hover:bg-gray-300`
- Icono: X, `w-4 h-4`

### Progress (Barra de Progreso)

**Características**:

- Altura estándar: automática del componente
- Altura pequeña (lotes): `h-1`
- Altura media (general): `h-2`
- Fondo: Gris claro
- Barra activa: Negro/gris oscuro
- Animación: Transición suave

### Button (Botón)

**Variante Primary (default)**:

- Fondo: `bg-black`
- Texto: `text-white`
- Hover: `hover:bg-gray-900`
- Padding: variable según contexto
- Radio: `rounded-lg` o `rounded-xl`

**Variante Outline**:

- Borde: `border border-current`
- Fondo: Transparente
- Hover: Variaciones sutiles

**Estado Disabled**:

- Opacidad: `opacity-50`
- Cursor: `cursor-not-allowed`

### Input / Label

**Input**:

- Fondo: `bg-input-background` (#f3f3f5)
- Borde: Sutil
- Radio: `rounded-lg`
- Padding: `px-3 py-2`
- Transición en focus

**Label**:

- Tamaño: `text-base`
- Peso: `font-medium`
- Color: `text-gray-900`

### Select

**Trigger**:

- Similar a Input
- Indicador de dropdown a la derecha

**Content**:

- Fondo blanco
- Sombra media
- Radio: `rounded-lg`
- Padding interno

**Items**:

- Padding: `px-2 py-1.5`
- Hover: Fondo gris claro
- Selected: Fondo gris más oscuro

### Switch

**Track**:

- Ancho: `w-11`
- Alto: `h-6`
- Radio: `rounded-full`
- Fondo OFF: `bg-switch-background` (#cbced4)
- Fondo ON: `bg-black`

**Thumb**:

- Tamaño: circular, proporcional al track
- Fondo: Blanco
- Transición suave

### Tabs

**TabsList**:

- Fondo: Gris muy claro
- Radio: `rounded-lg`
- Padding: pequeño

**TabsTrigger**:

- Padding: `px-3 py-1.5`
- Radio: `rounded-md`
- Activo: Fondo blanco, sombra sutil
- Inactivo: Transparente

**TabsContent**:

- Padding: `py-4` (arriba)

---

## Animaciones y Transiciones

### Librería

**Motion/React** (anteriormente Framer Motion)

### Patrones de Animación Comunes

#### 1. Fade In desde Arriba

```javascript
initial={{ opacity: 0, y: -20 }}
animate={{ opacity: 1, y: 0 }}
```

**Uso**: Headers de páginas

#### 2. Fade In desde Abajo

```javascript
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
```

**Uso**: Secciones de contenido, cards

#### 3. Fade In desde Izquierda

```javascript
initial={{ opacity: 0, x: -20 }}
animate={{ opacity: 1, x: 0 }}
```

**Uso**: Items de lista, archivos

#### 4. Fade In desde Derecha

```javascript
initial={{ opacity: 0, x: 20 }}
animate={{ opacity: 1, x: 0 }}
```

**Uso**: Cambios de vista

#### 5. Scale In

```javascript
initial={{ opacity: 0, scale: 0.9 }}
animate={{ opacity: 1, scale: 1 }}
```

**Uso**: Cards de éxito, modales

#### 6. Scale Spring (para iconos de éxito)

```javascript
initial={{ scale: 0 }}
animate={{ scale: 1 }}
transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
```

#### 7. Slide Horizontal (cambio de pregunta en Wizard)

```javascript
key={currentQuestion}
initial={{ opacity: 0, x: 20 }}
animate={{ opacity: 1, x: 0 }}
exit={{ opacity: 0, x: -20 }}
transition={{ duration: 0.3 }}
```

#### 8. Height Auto (listas expandibles)

```javascript
initial={{ opacity: 0, height: 0 }}
animate={{ opacity: 1, height: 'auto' }}
exit={{ opacity: 0, height: 0 }}
```

### Animaciones Interactivas (Hover/Tap)

#### Botones Estándar

```javascript
whileHover={{ scale: 1.02 }}
whileTap={{ scale: 0.98 }}
```

#### Iconos dentro de Cards

```javascript
className="... group-hover:scale-110 transition-transform duration-300"
```

#### Flechas Indicadoras

```javascript
className="... group-hover:translate-x-2 transition-transform duration-300"
```

#### Card del Asistente en Dashboard

```javascript
className="... group-hover:translate-x-2 transition-transform duration-300"
// Para el icono ArrowRight
```

### Delays y Stagger

#### Delays Fijos

- Header: sin delay
- Primera sección: `delay: 0.1`
- Segunda sección: `delay: 0.2`
- Tercera sección: `delay: 0.3`

#### Stagger en Listas

```javascript
transition={{ delay: index * 0.05 }}
```

**Uso**: Listas de archivos, opciones del wizard

#### Delays en Grid

```javascript
transition={{ delay: 0.1 + index * 0.05 }}
```

**Uso**: Grid de acciones rápidas en Dashboard

### Duraciones Estándar

- **Extra rápida**: `100ms` - Estados micro
- **Rápida**: `200ms` - Transiciones de color, opacidad
- **Normal**: `300ms` - Transiciones de layout, hover
- **Media**: `400ms` - Animaciones de entrada
- **Lenta**: `600ms` - Transiciones complejas

### AnimatePresence

**Uso**: Envolver elementos que se montan/desmontan condicionalmente

**Mode**:

- `mode="wait"` - Espera a que salga el anterior antes de entrar el nuevo (Wizard)
- Sin mode - Permite animaciones simultáneas (listas)

**Ejemplo**:

```javascript
<AnimatePresence mode="wait">
  {condition && (
    <motion.div
      initial={{ ... }}
      animate={{ ... }}
      exit={{ ... }}
    >
      ...
    </motion.div>
  )}
</AnimatePresence>
```

### Transiciones Específicas

#### Rotación Continua (icono de procesamiento)

```javascript
animate={{ rotate: 360 }}
transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
```

#### Spring Bounce

```javascript
transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
```

**Uso**: Layout ID en selección de tipos de conversión

---

## Notas de Implementación para PySide6

### Colores

Los valores RGB/HEX pueden traducirse directamente a `QColor`.

### Tipografía

- Usar `QFont` con tamaños en puntos (pt)
- Conversión aproximada: 16px = 12pt (factor ~0.75)
- Pesos: Normal=400, Medium=500, SemiBold=600, Bold=700

### Bordes y Radios

- Usar `border-radius` en QSS (Qt Style Sheets)
- Valores en px directamente

### Animaciones

- `QPropertyAnimation` para transiciones
- `QSequentialAnimationGroup` para secuencias
- `QParallelAnimationGroup` para animaciones simultáneas
- Duraciones en milisegundos

### Layout

- `QHBoxLayout` / `QVBoxLayout` para flexbox equivalente
- `QGridLayout` para grids
- `QStackedWidget` para cambios de vista

### Componentes

- `QPushButton` con `setStyleSheet()` para botones personalizados
- `QProgressBar` para barras de progreso
- `QComboBox` para selects
- `QCheckBox` / `QRadioButton` para switches (con estilo personalizado)
- `QLineEdit` para inputs
- `QLabel` para textos estáticos

### Scroll

- `QScrollArea` con `setWidgetResizable(True)`

### Drag & Drop

- Implementar `dragEnterEvent`, `dragLeaveEvent`, `dropEvent`
- Usar `QMimeData` para transferir archivos

---

## Resumen de Iconos Utilizados (lucide-react)

**Principales**:

- FileText - Logo, archivos
- Home - Dashboard
- Wand2 - Asistente
- Combine - Combinar
- Scissors - Dividir
- Archive - Comprimir
- RefreshCw - Convertir
- Shield - Seguridad
- ScanText - OCR
- FolderClock - Lotes

**Secundarios**:

- Upload - Dropzone
- Download - Descargar
- X - Cerrar/eliminar
- ArrowRight - Navegación
- ChevronRight - Siguiente
- Sparkles - Características especiales
- GripVertical - Arrastrar
- Play - Iniciar/procesando
- CheckCircle2 - Completado
- Clock - Pendiente
- Eye/EyeOff - Mostrar/ocultar contraseña
- Lock/Unlock - Encriptar/desencriptar
- Languages - Idiomas
- FileSearch - Búsqueda
- Image - Imágenes
- FileSpreadsheet - Word
- HelpCircle - Ayuda
- Folder - Carpeta

---

## Paleta de Colores Completa por Contexto

### Grises (Base)

- `gray-50`: #f9fafb - Fondos secundarios
- `gray-100`: #f3f4f6 - Elementos inactivos
- `gray-200`: #e5e7eb - Bordes
- `gray-300`: #d1d5db - Bordes dashed
- `gray-400`: #9ca3af - Iconos secundarios
- `gray-500`: #6b7280 - Textos secundarios
- `gray-600`: #4b5563 - Textos terciarios
- `gray-700`: #374151 - Textos en elementos hover
- `gray-800`: #1f2937 - Encabezados secundarios
- `gray-900`: #111827 - Textos principales, fondos activos

### Colores de Acento por Operación

- **Merge**: Sin acento específico, usa negro
- **Split**: Sin acento específico, usa negro
- **Compress**: `emerald`, `green`, `teal` para métricas de ahorro
- **Convert**: `blue`, `indigo`, `purple`, `pink`, `emerald`, `teal`, `orange`, `red` según tipo
- **Security**: `blue` para consejos
- **OCR**: `violet`, `indigo` para info de Tesseract
- **Batch**: `amber` para carpeta vigilada, `blue` para procesando, `green` para completado

---

Esta documentación describe exactamente el aspecto y funcionalidad visual de cada herramienta de LocalPDF v5, lista para ser utilizada como referencia en la implementación con PySide6.