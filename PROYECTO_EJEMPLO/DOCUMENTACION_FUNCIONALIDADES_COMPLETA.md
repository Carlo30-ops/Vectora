# LocalPDF v5 - Documentación Completa de Funcionalidades

## 📋 Índice General

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura de 8 Módulos](#arquitectura-de-8-módulos)
3. [Asistente Inteligente (Wizard)](#asistente-inteligente-wizard) ⭐
4. [Módulo 1: Operaciones Básicas](#módulo-1-operaciones-básicas)
5. [Módulo 2: Conversiones PDF](#módulo-2-conversiones-pdf)
6. [Módulo 3: Seguridad](#módulo-3-seguridad)
7. [Módulo 4: OCR](#módulo-4-ocr)
8. [Módulo 5: Procesamiento por Lotes](#módulo-5-procesamiento-por-lotes)
9. [Módulo 6: Layout Engine](#módulo-6-layout-engine)
10. [Módulo 7: Workflows Inteligentes](#módulo-7-workflows-inteligentes)
11. [Módulo 8: Dashboard y Navegación](#módulo-8-dashboard-y-navegación)
12. [Sistema de Componentes Compartidos](#sistema-de-componentes-compartidos)
13. [Flujos de Usuario Completos](#flujos-de-usuario-completos)
14. [Implementación Técnica](#implementación-técnica)

---

## Resumen Ejecutivo

### ¿Qué es LocalPDF v5?

**LocalPDF v5** es una aplicación profesional de manipulación de PDFs que funciona **100% offline**, diseñada como referencia visual para una aplicación de escritorio Python 3.10+ con PySide6.

### Características Principales

✅ **100% Offline**: Sin conexión a internet, privacidad total  
✅ **8 Módulos Integrados**: Operaciones completas para PDFs  
✅ **Asistente Inteligente**: Sistema de wizard conversacional  
✅ **Procesamiento por Lotes**: Automatización de operaciones masivas  
✅ **Layout Engine Avanzado**: Análisis de estructura en conversiones  
✅ **OCR con Tesseract**: Reconocimiento óptico de caracteres  
✅ **Diseño iOS Minimalista**: Interfaz profesional en blancos, negros y grises

### Tecnologías (Web - Referencia Visual)

- **Frontend**: React 18 + TypeScript
- **UI**: Tailwind CSS v4
- **Animaciones**: Motion/React (Framer Motion)
- **Componentes**: Biblioteca shadcn/ui personalizada
- **Iconos**: Lucide React (30+ iconos SVG generables)

### Objetivo del Proyecto

Esta aplicación web sirve como **referencia visual pixel-perfect** para implementar la interfaz de usuario en la aplicación de escritorio Python con PySide6, proporcionando:

1. **Diseño visual exacto** con especificaciones detalladas
2. **Lógica funcional** documentada para cada operación
3. **Flujos de usuario** completos y probados
4. **Iconos SVG** generados automáticamente para uso en Qt

---

## Arquitectura de 8 Módulos

LocalPDF v5 está estructurado en 8 módulos principales que cubren todas las necesidades de manipulación de PDFs:

```
┌─────────────────────────────────────────────────────────────┐
│                     LocalPDF v5                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Módulo 1   │  │  Módulo 2   │  │  Módulo 3   │        │
│  │ Operaciones │  │ Conversiones│  │  Seguridad  │        │
│  │   Básicas   │  │     PDF     │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Módulo 4   │  │  Módulo 5   │  │  Módulo 6   │        │
│  │     OCR     │  │  Proc. por  │  │   Layout    │        │
│  │  Tesseract  │  │    Lotes    │  │   Engine    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐                         │
│  │  Módulo 7   │  │  Módulo 8   │                         │
│  │  Workflows  │  │  Dashboard  │                         │
│  │ Inteligentes│  │ & Navegación│                         │
│  └─────────────┘  └─────────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Interconexión de Módulos

- **Dashboard** (Módulo 8) → Punto de entrada a todos los demás
- **Asistente Inteligente** (Módulo 7) → Recomienda módulos específicos
- **Procesamiento por Lotes** (Módulo 5) → Utiliza funciones de Módulos 1-4
- **Layout Engine** (Módulo 6) → Integrado en Conversiones (Módulo 2)

---

## Asistente Inteligente (Wizard) ⭐

### Descripción General

El **Asistente Inteligente** (Wizard) es el componente más innovador de LocalPDF v5. Es un sistema conversacional que guía al usuario a través de preguntas para identificar la operación exacta que necesita, especialmente útil para usuarios que no están familiarizados con terminología técnica.

### Filosofía y Objetivo

**Problema que resuelve**: Muchos usuarios no saben qué operación necesitan:

- "¿Cómo hago que mi PDF sea más pequeño?" → Necesita **Comprimir**
- "Quiero editar el PDF en Word" → Necesita **Convertir PDF a Word**
- "No puedo copiar el texto de mi PDF" → Necesita **OCR**

**Solución**: Sistema de preguntas en lenguaje natural que traduce necesidades en acciones técnicas.

### Arquitectura del Asistente

#### Estructura de Datos

```typescript
interface Question {
  id: string;                    // Identificador único
  question: string;              // Pregunta en lenguaje natural
  options: {
    text: string;                // Texto de la opción
    icon: LucideIcon;            // Icono visual
    result?: ViewType;           // Resultado final (operación)
    nextQuestion?: string;       // ID de siguiente pregunta
  }[];
}

const wizardQuestions: Record<string, Question> = {
  start: { ... },
  convert: { ... },
  // Más preguntas...
}
```

#### Flujo de Navegación del Asistente

```
                    INICIO
                      │
                      ▼
         ┌────────────────────────┐
         │  ¿Qué quieres hacer    │
         │   con tus PDFs?        │
         └────────────────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
    [Combinar]   [Separar]   [Reducir tamaño]
    → MERGE      → SPLIT     → COMPRESS
         │
         ▼
    [Convertir a otro formato]
         │
         ▼
    ┌──────────────────────┐
    │ ¿A qué formato       │
    │ quieres convertir?   │
    └──────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
[PDF→Word] [Word→PDF]
→ CONVERT  → CONVERT
         │
         ▼
    [Proteger]   [OCR]
    → SECURITY   → OCR
         │
         ▼
    ┌──────────────────────┐
    │  ¡Perfecto!          │
    │  Te recomiendo:      │
    │  [Ir a la función]   │
    └──────────────────────┘
```

### Preguntas Implementadas

#### Pregunta Inicial (start)

**Texto**: "¿Qué quieres hacer con tus PDFs?"

**Opciones**:

1. **"Combinar varios archivos en uno"**
   - Icono: Combine (dos archivos uniéndose)
   - Resultado directo: `merge`
   - Acción: Navega a Combinar PDFs

2. **"Separar o extraer páginas"**
   - Icono: Scissors (tijeras)
   - Resultado directo: `split`
   - Acción: Navega a Dividir PDF

3. **"Reducir el tamaño del archivo"**
   - Icono: Archive (archivo comprimido)
   - Resultado directo: `compress`
   - Acción: Navega a Comprimir PDF

4. **"Convertir a otro formato"**
   - Icono: RefreshCw (flechas circulares)
   - Siguiente pregunta: `convert`
   - Acción: Muestra sub-menú de conversión

5. **"Proteger con contraseña"**
   - Icono: Shield (escudo)
   - Resultado directo: `security`
   - Acción: Navega a Seguridad PDF

6. **"Hacer el texto buscable (OCR)"**
   - Icono: ScanText (documento con lupa)
   - Resultado directo: `ocr`
   - Acción: Navega a OCR

#### Pregunta de Conversión (convert)

**Texto**: "¿A qué formato quieres convertir?"

**Opciones**:

1. **"PDF a Word (DOCX)"**
   - Icono: FileText
   - Resultado: `convert` (con configuración PDF→Word)

2. **"Word a PDF"**
   - Icono: FileText
   - Resultado: `convert` (con configuración Word→PDF)

3. **"PDF a Imágenes"**
   - Icono: RefreshCw
   - Resultado: `convert` (con configuración PDF→Images)

4. **"Imágenes a PDF"**
   - Icono: RefreshCw
   - Resultado: `convert` (con configuración Images→PDF)

### Estados del Asistente

#### Estado 1: Pregunta Activa

```typescript
const [currentQuestion, setCurrentQuestion] = useState("start");
const [selectedPath, setSelectedPath] = useState<string[]>([]);
const [isComplete, setIsComplete] = useState(false);
```

**Interfaz mostrada**:

- Card con la pregunta actual
- Grid de opciones (2 columnas en desktop)
- Breadcrumb con el camino seleccionado
- Botón "Volver al inicio" si hay selecciones previas

#### Estado 2: Resultado Final

```typescript
const [recommendedAction, setRecommendedAction] =
  useState<ViewType | null>(null);
```

**Interfaz mostrada**:

- Card de éxito con fondo negro
- Icono de check animado
- Resumen del camino seleccionado
- Botón principal "Ir a la función"
- Botón secundario "Empezar de nuevo"

### Detalles Visuales del Asistente

#### Header del Asistente

```
┌────────────────────────────────────────────────┐
│  ┌──────┐                                      │
│  │ 🪄   │  Asistente Inteligente               │
│  └──────┘  Responde unas preguntas y te       │
│            ayudaré a encontrar la función       │
│            perfecta                             │
└────────────────────────────────────────────────┘
```

**Especificaciones**:

- Icono: 56×56px, fondo negro, rounded-2xl
- Título: text-3xl, font-bold
- Subtítulo: text-gray-600

#### Breadcrumb (Camino Seleccionado)

```
Reducir el tamaño → Convertir a otro formato → PDF a Word
```

**Características**:

- Pills con fondo blanco/60% + backdrop-blur
- Separadores: ChevronRight
- Animación: Fade in/out al cambiar

#### Cards de Opciones

```
┌────────────────────────────────────────┐
│  ┌──────┐                              │
│  │ ICON │  Combinar varios archivos    │
│  └──────┘  en uno                     → │
│                                         │
└────────────────────────────────────────┘
```

**Interactividad**:

- Hover: Escala 1.02, sombra, borde negro
- Click: Escala 0.98
- Icono: Escala 1.10 en hover
- Flecha derecha: Translate-x en hover

#### Pantalla de Resultado

```
┌──────────────────────────────────────────────┐
│              [Fondo Negro]                   │
│                                              │
│           ┌────────────┐                     │
│           │     ✓      │  (Círculo blanco)  │
│           └────────────┘                     │
│                                              │
│       ¡Perfecto! Te recomiendo:             │
│   Basándome en tus respuestas, esta es     │
│        la mejor opción para ti              │
│                                              │
│  ┌─────────────────────────────────────┐   │
│  │  Tu selección:                       │   │
│  │  1. Reducir el tamaño del archivo   │   │
│  │  2. ...                              │   │
│  └─────────────────────────────────────┘   │
│                                              │
│  [🪄 Ir a la función] [Empezar de nuevo]   │
│                                              │
└──────────────────────────────────────────────┘
```

### Lógica de Funcionamiento

#### Selección de Opción

```typescript
const handleOptionSelect = (
  option: (typeof question.options)[0],
) => {
  // 1. Agregar al camino
  const newPath = [...selectedPath, option.text];
  setSelectedPath(newPath);

  // 2. Verificar si es resultado final
  if (option.result) {
    setRecommendedAction(option.result);
    setIsComplete(true); // Mostrar pantalla de éxito
  }
  // 3. O continuar al siguiente nivel
  else if (option.nextQuestion) {
    setCurrentQuestion(option.nextQuestion);
  }
};
```

#### Navegación a la Función

```typescript
const handleGoToAction = () => {
  if (recommendedAction) {
    onNavigate(recommendedAction); // Cambia vista en App.tsx
  }
};
```

#### Reinicio

```typescript
const handleReset = () => {
  setCurrentQuestion("start");
  setSelectedPath([]);
  setIsComplete(false);
  setRecommendedAction(null);
};
```

### Animaciones del Asistente

#### Transiciones entre Preguntas

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

- Pregunta saliente: Fade out + slide izquierda
- Pregunta entrante: Fade in + slide desde derecha
- Duración: 300ms

#### Aparición de Opciones

```typescript
{question.options.map((option, index) => (
  <motion.button
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: index * 0.1 }}
  >
```

- Stagger animation: Cada opción aparece 100ms después
- Movimiento: Y: 20→0px
- Opacidad: 0→1

#### Pantalla de Resultado

```typescript
<motion.div
  initial={{ opacity: 0, scale: 0.9 }}
  animate={{ opacity: 1, scale: 1 }}
  transition={{ duration: 0.4 }}
>
```

- Zoom desde 90% a 100%
- Fade in simultáneo

#### Check Animado

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

- Spring animation (rebote)
- Delay de 200ms
- Stiffness alta para efecto "pop"

### Card de Ayuda

Al final del asistente, siempre visible:

```
┌──────────────────────────────────────────────┐
│  ✨  Sugerencia                              │
│                                              │
│  Si no estás seguro de qué operación        │
│  necesitas, este asistente te ayudará a     │
│  descubrir la mejor función para tu caso    │
│  específico. Simplemente responde las       │
│  preguntas y te guiaremos al lugar correcto.│
└──────────────────────────────────────────────┘
```

### Casos de Uso del Asistente

#### Caso 1: Usuario Inexperto

**Escenario**: Usuario tiene un PDF escaneado y quiere editar el texto.

**Flujo**:

1. Entra al Asistente
2. Ve opciones en lenguaje simple
3. No encuentra "editar", pero ve "Hacer el texto buscable (OCR)"
4. Selecciona OCR
5. Sistema explica que OCR hace el texto seleccionable
6. Usuario aplica OCR
7. Luego usa "Convertir a Word" para editar

#### Caso 2: Usuario Confundido entre Opciones

**Escenario**: Usuario quiere "hacer el PDF más liviano".

**Flujo**:

1. Lee "Reducir el tamaño del archivo"
2. Reconoce que eso es lo que necesita
3. Selecciona → Ir a Comprimir
4. Sin necesidad de saber el término "comprimir"

#### Caso 3: Conversión Específica

**Escenario**: Usuario quiere convertir Word a PDF.

**Flujo**:

1. Selecciona "Convertir a otro formato"
2. Segunda pregunta: "¿A qué formato?"
3. Selecciona "Word a PDF"
4. Navega directamente a Convertir con la configuración correcta

### Expansibilidad del Asistente

El sistema está diseñado para crecer fácilmente:

```typescript
// Agregar nueva pregunta intermedia
const wizardQuestions: Record<string, Question> = {
  start: { ... },
  convert: { ... },
  // Nueva rama de seguridad
  security_options: {
    id: 'security_options',
    question: '¿Qué tipo de protección necesitas?',
    options: [
      { text: 'Solo lectura', result: 'security' },
      { text: 'Encriptación completa', result: 'security' },
      { text: 'Proteger impresión', result: 'security' },
    ]
  }
};
```

### Métricas de Éxito del Asistente

En una implementación completa, el asistente podría trackear:

1. **Tasa de uso**: % de usuarios que usan el wizard vs menú directo
2. **Tasa de completación**: % que llegan a "Ir a la función"
3. **Rutas más comunes**: Qué caminos se seleccionan más
4. **Puntos de abandono**: Dónde los usuarios se detienen

### Implementación PySide6

#### Estructura de Clases

```python
class WizardDialog(QDialog):
    """Diálogo del Asistente Inteligente"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_question = "start"
        self.selected_path = []
        self.recommended_action = None

        self.setup_ui()
        self.show_question("start")

    def setup_ui(self):
        """Configura la interfaz"""
        layout = QVBoxLayout()

        # Header
        self.header = self.create_header()
        layout.addWidget(self.header)

        # Breadcrumb
        self.breadcrumb = QLabel()
        layout.addWidget(self.breadcrumb)

        # Contenedor de preguntas (QStackedWidget)
        self.question_stack = QStackedWidget()
        layout.addWidget(self.question_stack)

        self.setLayout(layout)

    def show_question(self, question_id: str):
        """Muestra una pregunta específica"""
        question_data = WIZARD_QUESTIONS[question_id]

        # Crear widget de pregunta
        question_widget = QWidget()
        q_layout = QVBoxLayout()

        # Título de pregunta
        title = QLabel(question_data['question'])
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        q_layout.addWidget(title)

        # Grid de opciones
        grid = QGridLayout()
        for i, option in enumerate(question_data['options']):
            btn = self.create_option_button(option)
            grid.addWidget(btn, i // 2, i % 2)

        q_layout.addLayout(grid)
        question_widget.setLayout(q_layout)
        self.question_stack.addWidget(question_widget)

    def create_option_button(self, option: dict) -> QPushButton:
        """Crea botón de opción con icono y texto"""
        btn = QPushButton()
        btn.clicked.connect(
            lambda: self.handle_option_select(option)
        )

        # Layout del botón
        layout = QHBoxLayout()
        icon_label = QLabel()
        # Cargar SVG del icono
        icon_label.setPixmap(QPixmap(f"icons/{option['icon']}.svg"))
        layout.addWidget(icon_label)

        text_label = QLabel(option['text'])
        layout.addWidget(text_label)

        btn.setLayout(layout)
        return btn

    def handle_option_select(self, option: dict):
        """Maneja selección de opción"""
        self.selected_path.append(option['text'])
        self.update_breadcrumb()

        if 'result' in option:
            # Resultado final
            self.recommended_action = option['result']
            self.show_result()
        elif 'next_question' in option:
            # Siguiente pregunta
            self.show_question(option['next_question'])

    def show_result(self):
        """Muestra pantalla de resultado final"""
        result_widget = ResultWidget(
            self.selected_path,
            self.recommended_action
        )
        result_widget.go_to_action.connect(self.navigate_to_action)
        self.question_stack.addWidget(result_widget)
        self.question_stack.setCurrentWidget(result_widget)

    def navigate_to_action(self):
        """Navega a la operación recomendada"""
        self.accept()  # Cierra el diálogo
        # Emitir señal al MainWindow
        self.parent().navigate_to_operation(self.recommended_action)
```

#### Datos del Wizard

```python
WIZARD_QUESTIONS = {
    'start': {
        'id': 'start',
        'question': '¿Qué quieres hacer con tus PDFs?',
        'options': [
            {
                'text': 'Combinar varios archivos en uno',
                'icon': 'combine',
                'result': 'merge'
            },
            {
                'text': 'Separar o extraer páginas',
                'icon': 'scissors',
                'result': 'split'
            },
            {
                'text': 'Reducir el tamaño del archivo',
                'icon': 'archive',
                'result': 'compress'
            },
            {
                'text': 'Convertir a otro formato',
                'icon': 'refresh',
                'next_question': 'convert'
            },
            {
                'text': 'Proteger con contraseña',
                'icon': 'shield',
                'result': 'security'
            },
            {
                'text': 'Hacer el texto buscable (OCR)',
                'icon': 'scan',
                'result': 'ocr'
            }
        ]
    },
    'convert': {
        'id': 'convert',
        'question': '¿A qué formato quieres convertir?',
        'options': [
            {
                'text': 'PDF a Word (DOCX)',
                'icon': 'file-text',
                'result': 'convert',
                'config': {'mode': 'pdf-to-word'}
            },
            {
                'text': 'Word a PDF',
                'icon': 'file-text',
                'result': 'convert',
                'config': {'mode': 'word-to-pdf'}
            },
            {
                'text': 'PDF a Imágenes',
                'icon': 'image',
                'result': 'convert',
                'config': {'mode': 'pdf-to-images'}
            },
            {
                'text': 'Imágenes a PDF',
                'icon': 'image',
                'result': 'convert',
                'config': {'mode': 'images-to-pdf'}
            }
        ]
    }
}
```

---

## Módulo 1: Operaciones Básicas

### 1.1 Combinar PDFs (Merge)

#### Descripción Funcional

Combina múltiples archivos PDF en un solo documento, preservando el orden definido por el usuario.

#### Características

- **Archivos múltiples**: Hasta 20 PDFs simultáneos
- **Reordenamiento**: Drag & drop para cambiar orden
- **Preview**: Lista visual de archivos con miniaturas
- **Progreso**: Barra de progreso en tiempo real

#### Flujo de Usuario

```
1. Seleccionar Archivos
   │
   ├─ Drag & Drop área
   │  └─ O selección desde explorador
   │
2. Ordenar Archivos
   │
   ├─ Arrastrar items para reordenar
   │  └─ Vista: Icono grip + Nombre + Tamaño + Número de páginas
   │
3. Iniciar Combinación
   │
   ├─ Click en "Combinar PDFs"
   │  ├─ Validación: Mínimo 2 archivos
   │  └─ Progreso: 0% → 100%
   │
4. Resultado
   │
   └─ Download archivo: "combined_document.pdf"
```

#### Estados

```typescript
const [files, setFiles] = useState<File[]>([]);
const [isProcessing, setIsProcessing] = useState(false);
const [progress, setProgress] = useState(0);
const [isComplete, setIsComplete] = useState(false);
```

#### Interfaz

**Header**:

- Icono: Combine (56×56px, fondo negro)
- Título: "Combinar PDFs"
- Descripción: "Une múltiples archivos PDF en uno solo"

**Dropzone**:

- Texto: "Arrastra tus PDFs aquí"
- Subtexto: "o haz clic para seleccionar archivos"
- Accept: `.pdf`
- Límite: 20 archivos

**Lista Reordenable** (Motion/React Reorder):

```
┌────────────────────────────────────────────┐
│  Orden de combinación (arrastra para      │
│  reordenar)                                │
├────────────────────────────────────────────┤
│  ≡  1. documento1.pdf        45 páginas   │
│  ≡  2. reporte.pdf           12 páginas   │
│  ≡  3. anexos.pdf             8 páginas   │
└────────────────────────────────────────────┘
```

**Progreso**:

```
Combinando archivos...
[████████████░░░░░░░░] 65%
```

**Resultado**:

```
┌────────────────────────────────────────────┐
│  ✓ ¡PDFs combinados exitosamente!         │
│                                            │
│  Archivo final: combined_document.pdf     │
│  Total de páginas: 65                     │
│                                            │
│  [⬇ Descargar]                            │
└────────────────────────────────────────────┘
```

#### Implementación Python

```python
from PyPDF2 import PdfMerger
from pathlib import Path

def merge_pdfs(file_paths: list[str], output_path: str) -> dict:
    """
    Combina múltiples PDFs en uno solo

    Args:
        file_paths: Lista de rutas de archivos PDF
        output_path: Ruta del archivo de salida

    Returns:
        dict con información del resultado
    """
    merger = PdfMerger()
    total_pages = 0

    try:
        for file_path in file_paths:
            merger.append(file_path)
            # Obtener número de páginas para tracking
            reader = PdfReader(file_path)
            total_pages += len(reader.pages)

        merger.write(output_path)
        merger.close()

        return {
            'success': True,
            'output_file': output_path,
            'total_pages': total_pages,
            'files_merged': len(file_paths)
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
```

### 1.2 Dividir PDF (Split)

#### Descripción Funcional

Extrae páginas específicas de un PDF o divide el documento en múltiples archivos según diferentes criterios.

#### Modos de División

1. **Por Rango**: Extrae páginas del X al Y
2. **Páginas Específicas**: Extrae páginas individuales (ej: 1,3,5,7-10)
3. **Cada N páginas**: Divide en bloques de N páginas

#### Interfaz - Tabs

```
┌────────────────────────────────────────────┐
│  [Por Rango]  [Páginas Específicas]  [Cada N]
├────────────────────────────────────────────┤
│                                            │
│  Tab 1: Por Rango                          │
│  ┌──────────────────────────────────────┐ │
│  │  Página inicial: [  1  ]             │ │
│  │  Página final:   [ 10  ]             │ │
│  │                                      │ │
│  │  Se extraerá: Páginas 1-10           │ │
│  └──────────────────────────────────────┘ │
│                                            │
└────────────────────────────────────────────┘
```

#### Implementación

```python
def split_pdf_by_range(
    input_path: str,
    start_page: int,
    end_page: int,
    output_path: str
) -> dict:
    """Divide PDF extrayendo un rango de páginas"""
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Validaciones
    if start_page < 1 or end_page > len(reader.pages):
        return {'success': False, 'error': 'Rango inválido'}

    # Extraer páginas (índices base-0)
    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])

    # Guardar
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    return {
        'success': True,
        'output_file': output_path,
        'pages_extracted': end_page - start_page + 1
    }

def split_pdf_by_pages(
    input_path: str,
    page_numbers: list[int],
    output_dir: str
) -> dict:
    """Divide PDF extrayendo páginas específicas"""
    reader = PdfReader(input_path)
    results = []

    for page_num in page_numbers:
        if page_num < 1 or page_num > len(reader.pages):
            continue

        writer = PdfWriter()
        writer.add_page(reader.pages[page_num - 1])

        output_path = Path(output_dir) / f"page_{page_num}.pdf"
        with open(output_path, 'wb') as f:
            writer.write(f)

        results.append(str(output_path))

    return {
        'success': True,
        'files_created': results,
        'count': len(results)
    }
```

### 1.3 Comprimir PDF

#### Descripción Funcional

Reduce el tamaño del archivo PDF optimizando imágenes y eliminando datos redundantes.

#### Niveles de Compresión

```python
COMPRESSION_LEVELS = {
    'low': {
        'value': 25,
        'label': 'Baja',
        'reduction': '~20%',
        'quality': 'Alta calidad',
        'image_quality': 95
    },
    'medium': {
        'value': 50,
        'label': 'Media',
        'reduction': '~40%',
        'quality': 'Calidad equilibrada',
        'image_quality': 85
    },
    'high': {
        'value': 75,
        'label': 'Alta',
        'reduction': '~60%',
        'quality': 'Compresión fuerte',
        'image_quality': 70
    },
    'extreme': {
        'value': 100,
        'label': 'Extrema',
        'reduction': '~80%',
        'quality': 'Máxima compresión',
        'image_quality': 50
    }
}
```

#### Interfaz - Slider

```
┌────────────────────────────────────────────┐
│  Nivel de compresión                       │
│                                            │
│  [━━━━━━━━━━━○━━━━━━━━━━━]  Media         │
│                                            │
│  📊  Reducción estimada: ~40%              │
│  ⭐  Calidad: Equilibrada                  │
│                                            │
│  Tamaño original:    5.2 MB                │
│  Tamaño estimado:    3.1 MB                │
│  Ahorro:             2.1 MB (40%)          │
└────────────────────────────────────────────┘
```

#### Implementación

```python
from pikepdf import Pdf

def compress_pdf(
    input_path: str,
    output_path: str,
    compression_level: str = 'medium'
) -> dict:
    """
    Comprime un PDF

    Args:
        input_path: Ruta del PDF original
        output_path: Ruta del PDF comprimido
        compression_level: 'low', 'medium', 'high', 'extreme'
    """
    level_config = COMPRESSION_LEVELS[compression_level]

    # Abrir PDF
    pdf = Pdf.open(input_path)

    # Optimizar cada página
    for page in pdf.pages:
        # Comprimir imágenes
        for img_key in page.images.keys():
            img = page.images[img_key]
            # Reducir calidad de imagen
            # (Lógica de compresión de imágenes)

    # Guardar con compresión
    pdf.save(
        output_path,
        compress_streams=True,
        stream_decode_level=pikepdf.StreamDecodeLevel.generalized
    )
    pdf.close()

    # Calcular estadísticas
    original_size = Path(input_path).stat().st_size
    compressed_size = Path(output_path).stat().st_size
    reduction = (1 - compressed_size / original_size) * 100

    return {
        'success': True,
        'original_size': original_size,
        'compressed_size': compressed_size,
        'reduction_percentage': reduction,
        'savings_bytes': original_size - compressed_size
    }
```

---

## Módulo 2: Conversiones PDF

### Descripción General

El módulo de conversiones maneja transformaciones bidireccionales entre PDFs y otros formatos, con énfasis en preservar la estructura del documento mediante el **Layout Engine**.

### Tipos de Conversión Soportados

```
PDF ←→ Word (DOCX)
PDF  →  Imágenes (PNG, JPG)
Imágenes → PDF
```

### 2.1 PDF a Word (con Layout Engine)

#### Descripción

Convierte documentos PDF a formato DOCX editable, analizando y preservando:

- Estructura de párrafos
- Estilos de texto (negrita, cursiva, tamaños)
- Tablas y su formato
- Imágenes y su posición
- Encabezados y pies de página

#### Fases de Conversión

```
1. ANÁLISIS DE ESTRUCTURA (Layout Engine)
   │
   ├─ Detección de bloques de texto
   ├─ Identificación de columnas
   ├─ Reconocimiento de tablas
   ├─ Ubicación de imágenes
   └─ Análisis de jerarquía (H1, H2, párrafos)
   │
2. EXTRACCIÓN DE CONTENIDO
   │
   ├─ Texto con formato
   ├─ Imágenes embebidas
   └─ Metadatos
   │
3. GENERACIÓN DOCX
   │
   ├─ Creación de documento Word
   ├─ Aplicación de estilos
   ├─ Inserción de elementos
   └─ Preservación de layout
   │
4. SALIDA
   └─ Archivo .docx editable
```

#### Interfaz - Selección de Tipo

```
┌────────────────────────────────────────────┐
│  Tipo de conversión                        │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────────┐  ┌──────────────┐   │
│  │ [SELECCIONADO]   │  │              │   │
│  │                  │  │              │   │
│  │  📄  PDF → Word  │  │ 📄 Word → PDF│   │
│  │                  │  │              │   │
│  │  Convierte PDF a │  │              │   │
│  │  formato DOCX    │  │              │   │
│  │  editable        │  │              │   │
│  └──────────────────┘  └──────────────┘   │
│                                            │
│  ┌──────────────────┐  ┌──────────────┐   │
│  │  🖼️ PDF→Imágenes │  │ 🖼️ Img→PDF   │   │
│  └──────────────────┘  └──────────────┘   │
└────────────────────────────────────────────┘
```

#### Progreso con Layout Engine

```
Procesando documento...

[████░░░░░░░░░░░░░░] 25% - Analizando estructura...
[████████░░░░░░░░░░] 50% - Aplicando Layout Engine...
[████████████░░░░░░] 75% - Generando archivo final...
[██████████████████] 100% - ¡Conversión completada!
```

#### Implementación

```python
from pdf2docx import Converter
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.high_level import extract_pages

class LayoutEngine:
    """Motor de análisis de estructura de PDF"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.layout_params = LAParams(
            line_margin=0.5,
            word_margin=0.1,
            char_margin=2.0,
            boxes_flow=0.5
        )

    def analyze_structure(self) -> dict:
        """
        Analiza la estructura del PDF

        Returns:
            dict con información de layout:
            - blocks: Bloques de texto detectados
            - tables: Tablas identificadas
            - images: Posiciones de imágenes
            - columns: Número de columnas por página
        """
        structure = {
            'pages': [],
            'has_tables': False,
            'has_columns': False,
            'total_images': 0
        }

        for page_num, page_layout in enumerate(
            extract_pages(self.pdf_path, laparams=self.layout_params)
        ):
            page_info = {
                'page_number': page_num + 1,
                'width': page_layout.width,
                'height': page_layout.height,
                'blocks': [],
                'images': []
            }

            # Analizar elementos de la página
            for element in page_layout:
                if isinstance(element, LTTextBox):
                    # Bloque de texto
                    block = {
                        'type': 'text',
                        'x0': element.x0,
                        'y0': element.y0,
                        'x1': element.x1,
                        'y1': element.y1,
                        'text': element.get_text()
                    }
                    page_info['blocks'].append(block)

                # Detectar columnas
                if self._detect_columns(page_layout):
                    structure['has_columns'] = True

            structure['pages'].append(page_info)

        return structure

    def _detect_columns(self, page_layout) -> bool:
        """Detecta si la página tiene múltiples columnas"""
        # Lógica de detección de columnas
        # Analiza distribución horizontal de bloques de texto
        pass

def convert_pdf_to_word(
    input_pdf: str,
    output_docx: str,
    use_layout_engine: bool = True
) -> dict:
    """
    Convierte PDF a Word con análisis de estructura

    Args:
        input_pdf: Ruta del PDF de entrada
        output_docx: Ruta del DOCX de salida
        use_layout_engine: Si debe usar análisis avanzado
    """

    if use_layout_engine:
        # 1. Analizar estructura
        engine = LayoutEngine(input_pdf)
        structure = engine.analyze_structure()

        # 2. Convertir con configuración optimizada
        cv = Converter(input_pdf)
        cv.convert(
            output_docx,
            start=0,
            end=None,
            multi_processing=True
        )
        cv.close()

        return {
            'success': True,
            'output_file': output_docx,
            'structure_info': structure,
            'has_tables': structure['has_tables'],
            'has_columns': structure['has_columns'],
            'total_pages': len(structure['pages'])
        }
    else:
        # Conversión simple
        cv = Converter(input_pdf)
        cv.convert(output_docx)
        cv.close()

        return {
            'success': True,
            'output_file': output_docx
        }
```

### 2.2 Word a PDF

#### Implementación

```python
from docx2pdf import convert as docx_to_pdf_convert

def convert_word_to_pdf(
    input_docx: str,
    output_pdf: str
) -> dict:
    """Convierte Word a PDF"""
    try:
        docx_to_pdf_convert(input_docx, output_pdf)

        return {
            'success': True,
            'output_file': output_pdf,
            'file_size': Path(output_pdf).stat().st_size
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
```

### 2.3 PDF a Imágenes

#### Implementación

```python
from pdf2image import convert_from_path

def convert_pdf_to_images(
    input_pdf: str,
    output_dir: str,
    dpi: int = 300,
    format: str = 'PNG'
) -> dict:
    """
    Convierte cada página del PDF a imagen

    Args:
        input_pdf: Ruta del PDF
        output_dir: Directorio de salida
        dpi: Resolución (300 recomendado para calidad)
        format: PNG o JPEG
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Convertir páginas
    images = convert_from_path(
        input_pdf,
        dpi=dpi,
        fmt=format.lower()
    )

    image_files = []
    for i, image in enumerate(images):
        output_file = output_path / f"page_{i+1}.{format.lower()}"
        image.save(output_file, format)
        image_files.append(str(output_file))

    return {
        'success': True,
        'images_created': len(image_files),
        'files': image_files,
        'dpi': dpi
    }
```

### 2.4 Imágenes a PDF

#### Implementación

```python
from PIL import Image

def convert_images_to_pdf(
    image_paths: list[str],
    output_pdf: str
) -> dict:
    """
    Combina múltiples imágenes en un PDF

    Args:
        image_paths: Lista de rutas de imágenes
        output_pdf: Ruta del PDF de salida
    """
    images = []

    # Cargar y convertir imágenes a RGB
    for img_path in image_paths:
        img = Image.open(img_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        images.append(img)

    # Guardar como PDF
    if images:
        images[0].save(
            output_pdf,
            save_all=True,
            append_images=images[1:] if len(images) > 1 else []
        )

    return {
        'success': True,
        'output_file': output_pdf,
        'pages': len(images)
    }
```

---

## Módulo 3: Seguridad

### Descripción General

Manejo completo de seguridad en PDFs: encriptación, desencriptación y configuración de permisos.

### Modos de Seguridad

```
1. ENCRIPTAR    - Protege con contraseña
2. DESENCRIPTAR - Remueve protección
3. PERMISOS     - Configura restricciones específicas
```

### 3.1 Encriptar PDF

#### Interfaz

```
┌────────────────────────────────────────────┐
│  🔒 Encriptar PDF                          │
├────────────────────────────────────────────┤
│                                            │
│  Contraseña:                               │
│  [•••••••••••]  👁️ Mostrar                │
│                                            │
│  Confirmar contraseña:                     │
│  [•••••••••••]                             │
│                                            │
│  ℹ️  La contraseña debe tener al menos    │
│      8 caracteres                          │
│                                            │
│  [Encriptar PDF]                           │
└────────────────────────────────────────────┘
```

#### Implementación

```python
from PyPDF2 import PdfReader, PdfWriter

def encrypt_pdf(
    input_path: str,
    output_path: str,
    password: str
) -> dict:
    """
    Encripta un PDF con contraseña

    Args:
        input_path: PDF original
        output_path: PDF encriptado
        password: Contraseña de protección
    """
    # Validación de contraseña
    if len(password) < 8:
        return {
            'success': False,
            'error': 'La contraseña debe tener al menos 8 caracteres'
        }

    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Copiar todas las páginas
    for page in reader.pages:
        writer.add_page(page)

    # Encriptar
    writer.encrypt(
        user_password=password,
        owner_password=password,
        algorithm="AES-256"
    )

    # Guardar
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    return {
        'success': True,
        'output_file': output_path,
        'encryption': 'AES-256'
    }
```

### 3.2 Desencriptar PDF

#### Implementación

```python
def decrypt_pdf(
    input_path: str,
    output_path: str,
    password: str
) -> dict:
    """
    Remueve la encriptación de un PDF

    Args:
        input_path: PDF encriptado
        output_path: PDF sin encriptar
        password: Contraseña del PDF
    """
    try:
        reader = PdfReader(input_path)

        # Verificar si está encriptado
        if not reader.is_encrypted:
            return {
                'success': False,
                'error': 'El PDF no está encriptado'
            }

        # Desencriptar
        if not reader.decrypt(password):
            return {
                'success': False,
                'error': 'Contraseña incorrecta'
            }

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        # Guardar sin encriptación
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return {
            'success': True,
            'output_file': output_path
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
```

### 3.3 Configurar Permisos

#### Interfaz

```
┌────────────────────────────────────────────┐
│  🛡️ Configurar Permisos                    │
├────────────────────────────────────────────┤
│                                            │
│  Contraseña de propietario:                │
│  [•••••••••••]                             │
│                                            │
│  Permisos permitidos:                      │
│                                            │
│  ✅ Permitir impresión                     │
│  ✅ Permitir copiar texto                  │
│  ❌ Permitir modificación                  │
│  ✅ Permitir anotaciones                   │
│                                            │
│  [Aplicar Permisos]                        │
└────────────────────────────────────────────┘
```

#### Implementación

```python
def set_pdf_permissions(
    input_path: str,
    output_path: str,
    owner_password: str,
    allow_printing: bool = True,
    allow_copy: bool = True,
    allow_modify: bool = False,
    allow_annotations: bool = True
) -> dict:
    """
    Configura permisos específicos en un PDF
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Configurar permisos
    permissions = 0
    if allow_printing:
        permissions |= 0b000000000100  # Bit de impresión
    if allow_copy:
        permissions |= 0b000000010000  # Bit de copia
    if allow_modify:
        permissions |= 0b000000001000  # Bit de modificación
    if allow_annotations:
        permissions |= 0b000000100000  # Bit de anotaciones

    writer.encrypt(
        user_password="",  # Sin contraseña de usuario
        owner_password=owner_password,
        permissions_flag=permissions
    )

    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    return {
        'success': True,
        'output_file': output_path,
        'permissions': {
            'print': allow_printing,
            'copy': allow_copy,
            'modify': allow_modify,
            'annotations': allow_annotations
        }
    }
```

---

## Módulo 4: OCR

### Descripción General

Reconocimiento Óptico de Caracteres (OCR) para convertir PDFs escaneados en documentos con texto buscable y seleccionable, usando **Tesseract OCR**.

### Características Principales

- **Detección automática**: Identifica páginas que necesitan OCR
- **Multiidioma**: Soporte para 6+ idiomas
- **Preservación**: Mantiene diseño original del PDF
- **Capa de texto**: Añade texto invisible sobre la imagen

### Idiomas Soportados

```python
LANGUAGES = [
    {'code': 'spa', 'name': 'Español'},
    {'code': 'eng', 'name': 'Inglés'},
    {'code': 'por', 'name': 'Portugués'},
    {'code': 'fra', 'name': 'Francés'},
    {'code': 'deu', 'name': 'Alemán'},
    {'code': 'ita', 'name': 'Italiano'},
]
```

### Flujo de OCR

```
1. DETECCIÓN
   │
   ├─ Analizar cada página
   ├─ Identificar si es imagen escaneada
   └─ Contar páginas que necesitan OCR
   │
2. PROCESAMIENTO
   │
   ├─ Por cada página detectada:
   │  ├─ Convertir a imagen
   │  ├─ Aplicar Tesseract OCR
   │  ├─ Extraer texto y coordenadas
   │  └─ Crear capa de texto invisible
   │
3. GENERACIÓN
   │
   ├─ Combinar imagen original + texto
   ├─ Preservar páginas sin OCR
   └─ Generar PDF con capa de texto
   │
4. RESULTADO
   └─ PDF buscable y seleccionable
```

### Interfaz

```
┌────────────────────────────────────────────┐
│  📱 OCR - Reconocimiento de Texto          │
├────────────────────────────────────────────┤
│                                            │
│  ℹ️  Detección Automática                  │
│  LocalPDF detecta automáticamente si tu   │
│  PDF contiene páginas escaneadas y aplica │
│  OCR solo donde es necesario.             │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  Idioma del documento:                     │
│  [Español ▼]                               │
│                                            │
│  [Seleccionar archivo PDF]                │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  Estado del procesamiento:                 │
│                                            │
│  📄 Páginas detectadas: 15                 │
│  ✅ Páginas procesadas: 8/15               │
│                                            │
│  Detectando páginas escaneadas...          │
│  Aplicando OCR con Tesseract...            │
│  Extrayendo texto...                       │
│  Generando PDF con capa de texto...        │
│                                            │
│  [████████████░░░░░░] 60%                  │
│                                            │
└────────────────────────────────────────────┘
```

### Implementación

```python
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class OCRProcessor:
    """Procesador de OCR para PDFs"""

    def __init__(self, tesseract_path: str = None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def detect_scanned_pages(self, pdf_path: str) -> list[int]:
        """
        Detecta qué páginas son imágenes escaneadas

        Returns:
            Lista de números de página que necesitan OCR
        """
        reader = PdfReader(pdf_path)
        scanned_pages = []

        for page_num, page in enumerate(reader.pages):
            # Extraer texto existente
            text = page.extract_text()

            # Si hay muy poco texto, probablemente es escaneado
            if len(text.strip()) < 50:  # Umbral ajustable
                scanned_pages.append(page_num + 1)

        return scanned_pages

    def apply_ocr(
        self,
        input_pdf: str,
        output_pdf: str,
        language: str = 'spa',
        progress_callback = None
    ) -> dict:
        """
        Aplica OCR a un PDF

        Args:
            input_pdf: Ruta del PDF original
            output_pdf: Ruta del PDF con OCR
            language: Código de idioma Tesseract
            progress_callback: Función para reportar progreso
        """
        # 1. Detectar páginas escaneadas
        scanned_pages = self.detect_scanned_pages(input_pdf)

        if not scanned_pages:
            return {
                'success': True,
                'message': 'No se detectaron páginas escaneadas',
                'pages_processed': 0
            }

        # 2. Convertir PDF a imágenes
        images = convert_from_path(
            input_pdf,
            dpi=300,  # Alta resolución para mejor OCR
            first_page=min(scanned_pages),
            last_page=max(scanned_pages)
        )

        # 3. Aplicar OCR a cada página
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        total_pages = len(reader.pages)
        scanned_index = 0

        for page_num in range(total_pages):
            if (page_num + 1) in scanned_pages:
                # Aplicar OCR
                image = images[scanned_index]
                ocr_data = pytesseract.image_to_data(
                    image,
                    lang=language,
                    output_type=pytesseract.Output.DICT
                )

                # Crear página con capa de texto
                page_with_text = self._create_searchable_page(
                    reader.pages[page_num],
                    ocr_data,
                    image.size
                )
                writer.add_page(page_with_text)

                scanned_index += 1

                # Reportar progreso
                if progress_callback:
                    progress = ((page_num + 1) / total_pages) * 100
                    progress_callback(
                        progress,
                        f"Procesando página {page_num + 1}/{total_pages}"
                    )
            else:
                # Página ya tiene texto, copiar directamente
                writer.add_page(reader.pages[page_num])

        # 4. Guardar resultado
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

        return {
            'success': True,
            'pages_processed': len(scanned_pages),
            'total_pages': total_pages,
            'output_file': output_pdf
        }

    def _create_searchable_page(
        self,
        original_page,
        ocr_data: dict,
        image_size: tuple
    ):
        """
        Crea una página con capa de texto invisible
        sobre la imagen original
        """
        # Crear un PDF temporal con el texto
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=image_size)

        # Configurar texto invisible
        can.setFillColorRGB(0, 0, 0, alpha=0)  # Transparente

        # Añadir cada palabra detectada por OCR
        n_boxes = len(ocr_data['text'])
        for i in range(n_boxes):
            if int(ocr_data['conf'][i]) > 60:  # Confianza > 60%
                text = ocr_data['text'][i]
                x, y = ocr_data['left'][i], ocr_data['top'][i]
                w, h = ocr_data['width'][i], ocr_data['height'][i]

                can.drawString(x, image_size[1] - y, text)

        can.save()

        # Combinar con página original
        packet.seek(0)
        text_pdf = PdfReader(packet)
        original_page.merge_page(text_pdf.pages[0])

        return original_page

# Uso
def perform_ocr(
    input_pdf: str,
    output_pdf: str,
    language: str = 'spa'
) -> dict:
    """Función principal de OCR"""
    processor = OCRProcessor()

    result = processor.apply_ocr(
        input_pdf,
        output_pdf,
        language=language,
        progress_callback=lambda p, msg: print(f"{p:.0f}%: {msg}")
    )

    return result
```

### Configuración de Tesseract

#### Windows

```batch
REM Instalar Tesseract
REM Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki

REM Configurar path en Python
set TESSERACT_PATH="C:\Program Files\Tesseract-OCR\tesseract.exe"
```

#### Linux/Mac

```bash
# Instalar Tesseract
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-spa  # Idioma español

# Tesseract se encuentra automáticamente en PATH
```

---

## Módulo 5: Procesamiento por Lotes

### Descripción General

Automatiza operaciones en múltiples archivos simultáneamente, con seguimiento individual de progreso y modo "carpeta vigilada" para procesamiento continuo.

### Operaciones por Lotes Soportadas

```python
BATCH_OPERATIONS = {
    'merge': 'Combinar todos los archivos en uno',
    'compress': 'Comprimir cada archivo individualmente',
    'convert': 'Convertir cada archivo a Word',
    'ocr': 'Aplicar OCR a todos',
    'encrypt': 'Encriptar todos con la misma contraseña'
}
```

### Características Principales

- **Procesamiento paralelo**: Múltiples archivos simultáneamente
- **Tracking individual**: Estado de cada archivo
- **Carpeta vigilada**: Procesa automáticamente archivos nuevos
- **Límite**: Hasta 50 archivos por lote

### Interfaz

```
┌────────────────────────────────────────────┐
│  📁 Procesamiento por Lotes                │
├────────────────────────────────────────────┤
│                                            │
│  Operación a realizar:                     │
│  [Comprimir cada uno ▼]                    │
│   ├─ Combinar todos                        │
│   ├─ Comprimir cada uno                    │
│   ├─ Convertir a Word                      │
│   ├─ Aplicar OCR                           │
│   └─ Encriptar todos                       │
│                                            │
│  🗂️ Carpeta vigilada         [Toggle: OFF]│
│   Procesa automáticamente archivos nuevos │
│                                            │
│  [Seleccionar múltiples archivos]         │
│   (máximo 50 archivos)                    │
│                                            │
├────────────────────────────────────────────┤
│  Estado del procesamiento:                 │
├────────────────────────────────────────────┤
│                                            │
│  ⏱️ documento1.pdf          [✓ Listo]      │
│  ⚙️ reporte.pdf             [65%]          │
│  ⏳ anexos.pdf              [Pendiente]    │
│  ✅ factura.pdf             [✓ Listo]      │
│                                            │
│  ──────────────────────────────────────    │
│  Progreso general: 45%                     │
│  [█████████░░░░░░░░░]                      │
│                                            │
└────────────────────────────────────────────┘
```

### Estados de Archivo

```python
class FileStatus(Enum):
    PENDING = 'pending'        # Esperando procesamiento
    PROCESSING = 'processing'  # En proceso
    COMPLETED = 'completed'    # Completado exitosamente
    ERROR = 'error'            # Error en procesamiento
```

### Implementación

```python
import concurrent.futures
from pathlib import Path
from typing import Callable, List
import time

class BatchProcessor:
    """Procesador de operaciones por lotes"""

    def __init__(
        self,
        operation: str,
        max_workers: int = 4
    ):
        self.operation = operation
        self.max_workers = max_workers
        self.file_statuses = {}

    def process_batch(
        self,
        file_paths: List[str],
        operation_function: Callable,
        progress_callback: Callable = None
    ) -> dict:
        """
        Procesa múltiples archivos en lote

        Args:
            file_paths: Lista de rutas de archivos
            operation_function: Función a aplicar a cada archivo
            progress_callback: Función para reportar progreso

        Returns:
            dict con resultados del procesamiento
        """
        total_files = len(file_paths)
        completed = 0
        results = []

        # Inicializar estados
        for path in file_paths:
            self.file_statuses[path] = {
                'status': 'pending',
                'progress': 0,
                'result': None
            }

        # Procesamiento paralelo
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            # Enviar trabajos
            future_to_file = {
                executor.submit(
                    self._process_single_file,
                    file_path,
                    operation_function,
                    progress_callback
                ): file_path
                for file_path in file_paths
            }

            # Recoger resultados
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]

                try:
                    result = future.result()
                    self.file_statuses[file_path]['status'] = 'completed'
                    self.file_statuses[file_path]['result'] = result
                    results.append(result)
                    completed += 1

                    # Reportar progreso general
                    if progress_callback:
                        overall_progress = (completed / total_files) * 100
                        progress_callback(overall_progress, file_path)

                except Exception as exc:
                    self.file_statuses[file_path]['status'] = 'error'
                    self.file_statuses[file_path]['error'] = str(exc)
                    results.append({
                        'success': False,
                        'file': file_path,
                        'error': str(exc)
                    })

        return {
            'success': True,
            'total_files': total_files,
            'completed': completed,
            'results': results,
            'file_statuses': self.file_statuses
        }

    def _process_single_file(
        self,
        file_path: str,
        operation_function: Callable,
        progress_callback: Callable
    ) -> dict:
        """Procesa un archivo individual"""
        # Actualizar estado
        self.file_statuses[file_path]['status'] = 'processing'

        # Función de progreso individual
        def individual_progress(progress: float):
            self.file_statuses[file_path]['progress'] = progress
            if progress_callback:
                progress_callback(progress, file_path)

        # Ejecutar operación
        result = operation_function(file_path, individual_progress)

        return result

# Uso con diferentes operaciones

def batch_compress(
    file_paths: List[str],
    output_dir: str,
    compression_level: str = 'medium'
) -> dict:
    """Comprime múltiples PDFs"""
    processor = BatchProcessor('compress')

    def compress_single(file_path, progress_cb):
        output_path = Path(output_dir) / f"compressed_{Path(file_path).name}"
        return compress_pdf(file_path, str(output_path), compression_level)

    return processor.process_batch(
        file_paths,
        compress_single,
        progress_callback=lambda p, f: print(f"{f}: {p:.0f}%")
    )

def batch_convert_to_word(
    file_paths: List[str],
    output_dir: str
) -> dict:
    """Convierte múltiples PDFs a Word"""
    processor = BatchProcessor('convert')

    def convert_single(file_path, progress_cb):
        output_path = Path(output_dir) / f"{Path(file_path).stem}.docx"
        return convert_pdf_to_word(file_path, str(output_path))

    return processor.process_batch(file_paths, convert_single)
```

### Carpeta Vigilada (Watch Folder)

```python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PDFWatcher(FileSystemEventHandler):
    """Vigila una carpeta y procesa automáticamente PDFs nuevos"""

    def __init__(
        self,
        operation: str,
        operation_function: Callable,
        output_dir: str
    ):
        self.operation = operation
        self.operation_function = operation_function
        self.output_dir = output_dir
        self.processed_files = set()

    def on_created(self, event):
        """Se ejecuta cuando se crea un archivo nuevo"""
        if event.is_directory:
            return

        file_path = event.src_path

        # Solo procesar PDFs
        if not file_path.endswith('.pdf'):
            return

        # Evitar procesar dos veces
        if file_path in self.processed_files:
            return

        # Esperar a que el archivo termine de copiarse
        time.sleep(1)

        # Procesar
        print(f"Nuevo archivo detectado: {file_path}")
        result = self.operation_function(file_path)

        if result['success']:
            self.processed_files.add(file_path)
            print(f"✅ Procesado: {file_path}")
        else:
            print(f"❌ Error: {file_path}")

def start_watch_folder(
    watch_dir: str,
    operation: str,
    operation_function: Callable,
    output_dir: str
):
    """
    Inicia vigilancia de carpeta

    Args:
        watch_dir: Carpeta a vigilar
        operation: Tipo de operación
        operation_function: Función a ejecutar
        output_dir: Carpeta de salida
    """
    event_handler = PDFWatcher(operation, operation_function, output_dir)
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=False)
    observer.start()

    print(f"🔍 Vigilando carpeta: {watch_dir}")
    print(f"📋 Operación: {operation}")
    print("Presiona Ctrl+C para detener...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    print("Vigilancia detenida")
```

---

## Módulo 6: Layout Engine

### Descripción General

El **Layout Engine** es el motor de análisis de estructura de documentos PDF que permite conversiones inteligentes preservando:

- Formato de texto (negrita, cursiva, tamaños)
- Estructura de párrafos y columnas
- Tablas y su formato
- Posición de imágenes
- Jerarquía de encabezados

### Funcionalidad Principal

El Layout Engine no es una operación independiente, sino una **tecnología transversal** que se integra principalmente en:

1. **Conversión PDF → Word** (Módulo 2)
2. **OCR** (Módulo 4) - Para preservar posición del texto
3. **Conversión PDF → Imágenes** - Para extracción precisa

### Componentes del Layout Engine

```python
class LayoutEngine:
    """Motor de análisis de estructura PDF"""

    components = {
        'text_analyzer': 'Detecta bloques de texto y jerarquía',
        'column_detector': 'Identifica columnas múltiples',
        'table_recognizer': 'Reconoce estructuras de tabla',
        'image_locator': 'Ubica y extrae imágenes',
        'header_footer_detector': 'Identifica encabezados/pies'
    }
```

### Interfaz en Dashboard

```
┌────────────────────────────────────────────┐
│  ✨  Layout Engine                         │
│                                            │
│  Conversión avanzada con análisis de      │
│  estructura del documento                  │
│                                            │
│  • Preserva formato de texto               │
│  • Detecta columnas automáticamente        │
│  • Reconoce tablas complejas               │
│  • Mantiene posición de imágenes           │
└────────────────────────────────────────────┘
```

### Implementación Detallada

Ya mostrada en Módulo 2 (Conversiones), la clase `LayoutEngine` que analiza estructura.

### Visualización del Proceso

```
DOCUMENTO ORIGINAL (PDF)
┌─────────────────────────────────┐
│ [Título Principal]              │
│                                 │
│ ┌───────┐  Párrafo con imagen  │
│ │ IMG   │  a la izquierda.     │
│ └───────┘  Texto continúa...   │
│                                 │
│ ┌───────────┬─────────────┐    │
│ │ Columna 1 │ Columna 2   │    │
│ │ Texto...  │ Más texto...│    │
│ └───────────┴─────────────┘    │
└─────────────────────────────────┘

        LAYOUT ENGINE ANALIZA
                 ↓
┌─────────────────────────────────┐
│ Estructura Detectada:           │
│ • H1: "Título Principal"        │
│ • Block 1: Párrafo + Imagen     │
│   - Image (left-aligned)        │
│   - Text (wrapping)             │
│ • Block 2: Tabla (2 columnas)   │
└─────────────────────────────────┘

        CONVERSIÓN A WORD
                 ↓
DOCUMENTO WORD CON FORMATO
┌─────────────────────────────────┐
│ Título Principal (Heading 1)    │
│                                 │
│ [Imagen] Párrafo editablecon   │
│          la imagen correcta-    │
│          mente posicionada.     │
│                                 │
│ ╔═══════════╦═════════════╗    │
│ ║ Columna 1 ║ Columna 2   ║    │
│ ║ Texto...  ║ Más texto...║    │
│ ╚═══════════╩═════════════╝    │
└─────────────────────────────────┘
```

---

## Módulo 7: Workflows Inteligentes

### Descripción General

El módulo de Workflows Inteligentes engloba:

1. **Asistente Inteligente (Wizard)** - Ya documentado extensamente
2. **Recomendaciones contextuales** - Sugerencias basadas en el tipo de archivo
3. **Flujos pre-configurados** - Operaciones encadenadas comunes

### 7.1 Asistente Inteligente

Ver sección completa anterior: [Asistente Inteligente (Wizard)](#asistente-inteligente-wizard)

### 7.2 Recomendaciones Contextuales

#### Concepto

Cuando el usuario carga un archivo, el sistema analiza sus características y sugiere operaciones relevantes.

#### Análisis Automático

```python
def analyze_pdf_and_recommend(pdf_path: str) -> dict:
    """
    Analiza un PDF y recomienda operaciones

    Returns:
        dict con recomendaciones
    """
    reader = PdfReader(pdf_path)
    file_size = Path(pdf_path).stat().st_size

    recommendations = []

    # 1. Si es muy grande → Comprimir
    if file_size > 10 * 1024 * 1024:  # > 10 MB
        recommendations.append({
            'operation': 'compress',
            'priority': 'high',
            'reason': f'El archivo es grande ({file_size/1024/1024:.1f} MB). '
                     'Puedes reducir su tamaño.'
        })

    # 2. Si tiene páginas escaneadas → OCR
    ocr_processor = OCRProcessor()
    scanned_pages = ocr_processor.detect_scanned_pages(pdf_path)
    if scanned_pages:
        recommendations.append({
            'operation': 'ocr',
            'priority': 'medium',
            'reason': f'Detectamos {len(scanned_pages)} páginas escaneadas. '
                     'OCR las haría buscables.'
        })

    # 3. Si no está encriptado pero tiene contenido sensible → Seguridad
    if not reader.is_encrypted:
        recommendations.append({
            'operation': 'security',
            'priority': 'low',
            'reason': 'Este PDF no está protegido. '
                     'Puedes encriptarlo para mayor seguridad.'
        })

    # 4. Si tiene muchas páginas → Split
    if len(reader.pages) > 50:
        recommendations.append({
            'operation': 'split',
            'priority': 'medium',
            'reason': f'El PDF tiene {len(reader.pages)} páginas. '
                     'Quizás quieras dividirlo.'
        })

    return {
        'recommendations': recommendations,
        'file_info': {
            'pages': len(reader.pages),
            'size_mb': file_size / 1024 / 1024,
            'encrypted': reader.is_encrypted
        }
    }
```

### 7.3 Flujos Pre-configurados

#### Flujos Comunes

```python
WORKFLOWS = {
    'scan_to_editable': {
        'name': 'Escaneo a Editable',
        'description': 'PDF escaneado → OCR → Word editable',
        'steps': [
            {'operation': 'ocr', 'params': {'language': 'spa'}},
            {'operation': 'convert', 'params': {'type': 'pdf-to-word'}}
        ]
    },
    'secure_compress': {
        'name': 'Comprimir y Proteger',
        'description': 'Reduce tamaño y encripta',
        'steps': [
            {'operation': 'compress', 'params': {'level': 'medium'}},
            {'operation': 'encrypt', 'params': {'ask_password': True}}
        ]
    },
    'merge_and_ocr': {
        'name': 'Combinar y Aplicar OCR',
        'description': 'Combina múltiples escaneados y aplica OCR',
        'steps': [
            {'operation': 'merge', 'params': {}},
            {'operation': 'ocr', 'params': {'language': 'spa'}}
        ]
    }
}
```

#### Ejecutor de Workflows

```python
class WorkflowExecutor:
    """Ejecuta flujos de trabajo encadenados"""

    def execute_workflow(
        self,
        workflow_id: str,
        initial_file: str,
        params: dict = None
    ) -> dict:
        """
        Ejecuta un workflow completo

        Args:
            workflow_id: ID del workflow a ejecutar
            initial_file: Archivo inicial
            params: Parámetros adicionales
        """
        workflow = WORKFLOWS[workflow_id]
        current_file = initial_file
        results = []

        for step in workflow['steps']:
            operation = step['operation']
            operation_params = {**step['params'], **(params or {})}

            # Ejecutar operación
            result = self._execute_operation(
                operation,
                current_file,
                operation_params
            )

            results.append(result)

            if not result['success']:
                return {
                    'success': False,
                    'failed_at': operation,
                    'results': results
                }

            # El output de esta operación es input de la siguiente
            current_file = result['output_file']

        return {
            'success': True,
            'final_file': current_file,
            'steps_completed': len(results),
            'results': results
        }
```

---

## Módulo 8: Dashboard y Navegación

### Descripción General

El Dashboard es el punto de entrada principal de la aplicación, proporcionando acceso rápido a todas las funcionalidades mediante cards visuales.

### Estructura del Dashboard

```
┌────────────────────────────────────────────────────────┐
│  Bienvenido a LocalPDF                                 │
│  Herramienta profesional para manipulación de PDFs    │
│  100% offline                                          │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  🪄  Asistente Inteligente         [NUEVO]      →│ │
│  │  Déjanos ayudarte a elegir la mejor operación    │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  Acciones Rápidas:                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Combinar │  │ Dividir  │  │Comprimir │           │
│  │   PDFs   │  │   PDF    │  │          │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │Convertir │  │Seguridad │  │   OCR    │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│                                                        │
│  Características Avanzadas:                           │
│  ┌──────────────────────────────────────────────┐    │
│  │  📁  Procesamiento por Lotes              → │    │
│  │  Automatiza operaciones en múltiples PDFs    │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  ✨  Layout Engine                            │    │
│  │  Conversión avanzada con análisis            │    │
│  └──────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────┘
```

### Componentes del Dashboard

#### Card del Asistente (Destacado)

- Fondo negro
- Icono de varita mágica
- Badge "NUEVO"
- Hover: Fondo más oscuro
- Click: Navega a Wizard

#### Cards de Acciones Rápidas

Grid de 3 columnas (2 filas):

```typescript
const quickActions = [
  {
    id: "merge",
    icon: Combine,
    title: "Combinar PDFs",
    description: "Une múltiples archivos en uno solo",
  },
  {
    id: "split",
    icon: Scissors,
    title: "Dividir PDF",
    description: "Separa páginas o rangos",
  },
  {
    id: "compress",
    icon: Archive,
    title: "Comprimir",
    description: "Reduce el tamaño del archivo",
  },
  {
    id: "convert",
    icon: RefreshCw,
    title: "Convertir",
    description: "PDF ↔ Word, Imágenes",
  },
  {
    id: "security",
    icon: Shield,
    title: "Seguridad",
    description: "Encriptar y proteger",
  },
  {
    id: "ocr",
    icon: ScanText,
    title: "OCR",
    description: "Reconocimiento de texto",
  },
];
```

#### Características Avanzadas

- Procesamiento por Lotes (clickeable)
- Layout Engine (informativo)

### Sistema de Navegación (Sidebar)

```
┌──────────────────────┐
│  LocalPDF  v5.0      │
├──────────────────────┤
│  🏠 Dashboard        │
│  🪄 Asistente [NEW]  │
│  ➕ Combinar         │
│  ✂️ Dividir          │
│  📦 Comprimir        │
│  🔄 Convertir        │
│  🛡️ Seguridad        │
│  🔍 OCR              │
│  📁 Lotes            │
├──────────────────────┤
│  🌐 100% Offline     │
└──────────────────────┘
```

### Implementación de Navegación

```typescript
// App.tsx
export type ViewType =
  | 'dashboard'
  | 'merge'
  | 'split'
  | 'compress'
  | 'convert'
  | 'security'
  | 'ocr'
  | 'batch'
  | 'wizard';

const [currentView, setCurrentView] = useState<ViewType>('dashboard');

const renderView = () => {
  switch (currentView) {
    case 'dashboard':
      return <Dashboard onNavigate={setCurrentView} />;
    case 'merge':
      return <MergePDF />;
    case 'wizard':
      return <Wizard onNavigate={setCurrentView} />;
    // ... otros casos
  }
};
```

---

## Sistema de Componentes Compartidos

### FileDropzone

Componente reutilizable para carga de archivos con drag & drop.

#### Props

```typescript
interface FileDropzoneProps {
  onFilesSelected: (files: File[]) => void;
  accept: string; // ej: ".pdf"
  multiple: boolean; // true/false
  maxFiles: number; // límite de archivos
  title: string; // texto principal
  description: string; // texto secundario
}
```

#### Implementación

```typescript
export function FileDropzone({
  onFilesSelected,
  accept,
  multiple,
  maxFiles,
  title,
  description
}: FileDropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files).filter(
      file => file.name.endsWith(accept.replace('.', ''))
    );

    if (files.length > maxFiles) {
      toast.error(`Máximo ${maxFiles} archivos permitidos`);
      return;
    }

    onFilesSelected(files);
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      onDragEnter={() => setIsDragging(true)}
      onDragLeave={() => setIsDragging(false)}
      className={`
        border-2 border-dashed rounded-2xl p-12
        transition-all duration-200
        ${isDragging
          ? 'border-indigo-500 bg-indigo-50'
          : 'border-gray-300 hover:border-gray-400'
        }
      `}
    >
      <div className="text-center">
        <Upload className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-4 text-lg font-semibold">{title}</h3>
        <p className="text-sm text-gray-600">{description}</p>
      </div>
    </div>
  );
}
```

### OperationHeader

Header consistente para cada operación.

```typescript
interface OperationHeaderProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export function OperationHeader({
  icon: Icon,
  title,
  description
}: OperationHeaderProps) {
  return (
    <div className="flex items-center gap-4 mb-4">
      <div className="w-14 h-14 bg-black rounded-2xl flex items-center justify-center">
        <Icon className="w-7 h-7 text-white" />
      </div>
      <div>
        <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
        <p className="text-gray-600">{description}</p>
      </div>
    </div>
  );
}
```

---

## Flujos de Usuario Completos

### Flujo 1: Primer Uso - Usuario Novato

```
1. Abrir aplicación
   ↓
2. Ver Dashboard
   - Card grande del Asistente capta atención
   ↓
3. Click en "Asistente Inteligente"
   ↓
4. Pregunta 1: "¿Qué quieres hacer?"
   - Lee opciones en lenguaje simple
   - Selecciona "Hacer el texto buscable (OCR)"
   ↓
5. Pantalla de resultado
   - "Te recomendamos: OCR"
   - Click en "Ir a la función"
   ↓
6. Vista de OCR
   - Selecciona idioma
   - Carga archivo
   - Procesa
   ↓
7. Descarga resultado
   ✓ Usuario exitoso sin conocimiento técnico
```

### Flujo 2: Usuario Experto - Acceso Directo

```
1. Abrir aplicación
   ↓
2. Click directo en Sidebar → "Combinar"
   ↓
3. Drag & drop de 5 PDFs
   ↓
4. Reordena archivos
   ↓
5. Click "Combinar PDFs"
   ↓
6. Descarga
   ✓ Flujo rápido, 3 clicks
```

### Flujo 3: Procesamiento por Lotes

```
1. Dashboard → "Procesamiento por Lotes"
   ↓
2. Selecciona operación: "Comprimir cada uno"
   ↓
3. Activa "Carpeta vigilada"
   ↓
4. Selecciona 20 PDFs
   ↓
5. Click "Iniciar Procesamiento"
   ↓
6. Ve progreso individual de cada archivo
   ↓
7. Progreso general: 100%
   ↓
8. Descarga todos los archivos comprimidos
   ✓ 20 archivos procesados automáticamente
```

### Flujo 4: Workflow Completo - PDF Escaneado a Word

```
1. Usuario tiene PDF escaneado
   ↓
2. Asistente → "Convertir a otro formato"
   ↓
3. "PDF a Word"
   ↓
4. Sistema detecta: PDF escaneado
   - Recomendación: "Aplicar OCR primero"
   ↓
5. Usuario acepta
   ↓
6. OCR automático
   - Idioma: Español
   - Progreso: Aplicando Tesseract...
   ↓
7. Conversión a Word con Layout Engine
   - Progreso: Analizando estructura...
   - Progreso: Generando DOCX...
   ↓
8. Resultado: Word editable con texto buscable
   ✓ Workflow inteligente completado
```

---

## Implementación Técnica

### Stack Tecnológico Web (Referencia Visual)

```
Frontend:
├─ React 18.3.1
├─ TypeScript 5.x
├─ Tailwind CSS 4.0
├─ Motion/React (Framer Motion)
└─ shadcn/ui components

Build:
├─ Vite
└─ PostCSS

Icons:
└─ Lucide React (30+ iconos)
```

### Stack Tecnológico Python (Objetivo)

```
UI Framework:
└─ PySide6 (Qt for Python)

PDF Processing:
├─ PyPDF2 (merge, split, encrypt)
├─ pikepdf (compression)
├─ pdf2docx (PDF to Word conversion)
└─ pdf2image (PDF to images)

OCR:
├─ pytesseract
└─ Tesseract OCR engine

Image Processing:
└─ Pillow (PIL)

Additional:
├─ reportlab (PDF generation)
├─ pdfminer.six (layout analysis)
└─ watchdog (folder watching)
```

### Estructura de Archivos Python Recomendada

```
localpdf_v5/
│
├── main.py                    # Entry point
├── requirements.txt
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py         # MainWindow principal
│   ├── sidebar.py             # Sidebar de navegación
│   ├── dashboard.py           # Vista Dashboard
│   └── wizard_dialog.py       # Asistente Inteligente
│
├── operations/
│   ├── __init__.py
│   ├── merge.py               # Lógica de combinar
│   ├── split.py               # Lógica de dividir
│   ├── compress.py            # Lógica de comprimir
│   ├── convert.py             # Lógica de conversión
│   ├── security.py            # Lógica de seguridad
│   ├── ocr.py                 # Lógica de OCR
│   └── batch.py               # Procesamiento por lotes
│
├── core/
│   ├── __init__.py
│   ├── layout_engine.py       # Motor de análisis de layout
│   ├── workflow.py            # Sistema de workflows
│   └── file_analyzer.py       # Análisis y recomendaciones
│
├── widgets/
│   ├── __init__.py
│   ├── file_dropzone.py       # Widget de carga de archivos
│   ├── operation_header.py    # Header de operaciones
│   └── progress_dialog.py     # Diálogo de progreso
│
├── resources/
│   ├── icons/
│   │   ├── combine.svg
│   │   ├── scissors.svg
│   │   └── ...                # 30+ iconos
│   └── styles/
│       └── stylesheet.qss     # Estilos Qt
│
└── utils/
    ├── __init__.py
    ├── validators.py          # Validaciones
    └── helpers.py             # Funciones auxiliares
```

### Mapeo Web → Python

#### Componentes React → Widgets Qt

```
Dashboard.tsx        → DashboardWidget(QWidget)
Wizard.tsx           → WizardDialog(QDialog)
MergePDF.tsx         → MergeOperation(QWidget)
Sidebar.tsx          → SidebarWidget(QWidget)
FileDropzone.tsx     → FileDropzoneWidget(QWidget)
```

#### Estados React → Variables de Instancia Qt

```typescript
// React
const [files, setFiles] = useState<File[]>([]);
const [isProcessing, setIsProcessing] = useState(false);
```

```python
# PySide6
class MergeOperation(QWidget):
    def __init__(self):
        self.files = []
        self.is_processing = False
```

#### Animaciones Motion/React → QPropertyAnimation

```typescript
// React
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
>
```

```python
# PySide6
animation = QPropertyAnimation(widget, b"pos")
animation.setDuration(300)
animation.setStartValue(QPoint(0, 20))
animation.setEndValue(QPoint(0, 0))
animation.start()
```

---

## Conclusión

LocalPDF v5 es una aplicación completa de manipulación de PDFs con 8 módulos integrados que cubren desde operaciones básicas hasta características avanzadas como el Asistente Inteligente y el Layout Engine.

### Puntos Clave

1. **Asistente Inteligente**: Sistema conversacional único que guía a usuarios inexpertos
2. **Layout Engine**: Análisis de estructura para conversiones precisas
3. **Procesamiento por Lotes**: Automatización de operaciones masivas
4. **OCR con Tesseract**: Conversión de escaneados a texto buscable
5. **Diseño Minimalista iOS**: Interfaz profesional y limpia
6. **Modular y Extensible**: Arquitectura que facilita agregar nuevas operaciones

### Referencias Cruzadas

- **Documentación Visual**: `DOCUMENTACION_LOCALPDF_V5.md` (121KB)
- **Documentación Técnica**: `DOCUMENTACION_TECNICA_LOCALPDF_V5.md` (153KB)
- **Sistema de Iconos**: `README_ICONOS.md`
- **Código Fuente**: `/src/app/` (componentes React)

### Implementación Recomendada

1. Comenzar con la estructura base (MainWindow + Sidebar)
2. Implementar operaciones básicas (Merge, Split, Compress)
3. Agregar OCR y Conversiones con Layout Engine
4. Implementar el Asistente Inteligente
5. Finalizar con Procesamiento por Lotes

---

**Documento generado para LocalPDF v5**  
**Versión**: 1.0  
**Fecha**: Enero 2025  
**Énfasis**: Asistente Inteligente y Funcionalidades Completas