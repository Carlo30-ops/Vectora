# LocalPDF v5 - Especificaciones Visuales Detalladas

## 📐 Guía Completa de Diseño, Transiciones y Animaciones

Esta documentación proporciona especificaciones pixel-perfect de todos los elementos visuales, transiciones fluidas, efectos hover, y posicionamiento exacto de iconos y contenedores.

---

## 📋 Índice

1. [Sistema de Iconos y Contenedores](#sistema-de-iconos-y-contenedores)
2. [Transiciones y Animaciones](#transiciones-y-animaciones)
3. [Estados Interactivos](#estados-interactivos)
4. [Componentes Detallados](#componentes-detallados)
5. [Especificaciones por Vista](#especificaciones-por-vista)
6. [Sistema de Colores y Efectos](#sistema-de-colores-y-efectos)
7. [Implementación en PySide6](#implementación-en-pyside6)

---

## Sistema de Iconos y Contenedores

### 1.1 Tipos de Contenedores de Iconos

LocalPDF v5 utiliza **4 tipos principales** de contenedores para iconos, cada uno con propósitos y estilos específicos:

#### Tipo A: Header de Operaciones (Grande)

**Dimensiones**: 56×56px (`w-14 h-14`)

**Especificaciones visuales**:
```css
Ancho: 56px
Alto: 56px
Background: #000000 (Negro sólido)
Border-radius: 16px (rounded-2xl)
Display: Flex
Align-items: Center
Justify-content: Center
```

**Icono interior**:
```css
Tamaño: 28×28px (w-7 h-7)
Color: #FFFFFF (Blanco)
Alineación: Centro absoluto
```

**Uso**: Headers principales de cada operación (Merge, Split, Compress, etc.)

**Ejemplo visual**:
```
┌──────────────────┐
│                  │  
│   ┌────────┐    │  56px
│   │  🔄   │    │  
│   │ 28px  │    │
│   └────────┘    │
│                  │
└──────────────────┘
     56px
```

**Código React**:
```typescript
<div className="w-14 h-14 bg-black rounded-2xl flex items-center justify-center">
  <RefreshCw className="w-7 h-7 text-white" />
</div>
```

**Transiciones**:
- Ninguna por defecto (elemento estático)
- Puede tener pulse en carga: `animate-pulse`

---

#### Tipo B: Dashboard Card de Asistente (Extra Grande)

**Dimensiones**: 64×64px (`w-16 h-16`)

**Especificaciones visuales**:
```css
Ancho: 64px
Alto: 64px
Background: #FFFFFF (Blanco - invertido del resto)
Border-radius: 16px (rounded-2xl)
Display: Flex
Align-items: Center
Justify-content: Center
Shadow: none (el contenedor padre tiene sombra)
```

**Icono interior**:
```css
Tamaño: 32×32px (w-8 h-8)
Color: #000000 (Negro - invertido)
Alineación: Centro absoluto
```

**Contexto**: Card principal del Asistente en Dashboard (fondo negro)

**Ejemplo visual**:
```
┌─────────────────────────┐
│  [FONDO NEGRO]          │
│                         │
│  ┌────────────┐         │
│  │  [BLANCO]  │  64px   │
│  │            │         │
│  │    🪄 32px │         │
│  │            │         │
│  └────────────┘         │
│      64px               │
└─────────────────────────┘
```

**Código React**:
```typescript
<div className="mb-8 bg-black rounded-3xl p-8">
  <div className="w-16 h-16 bg-white rounded-2xl flex items-center justify-center">
    <Wand2 className="w-8 h-8 text-black" />
  </div>
</div>
```

---

#### Tipo C: Cards de Acciones Rápidas (Mediano)

**Dimensiones**: 48×48px (`w-12 h-12`)

**Especificaciones visuales**:
```css
Ancho: 48px
Alto: 48px
Background: #000000 (Negro sólido)
Border-radius: 12px (rounded-xl)
Display: Flex
Align-items: Center
Justify-content: Center
Margin-bottom: 16px (mb-4)
```

**Icono interior**:
```css
Tamaño: 24×24px (w-6 h-6)
Color: #FFFFFF (Blanco)
Alineación: Centro absoluto
```

**Transiciones en hover del contenedor padre**:
```css
Transform: scale(1.10)
Duration: 300ms
Timing-function: ease-in-out
```

**Ejemplo visual**:
```
Card Normal                Card Hover
┌──────────┐              ┌──────────┐
│          │              │          │
│  ┌────┐  │              │  ┌────┐  │ ← Scale 1.1
│  │ 🔗 │  │  ──Hover──>  │  │ 🔗 │  │
│  └────┘  │              │  └────┘  │
│   48px   │              │   53px   │
└──────────┘              └──────────┘
```

**Código React**:
```typescript
<div className="group cursor-pointer">
  <div className="bg-gray-50 hover:bg-gray-100 rounded-2xl p-6">
    <div className="w-12 h-12 bg-black rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
      <Icon className="w-6 h-6 text-white" />
    </div>
  </div>
</div>
```

**Desglose de la transición**:
1. **Estado inicial**: `scale(1)` - Tamaño normal 48×48px
2. **Hover en card padre**: Activa `group-hover:scale-110`
3. **Estado final**: `scale(1.1)` - Tamaño 52.8×52.8px (aprox 53px)
4. **Duración**: 300ms
5. **Easing**: ease-in-out (suave entrada y salida)

---

#### Tipo D: Opciones del Wizard (Mediano Interactivo)

**Dimensiones**: 48×48px (`w-12 h-12`)

**Especificaciones visuales**:
```css
Ancho: 48px
Alto: 48px
Background: #000000 (Negro sólido)
Border-radius: 12px (rounded-xl)
Display: Flex
Align-items: Center
Justify-content: Center
Flex-shrink: 0
```

**Icono interior**:
```css
Tamaño: 24×24px (w-6 h-6)
Color: #FFFFFF (Blanco)
Alineación: Centro absoluto
```

**Transiciones múltiples**:

1. **Hover del contenedor padre (botón)**:
   ```css
   Transform: scale(1.02)
   Duration: 200ms (implícito en transition-all)
   ```

2. **Hover del icono mismo**:
   ```css
   Transform: scale(1.10)
   Duration: 200ms
   ```

3. **Click (whileTap)**:
   ```css
   Transform: scale(0.98)
   Duration: 100ms
   ```

**Ejemplo visual completo**:
```
Estado Normal
┌─────────────────────────────────────┐
│  ┌────┐                             │
│  │ 🔗 │  Combinar varios archivos → │
│  └────┘                             │
└─────────────────────────────────────┘

Estado Hover
┌─────────────────────────────────────┐
│  ┌────┐                             │ ← Botón scale 1.02
│  │ 🔗 │  Combinar varios archivos → │ ← Flecha translate-x
│  └────┘                             │ ← Icono scale 1.10
│   ↑                                 │
│  53px                               │
└─────────────────────────────────────┘

Estado Click (Tap)
┌─────────────────────────────────────┐
│  ┌──┐                               │ ← Botón scale 0.98
│  │🔗│  Combinar varios archivos →   │
│  └──┘                               │
│  47px                               │
└─────────────────────────────────────┘
```

**Código React**:
```typescript
<motion.button
  className="group relative p-6 bg-white hover:bg-gray-50 rounded-2xl border border-gray-200 hover:border-gray-900 transition-all"
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
>
  <div className="flex items-start gap-4">
    <div className="w-12 h-12 bg-black rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
      <Icon className="w-6 h-6 text-white" />
    </div>
    <div className="flex-1">
      <p className="font-medium text-gray-800 group-hover:text-indigo-900">
        {option.text}
      </p>
    </div>
    <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-indigo-500 group-hover:translate-x-1 transition-all" />
  </div>
</motion.button>
```

---

#### Tipo E: Sidebar Logo (Mediano)

**Dimensiones**: 40×40px (`w-10 h-10`)

**Especificaciones visuales**:
```css
Ancho: 40px
Alto: 40px
Background: #000000 (Negro sólido)
Border-radius: 16px (rounded-2xl)
Display: Flex
Align-items: Center
Justify-content: Center
```

**Icono interior**:
```css
Tamaño: 24×24px (w-6 h-6)
Color: #FFFFFF (Blanco)
Alineación: Centro absoluto
```

**Uso**: Logo en header del Sidebar

```
┌─────────────────────────┐
│  ┌────┐  LocalPDF       │
│  │ 📄 │  v5.0           │
│  └────┘                 │
│  40x40                  │
└─────────────────────────┘
```

---

#### Tipo F: FileDropzone (Grande Animado)

**Dimensiones**: 64×64px (`w-16 h-16`)

**Especificaciones visuales**:
```css
Ancho: 64px
Alto: 64px
Background: #000000 (Negro sólido)
Border-radius: 16px (rounded-2xl)
Display: Flex
Align-items: Center
Justify-content: Center
Margin: 0 auto 16px (mx-auto mb-4)
```

**Icono interior**:
```css
Tamaño: 32×32px (w-8 h-8)
Color: #FFFFFF (Blanco)
Alineación: Centro absoluto
```

**Animaciones especiales**:

1. **En estado de arrastre (isDragging)**:
   ```typescript
   <motion.div
     animate={isDragging ? { scale: 1.1 } : { scale: 1 }}
     transition={{ type: 'spring', stiffness: 300, damping: 20 }}
   >
   ```
   - Transform: scale(1.1) - Se agranda 10%
   - Type: Spring animation (rebote)
   - Stiffness: 300 (rigidez alta = respuesta rápida)
   - Damping: 20 (amortiguación = rebote controlado)

2. **Contenedor exterior en arrastre**:
   ```css
   Transform: scale(1.05)
   Border-color: #111827 (gray-900)
   Background: #F9FAFB (gray-50)
   ```

**Ejemplo visual de animación**:
```
Estado Normal              Estado Dragging
┌──────────────┐          ┌──────────────┐
│              │          │              │
│   ┌──────┐  │          │   ┌──────┐  │
│   │  📤  │  │          │   │  📤  │  │ ← Scale 1.1
│   │ 64px │  │  ─Drag─→ │   │ 70px │  │ ← Spring bounce
│   └──────┘  │          │   └──────┘  │
│              │          │              │
└──────────────┘          └──────────────┘
  Border: gray-300          Border: gray-900
  BG: white                 BG: gray-50
                            Scale outer: 1.05
```

**Código React completo**:
```typescript
<motion.div
  onDragEnter={handleDragEnter}
  onDragOver={handleDragOver}
  onDragLeave={handleDragLeave}
  onDrop={handleDrop}
  className={`
    relative border-2 border-dashed rounded-3xl p-12 text-center cursor-pointer
    transition-all duration-300
    ${isDragging 
      ? 'border-gray-900 bg-gray-50 scale-105' 
      : 'border-gray-300 bg-white hover:bg-gray-50'
    }
  `}
  whileHover={{ scale: 1.01 }}
>
  <motion.div
    animate={isDragging ? { scale: 1.1 } : { scale: 1 }}
    transition={{ type: 'spring', stiffness: 300, damping: 20 }}
  >
    <div className="w-16 h-16 bg-black rounded-2xl flex items-center justify-center mx-auto mb-4">
      <Upload className="w-8 h-8 text-white" />
    </div>
  </motion.div>
</motion.div>
```

---

#### Tipo G: Iconos de Lista de Archivos (Pequeño)

**Dimensiones**: 40×40px (`w-10 h-10`)

**Especificaciones visuales**:
```css
Ancho: 40px
Alto: 40px
Background: #000000 (Negro sólido)
Border-radius: 8px (rounded-lg)
Display: Flex
Align-items: Center
Justify-content: Center
Flex-shrink: 0
```

**Icono interior**:
```css
Tamaño: 20×20px (w-5 h-5)
Color: #FFFFFF (Blanco)
Alineación: Centro absoluto
```

**Uso**: Items en listas de archivos seleccionados

```
┌─────────────────────────────────────┐
│  ┌────┐  documento.pdf      2.5 MB │
│  │ 📄 │                          ✕  │
│  └────┘                             │
│  40x40                              │
└─────────────────────────────────────┘
```

---

#### Tipo H: Resultado Final - Check Circle (Extra Grande)

**Dimensiones**: 80×80px (`w-20 h-20`)

**Especificaciones visuales**:
```css
Ancho: 80px
Alto: 80px
Background: #FFFFFF (Blanco)
Border-radius: 50% (rounded-full - círculo perfecto)
Display: Flex
Align-items: Center
Justify-content: Center
Margin: 0 auto 16px (mx-auto mb-4)
Box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1) (shadow-xl)
```

**Icono interior**:
```css
Tamaño: 40×40px (w-10 h-10)
Color: #000000 (Negro)
Alineación: Centro absoluto
```

**Animación especial - Spring Pop**:
```typescript
<motion.div
  initial={{ scale: 0 }}
  animate={{ scale: 1 }}
  transition={{ 
    delay: 0.2,           // Espera 200ms
    type: 'spring',       // Animación tipo resorte
    stiffness: 200        // Rebote moderado
  }}
>
```

**Ejemplo visual de animación**:
```
Frame 0ms (Initial)    Frame 200ms (Delay)   Frame 400ms (Peak)    Frame 600ms (Final)
        •                    ○                    ◉                     ●
     scale: 0             scale: 0            scale: 1.2             scale: 1
                                              (overshoot)           (settled)
                                                  ↑
                                            Spring bounce
```

**Código React**:
```typescript
<div className="bg-gray-900 rounded-2xl p-8">
  <div className="text-center mb-6">
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
      className="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-4 shadow-xl"
    >
      <CheckCircle2 className="w-10 h-10 text-black" />
    </motion.div>
  </div>
</div>
```

---

#### Tipo I: Breadcrumb Steps (Pequeño Circular)

**Dimensiones**: 24×24px (`w-6 h-6`)

**Especificaciones visuales**:
```css
Ancho: 24px
Alto: 24px
Background: #FFFFFF (Blanco)
Border-radius: 50% (rounded-full)
Display: Flex
Align-items: Center
Justify-content: Center
Flex-shrink: 0
```

**Texto interior**:
```css
Font-size: 12px (text-xs)
Font-weight: 700 (font-bold)
Color: #000000 (Negro)
Line-height: 1
```

**Contexto**: Pantalla de resultado del Wizard

```
Tu selección:
┌──────────────────────────────────┐
│  ① Reducir el tamaño del archivo │
│  ② Convertir a otro formato      │
│  ③ PDF a Word                    │
└──────────────────────────────────┘
   24px círculos
```

**Código React**:
```typescript
<div className="w-6 h-6 bg-white rounded-full flex items-center justify-center flex-shrink-0">
  <span className="text-black text-xs font-bold">{index + 1}</span>
</div>
```

---

### 1.2 Tabla Resumen de Contenedores de Iconos

| Tipo | Tamaño Box | Radio | Icono | Uso | Hover Effect |
|------|-----------|-------|-------|-----|--------------|
| **A - Header** | 56×56px | 16px | 28×28px | Headers de operaciones | Ninguno |
| **B - Asistente** | 64×64px | 16px | 32×32px | Card Dashboard Wizard | Ninguno (contenedor padre) |
| **C - Quick Actions** | 48×48px | 12px | 24×24px | Cards Dashboard | Scale 1.10 (300ms) |
| **D - Wizard Options** | 48×48px | 12px | 24×24px | Opciones Wizard | Scale 1.10 (200ms) |
| **E - Sidebar Logo** | 40×40px | 16px | 24×24px | Logo Sidebar | Ninguno |
| **F - Dropzone** | 64×64px | 16px | 32×32px | FileDropzone | Spring scale 1.1 |
| **G - File List** | 40×40px | 8px | 20×20px | Lista archivos | Ninguno |
| **H - Check Result** | 80×80px | 50% | 40×40px | Resultado final | Spring pop desde 0 |
| **I - Breadcrumb** | 24×24px | 50% | 12px texto | Pasos Wizard | Stagger fade in |

---

## Transiciones y Animaciones

### 2.1 Animaciones de Entrada (Mount Animations)

#### Header de Página

**Aplicado a**: Todos los headers de operaciones y vistas

```typescript
<motion.div
  initial={{ opacity: 0, y: -20 }}
  animate={{ opacity: 1, y: 0 }}
  className="mb-8"
>
```

**Especificaciones técnicas**:
```
Propiedad: opacity, y (vertical position)
Inicial: 
  - opacity: 0 (invisible)
  - y: -20px (20px arriba de posición final)
Final:
  - opacity: 1 (completamente visible)
  - y: 0 (posición normal)
Duración: 300ms (default de Motion)
Easing: ease-out (default)
```

**Timeline visual**:
```
Frame 0ms:           Frame 100ms:        Frame 200ms:        Frame 300ms:
                                                             
    ↑ -20px             ↑ -13px             ↑ -5px              ↓ 0px
   (...)               (...)               (Título)           [Título]
  opacity: 0        opacity: 0.3        opacity: 0.7       opacity: 1
```

---

#### Stagger Animation - Cards

**Aplicado a**: Quick Actions en Dashboard, opciones en Wizard

```typescript
{quickActions.map((action, index) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: 0.1 + index * 0.05 }}
  >
))}
```

**Especificaciones técnicas**:
```
Propiedad: opacity, y
Inicial:
  - opacity: 0
  - y: 20px (20px abajo de posición final)
Final:
  - opacity: 1
  - y: 0
Delay: Incremental
  - Card 1: 100ms
  - Card 2: 150ms
  - Card 3: 200ms
  - Card 4: 250ms
  - Card 5: 300ms
  - Card 6: 350ms
Duración: 300ms cada una
```

**Timeline visual para 6 cards**:
```
Time →   0ms    100ms   150ms   200ms   250ms   300ms   350ms   400ms   450ms   650ms

Card 1:  [····] [████████████████████████████████████████████]
Card 2:         [····] [██████████████████████████████████████]
Card 3:                [····] [████████████████████████████████]
Card 4:                       [····] [██████████████████████████]
Card 5:                              [····] [████████████████████]
Card 6:                                     [····] [██████████████]

Efecto resultante: Cascada suave de aparición
```

---

#### Slide Lateral - Wizard Questions

**Aplicado a**: Cambio entre preguntas en Wizard

```typescript
<AnimatePresence mode="wait">
  <motion.div
    key={currentQuestion}
    initial={{ opacity: 0, x: 20 }}
    animate={{ opacity: 1, x: 0 }}
    exit={{ opacity: 0, x: -20 }}
    transition={{ duration: 0.3 }}
  >
```

**Especificaciones técnicas**:
```
Mode: wait (espera a que salga el anterior antes de entrar el nuevo)

Entrada:
  - initial: opacity: 0, x: 20px (derecha)
  - animate: opacity: 1, x: 0

Salida:
  - exit: opacity: 0, x: -20px (izquierda)

Duración: 300ms
```

**Timeline visual de transición**:
```
Pregunta A (saliendo)              Pregunta B (entrando)

Frame 0ms:
[Pregunta A completa]              [invisible, x: +20px]
   x: 0, opacity: 1                   x: 20, opacity: 0

Frame 150ms:
[Pregunta A parcial]               [invisible, x: +20px]
   x: -10, opacity: 0.5               x: 20, opacity: 0

Frame 300ms:
[invisible, x: -20px]              [invisible, x: +10px]
   x: -20, opacity: 0                 x: 10, opacity: 0.5

Frame 450ms:
[fuera de vista]                   [Pregunta B parcial]
                                      x: 5, opacity: 0.75

Frame 600ms:
[fuera de vista]                   [Pregunta B completa]
                                      x: 0, opacity: 1
```

---

### 2.2 Animaciones de Hover

#### Scale Animation - Buttons y Cards

**Tipo 1: Scale Ligero (Botones Wizard)**

```typescript
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
>
```

**Especificaciones**:
```
Hover:
  - Transform: scale(1.02)
  - Equivalente a: 102% del tamaño original
  - Duración: ~150ms (implícito)
  - Easing: ease-out

Tap (click):
  - Transform: scale(0.98)
  - Equivalente a: 98% del tamaño original
  - Duración: ~100ms
  - Easing: ease-in
```

**Ejemplo visual con botón de 300×80px**:
```
Normal               Hover                Tap
┌────────────┐      ┌─────────────┐      ┌───────────┐
│            │      │             │      │           │
│   Botón    │  →   │    Botón    │  →   │   Botón   │
│            │      │             │      │           │
└────────────┘      └─────────────┘      └───────────┘
  300×80px           306×81.6px           294×78.4px
  scale: 1           scale: 1.02          scale: 0.98
```

---

**Tipo 2: Scale Icono (Dashboard Cards)**

```css
.group-hover:scale-110
transition-transform duration-300
```

**Especificaciones**:
```
Selector: group-hover (activa cuando el padre tiene hover)
Transform: scale(1.10)
Equivalente: 110% del tamaño original
Duración: 300ms
Property: transform únicamente
Easing: ease-in-out (default)
```

**Ejemplo con icono 48×48px**:
```
Card Normal                Card Hover
┌──────────────┐          ┌──────────────┐
│              │          │              │
│   ┌────┐    │          │   ┌────┐    │
│   │ 🔗 │    │   Hover  │   │ 🔗 │    │ ← Icono: 53×53px
│   └────┘    │    →     │   └────┘    │
│   48×48     │          │   53×53     │
│              │          │              │
└──────────────┘          └──────────────┘

Timeline del scale:
0ms ───────── 300ms
[48px] → [53px]
  ████████████
```

---

#### Translate Animation - Flechas de Navegación

**Aplicado a**: Flechas `→` en cards del Dashboard y Wizard

```css
.group-hover:translate-x-1
transition-all
```

**Especificaciones**:
```
Property: transform: translateX()
Normal: translateX(0)
Hover: translateX(4px) (translate-x-1 = 0.25rem = 4px)
Duración: 200ms (transition-all)
Easing: ease-in-out
```

**Ejemplo visual**:
```
Normal:  Combinar archivos     →
Hover:   Combinar archivos      →
                              ↑
                         +4px derecha
```

**Timeline**:
```
0ms: translateX(0px)
50ms: translateX(1px)
100ms: translateX(2px)
150ms: translateX(3px)
200ms: translateX(4px) ✓
```

---

#### Color Transitions

**Tipo 1: Background Color**

```css
hover:bg-gray-100
transition-all duration-300
```

**Especificaciones**:
```
Property: background-color
Normal: #F9FAFB (gray-50)
Hover: #F3F4F6 (gray-100)
Duración: 300ms
Easing: ease-in-out
```

---

**Tipo 2: Border Color**

```css
border-gray-200
hover:border-gray-900
transition-all
```

**Especificaciones**:
```
Property: border-color
Normal: #E5E7EB (gray-200) - Borde sutil
Hover: #111827 (gray-900) - Borde oscuro
Duración: 200ms (default transition-all)
Easing: ease-in-out
```

**Ejemplo visual de borde**:
```
Normal                       Hover
┌─────────────────┐         ┏━━━━━━━━━━━━━━━┓
│ Opción A        │    →    ┃ Opción A      ┃
└─────────────────┘         ┗━━━━━━━━━━━━━━━┛
  gray-200 (sutil)            gray-900 (fuerte)
  1px                         2px (visual)
```

---

**Tipo 3: Text Color**

```css
text-gray-800
group-hover:text-indigo-900
```

**Especificaciones**:
```
Property: color
Normal: #1F2937 (gray-800)
Hover: #312E81 (indigo-900)
Duración: ~150ms (implícito en transition)
```

---

### 2.3 Animaciones Especiales

#### Spring Animation - Check Circle

```typescript
<motion.div
  initial={{ scale: 0 }}
  animate={{ scale: 1 }}
  transition={{ 
    delay: 0.2,
    type: 'spring',
    stiffness: 200
  }}
>
```

**Parámetros de Spring**:
```
Type: spring (física de resorte)
Stiffness: 200
  - Valores típicos: 100 (suave) - 400 (rígido)
  - 200 = Rebote moderado, natural
Damping: 10 (default)
  - Controla la amortiguación del rebote
Delay: 200ms
  - Espera antes de iniciar
```

**Curva de animación visual**:
```
Scale
 1.2│        ╱╲
    │       ╱  ╲___
 1.0│  ____╱       ╲______ (final)
    │ ╱
 0.5│╱
    │
 0.0│─────┬─────┬─────┬─────┬─────→ Time
     0   200ms 400ms 600ms 800ms

Fases:
1. Delay (0-200ms): scale = 0
2. Expansion rápida (200-400ms): scale 0→1.15 (overshoot)
3. Rebote (400-600ms): scale 1.15→0.95 (undershoot)
4. Estabilización (600-800ms): scale 0.95→1.0
```

---

#### Backdrop Blur - Breadcrumb

```css
bg-white/60 backdrop-blur-xl
```

**Especificaciones**:
```
Background: rgba(255, 255, 255, 0.6)
  - Blanco al 60% de opacidad
Backdrop-filter: blur(24px)
  - Desenfoque del contenido detrás
```

**Ejemplo visual**:
```
Sin backdrop-blur                Con backdrop-blur
┌─────────────────┐             ┌─────────────────┐
│ Fondo nítido    │             │ Fondo borroso   │
│ ▓▓▓▓▓▓▓▓▓▓▓▓   │             │ ░░░░░░░░░░░░   │
│                 │             │                 │
│ [Breadcrumb]    │             │ [Breadcrumb]    │
└─────────────────┘             └─────────────────┘
  Texto difícil                   Texto legible
  de leer                         contraste mejorado
```

---

#### Glassmorphism - Processing Card

```css
bg-white/60 backdrop-blur-xl rounded-2xl border border-white/50
```

**Especificaciones completas**:
```
Background: rgba(255, 255, 255, 0.6)
Backdrop-filter: blur(24px)
Border: 1px solid rgba(255, 255, 255, 0.5)
Border-radius: 16px
Box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07) (opcional)
```

**Stack visual**:
```
    Capa 5: Contenido (texto, progreso)
         ↓
    Capa 4: Border rgba(255,255,255,0.5)
         ↓
    Capa 3: Background rgba(255,255,255,0.6)
         ↓
    Capa 2: Backdrop-blur (24px)
         ↓
    Capa 1: Fondo de la página (blurred)
```

---

#### Layout Animation - Shared Layout

**Aplicado a**: Selección de tipo de conversión en ConvertPDF

```typescript
{isSelected && (
  <motion.div
    layoutId="selectedConversion"
    className="absolute inset-0 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl"
    transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
  />
)}
```

**Especificaciones**:
```
LayoutId: "selectedConversion"
  - Permite transición suave entre elementos
Position: absolute
Inset: 0 (cubre todo el padre)
Background: Gradiente
  - from-blue-50: #EFF6FF
  - to-indigo-50: #EEF2FF
Transition:
  - Type: spring
  - Bounce: 0.2 (rebote reducido)
  - Duration: 600ms
```

**Ejemplo visual de transición**:
```
Card A seleccionado          Usuario click Card B          Card B seleccionado

┌─────────────┐             ┌─────────────┐             ┌─────────────┐
│ [GRADIENTE] │             │             │             │             │
│             │             │  ╭─────╮    │             │ [GRADIENTE] │
│  PDF→Word   │    Click    │  │ ↘   │    │    Spring   │             │
│             │      →      │  ╰─────╯    │      →      │  Word→PDF   │
└─────────────┘             │      ↘      │             └─────────────┘
                            │       ↘     │
                            └─────────╲───┘
                                      Animación de movimiento
```

**Timeline**:
```
0ms:     Gradiente en Card A
100ms:   Gradiente comienza a moverse
300ms:   Gradiente a mitad de camino (con bounce)
600ms:   Gradiente llega a Card B
```

---

### 2.4 Animaciones de Lista (AnimatePresence)

#### File List Stagger

```typescript
{selectedFiles.map((file, index) => (
  <motion.div
    initial={{ opacity: 0, x: -20 }}
    animate={{ opacity: 1, x: 0 }}
    exit={{ opacity: 0, x: 20 }}
    transition={{ delay: index * 0.05 }}
  >
))}
```

**Especificaciones**:
```
Entrada (cada item):
  - Initial: opacity 0, translateX(-20px)
  - Animate: opacity 1, translateX(0)
  - Delay: 0ms, 50ms, 100ms, 150ms... (incremental)

Salida (cuando se elimina):
  - Exit: opacity 0, translateX(20px)
  - Duración: default 300ms
```

**Timeline para 4 archivos entrando**:
```
File 1:  ←[████████] (0ms delay)
File 2:     ←[████████] (50ms delay)
File 3:        ←[████████] (100ms delay)
File 4:           ←[████████] (150ms delay)

Total duración: 450ms (150ms delay + 300ms animación)
```

**Timeline para eliminación de File 2**:
```
Antes:                      Después (animado):
File 1 ████████            File 1 ████████
File 2 ████████            File 2 ────────→ [fade out + slide right]
File 3 ████████            File 3 ↑ [slide up] ████████
File 4 ████████            File 4 ↑ [slide up] ████████
```

---

#### Breadcrumb Fade In/Out

```typescript
<AnimatePresence>
  {selectedPath.length > 0 && !isComplete && (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
    >
```

**Especificaciones**:
```
Entrada:
  - Initial: opacity 0, y: -10px (arriba)
  - Animate: opacity 1, y: 0
  - Duración: 300ms

Salida:
  - Exit: opacity 0, y: -10px (arriba)
  - Duración: 300ms
```

---

## Estados Interactivos

### 3.1 Estados de Botones

#### Botón Primary (Negro)

```css
bg-black hover:bg-gray-900 text-white
disabled:opacity-50 disabled:cursor-not-allowed
```

**Estados**:

1. **Normal**:
   ```
   Background: #000000
   Color: #FFFFFF
   Cursor: pointer
   Opacity: 1
   ```

2. **Hover**:
   ```
   Background: #111827 (gray-900)
   Color: #FFFFFF
   Cursor: pointer
   Opacity: 1
   Transition: 150ms
   ```

3. **Active (click)**:
   ```
   Background: #1F2937 (gray-800 - más claro)
   Color: #FFFFFF
   Transform: scale(0.98) (si tiene whileTap)
   ```

4. **Disabled**:
   ```
   Background: #000000
   Color: #FFFFFF
   Cursor: not-allowed
   Opacity: 0.5
   Pointer-events: none
   ```

**Ejemplo visual**:
```
Normal        Hover         Active        Disabled
┌─────────┐  ┌─────────┐  ┌────────┐   ┌─────────┐
│ Procesar│  │ Procesar│  │Procesar│   │ Procesar│
└─────────┘  └─────────┘  └────────┘   └─────────┘
  #000000      #111827     #1F2937      #00000080
  100%         100%        scale 0.98    50% opacity
```

---

#### Botón Outline

```css
variant="outline"
border-white text-white hover:bg-white/10
```

**Estados**:

1. **Normal**:
   ```
   Background: transparent
   Border: 1px solid #FFFFFF
   Color: #FFFFFF
   ```

2. **Hover**:
   ```
   Background: rgba(255, 255, 255, 0.1)
   Border: 1px solid #FFFFFF
   Color: #FFFFFF
   ```

---

### 3.2 Estados de Cards

#### Dashboard Quick Action Card

**Estados**:

1. **Normal**:
   ```
   Background: #F9FAFB (gray-50)
   Border: 1px solid #E5E7EB (gray-200)
   Shadow: none
   Icon scale: 1
   ```

2. **Hover**:
   ```
   Background: #F3F4F6 (gray-100)
   Border: 1px solid #E5E7EB
   Shadow: none
   Icon scale: 1.1
   Cursor: pointer
   Transition: all 300ms ease-in-out
   ```

3. **Active (durante click)**:
   ```
   Background: #E5E7EB (gray-200)
   Icon scale: 1.05
   ```

---

#### Wizard Option Button

**Estados**:

1. **Normal**:
   ```
   Background: #FFFFFF (white)
   Border: 1px solid #E5E7EB (gray-200)
   Text: #1F2937 (gray-800)
   Icon container scale: 1
   Arrow color: #9CA3AF (gray-400)
   ```

2. **Hover**:
   ```
   Background: #F9FAFB (gray-50)
   Border: 1px solid #111827 (gray-900) ← Cambio principal
   Text: #312E81 (indigo-900)
   Icon container scale: 1.1
   Arrow color: #6366F1 (indigo-500)
   Arrow translateX: 4px
   Shadow: 0 4px 6px rgba(0,0,0,0.1)
   Card scale: 1.02
   ```

3. **Active (whileTap)**:
   ```
   Card scale: 0.98
   ```

**Comparación visual**:
```
NORMAL                           HOVER
┌────────────────────────┐      ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
│  ┌────┐                │      ┃  ┌────┐                ┃
│  │ 🔗 │  Combinar  →   │  →   ┃  │ 🔗 │  Combinar   →  ┃
│  └────┘                │      ┃  └────┘              ↗ ┃
│  gray-200              │      ┃  gray-900  +4px scale ┃
└────────────────────────┘      ┗━━━━━━━━━━━━━━━━━━━━━━━━┛
  Borde sutil                     Borde fuerte + sombra
  Icono 48px                      Icono 53px
  Flecha normal                   Flecha indigo + movida
```

---

### 3.3 Estados de FileDropzone

**Estados**:

1. **Normal**:
   ```
   Background: #FFFFFF (white)
   Border: 2px dashed #D1D5DB (gray-300)
   Border-radius: 24px (rounded-3xl)
   Icon scale: 1
   Container scale: 1
   ```

2. **Hover** (sin arrastrar):
   ```
   Background: #F9FAFB (gray-50)
   Border: 2px dashed #D1D5DB
   Container scale: 1.01
   ```

3. **Dragging** (isDragging = true):
   ```
   Background: #F9FAFB (gray-50)
   Border: 2px dashed #111827 (gray-900) ← Cambio principal
   Container scale: 1.05
   Icon scale: 1.1 (con spring animation)
   ```

**Comparación visual**:
```
NORMAL                    HOVER                     DRAGGING
┌──────────────┐         ┌──────────────┐         ┏━━━━━━━━━━━━━━┓
│              │         │              │         ┃              ┃
│   ┌──────┐  │         │   ┌──────┐  │         ┃   ┌──────┐  ┃
│   │  📤  │  │    →    │   │  📤  │  │    →    ┃   │  📤  │  ┃
│   │ 64px │  │         │   │ 64px │  │         ┃   │ 70px │  ┃
│   └──────┘  │         │   └──────┘  │         ┃   └──────┘  ┃
│              │         │              │         ┃              ┃
└──────────────┘         └──────────────┘         ┗━━━━━━━━━━━━━━┛
  white                   gray-50                  gray-50
  border gray-300         border gray-300          border gray-900
  scale: 1                scale: 1.01              scale: 1.05
  icon: 64px              icon: 64px               icon: 70px (spring)
```

---

### 3.4 Estados de Conversion Type Cards

**Estados**:

1. **No seleccionado**:
   ```
   Background: #F9FAFB (gray-50)
   Border: 1px solid #E5E7EB (gray-200)
   Icon background: #000000 (black)
   Icon color: #FFFFFF (white)
   Text: #111827 (gray-900)
   Description: #6B7280 (gray-600)
   ```

2. **No seleccionado + Hover**:
   ```
   Background: #F3F4F6 (gray-100)
   Scale: 1.02
   ```

3. **Seleccionado**:
   ```
   Background: Gradiente (varía según tipo)
     - PDF→Word: from-blue-50 to-indigo-50
     - Word→PDF: from-purple-50 to-pink-50
     - PDF→Images: from-emerald-50 to-teal-50
     - Images→PDF: from-orange-50 to-red-50
   Border: 2px solid #111827 (gray-900)
   Icon background: #FFFFFF (white) ← Invertido
   Icon color: #000000 (black) ← Invertido
   Text: #FFFFFF (white)
   Description: #D1D5DB (gray-300)
   Shadow: 0 4px 6px rgba(0,0,0,0.1)
   ```

4. **Transición de selección** (Layout animation):
   ```
   Gradiente se mueve de card anterior a nueva
   Duración: 600ms
   Spring bounce: 0.2
   ```

**Comparación visual**:
```
NO SELECCIONADO             SELECCIONADO
┌──────────────────┐       ┏━━━━━━━━━━━━━━━━━━┓
│  ┌────┐          │       ┃  ┌────┐          ┃
│  │📄 │ PDF→Word │       ┃  │📄 │ PDF→Word ┃
│  │BLK│          │       ┃  │WHT│          ┃
│  └────┘          │       ┃  └────┘          ┃
│  gray-50         │       ┃  [GRADIENTE]     ┃
│  border gray-200 │       ┃  border gray-900 ┃
└──────────────────┘       ┗━━━━━━━━━━━━━━━━━━┛
  Icono: negro fondo         Icono: blanco fondo
  Texto: gris                Texto: blanco
```

---

## Componentes Detallados

### 4.1 Sidebar

#### Dimensiones Exactas

```
┌─────────────────────────────┐
│  Padding: 24px              │
│  ┌───────────────────────┐  │
│  │ Logo Container        │  │ ← 40×40px
│  │ LocalPDF v5.0         │  │
│  └───────────────────────┘  │
│  Border-bottom: 1px gray-200│
├─────────────────────────────┤
│  Padding: 16px              │
│  ┌───────────────────────┐  │
│  │ ● Dashboard           │  │ ← 56px alto cada uno
│  │ ● Asistente [Nuevo]   │  │
│  │ ● Combinar            │  │
│  │ ...                   │  │
│  └───────────────────────┘  │
│  Space-y: 4px entre items   │
│                             │
│  (Scroll si necesario)      │
│                             │
├─────────────────────────────┤
│  Padding: 16px              │
│  ┌───────────────────────┐  │
│  │ 🌐 100% Offline       │  │ ← 72px alto
│  │ Sin conexión requerida│  │
│  └───────────────────────┘  │
└─────────────────────────────┘
      256px total width
```

#### Menu Item - Especificaciones Pixel-Perfect

```
ITEM NORMAL (No activo, no hover)
┌─────────────────────────────────────┐
│  [16px padding]                     │
│  ┌────────────────────────────────┐ │
│  │ 📄 Dashboard                   │ │ ← 48px alto
│  │ ↑  ↑                           │ │
│  │ 20px gap:12px                  │ │
│  └────────────────────────────────┘ │
│  [16px padding]                     │
└─────────────────────────────────────┘

Padding horizontal: 16px (px-4)
Padding vertical: 12px (py-3)
Gap entre icono y texto: 12px (gap-3)
Border-radius: 12px (rounded-xl)
Background: transparent
```

```
ITEM HOVER
┌─────────────────────────────────────┐
│  ┌────────────────────────────────┐ │
│  │ 📄 Dashboard                   │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘

Background: #F3F4F6 (gray-100)
Scale: 1.02
Duración: 200ms
```

```
ITEM ACTIVO
┌─────────────────────────────────────┐
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│  ┃ 📄 Dashboard                  ┃ │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │
└─────────────────────────────────────┘

Background: #111827 (gray-900)
Text color: #FFFFFF (white)
Icon color: #FFFFFF (white)
```

#### Badge "Nuevo"

```
Posición: ml-auto (extremo derecho)
Padding: 2px 8px (px-2 py-0.5)
Font-size: 12px (text-xs)
Font-weight: 600 (font-semibold)
Background: #000000 (black)
Color: #FFFFFF (white)
Border-radius: 9999px (rounded-full)
```

**Visual**:
```
┌────────────────────────────────────┐
│ 🪄 Asistente              [Nuevo] │
│    ↑                         ↑    │
│  icon                     badge   │
└────────────────────────────────────┘
```

---

### 4.2 Dashboard

#### Wizard Card (Destacado)

**Dimensiones completas**:
```
┌──────────────────────────────────────────────┐
│  Padding: 32px (p-8)                         │
│  ┌────────────────────────────────────────┐  │
│  │  ┌────┐  Asistente Inteligente       → │  │
│  │  │🪄 │  Déjanos ayudarte...            │  │
│  │  └────┘                                 │  │
│  │  64x64                                  │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘

Container:
  Background: #000000 (black)
  Border-radius: 24px (rounded-3xl)
  Padding: 32px (p-8)
  Margin-bottom: 32px (mb-8)

Icono:
  Container: 64×64px, white background
  Icon: 32×32px, black color

Texto:
  Título: text-2xl (24px), font-bold, white
  Descripción: text-base (16px), gray-300

Flecha:
  Tamaño: 24×24px (w-6 h-6)
  Color: white
  Hover translateX: 8px
  Transition: 300ms
```

#### Quick Actions Grid

**Layout**:
```
Desktop (lg):    Tablet (md):     Mobile:
┌───┬───┬───┐   ┌─────┬─────┐   ┌─────────┐
│ A │ B │ C │   │  A  │  B  │   │    A    │
├───┼───┼───┤   ├─────┼─────┤   ├─────────┤
│ D │ E │ F │   │  C  │  D  │   │    B    │
└───┴───┴───┘   ├─────┼─────┤   ├─────────┤
3 columnas      │  E  │  F  │   │    C    │
                └─────┴─────┘   ├─────────┤
                2 columnas      │    D    │
                                ├─────────┤
                                │    E    │
                                ├─────────┤
                                │    F    │
                                └─────────┘
                                1 columna

Grid gap: 16px (gap-4)
```

**Cada card**:
```
┌──────────────────────────────┐
│  Padding: 24px               │
│  ┌────────────────────────┐  │
│  │ ┌────┐                 │  │
│  │ │ 🔗 │                 │  │ ← 48×48px icon
│  │ └────┘                 │  │
│  │                        │  │
│  │ Combinar PDFs          │  │ ← font-semibold, gray-900
│  │                        │  │
│  │ Une múltiples archivos │  │ ← text-sm, gray-600
│  │ en uno solo            │  │
│  └────────────────────────┘  │
└──────────────────────────────┘

Container:
  Background: gray-50 → gray-100 (hover)
  Border: 1px solid gray-200
  Border-radius: 16px (rounded-2xl)
  Padding: 24px (p-6)
  Transition: all 300ms

Icon container:
  Size: 48×48px
  Background: black
  Border-radius: 12px
  Margin-bottom: 16px
  Hover scale: 1.10
  Transition: transform 300ms
```

---

### 4.3 Wizard

#### Header

```
┌────────────────────────────────────────────┐
│  ┌────┐  Asistente Inteligente             │
│  │🪄 │  Responde unas preguntas y te       │
│  └────┘  ayudaré a encontrar la función... │
│  56x56                                     │
└────────────────────────────────────────────┘

Margin-bottom: 32px (mb-8)

Icon container:
  Size: 56×56px
  Background: black
  Border-radius: 16px

Título:
  Font-size: 30px (text-3xl)
  Font-weight: 700 (font-bold)
  Color: gray-900

Descripción:
  Font-size: 16px (text-base)
  Color: gray-600
```

#### Breadcrumb

```
[Reducir el tamaño] → [Convertir] → [PDF a Word]

Cada pill:
  Padding: 4px 12px (py-1 px-3)
  Background: rgba(255,255,255,0.6)
  Backdrop-filter: blur(24px)
  Border-radius: 9999px (rounded-full)
  Font-size: 14px (text-sm)
  Color: gray-600

Separador:
  Icon: ChevronRight
  Size: 16×16px
  Color: gray-400
  Margin: 0 8px (gap-2)
```

#### Question Card

```
┌─────────────────────────────────────────────┐
│  Padding: 32px (p-8)                        │
│  Background: gray-50                        │
│  Border: 1px gray-200                       │
│  Border-radius: 16px                        │
│                                             │
│  ❓ ¿Qué quieres hacer con tus PDFs?       │
│     ↑                                       │
│   24×24px, indigo-500                       │
│                                             │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ Option 1     │  │ Option 2     │        │
│  └──────────────┘  └──────────────┘        │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ Option 3     │  │ Option 4     │        │
│  └──────────────┘  └──────────────┘        │
│                                             │
└─────────────────────────────────────────────┘

Grid: 2 columnas en desktop, 1 en mobile
Gap: 16px (gap-4)
```

#### Option Button

```
┌──────────────────────────────────────────────┐
│  Padding: 24px (p-6)                         │
│  ┌────────────────────────────────────────┐  │
│  │ ┌────┐  Combinar varios archivos   →  │  │
│  │ │ 🔗 │                                 │  │
│  │ └────┘                                 │  │
│  │ 48px   ← gap: 16px → ← flex-1 → 20px  │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘

Container:
  Padding: 24px
  Background: white → gray-50 (hover)
  Border: 1px gray-200 → 2px gray-900 (hover)
  Border-radius: 16px
  Display: flex
  Align-items: start
  Gap: 16px

Hover effects (simultáneos):
  - Card scale: 1.02
  - Border: gray-900 + shadow-md
  - Icon scale: 1.10
  - Text color: gray-800 → indigo-900
  - Arrow color: gray-400 → indigo-500
  - Arrow translateX: +4px
```

#### Result Screen

```
┌──────────────────────────────────────────────┐
│  Background: gray-900                        │
│  Padding: 32px                               │
│  Border-radius: 16px                         │
│                                              │
│       ┌──────┐                               │
│       │  ✓   │  ← 80×80px, white, circular  │
│       └──────┘                               │
│                                              │
│  ¡Perfecto! Te recomiendo:                  │ ← text-2xl, bold, white
│  Basándome en tus respuestas...             │ ← text-base, gray-300
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │ Tu selección:                          │ │ ← Glassmorphism
│  │ ① Reducir el tamaño                    │ │
│  │ ② Convertir a otro formato             │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  [🪄 Ir a la función] [Empezar de nuevo]   │
│                                              │
└──────────────────────────────────────────────┘

Check circle animation:
  Initial: scale(0)
  Animate: scale(1)
  Delay: 200ms
  Spring: stiffness 200

Selection list animation:
  Each item staggered by 100ms
  Slide from left: x: -20 → 0
  Fade in: opacity: 0 → 1
```

---

### 4.4 FileDropzone

#### Dimensiones y Estados

```
NORMAL STATE
┌────────────────────────────────────────────┐
│  Padding: 48px (p-12)                      │
│  Border: 2px dashed gray-300               │
│  Border-radius: 24px                       │
│                                            │
│         ┌────────┐                         │
│         │   📤   │  ← 64×64px, black bg   │
│         └────────┘                         │
│                                            │
│    Arrastra archivos aquí                 │ ← text-lg, bold
│    o haz clic para seleccionar            │ ← text-sm, gray-600
│    Máximo 10 archivos                     │ ← text-xs, gray-400
│                                            │
└────────────────────────────────────────────┘

DRAGGING STATE
┌━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ← scale 1.05
┃  Border: 2px dashed gray-900               ┃
┃  Background: gray-50                       ┃
┃                                            ┃
┃         ┌────────┐                         ┃
┃         │   📤   │  ← 70×70px (scale 1.1) ┃
┃         └────────┘     Spring animation   ┃
┃                                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

#### File List Item

```
┌──────────────────────────────────────────────┐
│  ┌────┐  documento.pdf              ✕       │
│  │ 📄 │  2.5 MB                              │
│  └────┘                                      │
│  40px    ← gap: 12px → ← flex-1 → 32px     │
└──────────────────────────────────────────────┘

Container:
  Padding: 12px (p-3)
  Background: gray-50 → gray-100 (hover)
  Border: 1px gray-200
  Border-radius: 12px

Icon container:
  Size: 40×40px
  Background: black
  Border-radius: 8px

Delete button:
  Size: 32×32px
  Background: gray-200 → gray-300 (hover)
  Opacity: 0 → 1 (group-hover)
  Transition: opacity 200ms
```

---

## Especificaciones por Vista

### 5.1 Merge PDF

**Reorderable List**:
```
┌──────────────────────────────────────────────┐
│  ≡  1. documento1.pdf          45 páginas   │
│  ≡  2. reporte.pdf             12 páginas   │
│  ≡  3. anexos.pdf               8 páginas   │
└──────────────────────────────────────────────┘

Cada item:
  Padding: 16px (p-4)
  Background: white
  Border: 1px gray-200
  Border-radius: 12px
  Cursor: move (grab cuando arrastre)
  Hover: shadow-sm

Grip icon (≡):
  Size: 20×20px (w-5 h-5)
  Color: gray-400
  Margin-right: 12px

Drag animation (Motion Reorder):
  - While dragging: z-index aumentado
  - Smooth reordering de otros items
  - Duración: 200ms
```

**Progress Bar durante merge**:
```
Combinando archivos...
[████████████░░░░░░░░] 65%

Container:
  Background: white/60 + backdrop-blur-xl
  Padding: 24px
  Border: 1px white/50
  Border-radius: 16px

Progress bar:
  Height: 8px (h-2)
  Background: gray-200
  Fill: black
  Border-radius: 4px
  Transition: width 100ms ease-out
```

---

### 5.2 Convert PDF

**Conversion Type Selection**:
```
Tipo de conversión

┌──────────────────┐  ┌──────────────────┐
│ [SELECCIONADO]   │  │                  │
│                  │  │                  │
│ PDF → Word       │  │ Word → PDF       │
│ Convierte...     │  │ Convierte...     │
└──────────────────┘  └──────────────────┘
  Gradiente azul       Gray-50

┌──────────────────┐  ┌──────────────────┐
│ PDF → Imágenes   │  │ Imágenes → PDF   │
└──────────────────┘  └──────────────────┘

Grid: 2 columnas (md:grid-cols-2)
Gap: 16px (gap-4)
```

**Layout Engine Info Card**:
```
┌────────────────────────────────────────────┐
│  ┌────┐  Layout Engine Avanzado            │
│  │ 🔄 │                                     │
│  └────┘  Este proceso utiliza...           │
│  40x40                                     │
│          • Detectar y preservar...         │
│          • Mantener el formato...          │
│          • Reconocer imágenes...           │
└────────────────────────────────────────────┘

Background: gray-50
Border: 1px gray-200
Border-radius: 16px
Padding: 24px

Bullet points:
  Size: 6×6px circle
  Color: indigo-500
  Gap: 8px
```

---

### 5.3 Batch Processing

**File Status List**:
```
┌────────────────────────────────────────────┐
│  ⏱️ documento1.pdf          [✓ Listo]      │
│  ⚙️ reporte.pdf             [65%]          │
│  ⏳ anexos.pdf              [Pendiente]    │
│  ✅ factura.pdf             [✓ Listo]      │
└────────────────────────────────────────────┘

Estados y colores:
  Pending:
    Icon: Clock (⏳), gray-400
    Badge: "Pendiente", gray-100 bg, gray-600 text

  Processing:
    Icon: Play (rotating), blue-500
    Badge: "65%", blue-100 bg, blue-600 text
    Progress bar: blue fill

  Completed:
    Icon: CheckCircle2 (✅), green-500
    Badge: "✓ Listo", green-100 bg, green-600 text

Rotating animation (Processing):
  <motion.div
    animate={{ rotate: 360 }}
    transition={{ 
      duration: 2,
      repeat: Infinity,
      ease: 'linear'
    }}
  >
```

**Overall Progress**:
```
Progreso general                           45%
[█████████░░░░░░░░]

Bar height: 8px (h-2)
Container padding: 16px top
Border-top: 1px gray-200
```

---

## Sistema de Colores y Efectos

### 6.1 Paleta de Grises

```
gray-50:  #F9FAFB  - Fondos secundarios, cards
gray-100: #F3F4F6  - Hover states ligeros
gray-200: #E5E7EB  - Bordes sutiles
gray-300: #D1D5DB  - Bordes dropzone
gray-400: #9CA3AF  - Iconos secundarios, flechas
gray-500: #6B7280  - Texto secundario
gray-600: #4B5563  - Texto descripción
gray-700: #374151  - Texto sidebar no activo
gray-800: #1F2937  - Texto principal
gray-900: #111827  - Backgrounds activos, borders hover
black:    #000000  - Contenedores de iconos
white:    #FFFFFF  - Fondos principales
```

### 6.2 Colores de Acento

```
indigo-500:  #6366F1  - Hover states en Wizard
indigo-700:  #4338CA  - Info cards
indigo-900:  #312E81  - Texto hover Wizard

blue-50:     #EFF6FF  - Gradientes conversión
blue-500:    #3B82F6  - Processing state
blue-600:    #2563EB  - Badges processing

emerald-50:  #ECFDF5  - Gradientes conversión
green-500:   #10B981  - Success states
green-600:   #059669  - Badges completed

amber-50:    #FFFBEB  - Warning backgrounds
amber-600:   #D97706  - Warning states

purple-50:   #FAF5FF  - Gradientes conversión
pink-50:     #FDF2F8  - Gradientes conversión
orange-50:   #FFF7ED  - Gradientes conversión
red-50:      #FEF2F2  - Gradientes conversión
```

### 6.3 Sombras

```
shadow-sm:   0 1px 2px 0 rgb(0 0 0 / 0.05)
  Uso: Cards en hover ligero

shadow-md:   0 4px 6px -1px rgb(0 0 0 / 0.1),
             0 2px 4px -2px rgb(0 0 0 / 0.1)
  Uso: Wizard options hover, selected cards

shadow-xl:   0 20px 25px -5px rgb(0 0 0 / 0.1),
             0 8px 10px -6px rgb(0 0 0 / 0.1)
  Uso: Check circle resultado final
```

### 6.4 Efectos de Blur

```
backdrop-blur-xl: blur(24px)
  Uso: Breadcrumb, processing card, result panels

backdrop-blur-sm: blur(4px)
  Uso: Overlays ligeros
```

### 6.5 Gradientes

```
PDF→Word:
  from-blue-50 to-indigo-50
  #EFF6FF → #EEF2FF

Word→PDF:
  from-purple-50 to-pink-50
  #FAF5FF → #FDF2F8

PDF→Images:
  from-emerald-50 to-teal-50
  #ECFDF5 → #F0FDFA

Images→PDF:
  from-orange-50 to-red-50
  #FFF7ED → #FEF2F2
```

---

## Implementación en PySide6

### 7.1 Contenedores de Iconos en Qt

#### Tipo A: Header (56×56px)

```python
# Widget contenedor
icon_container = QWidget()
icon_container.setFixedSize(56, 56)
icon_container.setStyleSheet("""
    QWidget {
        background-color: #000000;
        border-radius: 16px;
    }
""")

# Layout para centrar icono
layout = QVBoxLayout(icon_container)
layout.setContentsMargins(0, 0, 0, 0)
layout.setAlignment(Qt.AlignCenter)

# Label con icono SVG
icon_label = QLabel()
pixmap = QPixmap("icons/refresh.svg")
pixmap = pixmap.scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
icon_label.setPixmap(pixmap)
layout.addWidget(icon_label)
```

#### Tipo C: Dashboard Card (48×48px con hover)

```python
class IconContainer(QWidget):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.setFixedSize(48, 48)
        self.icon_path = icon_path
        self.scale_factor = 1.0
        
        self.setStyleSheet("""
            QWidget {
                background-color: #000000;
                border-radius: 12px;
            }
        """)
        
        self.setup_icon()
    
    def setup_icon(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        
        self.icon_label = QLabel()
        pixmap = QPixmap(self.icon_path)
        pixmap = pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(pixmap)
        layout.addWidget(self.icon_label)
    
    def scale_icon(self, scale):
        """Anima el scale del icono"""
        self.scale_animation = QPropertyAnimation(self, b"scale_factor")
        self.scale_animation.setDuration(300)
        self.scale_animation.setStartValue(self.scale_factor)
        self.scale_animation.setEndValue(scale)
        self.scale_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.scale_animation.start()
```

---

### 7.2 Animaciones de Entrada

#### Fade In + Slide Down (Header)

```python
def animate_header_entrance(widget):
    """Anima entrada del header desde arriba con fade"""
    
    # Animación de opacidad
    opacity_effect = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(opacity_effect)
    
    opacity_animation = QPropertyAnimation(opacity_effect, b"opacity")
    opacity_animation.setDuration(300)
    opacity_animation.setStartValue(0.0)
    opacity_animation.setEndValue(1.0)
    opacity_animation.setEasingCurve(QEasingCurve.OutQuad)
    
    # Animación de posición
    start_pos = widget.pos()
    temp_pos = QPoint(start_pos.x(), start_pos.y() - 20)
    widget.move(temp_pos)
    
    pos_animation = QPropertyAnimation(widget, b"pos")
    pos_animation.setDuration(300)
    pos_animation.setStartValue(temp_pos)
    pos_animation.setEndValue(start_pos)
    pos_animation.setEasingCurve(QEasingCurve.OutQuad)
    
    # Grupo de animaciones
    animation_group = QParallelAnimationGroup()
    animation_group.addAnimation(opacity_animation)
    animation_group.addAnimation(pos_animation)
    animation_group.start()
    
    return animation_group
```

#### Stagger Animation (Cards)

```python
def animate_cards_stagger(card_widgets, base_delay=100):
    """Anima entrada de cards con retraso incremental"""
    
    animations = []
    
    for index, card in enumerate(card_widgets):
        # Calcular delay
        delay = base_delay + (index * 50)  # 100ms, 150ms, 200ms...
        
        # Timer para delay
        QTimer.singleShot(delay, lambda c=card: animate_card_entrance(c))
    
    return animations

def animate_card_entrance(card):
    """Anima una card individual desde abajo con fade"""
    
    # Opacidad
    opacity_effect = QGraphicsOpacityEffect()
    card.setGraphicsEffect(opacity_effect)
    
    opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
    opacity_anim.setDuration(300)
    opacity_anim.setStartValue(0.0)
    opacity_anim.setEndValue(1.0)
    
    # Posición Y
    start_pos = card.pos()
    temp_pos = QPoint(start_pos.x(), start_pos.y() + 20)
    card.move(temp_pos)
    
    pos_anim = QPropertyAnimation(card, b"pos")
    pos_anim.setDuration(300)
    pos_anim.setStartValue(temp_pos)
    pos_anim.setEndValue(start_pos)
    pos_anim.setEasingCurve(QEasingCurve.OutQuad)
    
    group = QParallelAnimationGroup()
    group.addAnimation(opacity_anim)
    group.addAnimation(pos_anim)
    group.start()
```

---

### 7.3 Animaciones de Hover

#### Scale on Hover

```python
class ScalableButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.scale_normal = 1.0
        self.scale_hover = 1.02
        self.scale_press = 0.98
        
    def enterEvent(self, event):
        """Evento cuando mouse entra"""
        self.animate_scale(self.scale_hover, duration=150)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Evento cuando mouse sale"""
        self.animate_scale(self.scale_normal, duration=150)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Evento cuando se presiona"""
        self.animate_scale(self.scale_press, duration=100)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Evento cuando se suelta"""
        if self.underMouse():
            self.animate_scale(self.scale_hover, duration=100)
        else:
            self.animate_scale(self.scale_normal, duration=100)
        super().mouseReleaseEvent(event)
    
    def animate_scale(self, target_scale, duration=150):
        """Anima el scale del botón"""
        # Usando QGraphicsScale transform
        # (Implementación simplificada, requiere más setup)
        pass
```

---

### 7.4 Spring Animation (Check Circle)

```python
from PyQt6.QtCore import QEasingCurve

def animate_check_circle_pop(circle_widget):
    """Anima aparición del círculo con efecto spring"""
    
    # Configurar escala inicial
    circle_widget.setFixedSize(0, 0)
    
    # Animación de tamaño
    size_animation = QPropertyAnimation(circle_widget, b"size")
    size_animation.setDuration(600)  # 600ms como en React
    size_animation.setStartValue(QSize(0, 0))
    size_animation.setEndValue(QSize(80, 80))
    
    # Curva de spring usando OutElastic para simular spring
    # Nota: Qt no tiene spring nativo, OutElastic simula el rebote
    size_animation.setEasingCurve(QEasingCurve.OutElastic)
    
    # Delay de 200ms
    QTimer.singleShot(200, size_animation.start)
    
    return size_animation
```

---

### 7.5 Glassmorphism en Qt

```python
class GlassmorphismWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Efecto de blur
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(24)  # 24px blur
        self.setGraphicsEffect(blur_effect)
        
        # Stylesheet con transparencia
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 16px;
            }
        """)
        
        # Atributos de ventana para transparencia
        self.setAttribute(Qt.WA_TranslucentBackground)
```

---

### 7.6 FileDropzone con Estados

```python
class FileDropzone(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dragging = False
        self.setup_ui()
        self.setAcceptDrops(True)
    
    def setup_ui(self):
        self.setFixedHeight(300)
        self.apply_normal_style()
    
    def apply_normal_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 2px dashed #D1D5DB;
                border-radius: 24px;
            }
        """)
    
    def apply_dragging_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F9FAFB;
                border: 2px dashed #111827;
                border-radius: 24px;
            }
        """)
    
    def dragEnterEvent(self, event):
        """Cuando comienza el drag"""
        self.is_dragging = True
        self.apply_dragging_style()
        
        # Animar scale del container
        self.animate_scale(1.05, duration=300)
        
        # Animar scale del icono (con spring)
        self.animate_icon_spring()
        
        event.accept()
    
    def dragLeaveEvent(self, event):
        """Cuando termina el drag"""
        self.is_dragging = False
        self.apply_normal_style()
        self.animate_scale(1.0, duration=300)
        event.accept()
    
    def animate_icon_spring(self):
        """Anima icono con efecto spring"""
        icon_animation = QPropertyAnimation(self.icon_widget, b"size")
        icon_animation.setDuration(400)
        icon_animation.setStartValue(QSize(64, 64))
        icon_animation.setEndValue(QSize(70, 70))  # Scale 1.1
        icon_animation.setEasingCurve(QEasingCurve.OutElastic)
        icon_animation.start()
```

---

### 7.7 Progress Bar Animado

```python
class AnimatedProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
    
    def setup_style(self):
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #E5E7EB;
                border-radius: 4px;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #000000;
                border-radius: 4px;
            }
        """)
        
        self.setTextVisible(False)
    
    def setValue(self, value):
        """Override para animar el cambio de valor"""
        current = self.value()
        
        # Animación suave del valor
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(100)  # 100ms por cambio
        self.animation.setStartValue(current)
        self.animation.setEndValue(value)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()
```

---

## Resumen de Timing y Duraciones

### Tabla de Duraciones

| Tipo de Animación | Duración | Easing | Uso |
|------------------|----------|---------|-----|
| **Fade in/out** | 300ms | ease-out | Entradas generales |
| **Slide lateral** | 300ms | ease-in-out | Cambio preguntas Wizard |
| **Hover scale ligero** | 150ms | ease-out | Botones whileHover 1.02 |
| **Hover scale icono** | 300ms | ease-in-out | Iconos en cards 1.10 |
| **Click (tap)** | 100ms | ease-in | whileTap 0.98 |
| **Translate flecha** | 200ms | ease-in-out | Flechas → +4px |
| **Color transitions** | 150-300ms | ease-in-out | Backgrounds, borders |
| **Spring pop** | 600ms | spring | Check circle resultado |
| **Layout shared** | 600ms | spring 0.2 | Cambio tipo conversión |
| **Stagger delay** | 50-100ms | - | Incremento entre items |
| **File list item** | 300ms + 50ms/item | ease-out | Lista archivos |
| **Dropzone drag** | 300ms | spring | FileDropzone states |
| **Progress bar** | 100ms | ease-out | Actualización progreso |

---

## Checklist de Implementación

### Para cada Contenedor de Icono:

- [ ] Tamaño exacto del container (40px, 48px, 56px, 64px, 80px)
- [ ] Border-radius correcto (8px, 12px, 16px, 50%)
- [ ] Color de fondo (#000 o #FFF según contexto)
- [ ] Tamaño del icono interior (proporcional al container)
- [ ] Color del icono (#FFF o #000 invertido)
- [ ] Centrado perfecto (flexbox con align/justify center)
- [ ] Transiciones hover si aplica (scale 1.10, duración 300ms)

### Para cada Animación:

- [ ] Valores inicial y final definidos
- [ ] Duración apropiada según tabla
- [ ] Easing curve correcto
- [ ] Delay si es stagger animation
- [ ] Cleanup en unmount (AnimatePresence)

### Para cada Card/Button:

- [ ] Estados: normal, hover, active, disabled
- [ ] Transiciones suaves entre estados
- [ ] Borders y sombras apropiadas
- [ ] Text colors por estado
- [ ] Scale effects si aplica
- [ ] Cursor apropiado (pointer, not-allowed)

---

**Documento creado para LocalPDF v5**  
**Versión**: 1.0  
**Especificaciones**: Pixel-perfect, timing exact  
**Fecha**: Enero 2025
