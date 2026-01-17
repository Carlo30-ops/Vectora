# LocalPDF v5 - Modo Oscuro Profesional Estilo Apple

## 🌙 Documentación Completa del Dark Mode

Esta documentación detalla la implementación completa del modo oscuro profesional inspirado en el diseño de iOS y productos Apple, manteniendo la estética minimalista y las transiciones fluidas.

---

## 📋 Índice

1. [Sistema de Colores Apple Dark Mode](#sistema-de-colores-apple-dark-mode)
2. [Arquitectura del Tema](#arquitectura-del-tema)
3. [Toggle de Tema](#toggle-de-tema)
4. [Componentes Adaptados](#componentes-adaptados)
5. [Transiciones y Efectos](#transiciones-y-efectos)
6. [Glassmorphism en Dark Mode](#glassmorphism-en-dark-mode)
7. [Implementación en PySide6](#implementación-en-pyside6)

---

## Sistema de Colores Apple Dark Mode

### 1.1 Paleta de Grises Oscuros (Apple iOS)

Apple utiliza una paleta específica de grises oscuros que proporcionan profundidad y jerarquía visual:

```css
/* Colores base de iOS Dark Mode */
--black-base: #000000           /* Negro puro para fondo principal */
--gray-elevated-1: #1C1C1E      /* Primer nivel de elevación */
--gray-elevated-2: #2C2C2E      /* Segundo nivel de elevación */
--gray-elevated-3: #3A3A3C      /* Tercer nivel de elevación */
--gray-separator: #38383A       /* Separadores y bordes */
--gray-fill: rgba(120,120,128,0.36) /* Fills de inputs */
```

#### Uso de Elevaciones

```
┌────────────────────────────────────────┐
│  #000000 (Negro base)                  │
│  ┌──────────────────────────────────┐  │
│  │  #1C1C1E (Cards, Sidebar)        │  │
│  │  ┌────────────────────────────┐  │  │
│  │  │  #2C2C2E (Opciones hover)  │  │  │
│  │  │  ┌──────────────────────┐  │  │  │
│  │  │  │  #3A3A3C (Activo)    │  │  │  │
│  │  │  └──────────────────────┘  │  │  │
│  │  └────────────────────────────┘  │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

### 1.2 Colores de Texto (Labels)

Apple define etiquetas de texto con opacidades específicas:

```css
/* Labels en Dark Mode */
--label-primary: #FFFFFF         /* Texto principal */
--label-secondary: #98989D       /* Texto secundario (60% opacity) */
--label-tertiary: #48484A        /* Texto terciario (30% opacity) */
--label-quaternary: #3A3A3C      /* Texto cuaternario (18% opacity) */

/* Opacidades aplicadas sobre blanco */
Primary:    rgba(255, 255, 255, 1.0)   - 100%
Secondary:  rgba(255, 255, 255, 0.6)   - 60%
Tertiary:   rgba(255, 255, 255, 0.3)   - 30%
Quaternary: rgba(255, 255, 255, 0.18)  - 18%
```

### 1.3 Inversión de Iconos (Estilo Apple)

En modo oscuro, Apple invierte los elementos visuales clave para mantener el contraste:

**Light Mode**:
```
Container: Negro (#000000)
Icono: Blanco (#FFFFFF)
```

**Dark Mode**:
```
Container: Blanco (#FFFFFF)
Icono: Negro (#000000)
```

**Ejemplo visual**:
```
LIGHT MODE                  DARK MODE
┌─────────────┐            ┌─────────────┐
│  ⬛ Negro   │            │  ⬜ Blanco  │
│   🔗 Blanco │            │   🔗 Negro  │
└─────────────┘            └─────────────┘
```

### 1.4 Colores de Acento Vibrantes

Los colores de acento se vuelven más vibrantes en dark mode para mejor visibilidad:

```css
/* Light Mode → Dark Mode */
Indigo:
  Light: #6366F1  →  Dark: #818CF8  (+brightness)
  
Blue:
  Light: #3B82F6  →  Dark: #60A5FA
  
Green:
  Light: #10B981  →  Dark: #34D399
  
Amber:
  Light: #F59E0B  →  Dark: #FBBF24

Purple:
  Light: #8B5CF6  →  Dark: #A78BFA
```

---

## Arquitectura del Tema

### 2.1 ThemeContext

Sistema de contexto React para gestión global del tema:

```typescript
// src/app/context/ThemeContext.tsx

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(() => {
    // 1. Verificar localStorage
    const saved = localStorage.getItem('theme') as Theme;
    if (saved) return saved;
    
    // 2. Detectar preferencia del sistema
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    
    // 3. Default: light
    return 'light';
  });

  useEffect(() => {
    // Aplicar clase al HTML
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    
    // Persistir preferencia
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

### 2.2 Integración en App

```typescript
// App.tsx
import { ThemeProvider } from './context/ThemeContext';

export default function App() {
  return (
    <ThemeProvider>
      <div className="flex h-screen bg-gray-50 dark:bg-black overflow-hidden transition-colors duration-300">
        {/* ... */}
      </div>
    </ThemeProvider>
  );
}
```

**Características clave**:
- ✅ Persistencia en localStorage
- ✅ Detección de preferencia del sistema
- ✅ Clase `dark` en `<html>` para Tailwind
- ✅ Transición suave de 300ms

---

## Toggle de Tema

### 3.1 Diseño del Toggle (Estilo iOS)

El toggle sigue el diseño exacto de los switches de iOS:

```
┌──────────────────────────────┐
│  ●────────○                  │  OFF (Light)
│  [Sun]        [Moon]         │
└──────────────────────────────┘

┌──────────────────────────────┐
│  ○────────●                  │  ON (Dark)
│  [Sun]        [Moon]         │
└──────────────────────────────┘
```

### 3.2 Especificaciones Visuales

**Dimensiones**:
```
Container: 64px × 32px (w-16 h-8)
Knob: 24px × 24px (w-6 h-6)
Border-radius: 9999px (rounded-full)
```

**Colores**:
```css
/* Track Background */
Light Mode: #E5E7EB (gray-200)
Dark Mode:  #374151 (gray-700)

/* Knob */
Light Mode: #FFFFFF (white)
Dark Mode:  #111827 (gray-900)
```

**Posiciones del Knob**:
```
Light: x = 0 (left: 4px)
Dark:  x = 32px (right: 4px)
```

### 3.3 Animaciones del Toggle

#### Spring Animation del Knob

```typescript
<motion.div
  animate={{
    x: isDark ? 32 : 0,
  }}
  transition={{
    type: 'spring',
    stiffness: 500,  // Alta rigidez para respuesta rápida
    damping: 30,     // Amortiguación para suavidad
  }}
>
```

**Curva de animación**:
```
Position
32px │         ╱─────
     │        ╱
     │       ╱
     │      ╱
 0px │─────╯
     └────────────────→ Time
     0ms         200ms

Spring overshoot: Pequeño rebote al llegar
```

#### Cross-fade de Iconos

Dos iconos dentro del knob se alternan:

```typescript
{/* Moon icon (dark mode) */}
<motion.div
  animate={{
    scale: isDark ? 1 : 0,
    opacity: isDark ? 1 : 0,
  }}
>
  <Moon className="w-3.5 h-3.5 text-indigo-400" />
</motion.div>

{/* Sun icon (light mode) */}
<motion.div
  animate={{
    scale: isDark ? 0 : 1,
    opacity: isDark ? 0 : 1,
  }}
>
  <Sun className="w-3.5 h-3.5 text-amber-500" />
</motion.div>
```

**Timeline**:
```
        Light → Dark
Moon:   [fade out] ──→ [fade in]
Sun:    [fade in]  ──→ [fade out]
Scale:  0 ─────────→ 1
Duración: sincronizada con movimiento del knob
```

#### Iconos de Fondo

Iconos sutiles en el track que indican el estado:

```typescript
{/* Background icons */}
<motion.div
  animate={{
    opacity: isDark ? 0.3 : 0,
    scale: isDark ? 1 : 0.8,
  }}
>
  <Moon className="w-3 h-3 text-gray-400" />
</motion.div>
```

**Comportamiento**:
- Opacity 30% cuando activos
- Scale 0.8 cuando inactivos
- Fade suave al cambiar

### 3.4 Código Completo del Toggle

```typescript
import { motion } from 'motion/react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === 'dark';

  return (
    <button
      onClick={toggleTheme}
      className="relative w-16 h-8 rounded-full bg-gray-200 dark:bg-gray-700 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-900"
      aria-label="Toggle theme"
    >
      {/* Track animado */}
      <motion.div
        className="absolute inset-0 rounded-full"
        animate={{
          backgroundColor: isDark ? '#374151' : '#E5E7EB',
        }}
        transition={{ duration: 0.3 }}
      />
      
      {/* Knob con spring */}
      <motion.div
        className="absolute top-1 left-1 w-6 h-6 bg-white dark:bg-gray-900 rounded-full shadow-lg flex items-center justify-center"
        animate={{
          x: isDark ? 32 : 0,
        }}
        transition={{
          type: 'spring',
          stiffness: 500,
          damping: 30,
        }}
      >
        {/* Iconos alternados */}
        <motion.div
          initial={false}
          animate={{
            scale: isDark ? 1 : 0,
            opacity: isDark ? 1 : 0,
          }}
          className="absolute"
        >
          <Moon className="w-3.5 h-3.5 text-indigo-400" />
        </motion.div>
        
        <motion.div
          initial={false}
          animate={{
            scale: isDark ? 0 : 1,
            opacity: isDark ? 0 : 1,
          }}
          className="absolute"
        >
          <Sun className="w-3.5 h-3.5 text-amber-500" />
        </motion.div>
      </motion.div>
      
      {/* Iconos de fondo */}
      <div className="absolute inset-0 flex items-center justify-between px-2 pointer-events-none">
        <motion.div
          animate={{
            opacity: isDark ? 0.3 : 0,
            scale: isDark ? 1 : 0.8,
          }}
        >
          <Moon className="w-3 h-3 text-gray-400" />
        </motion.div>
        <motion.div
          animate={{
            opacity: isDark ? 0 : 0.3,
            scale: isDark ? 0.8 : 1,
          }}
        >
          <Sun className="w-3 h-3 text-gray-500" />
        </motion.div>
      </div>
    </button>
  );
}
```

---

## Componentes Adaptados

### 4.1 Sidebar (Barra Lateral)

#### Header del Sidebar

```tsx
<div className="p-6 border-b border-gray-200 dark:border-gray-800">
  <div className="flex items-center gap-3">
    {/* Logo invertido */}
    <div className="w-10 h-10 bg-black dark:bg-white rounded-2xl flex items-center justify-center transition-colors duration-300">
      <FileText className="w-6 h-6 text-white dark:text-black" />
    </div>
    <div>
      <h1 className="text-lg font-semibold text-gray-900 dark:text-white">
        LocalPDF
      </h1>
      <p className="text-xs text-gray-500 dark:text-gray-400">v5.0</p>
    </div>
  </div>
</div>
```

**Cambios visuales**:
```
LIGHT MODE               DARK MODE
┌──────────────┐        ┌──────────────┐
│ ⬛ LocalPDF  │   →    │ ⬜ LocalPDF  │
│    v5.0      │        │    v5.0      │
└──────────────┘        └──────────────┘
  Negro/Blanco            Blanco/Negro
  Gray-900 texto          White texto
  Border gray-200         Border gray-800
```

#### Menu Items

**Estados en Dark Mode**:

```tsx
<motion.button
  className={`
    ${isActive 
      ? 'bg-gray-900 dark:bg-white text-white dark:text-black' 
      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
    }
  `}
>
```

**Comparación visual**:
```
LIGHT MODE                      DARK MODE

Normal:
┌─────────────────┐            ┌─────────────────┐
│ 📄 Dashboard    │            │ 📄 Dashboard    │
│ gray-700        │            │ gray-300        │
└─────────────────┘            └─────────────────┘

Hover:
┌─────────────────┐            ┌─────────────────┐
│ 📄 Dashboard    │            │ 📄 Dashboard    │
│ bg-gray-100     │            │ bg-gray-800     │
└─────────────────┘            └─────────────────┘

Activo:
┌─────────────────┐            ┌─────────────────┐
│ 📄 Dashboard    │            │ 📄 Dashboard    │
│ bg-gray-900     │            │ bg-white        │
│ text-white      │            │ text-black      │
└─────────────────┘            └─────────────────┘
```

#### Badge "Nuevo"

Inversión del badge en items activos:

```tsx
<span className="ml-auto px-2 py-0.5 text-xs font-semibold bg-black dark:bg-white text-white dark:text-black rounded-full">
  {item.badge}
</span>
```

#### Footer con Toggle

```tsx
<div className="p-4 border-t border-gray-200 dark:border-gray-800 space-y-3">
  {/* Theme Toggle */}
  <div className="flex items-center justify-between px-2">
    <span className="text-xs font-medium text-gray-600 dark:text-gray-400">Tema</span>
    <ThemeToggle />
  </div>
  
  {/* Offline Badge */}
  <div className="bg-gray-100 dark:bg-gray-800 rounded-xl p-4 transition-colors duration-300">
    <p className="text-xs text-gray-900 dark:text-white font-medium mb-1">100% Offline</p>
    <p className="text-xs text-gray-600 dark:text-gray-400">Sin conexión requerida</p>
  </div>
</div>
```

---

### 4.2 Dashboard

#### Card del Asistente con Gradiente

Gradiente invertido en dark mode:

```tsx
<motion.div
  className="mb-8 bg-gradient-to-br from-gray-900 to-black dark:from-white dark:to-gray-100 rounded-3xl p-8 cursor-pointer group hover:shadow-2xl hover:shadow-indigo-500/20 dark:hover:shadow-white/10 transition-all duration-300"
>
```

**Gradientes**:
```
LIGHT MODE:
  from-gray-900 (#111827)
  to-black (#000000)
  Texto: white
  Icono container: white
  Icono: black

DARK MODE:
  from-white (#FFFFFF)
  to-gray-100 (#F3F4F6)
  Texto: black
  Icono container: black
  Icono: white
```

**Hover Shadow**:
```
Light: shadow-indigo-500/20  (Sombra azul sutil)
Dark:  shadow-white/10       (Sombra blanca muy sutil)
```

#### Quick Actions Cards

Elevación con colores Apple:

```tsx
<div className="bg-gray-50 dark:bg-[#1C1C1E] hover:bg-gray-100 dark:hover:bg-[#2C2C2E] rounded-2xl p-6 transition-all duration-300 border border-gray-200 dark:border-gray-800 h-full">
  <div className="w-12 h-12 bg-black dark:bg-white rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
    <Icon className="w-6 h-6 text-white dark:text-black" />
  </div>
  <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{action.title}</h3>
  <p className="text-sm text-gray-600 dark:text-gray-400">{action.description}</p>
</div>
```

**Jerarquía de colores**:
```
                  LIGHT MODE       DARK MODE
Background:       gray-50          #1C1C1E (elevated-1)
Hover:            gray-100         #2C2C2E (elevated-2)
Border:           gray-200         gray-800
Icon Container:   black            white
Icon:             white            black
Título:           gray-900         white
Descripción:      gray-600         gray-400
```

---

### 4.3 Wizard

#### Question Cards

```tsx
<div className="bg-gray-50 dark:bg-[#1C1C1E] rounded-2xl p-8 border border-gray-200 dark:border-gray-800 mb-6 transition-colors duration-300">
  <div className="flex items-start gap-3 mb-6">
    <HelpCircle className="w-6 h-6 text-indigo-500 dark:text-indigo-400 flex-shrink-0 mt-1" />
    <h2 className="text-2xl font-semibold text-gray-800 dark:text-white">
      {question.question}
    </h2>
  </div>
```

**Color de acento ajustado**:
```
Light: indigo-500 (#6366F1)
Dark:  indigo-400 (#818CF8) ← Más brillante
```

#### Option Buttons

Estados complejos en dark mode:

```tsx
<motion.button
  className="group relative p-6 bg-white dark:bg-[#2C2C2E] hover:bg-gray-50 dark:hover:bg-[#3A3A3C] rounded-2xl border border-gray-200 dark:border-gray-700 hover:border-gray-900 dark:hover:border-gray-500 transition-all text-left hover:shadow-md"
>
```

**Estados detallados**:
```
                    LIGHT MODE              DARK MODE
Normal:
  Background:       white                   #2C2C2E (elevated-2)
  Border:           gray-200                gray-700
  Text:             gray-800                white
  Arrow:            gray-400                gray-600

Hover:
  Background:       gray-50                 #3A3A3C (elevated-3)
  Border:           gray-900                gray-500
  Text:             indigo-900              indigo-400
  Arrow:            indigo-500              indigo-400
  Arrow Move:       +4px right              +4px right
  Shadow:           shadow-md               shadow-md
  Icon Scale:       1.10                    1.10
```

#### Breadcrumb Pills

Glassmorphism adaptado:

```tsx
<span className="text-sm text-gray-600 dark:text-gray-400 bg-white/60 dark:bg-white/10 backdrop-blur-xl px-3 py-1 rounded-full">
  {step}
</span>
```

**Especificaciones**:
```
LIGHT MODE:
  Background: rgba(255, 255, 255, 0.6) - Blanco semi-transparente
  Text: gray-600
  Backdrop-blur: 24px
  Sobre fondo: gray-50

DARK MODE:
  Background: rgba(255, 255, 255, 0.1) - Blanco muy sutil
  Text: gray-400
  Backdrop-blur: 24px
  Sobre fondo: black
```

#### Result Screen

Inversión completa del resultado:

```tsx
<div className="bg-gradient-to-br from-gray-900 to-black dark:from-white dark:to-gray-100 rounded-2xl p-8 transition-colors duration-300">
  <motion.div className="w-20 h-20 bg-white dark:bg-black rounded-full flex items-center justify-center mx-auto mb-4 shadow-xl">
    <CheckCircle2 className="w-10 h-10 text-black dark:text-white" />
  </motion.div>
  <h2 className="text-2xl font-bold text-white dark:text-black mb-2">
    ¡Perfecto! Te recomiendo:
  </h2>
  <p className="text-gray-300 dark:text-gray-600">
    Basándome en tus respuestas, esta es la mejor opción para ti
  </p>
</div>
```

**Selection List**:
```tsx
<div className="bg-white/10 dark:bg-black/10 backdrop-blur-xl rounded-xl p-6 mb-6">
  <h3 className="font-semibold text-white dark:text-black mb-3">Tu selección:</h3>
  <div className="space-y-2">
    {selectedPath.map((step, index) => (
      <div className="flex items-center gap-3">
        <div className="w-6 h-6 bg-white dark:bg-black rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-black dark:text-white text-xs font-bold">{index + 1}</span>
        </div>
        <p className="text-gray-300 dark:text-gray-600">{step}</p>
      </div>
    ))}
  </div>
</div>
```

---

## Transiciones y Efectos

### 5.1 Transition Global

Todas las transiciones de color tienen duración consistente:

```css
transition-colors duration-300
```

Esto asegura que el cambio de modo sea suave y sincronizado en todos los elementos.

### 5.2 Elementos que Transicionan

#### Background Colors
```tsx
bg-white dark:bg-black transition-colors duration-300
bg-gray-50 dark:bg-[#1C1C1E] transition-colors duration-300
```

#### Text Colors
```tsx
text-gray-900 dark:text-white
text-gray-600 dark:text-gray-400
```

#### Border Colors
```tsx
border-gray-200 dark:border-gray-800
```

#### Icon Containers
```tsx
bg-black dark:bg-white transition-colors duration-300
```

### 5.3 Timeline de Cambio de Tema

Cuando el usuario hace click en el toggle:

```
0ms     Toggle clicked
        └─ toggleTheme() ejecutado
        
10ms    ThemeContext actualiza estado
        └─ theme: 'light' → 'dark'
        
20ms    useEffect detecta cambio
        └─ document.documentElement.classList.add('dark')
        
30ms    Tailwind aplica clases dark:*
        └─ Todas las propiedades CSS con dark: prefix activas
        
30-330ms  Transiciones visuales (300ms)
        ├─ Backgrounds cambian
        ├─ Textos cambian
        ├─ Bordes cambian
        ├─ Iconos invierten
        └─ Toggle se anima
        
330ms   Cambio completo
        └─ localStorage.setItem('theme', 'dark')
```

### 5.4 Sincronización de Animaciones

Elementos que deben animarse simultáneamente:

```tsx
{/* Todos con transition-colors duration-300 */}
<div className="bg-white dark:bg-black transition-colors duration-300">
  <div className="bg-black dark:bg-white transition-colors duration-300">
    <Icon className="text-white dark:text-black" />
  </div>
  <h1 className="text-gray-900 dark:text-white">Título</h1>
  <p className="text-gray-600 dark:text-gray-400">Descripción</p>
</div>
```

**Resultado**: Cambio fluido y sincronizado de todos los elementos en 300ms.

---

## Glassmorphism en Dark Mode

### 6.1 Breadcrumb Pills

El glassmorphism debe adaptarse al fondo oscuro:

**Light Mode**:
```css
background: rgba(255, 255, 255, 0.6);  /* Blanco translúcido */
backdrop-filter: blur(24px);
color: #6B7280;  /* gray-600 */
```

**Dark Mode**:
```css
background: rgba(255, 255, 255, 0.1);  /* Blanco muy sutil */
backdrop-filter: blur(24px);
color: #9CA3AF;  /* gray-400 - más claro */
```

**Ejemplo visual**:
```
LIGHT MODE (sobre gray-50)
┌─────────────────────────────┐
│  Fondo gris claro           │
│  ┌───────────────────────┐  │
│  │ [Pill] Semi-opaco     │  │ ← rgba(255,255,255,0.6)
│  │ Texto oscuro          │  │
│  └───────────────────────┘  │
└─────────────────────────────┘

DARK MODE (sobre black)
┌─────────────────────────────┐
│  Fondo negro                │
│  ┌───────────────────────┐  │
│  │ [Pill] Muy sutil      │  │ ← rgba(255,255,255,0.1)
│  │ Texto claro           │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

### 6.2 Result Panel Glassmorphism

```tsx
<div className="bg-white/10 dark:bg-black/10 backdrop-blur-xl rounded-xl p-6">
```

**Comparación**:
```
                LIGHT MODE              DARK MODE
Background:     rgba(255,255,255,0.1)  rgba(0,0,0,0.1)
Backdrop:       blur(24px)             blur(24px)
Sobre:          Gradiente oscuro       Gradiente claro
Contraste:      Blanco sobre negro     Negro sobre blanco
```

---

## Implementación en PySide6

### 7.1 Sistema de Temas Qt

```python
from enum import Enum
from PyQt6.QtCore import QSettings, pyqtSignal, QObject

class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"

class ThemeManager(QObject):
    """Gestor de temas para la aplicación"""
    
    theme_changed = pyqtSignal(str)  # Señal cuando cambia el tema
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings("LocalPDF", "Theme")
        self._theme = self._load_theme()
    
    def _load_theme(self) -> Theme:
        """Carga tema guardado o detecta preferencia del sistema"""
        saved = self.settings.value("theme", None)
        
        if saved:
            return Theme(saved)
        
        # Detectar tema del sistema (Qt 6.5+)
        from PyQt6.QtGui import QPalette, QGuiApplication
        palette = QGuiApplication.palette()
        
        # Si el color del window es oscuro, usar dark mode
        if palette.color(QPalette.ColorRole.Window).lightness() < 128:
            return Theme.DARK
        
        return Theme.LIGHT
    
    @property
    def theme(self) -> Theme:
        return self._theme
    
    def toggle_theme(self):
        """Alterna entre light y dark"""
        if self._theme == Theme.LIGHT:
            self.set_theme(Theme.DARK)
        else:
            self.set_theme(Theme.LIGHT)
    
    def set_theme(self, theme: Theme):
        """Establece un tema específico"""
        if self._theme != theme:
            self._theme = theme
            self.settings.setValue("theme", theme.value)
            self.theme_changed.emit(theme.value)
            self._apply_theme()
    
    def _apply_theme(self):
        """Aplica el tema actual a la aplicación"""
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        
        if self._theme == Theme.DARK:
            app.setStyleSheet(DARK_STYLESHEET)
        else:
            app.setStyleSheet(LIGHT_STYLESHEET)
```

### 7.2 Stylesheets de Apple

```python
# Colores Apple Dark Mode
DARK_COLORS = {
    'black_base': '#000000',
    'elevated_1': '#1C1C1E',
    'elevated_2': '#2C2C2E',
    'elevated_3': '#3A3A3C',
    'separator': '#38383A',
    'label_primary': '#FFFFFF',
    'label_secondary': '#98989D',
    'label_tertiary': '#48484A',
}

LIGHT_COLORS = {
    'white_base': '#FFFFFF',
    'gray_50': '#F9FAFB',
    'gray_100': '#F3F4F6',
    'gray_200': '#E5E7EB',
    'gray_600': '#6B7280',
    'gray_900': '#111827',
}

DARK_STYLESHEET = f"""
    /* Main Window */
    QMainWindow {{
        background-color: {DARK_COLORS['black_base']};
    }}
    
    /* Sidebar */
    QWidget#sidebar {{
        background-color: {DARK_COLORS['elevated_1']};
        border-right: 1px solid {DARK_COLORS['separator']};
    }}
    
    /* Cards */
    QWidget.card {{
        background-color: {DARK_COLORS['elevated_1']};
        border: 1px solid {DARK_COLORS['separator']};
        border-radius: 16px;
    }}
    
    QWidget.card:hover {{
        background-color: {DARK_COLORS['elevated_2']};
    }}
    
    /* Labels */
    QLabel {{
        color: {DARK_COLORS['label_primary']};
    }}
    
    QLabel.secondary {{
        color: {DARK_COLORS['label_secondary']};
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {DARK_COLORS['elevated_2']};
        color: {DARK_COLORS['label_primary']};
        border: 1px solid {DARK_COLORS['separator']};
        border-radius: 12px;
        padding: 12px 16px;
    }}
    
    QPushButton:hover {{
        background-color: {DARK_COLORS['elevated_3']};
    }}
    
    QPushButton:pressed {{
        background-color: {DARK_COLORS['separator']};
    }}
    
    /* Menu Items Activo */
    QPushButton.active {{
        background-color: #FFFFFF;
        color: #000000;
    }}
"""

LIGHT_STYLESHEET = f"""
    /* Main Window */
    QMainWindow {{
        background-color: {LIGHT_COLORS['white_base']};
    }}
    
    /* Sidebar */
    QWidget#sidebar {{
        background-color: {LIGHT_COLORS['white_base']};
        border-right: 1px solid {LIGHT_COLORS['gray_200']};
    }}
    
    /* Cards */
    QWidget.card {{
        background-color: {LIGHT_COLORS['gray_50']};
        border: 1px solid {LIGHT_COLORS['gray_200']};
        border-radius: 16px;
    }}
    
    QWidget.card:hover {{
        background-color: {LIGHT_COLORS['gray_100']};
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {LIGHT_COLORS['gray_100']};
        color: {LIGHT_COLORS['gray_900']};
        border: 1px solid {LIGHT_COLORS['gray_200']};
        border-radius: 12px;
        padding: 12px 16px;
    }}
    
    /* Menu Items Activo */
    QPushButton.active {{
        background-color: #111827;
        color: #FFFFFF;
    }}
"""
```

### 7.3 Toggle Widget en Qt

```python
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QPainter, QColor, QPen

class ThemeToggle(QWidget):
    """Toggle de tema estilo iOS"""
    
    def __init__(self, theme_manager: ThemeManager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setFixedSize(64, 32)
        
        # Estado
        self.is_dark = theme_manager.theme == Theme.DARK
        self.knob_position = 32 if self.is_dark else 0
        
        # Animación del knob
        self.animation = QPropertyAnimation(self, b"knob_pos")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Conectar señal
        theme_manager.theme_changed.connect(self.on_theme_changed)
    
    def mousePressEvent(self, event):
        """Click para cambiar tema"""
        self.theme_manager.toggle_theme()
    
    def on_theme_changed(self, theme: str):
        """Animar cambio de tema"""
        self.is_dark = (theme == "dark")
        target = 32 if self.is_dark else 0
        
        self.animation.setStartValue(self.knob_position)
        self.animation.setEndValue(target)
        self.animation.start()
    
    @property
    def knob_pos(self):
        return self.knob_position
    
    @knob_pos.setter
    def knob_pos(self, value):
        self.knob_position = value
        self.update()  # Repintar
    
    def paintEvent(self, event):
        """Dibuja el toggle"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Track
        track_color = QColor('#374151' if self.is_dark else '#E5E7EB')
        painter.setBrush(track_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, 64, 32, 16, 16)
        
        # Knob
        knob_color = QColor('#111827' if self.is_dark else '#FFFFFF')
        painter.setBrush(knob_color)
        painter.drawEllipse(
            int(self.knob_position) + 4,
            4,
            24,
            24
        )
        
        # Shadow del knob
        # (Implementar con QGraphicsDropShadowEffect si se desea)
```

### 7.4 Aplicación del Tema a Widgets Específicos

```python
class IconContainer(QWidget):
    """Contenedor de icono con inversión automática"""
    
    def __init__(self, icon_path: str, theme_manager: ThemeManager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.icon_path = icon_path
        
        self.setFixedSize(48, 48)
        self.update_style()
        
        # Conectar cambio de tema
        theme_manager.theme_changed.connect(self.update_style)
    
    def update_style(self):
        """Actualiza estilo según tema"""
        is_dark = self.theme_manager.theme == Theme.DARK
        
        bg_color = '#FFFFFF' if is_dark else '#000000'
        icon_color = '#000000' if is_dark else '#FFFFFF'
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 12px;
            }}
        """)
        
        # Recargar icono con color apropiado
        self.load_icon(icon_color)
    
    def load_icon(self, color: str):
        """Carga icono SVG con color específico"""
        # Implementar carga de SVG con color
        pass
```

---

## Resumen de Características

### ✨ Características Implementadas

1. **Sistema de Temas Completo**
   - ✅ ThemeContext con React
   - ✅ Persistencia en localStorage
   - ✅ Detección de preferencia del sistema
   - ✅ Toggle animado estilo iOS

2. **Colores Apple Dark Mode**
   - ✅ Negro base (#000000)
   - ✅ Elevaciones (#1C1C1E, #2C2C2E, #3A3A3C)
   - ✅ Labels con opacidades correctas
   - ✅ Separadores y borders

3. **Inversión de Iconos**
   - ✅ Containers negro → blanco
   - ✅ Iconos blanco → negro
   - ✅ Transición suave 300ms

4. **Componentes Adaptados**
   - ✅ Sidebar completo
   - ✅ Dashboard con gradientes invertidos
   - ✅ Wizard con glassmorphism
   - ✅ Todas las cards y buttons

5. **Transiciones Profesionales**
   - ✅ 300ms consistentes
   - ✅ Spring animations en toggle
   - ✅ Cross-fade de iconos
   - ✅ Sincronización perfecta

6. **Glassmorphism Adaptativo**
   - ✅ Breadcrumb pills
   - ✅ Result panels
   - ✅ Backdrop blur 24px
   - ✅ Opacidades ajustadas

### 🎨 Estética Apple

- Minimalismo extremo
- Elevaciones sutiles
- Gradientes suaves
- Shadows delicadas
- Transiciones fluidas
- Atención al detalle

---

**Documento creado para LocalPDF v5**  
**Versión**: 1.0 Dark Mode  
**Estilo**: Apple iOS Professional  
**Fecha**: Enero 2025
