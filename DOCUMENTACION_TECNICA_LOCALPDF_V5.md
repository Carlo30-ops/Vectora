# LocalPDF v5 - Documentación Técnica y Funcional

## 📋 Índice
1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Gestión de Estado](#gestión-de-estado)
3. [Flujo de Navegación](#flujo-de-navegación)
4. [Lógica de Operaciones PDF](#lógica-de-operaciones-pdf)
5. [Procesamiento de Archivos](#procesamiento-de-archivos)
6. [Validaciones y Manejo de Errores](#validaciones-y-manejo-de-errores)
7. [Sistema de Notificaciones](#sistema-de-notificaciones)
8. [Componentes Compartidos](#componentes-compartidos)
9. [Integración con Bibliotecas](#integración-con-bibliotecas)
10. [Flujos de Usuario Completos](#flujos-de-usuario-completos)

---

## Arquitectura del Sistema

### Estructura de Componentes

```
LocalPDF v5 (React + TypeScript)
│
├── App.tsx (Raíz)
│   ├── Estado: currentView (ViewType)
│   ├── Renderizado condicional de vistas
│   └── Sistema de notificaciones (Toaster)
│
├── Componentes de Layout
│   ├── Sidebar.tsx (Navegación)
│   └── Toaster (Notificaciones globales)
│
├── Vistas Principales
│   ├── Dashboard.tsx
│   ├── Wizard.tsx
│   └── Operaciones (6 componentes)
│       ├── MergePDF.tsx
│       ├── SplitPDF.tsx
│       ├── CompressPDF.tsx
│       ├── ConvertPDF.tsx
│       ├── SecurityPDF.tsx
│       ├── OCRPdf.tsx
│       └── BatchProcessing.tsx
│
└── Componentes Compartidos
    ├── FileDropzone.tsx
    ├── OperationHeader.tsx
    └── UI Components (buttons, inputs, etc.)
```

### Patrón de Arquitectura

**Tipo**: Arquitectura de Componentes con Estado Local (Component-Based Architecture)

**Características**:
- Cada operación es un componente independiente autocontenido
- Estado local en cada componente (no hay estado global/Redux)
- Comunicación padre-hijo mediante props
- Componentes reutilizables con props tipadas

**Ventajas para Desktop (PySide6)**:
- Fácil traducción a widgets independientes
- Cada operación puede ser una ventana/diálogo separado
- Estado local = variables de instancia en clases Qt

---

## Gestión de Estado

### Estado Global (App.tsx)

```typescript
// Estado único a nivel de aplicación
const [currentView, setCurrentView] = useState<ViewType>('dashboard');

// Tipos de vista disponibles
type ViewType = 
  | 'dashboard'    // Pantalla inicial
  | 'merge'        // Combinar PDFs
  | 'split'        // Dividir PDF
  | 'compress'     // Comprimir PDF
  | 'convert'      // Convertir archivos
  | 'security'     // Seguridad PDF
  | 'ocr'          // OCR
  | 'batch'        // Procesamiento por lotes
  | 'wizard';      // Asistente inteligente
```

**Flujo de cambio de vista**:
1. Usuario hace clic en Sidebar → `onNavigate(viewType)`
2. App actualiza `currentView`
3. Se desmonta componente anterior, se monta el nuevo
4. Cada componente inicia con estado limpio

**Equivalente PySide6**:
```python
class MainWindow(QMainWindow):
    def __init__(self):
        self.current_view = "dashboard"
        self.stacked_widget = QStackedWidget()
        # Agregar todas las vistas al stack
```

### Estado por Operación (Patrón Común)

Cada operación mantiene su propio estado local:

```typescript
// Estado de archivos
const [files, setFiles] = useState<File[]>([]);

// Estado de procesamiento
const [isProcessing, setIsProcessing] = useState(false);
const [progress, setProgress] = useState(0);
const [isComplete, setIsComplete] = useState(false);

// Configuración específica de la operación
const [operationConfig, setOperationConfig] = useState(defaultConfig);
```

**Ciclo de vida del estado**:
1. **Inicial**: Todos los valores en default
2. **Archivos seleccionados**: `files` se llena
3. **Procesando**: `isProcessing = true`, `progress` 0→100
4. **Completado**: `isComplete = true`, `isProcessing = false`
5. **Reset**: Al cambiar de vista o reiniciar

---

## Flujo de Navegación

### Diagrama de Navegación

```
                    [Dashboard]
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    [Wizard]      [Operaciones]    [Características]
        │                │                │
    Pregunta 1      ┌────┴────┐      [Lotes]
        │           │         │
    Pregunta 2  [Merge]   [Split]
        │       [Compress] [Convert]
    Resultado   [Security] [OCR]
        │
    Navigate → [Operación específica]
```

### Lógica de Navegación

#### Desde Dashboard
```typescript
interface DashboardProps {
  onNavigate: (view: ViewType) => void;
}

// Card del Asistente
onClick={() => onNavigate('wizard')}

// Cards de Acciones Rápidas
onClick={() => onNavigate(action.id)}
// Donde action.id puede ser: 'merge', 'split', 'compress', etc.

// Card de Lotes
onClick={() => onNavigate('batch')}
```

#### Desde Sidebar
```typescript
interface SidebarProps {
  currentView: ViewType;
  onNavigate: (view: ViewType) => void;
}

// Cada botón de menú
onClick={() => onNavigate(item.id)}

// Actualiza currentView en App
// Renderiza automáticamente el componente correspondiente
```

#### Desde Wizard
```typescript
interface WizardProps {
  onNavigate: (view: ViewType) => void;
}

// Al completar el flujo de preguntas
const handleGoToAction = () => {
  if (recommendedAction) {
    onNavigate(recommendedAction); // Navega a la operación recomendada
  }
};
```

**Implementación PySide6**:
```python
def navigate_to_view(self, view_name: str):
    """Cambia la vista actual"""
    self.current_view = view_name
    index = self.view_indices[view_name]
    self.stacked_widget.setCurrentIndex(index)
    self.update_sidebar_selection(view_name)
```

---

## Lógica de Operaciones PDF

### 1. Combinar PDFs (MergePDF)

#### Estados Específicos
```typescript
const [files, setFiles] = useState<File[]>([]);  // Lista de PDFs a combinar
const [isProcessing, setIsProcessing] = useState(false);
const [progress, setProgress] = useState(0);
const [isComplete, setIsComplete] = useState(false);
```

#### Algoritmo de Combinación

```
INICIO
│
├─ Validación
│  └─ ¿files.length >= 2?
│     ├─ NO → Error: "Necesitas al menos 2 archivos"
│     └─ SÍ → Continuar
│
├─ Inicio del Proceso
│  ├─ setIsProcessing(true)
│  ├─ setProgress(0)
│  └─ setIsComplete(false)
│
├─ Procesamiento Simulado
│  └─ FOR i = 0 TO 100 STEP 10
│     ├─ await sleep(200ms)
│     ├─ setProgress(i)
│     └─ Actualizar UI
│
├─ Finalización
│  ├─ setIsProcessing(false)
│  ├─ setIsComplete(true)
│  └─ Notificación: "¡PDFs combinados exitosamente!"
│
└─ FIN
```

#### Reordenamiento de Archivos (Drag & Drop)

**Biblioteca**: `motion/react` (Reorder component)

```typescript
<Reorder.Group axis="y" values={files} onReorder={setFiles}>
  {files.map((file, index) => (
    <Reorder.Item key={file.name} value={file}>
      {/* Contenido del item */}
    </Reorder.Item>
  ))}
</Reorder.Group>
```

**Lógica**:
- El usuario arrastra un item
- `onReorder` recibe el nuevo array ordenado
- `setFiles` actualiza el estado
- La UI se re-renderiza automáticamente

**Equivalente PySide6**:
```python
class ReorderableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragDropMode(QAbstractItemView.InternalMove)
    
    def dropEvent(self, event):
        # Capturar el nuevo orden
        super().dropEvent(event)
        self.emit_new_order()
```

#### Proceso Real con PyPDF2 (Implementación Python)

```python
from PyPDF2 import PdfMerger

def merge_pdfs(file_paths: list[str], output_path: str, progress_callback=None):
    """
    Combina múltiples PDFs en uno solo
    
    Args:
        file_paths: Lista de rutas de archivos en orden
        output_path: Ruta del archivo de salida
        progress_callback: Función para reportar progreso (0-100)
    """
    merger = PdfMerger()
    total_files = len(file_paths)
    
    for i, path in enumerate(file_paths):
        try:
            merger.append(path)
            if progress_callback:
                progress = int((i + 1) / total_files * 100)
                progress_callback(progress)
        except Exception as e:
            raise PDFProcessingError(f"Error al procesar {path}: {str(e)}")
    
    merger.write(output_path)
    merger.close()
```

---

### 2. Dividir PDF (SplitPDF)

#### Estados Específicos
```typescript
const [files, setFiles] = useState<File[]>([]);
const [splitMode, setSplitMode] = useState<SplitMode>('range');
const [rangeStart, setRangeStart] = useState('1');
const [rangeEnd, setRangeEnd] = useState('');
const [specificPages, setSpecificPages] = useState('');
const [everyNPages, setEveryNPages] = useState('1');
```

#### Tipos de División

**1. Por Rango (range)**
```
Input: rangeStart = 5, rangeEnd = 10
Output: Archivo con páginas 5, 6, 7, 8, 9, 10
```

**2. Páginas Específicas (pages)**
```
Input: specificPages = "1, 3, 5-8, 12"
Parser:
  - Divide por comas: ["1", "3", "5-8", "12"]
  - Procesa cada elemento:
    * "1" → [1]
    * "3" → [3]
    * "5-8" → [5, 6, 7, 8]
    * "12" → [12]
  - Resultado: [1, 3, 5, 6, 7, 8, 12]
Output: Archivo con esas páginas
```

**3. Cada N Páginas (every)**
```
Input: everyNPages = 3, Total páginas = 10
Output: 
  - Archivo 1: páginas 1-3
  - Archivo 2: páginas 4-6
  - Archivo 3: páginas 7-9
  - Archivo 4: página 10
```

#### Algoritmo de Parsing de Páginas

```python
def parse_page_specification(spec: str) -> list[int]:
    """
    Parsea especificación de páginas como "1, 3, 5-8, 12"
    
    Returns:
        Lista de números de página (ordenada, sin duplicados)
    """
    pages = set()
    parts = spec.split(',')
    
    for part in parts:
        part = part.strip()
        
        if '-' in part:
            # Rango: "5-8"
            start, end = part.split('-')
            start_num = int(start.strip())
            end_num = int(end.strip())
            pages.update(range(start_num, end_num + 1))
        else:
            # Página individual: "3"
            pages.add(int(part))
    
    return sorted(list(pages))
```

#### Validaciones

```python
def validate_split_config(mode: str, config: dict, total_pages: int) -> tuple[bool, str]:
    """
    Valida la configuración de división
    
    Returns:
        (es_valido, mensaje_error)
    """
    if mode == 'range':
        start = config.get('rangeStart', 1)
        end = config.get('rangeEnd', total_pages)
        
        if start < 1 or end > total_pages:
            return False, f"El rango debe estar entre 1 y {total_pages}"
        
        if start > end:
            return False, "La página inicial debe ser menor que la final"
    
    elif mode == 'pages':
        try:
            pages = parse_page_specification(config['specificPages'])
            if any(p < 1 or p > total_pages for p in pages):
                return False, f"Todas las páginas deben estar entre 1 y {total_pages}"
        except ValueError:
            return False, "Formato de páginas inválido"
    
    elif mode == 'every':
        n = config.get('everyNPages', 1)
        if n < 1:
            return False, "Debe dividir cada 1 o más páginas"
    
    return True, ""
```

#### Proceso Real con PyPDF2

```python
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_by_range(input_path: str, output_path: str, start: int, end: int):
    """Extrae un rango de páginas"""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Ajustar a índices 0-based
    for page_num in range(start - 1, end):
        writer.add_page(reader.pages[page_num])
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

def split_pdf_every_n(input_path: str, output_dir: str, n: int) -> list[str]:
    """Divide cada N páginas"""
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    output_files = []
    
    for i in range(0, total_pages, n):
        writer = PdfWriter()
        end = min(i + n, total_pages)
        
        for page_num in range(i, end):
            writer.add_page(reader.pages[page_num])
        
        output_path = os.path.join(output_dir, f"part_{i//n + 1}.pdf")
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        output_files.append(output_path)
    
    return output_files
```

---

### 3. Comprimir PDF (CompressPDF)

#### Estados Específicos
```typescript
const [files, setFiles] = useState<File[]>([]);
const [compressionValue, setCompressionValue] = useState([50]); // Slider 0-100
const [originalSize, setOriginalSize] = useState(0);
const [compressedSize, setCompressedSize] = useState(0);
```

#### Niveles de Compresión

```typescript
const compressionLevels = {
  low: { 
    value: 25, 
    label: 'Baja', 
    reduction: '~20%', 
    quality: 'Alta calidad' 
  },
  medium: { 
    value: 50, 
    label: 'Media', 
    reduction: '~40%', 
    quality: 'Calidad equilibrada' 
  },
  high: { 
    value: 75, 
    label: 'Alta', 
    reduction: '~60%', 
    quality: 'Compresión fuerte' 
  },
  extreme: { 
    value: 100, 
    label: 'Extrema', 
    reduction: '~80%', 
    quality: 'Máxima compresión' 
  },
};
```

#### Algoritmo de Determinación de Nivel

```typescript
const getCompressionLevel = (value: number): CompressionLevel => {
  if (value <= 25) return 'low';
  if (value <= 50) return 'medium';
  if (value <= 75) return 'high';
  return 'extreme';
};
```

#### Cálculo de Tamaño Comprimido (Simulado)

```typescript
const handleCompress = async () => {
  // Calcular tamaño original
  const totalSize = files.reduce((acc, file) => acc + file.size, 0);
  setOriginalSize(totalSize);
  
  // Simular compresión
  const reduction = compressionValue[0] / 100; // 0.0 - 1.0
  const compressed = totalSize * (1 - reduction * 0.7); // 70% del slider
  setCompressedSize(compressed);
  
  // Ejemplo:
  // compressionValue = 50 (media)
  // reduction = 0.5
  // compressed = totalSize * (1 - 0.5 * 0.7) = totalSize * 0.65
  // Reducción real: 35%
};
```

#### Métricas de Resultado

```typescript
// Porcentaje de ahorro
const savingsPercent = ((originalSize - compressedSize) / originalSize) * 100;

// Formato de display
const formatSize = (bytes: number) => {
  return (bytes / 1024 / 1024).toFixed(2) + ' MB';
};
```

#### Proceso Real de Compresión

```python
from PIL import Image
import pikepdf

def compress_pdf(input_path: str, output_path: str, quality: str, progress_callback=None):
    """
    Comprime un PDF reduciendo la calidad de imágenes
    
    Args:
        quality: 'low' (90%), 'medium' (70%), 'high' (50%), 'extreme' (30%)
    """
    quality_map = {
        'low': 90,
        'medium': 70,
        'high': 50,
        'extreme': 30
    }
    
    jpeg_quality = quality_map[quality]
    
    with pikepdf.open(input_path) as pdf:
        total_pages = len(pdf.pages)
        
        for i, page in enumerate(pdf.pages):
            # Extraer y recomprimir imágenes
            for img_key in page.images.keys():
                img = page.images[img_key]
                # Recomprimir con nuevo nivel de calidad
                # (Implementación compleja - simplificada aquí)
            
            if progress_callback:
                progress = int((i + 1) / total_pages * 100)
                progress_callback(progress)
        
        pdf.save(output_path, compress_streams=True)
    
    # Calcular métricas
    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)
    savings = (1 - compressed_size / original_size) * 100
    
    return {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'savings_percent': savings
    }
```

**Estrategias de Compresión**:
1. **Compresión de imágenes**: Reducir calidad JPEG
2. **Compresión de streams**: `compress_streams=True` en pikepdf
3. **Eliminación de metadatos**: Opcional
4. **Deduplicación de objetos**: Objetos duplicados se unifican

---

### 4. Convertir Archivos (ConvertPDF)

#### Estados Específicos
```typescript
const [selectedType, setSelectedType] = useState<ConversionType>('pdf-to-word');
const [files, setFiles] = useState<File[]>([]);
```

#### Tipos de Conversión

```typescript
type ConversionType = 
  | 'pdf-to-word'     // PDF → DOCX
  | 'pdf-to-images'   // PDF → PNG/JPG
  | 'word-to-pdf'     // DOCX → PDF
  | 'images-to-pdf';  // IMG → PDF

const conversionTypes = [
  {
    id: 'pdf-to-word',
    title: 'PDF → Word',
    accept: '.pdf',
    icon: FileText,
    hasLayoutEngine: true  // Usa Layout Engine
  },
  {
    id: 'word-to-pdf',
    title: 'Word → PDF',
    accept: '.doc,.docx',
    icon: FileSpreadsheet,
    hasLayoutEngine: false
  },
  {
    id: 'pdf-to-images',
    title: 'PDF → Imágenes',
    accept: '.pdf',
    icon: Image,
    hasLayoutEngine: false
  },
  {
    id: 'images-to-pdf',
    title: 'Imágenes → PDF',
    accept: '.jpg,.jpeg,.png',
    icon: Image,
    hasLayoutEngine: false,
    allowMultiple: true
  },
];
```

#### Layout Engine (PDF → Word)

**Concepto**: Sistema avanzado de análisis de estructura del documento

**Fases del Layout Engine**:

```
1. Análisis de Estructura (25%)
   ├─ Detección de bloques de texto
   ├─ Identificación de párrafos
   ├─ Reconocimiento de encabezados
   └─ Detección de listas y tablas

2. Aplicación de Layout Engine (50%)
   ├─ Preservar formato de tablas
   ├─ Mantener columnas
   ├─ Detectar imágenes y gráficos
   └─ Reconstruir estructura jerárquica

3. Generación de Archivo Final (75%)
   ├─ Crear documento Word
   ├─ Aplicar estilos
   ├─ Insertar imágenes
   └─ Formatear tablas

4. Finalización (100%)
   └─ Guardar archivo DOCX
```

**Mensajes de Progreso**:
```typescript
if (progress === 25) toast.info('Analizando estructura del documento...');
if (progress === 50) toast.info('Aplicando Layout Engine...');
if (progress === 75) toast.info('Generando archivo final...');
```

#### Implementación Real - PDF a Word

```python
from pdf2docx import Converter

def pdf_to_word_with_layout(input_path: str, output_path: str, progress_callback=None):
    """
    Convierte PDF a Word preservando layout
    
    Usa pdf2docx que implementa Layout Engine
    """
    cv = Converter(input_path)
    
    def progress_wrapper(current, total):
        if progress_callback:
            percent = int((current / total) * 100)
            
            # Mensajes según fase
            if percent == 25:
                progress_callback(percent, "Analizando estructura del documento...")
            elif percent == 50:
                progress_callback(percent, "Aplicando Layout Engine...")
            elif percent == 75:
                progress_callback(percent, "Generando archivo final...")
            else:
                progress_callback(percent, f"Procesando... {percent}%")
    
    cv.convert(output_path, start=0, end=None, progress=progress_wrapper)
    cv.close()
```

**Características del Layout Engine**:
- **Detección de tablas**: Identifica bordes y celdas
- **Preservación de columnas**: Mantiene layout multi-columna
- **Reconocimiento de listas**: Bullets, numeración
- **Extracción de imágenes**: Preserva posición y tamaño
- **Análisis de fuentes**: Mantiene tipos y tamaños

#### Word a PDF

```python
from docx2pdf import convert

def word_to_pdf(input_path: str, output_path: str):
    """
    Convierte Word a PDF
    
    Requiere Microsoft Word instalado (Windows) o LibreOffice (Linux)
    """
    convert(input_path, output_path)
```

#### PDF a Imágenes

```python
from pdf2image import convert_from_path

def pdf_to_images(input_path: str, output_dir: str, dpi: int = 300, 
                  format: str = 'PNG', progress_callback=None) -> list[str]:
    """
    Convierte cada página del PDF en una imagen
    
    Args:
        dpi: Resolución (150=baja, 300=alta, 600=muy alta)
        format: 'PNG' o 'JPEG'
    """
    images = convert_from_path(input_path, dpi=dpi)
    output_files = []
    total_pages = len(images)
    
    for i, image in enumerate(images):
        output_path = os.path.join(output_dir, f'page_{i+1}.{format.lower()}')
        image.save(output_path, format)
        output_files.append(output_path)
        
        if progress_callback:
            progress = int((i + 1) / total_pages * 100)
            progress_callback(progress)
    
    return output_files
```

#### Imágenes a PDF

```python
from PIL import Image

def images_to_pdf(image_paths: list[str], output_path: str, progress_callback=None):
    """
    Combina múltiples imágenes en un PDF
    """
    images = []
    total_images = len(image_paths)
    
    # Cargar todas las imágenes
    for i, path in enumerate(image_paths):
        img = Image.open(path)
        
        # Convertir a RGB si es necesario (PNG con transparencia)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        images.append(img)
        
        if progress_callback:
            progress = int((i + 1) / total_images * 50)  # Primera mitad
            progress_callback(progress)
    
    # Guardar como PDF
    if images:
        images[0].save(
            output_path, 
            save_all=True, 
            append_images=images[1:],
            resolution=100.0
        )
        
        if progress_callback:
            progress_callback(100)
```

---

### 5. Seguridad PDF (SecurityPDF)

#### Estados Específicos
```typescript
const [mode, setMode] = useState<SecurityMode>('encrypt');
const [password, setPassword] = useState('');
const [confirmPassword, setConfirmPassword] = useState('');
const [showPassword, setShowPassword] = useState(false);

// Permisos (solo modo 'permissions')
const [allowPrint, setAllowPrint] = useState(true);
const [allowCopy, setAllowCopy] = useState(true);
const [allowModify, setAllowModify] = useState(false);
const [allowAnnotations, setAllowAnnotations] = useState(true);
```

#### Modos de Seguridad

```typescript
type SecurityMode = 
  | 'encrypt'      // Agregar contraseña
  | 'decrypt'      // Quitar contraseña
  | 'permissions'; // Configurar permisos

const securityModes = [
  {
    id: 'encrypt',
    title: 'Encriptar',
    description: 'Protege tu PDF con contraseña',
    requiresPassword: true,
    requiresConfirm: true
  },
  {
    id: 'decrypt',
    title: 'Desencriptar',
    description: 'Remueve la protección del PDF',
    requiresPassword: true,
    requiresConfirm: false
  },
  {
    id: 'permissions',
    title: 'Permisos',
    description: 'Configura restricciones específicas',
    requiresPassword: false,
    requiresConfirm: false,
    showPermissions: true
  },
];
```

#### Validaciones de Contraseña

```typescript
const handleProcess = async () => {
  // Validación 1: Archivo seleccionado
  if (files.length === 0) {
    toast.error('Por favor selecciona un archivo PDF');
    return;
  }
  
  // Validación 2: Contraseña requerida
  if (mode === 'encrypt' || mode === 'decrypt') {
    if (!password) {
      toast.error('Por favor ingresa una contraseña');
      return;
    }
  }
  
  // Validación 3: Confirmación de contraseña
  if (mode === 'encrypt' && password !== confirmPassword) {
    toast.error('Las contraseñas no coinciden');
    return;
  }
  
  // Validación 4: Fortaleza de contraseña (opcional)
  if (mode === 'encrypt') {
    if (password.length < 8) {
      toast.warning('Se recomienda usar al menos 8 caracteres');
    }
  }
  
  // Procesar...
};
```

#### Implementación Real - Encriptar

```python
import pikepdf

def encrypt_pdf(input_path: str, output_path: str, password: str, 
                permissions: dict = None):
    """
    Encripta un PDF con contraseña
    
    Args:
        password: Contraseña del usuario
        permissions: Dict con permisos (None = todos los permisos)
    """
    with pikepdf.open(input_path) as pdf:
        # Configurar permisos
        if permissions:
            encryption_dict = pikepdf.Encryption(
                owner=password,  # Contraseña del propietario
                user=password,   # Contraseña del usuario
                R=6,  # Versión de encriptación (AES-256)
                allow=pikepdf.Permissions(
                    print_=permissions.get('allowPrint', True),
                    modify=permissions.get('allowModify', False),
                    extract=permissions.get('allowCopy', True),
                    annotate=permissions.get('allowAnnotations', True)
                )
            )
        else:
            # Encriptación simple (todos los permisos)
            encryption_dict = pikepdf.Encryption(
                owner=password,
                user=password,
                R=6
            )
        
        pdf.save(output_path, encryption=encryption_dict)
```

#### Implementación Real - Desencriptar

```python
def decrypt_pdf(input_path: str, output_path: str, password: str):
    """
    Remueve la encriptación de un PDF
    
    Raises:
        PasswordError: Si la contraseña es incorrecta
    """
    try:
        with pikepdf.open(input_path, password=password) as pdf:
            # Guardar sin encriptación
            pdf.save(output_path)
    except pikepdf.PasswordError:
        raise PDFSecurityError("Contraseña incorrecta")
```

#### Configuración de Permisos

```python
class PDFPermissions:
    """Configuración de permisos del PDF"""
    
    def __init__(self):
        self.allow_print = True
        self.allow_copy = True
        self.allow_modify = False
        self.allow_annotations = True
    
    def to_pikepdf(self) -> pikepdf.Permissions:
        """Convierte a objeto pikepdf.Permissions"""
        return pikepdf.Permissions(
            print_=self.allow_print,
            modify=self.allow_modify,
            extract=self.allow_copy,
            annotate=self.allow_annotations
        )
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea desde diccionario"""
        perms = cls()
        perms.allow_print = data.get('allowPrint', True)
        perms.allow_copy = data.get('allowCopy', True)
        perms.allow_modify = data.get('allowModify', False)
        perms.allow_annotations = data.get('allowAnnotations', True)
        return perms
```

**Tipos de Permisos**:
1. **Impresión**: Permite imprimir el documento
2. **Copiar texto**: Permite seleccionar y copiar contenido
3. **Modificar**: Permite editar el documento
4. **Anotaciones**: Permite agregar comentarios y marcas

---

### 6. OCR - Reconocimiento de Texto (OCRPdf)

#### Estados Específicos
```typescript
const [files, setFiles] = useState<File[]>([]);
const [language, setLanguage] = useState('spa'); // Idioma OCR
const [detectedPages, setDetectedPages] = useState(0); // Páginas escaneadas detectadas
const [processedPages, setProcessedPages] = useState(0); // Páginas procesadas
```

#### Idiomas Disponibles

```typescript
const languages = [
  { code: 'spa', name: 'Español' },
  { code: 'eng', name: 'Inglés' },
  { code: 'por', name: 'Portugués' },
  { code: 'fra', name: 'Francés' },
  { code: 'deu', name: 'Alemán' },
  { code: 'ita', name: 'Italiano' },
];
```

**Códigos Tesseract**: Formato ISO 639-2 (3 letras)

#### Algoritmo de OCR

```
INICIO
│
├─ Detección de Páginas Escaneadas (10%)
│  └─ Analizar cada página del PDF
│     ├─ ¿Tiene texto nativo? → Saltar
│     └─ ¿Es imagen? → Marcar para OCR
│
├─ Aplicación de OCR con Tesseract (30-60%)
│  └─ Para cada página marcada:
│     ├─ Extraer imagen de la página
│     ├─ Preprocesar imagen (binarización, deskew)
│     ├─ Aplicar OCR con idioma seleccionado
│     └─ Extraer texto reconocido
│
├─ Generación de Capa de Texto (60-90%)
│  └─ Para cada página procesada:
│     ├─ Mantener imagen original
│     ├─ Agregar capa de texto invisible
│     └─ Posicionar texto sobre imagen
│
├─ Finalización (90-100%)
│  ├─ Combinar todas las páginas
│  ├─ Guardar PDF con texto buscable
│  └─ Generar reporte de páginas procesadas
│
└─ FIN
```

#### Mensajes de Progreso

```typescript
if (progress === 10) toast.info('Detectando páginas escaneadas...');
if (progress === 30) toast.info('Aplicando OCR con Tesseract...');
if (progress === 60) toast.info('Extrayendo texto...');
if (progress === 90) toast.info('Generando PDF con capa de texto...');
```

#### Actualización de Progreso con Páginas

```typescript
setProcessedPages(Math.floor((progress / 100) * detectedPages));

// Ejemplo:
// detectedPages = 15
// progress = 50
// processedPages = Math.floor(0.5 * 15) = 7
// Muestra: "Procesando: 7 / 15 páginas"
```

#### Implementación Real con Tesseract

```python
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import PyPDF2

def detect_scanned_pages(pdf_path: str) -> list[int]:
    """
    Detecta qué páginas son imágenes escaneadas (sin texto)
    
    Returns:
        Lista de índices de páginas escaneadas (0-based)
    """
    scanned_pages = []
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text().strip()
            
            # Si tiene muy poco texto, probablemente es escaneada
            if len(text) < 50:
                scanned_pages.append(i)
    
    return scanned_pages

def apply_ocr_to_pdf(input_path: str, output_path: str, language: str = 'spa',
                     progress_callback=None):
    """
    Aplica OCR a páginas escaneadas de un PDF
    
    Args:
        language: Código de idioma Tesseract ('spa', 'eng', etc.)
    """
    # Detectar páginas escaneadas
    scanned_pages = detect_scanned_pages(input_path)
    total_scanned = len(scanned_pages)
    
    if total_scanned == 0:
        raise OCRError("No se detectaron páginas escaneadas")
    
    if progress_callback:
        progress_callback(10, f"Detectadas {total_scanned} páginas escaneadas")
    
    # Convertir PDF a imágenes
    images = convert_from_path(input_path, dpi=300)
    
    # Procesar cada página escaneada
    ocr_results = []
    for i, page_idx in enumerate(scanned_pages):
        image = images[page_idx]
        
        # Preprocesar imagen
        image = preprocess_image(image)
        
        # Aplicar OCR
        text = pytesseract.image_to_string(image, lang=language)
        ocr_results.append({
            'page': page_idx,
            'text': text
        })
        
        if progress_callback:
            progress = 30 + int((i + 1) / total_scanned * 30)  # 30-60%
            progress_callback(progress, f"OCR: {i+1}/{total_scanned} páginas")
    
    # Crear PDF con capa de texto
    create_searchable_pdf(input_path, output_path, ocr_results, progress_callback)
    
    return {
        'total_pages': len(images),
        'scanned_pages': total_scanned,
        'processed_pages': len(ocr_results)
    }

def preprocess_image(image: Image) -> Image:
    """
    Preprocesa imagen para mejor OCR
    """
    # Convertir a escala de grises
    image = image.convert('L')
    
    # Binarización (blanco y negro)
    threshold = 150
    image = image.point(lambda p: 255 if p > threshold else 0)
    
    # Opcional: Deskew (corregir inclinación)
    # Opcional: Denoise (reducir ruido)
    
    return image

def create_searchable_pdf(input_path: str, output_path: str, 
                          ocr_results: list, progress_callback=None):
    """
    Crea PDF con capa de texto buscable sobre imágenes
    """
    # Usar OCRmyPDF o pdf2pdfocr para este proceso
    # (Implementación compleja - simplificada aquí)
    
    if progress_callback:
        progress_callback(90, "Generando PDF con capa de texto...")
    
    # ... código de creación de PDF ...
    
    if progress_callback:
        progress_callback(100, "¡OCR completado!")
```

**Optimizaciones de OCR**:
1. **DPI óptimo**: 300 DPI (balance entre calidad y velocidad)
2. **Preprocesamiento**: Binarización, deskew, denoise
3. **Detección inteligente**: Solo procesar páginas sin texto
4. **Paralelización**: Procesar múltiples páginas simultáneamente

---

### 7. Procesamiento por Lotes (BatchProcessing)

#### Estados Específicos
```typescript
const [files, setFiles] = useState<File[]>([]);
const [operation, setOperation] = useState<BatchOperation>('compress');
const [watchFolder, setWatchFolder] = useState(false);
const [fileStatuses, setFileStatuses] = useState<FileStatus[]>([]);
const [overallProgress, setOverallProgress] = useState(0);

interface FileStatus {
  name: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  progress: number;
}
```

#### Operaciones por Lotes

```typescript
type BatchOperation = 
  | 'merge'      // Combinar todos en uno
  | 'compress'   // Comprimir cada uno
  | 'convert'    // Convertir cada uno a Word
  | 'ocr'        // Aplicar OCR a cada uno
  | 'encrypt';   // Encriptar cada uno

const batchOperations = [
  { 
    id: 'merge', 
    name: 'Combinar todos', 
    description: 'Une todos los archivos en uno',
    outputType: 'single'  // Un solo archivo de salida
  },
  { 
    id: 'compress', 
    name: 'Comprimir cada uno', 
    description: 'Reduce el tamaño de cada PDF',
    outputType: 'multiple'  // Un archivo por cada entrada
  },
  // ... resto
];
```

#### Algoritmo de Procesamiento por Lotes

```
INICIO
│
├─ Validación
│  └─ ¿files.length > 0?
│     ├─ NO → Error
│     └─ SÍ → Continuar
│
├─ Inicialización
│  ├─ Crear array de FileStatus (todos 'pending')
│  ├─ setFileStatuses(statuses)
│  └─ setOverallProgress(0)
│
├─ Bucle de Procesamiento
│  └─ FOR i = 0 TO files.length - 1
│     │
│     ├─ Actualizar estado a 'processing'
│     │  └─ setFileStatuses(prev => prev.map((s, idx) => 
│     │       idx === i ? { ...s, status: 'processing' } : s
│     │     ))
│     │
│     ├─ Procesar archivo individual
│     │  └─ FOR p = 0 TO 100 STEP 20
│     │     ├─ await sleep(100ms)
│     │     └─ Actualizar progress del archivo
│     │        └─ setFileStatuses(prev => prev.map((s, idx) => 
│     │             idx === i ? { ...s, progress: p } : s
│     │           ))
│     │
│     ├─ Marcar como 'completed'
│     │  └─ setFileStatuses(prev => prev.map((s, idx) => 
│     │       idx === i ? { ...s, status: 'completed', progress: 100 } : s
│     │     ))
│     │
│     └─ Actualizar progreso general
│        └─ setOverallProgress(((i + 1) / files.length) * 100)
│
├─ Finalización
│  ├─ setIsComplete(true)
│  └─ Notificación: "¡{N} archivos procesados!"
│
└─ FIN
```

#### Manejo de Estados de Archivos

```typescript
// Estado inicial
const initialStatuses: FileStatus[] = files.map(file => ({
  name: file.name,
  status: 'pending',
  progress: 0,
}));

// Actualización inmutable del estado
const updateFileStatus = (index: number, updates: Partial<FileStatus>) => {
  setFileStatuses(prev => 
    prev.map((status, idx) => 
      idx === index 
        ? { ...status, ...updates }
        : status
    )
  );
};

// Uso
updateFileStatus(0, { status: 'processing' });
updateFileStatus(0, { progress: 50 });
updateFileStatus(0, { status: 'completed', progress: 100 });
```

#### Iconos por Estado

```typescript
const getStatusIcon = (status: FileStatus['status']) => {
  switch (status) {
    case 'pending':
      return <Clock className="w-5 h-5 text-gray-400" />;
    
    case 'processing':
      return (
        <motion.div animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity }}>
          <Play className="w-5 h-5 text-blue-500" />
        </motion.div>
      );
    
    case 'completed':
      return <CheckCircle2 className="w-5 h-5 text-green-500" />;
    
    case 'error':
      return <XCircle className="w-5 h-5 text-red-500" />;
  }
};
```

#### Implementación Real - Procesamiento por Lotes

```python
from typing import Callable, List
from dataclasses import dataclass
from enum import Enum

class ProcessingStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class FileStatus:
    name: str
    status: ProcessingStatus
    progress: int
    error_message: str = ""

class BatchProcessor:
    """Procesador por lotes de archivos PDF"""
    
    def __init__(self, operation: str):
        self.operation = operation
        self.file_statuses: List[FileStatus] = []
        self.overall_progress = 0
    
    def process_batch(self, file_paths: List[str], 
                      status_callback: Callable = None,
                      progress_callback: Callable = None):
        """
        Procesa un lote de archivos
        
        Args:
            status_callback: (file_index, status) -> None
            progress_callback: (overall_percent) -> None
        """
        # Inicializar estados
        self.file_statuses = [
            FileStatus(name=os.path.basename(path), 
                      status=ProcessingStatus.PENDING, 
                      progress=0)
            for path in file_paths
        ]
        
        total_files = len(file_paths)
        
        # Procesar cada archivo
        for i, file_path in enumerate(file_paths):
            try:
                # Actualizar a processing
                self._update_file_status(i, ProcessingStatus.PROCESSING)
                if status_callback:
                    status_callback(i, self.file_statuses[i])
                
                # Procesar según operación
                output_path = self._get_output_path(file_path)
                
                def file_progress(percent):
                    self._update_file_progress(i, percent)
                    if status_callback:
                        status_callback(i, self.file_statuses[i])
                
                self._process_single_file(file_path, output_path, file_progress)
                
                # Marcar como completado
                self._update_file_status(i, ProcessingStatus.COMPLETED, 100)
                if status_callback:
                    status_callback(i, self.file_statuses[i])
                
            except Exception as e:
                # Marcar como error
                self._update_file_status(i, ProcessingStatus.ERROR, 0, str(e))
                if status_callback:
                    status_callback(i, self.file_statuses[i])
            
            # Actualizar progreso general
            self.overall_progress = int(((i + 1) / total_files) * 100)
            if progress_callback:
                progress_callback(self.overall_progress)
    
    def _process_single_file(self, input_path: str, output_path: str, 
                            progress_callback: Callable):
        """Procesa un archivo individual según la operación"""
        if self.operation == 'compress':
            compress_pdf(input_path, output_path, 'medium', progress_callback)
        elif self.operation == 'convert':
            pdf_to_word_with_layout(input_path, output_path, progress_callback)
        elif self.operation == 'ocr':
            apply_ocr_to_pdf(input_path, output_path, 'spa', progress_callback)
        # ... otras operaciones
    
    def _update_file_status(self, index: int, status: ProcessingStatus, 
                           progress: int = None, error: str = ""):
        """Actualiza el estado de un archivo"""
        self.file_statuses[index].status = status
        if progress is not None:
            self.file_statuses[index].progress = progress
        if error:
            self.file_statuses[index].error_message = error
    
    def _update_file_progress(self, index: int, progress: int):
        """Actualiza solo el progreso"""
        self.file_statuses[index].progress = progress
```

#### Carpeta Vigilada (Watch Folder)

**Concepto**: Monitorea una carpeta y procesa automáticamente nuevos archivos

```python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PDFWatcherHandler(FileSystemEventHandler):
    """Manejador de eventos de archivos PDF"""
    
    def __init__(self, batch_processor: BatchProcessor, callback: Callable):
        self.batch_processor = batch_processor
        self.callback = callback
    
    def on_created(self, event):
        """Se ejecuta cuando se crea un archivo nuevo"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        # Verificar si es PDF
        if file_path.lower().endswith('.pdf'):
            print(f"Nuevo archivo detectado: {file_path}")
            
            # Esperar a que termine de copiarse
            time.sleep(1)
            
            # Procesar automáticamente
            self.batch_processor.process_batch([file_path], self.callback)

def setup_watch_folder(folder_path: str, operation: str, callback: Callable):
    """
    Configura la carpeta vigilada
    
    Args:
        folder_path: Ruta de la carpeta a vigilar
        operation: Operación a realizar automáticamente
        callback: Función a llamar cuando se procesa un archivo
    """
    batch_processor = BatchProcessor(operation)
    event_handler = PDFWatcherHandler(batch_processor, callback)
    
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    
    print(f"Vigilando carpeta: {folder_path}")
    print(f"Operación automática: {operation}")
    
    return observer  # Retornar para poder detenerlo después

# Uso
observer = setup_watch_folder(
    "/ruta/a/carpeta", 
    "compress",
    lambda idx, status: print(f"Archivo {idx}: {status}")
)

# Para detener
observer.stop()
observer.join()
```

---

## Procesamiento de Archivos

### FileDropzone - Gestión de Archivos

#### Eventos de Drag & Drop

```typescript
// Evento: Archivo arrastrado sobre la zona
const handleDragEnter = (e: React.DragEvent) => {
  e.preventDefault();
  e.stopPropagation();
  setIsDragging(true);  // Activar estado visual
};

// Evento: Archivo sale de la zona
const handleDragLeave = (e: React.DragEvent) => {
  e.preventDefault();
  e.stopPropagation();
  setIsDragging(false);  // Desactivar estado visual
};

// Evento: Archivo se mantiene sobre la zona (requerido)
const handleDragOver = (e: React.DragEvent) => {
  e.preventDefault();  // Crucial: permitir drop
  e.stopPropagation();
};

// Evento: Archivo soltado
const handleDrop = (e: React.DragEvent) => {
  e.preventDefault();
  e.stopPropagation();
  setIsDragging(false);
  
  // Extraer archivos
  const droppedFiles = Array.from(e.dataTransfer.files);
  
  // Aplicar límite
  const limitedFiles = droppedFiles.slice(0, maxFiles);
  
  // Actualizar estado
  setSelectedFiles(limitedFiles);
  onFilesSelected(limitedFiles);
};
```

#### Selección Manual de Archivos

```typescript
const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
  const inputFiles = Array.from(e.target.files || []);
  const limitedFiles = inputFiles.slice(0, maxFiles);
  
  setSelectedFiles(limitedFiles);
  onFilesSelected(limitedFiles);
};

// Input oculto
<input
  type="file"
  accept={accept}  // ".pdf", ".doc,.docx", etc.
  multiple={multiple}
  onChange={handleFileInput}
  className="absolute inset-0 opacity-0 cursor-pointer"
/>
```

#### Eliminación de Archivos

```typescript
const removeFile = (index: number) => {
  // Filtrar el archivo en el índice especificado
  const newFiles = selectedFiles.filter((_, i) => i !== index);
  
  // Actualizar estado local
  setSelectedFiles(newFiles);
  
  // Notificar al padre
  onFilesSelected(newFiles);
};
```

#### Validación de Archivos

```python
def validate_file(file_path: str, operation: str) -> tuple[bool, str]:
    """
    Valida si un archivo es válido para la operación
    
    Returns:
        (es_valido, mensaje_error)
    """
    # Verificar existencia
    if not os.path.exists(file_path):
        return False, "El archivo no existe"
    
    # Verificar tamaño
    max_size = 100 * 1024 * 1024  # 100 MB
    if os.path.getsize(file_path) > max_size:
        return False, "El archivo excede el tamaño máximo (100 MB)"
    
    # Verificar extensión según operación
    extension = os.path.splitext(file_path)[1].lower()
    
    valid_extensions = {
        'merge': ['.pdf'],
        'split': ['.pdf'],
        'compress': ['.pdf'],
        'convert_to_word': ['.pdf'],
        'convert_to_pdf': ['.doc', '.docx'],
        'security': ['.pdf'],
        'ocr': ['.pdf'],
    }
    
    if operation in valid_extensions:
        if extension not in valid_extensions[operation]:
            return False, f"Extensión no válida. Se esperaba: {', '.join(valid_extensions[operation])}"
    
    # Verificar integridad del PDF
    if extension == '.pdf':
        try:
            with open(file_path, 'rb') as f:
                PyPDF2.PdfReader(f)
        except Exception as e:
            return False, f"El PDF está corrupto: {str(e)}"
    
    return True, ""
```

---

## Validaciones y Manejo de Errores

### Sistema de Validaciones

#### Validaciones por Operación

```python
class ValidationError(Exception):
    """Error de validación"""
    pass

class PDFValidator:
    """Validador de operaciones PDF"""
    
    @staticmethod
    def validate_merge(files: List[str]) -> None:
        """Valida operación de combinar"""
        if len(files) < 2:
            raise ValidationError("Se requieren al menos 2 archivos para combinar")
        
        if len(files) > 50:
            raise ValidationError("Máximo 50 archivos permitidos")
        
        for file in files:
            if not file.lower().endswith('.pdf'):
                raise ValidationError(f"Archivo no válido: {file}")
    
    @staticmethod
    def validate_split(file: str, mode: str, config: dict, total_pages: int) -> None:
        """Valida operación de dividir"""
        if mode == 'range':
            start = config.get('start', 1)
            end = config.get('end', total_pages)
            
            if start < 1:
                raise ValidationError("La página inicial debe ser >= 1")
            
            if end > total_pages:
                raise ValidationError(f"La página final no puede exceder {total_pages}")
            
            if start > end:
                raise ValidationError("La página inicial debe ser <= página final")
        
        elif mode == 'pages':
            pages = parse_page_specification(config['pages'])
            
            if not pages:
                raise ValidationError("Debe especificar al menos una página")
            
            if max(pages) > total_pages:
                raise ValidationError(f"Página {max(pages)} excede el total de {total_pages}")
        
        elif mode == 'every':
            n = config.get('n', 1)
            
            if n < 1:
                raise ValidationError("Debe dividir cada 1 o más páginas")
    
    @staticmethod
    def validate_compress(files: List[str], quality: str) -> None:
        """Valida operación de comprimir"""
        if not files:
            raise ValidationError("Debe seleccionar al menos un archivo")
        
        valid_qualities = ['low', 'medium', 'high', 'extreme']
        if quality not in valid_qualities:
            raise ValidationError(f"Calidad inválida. Use: {', '.join(valid_qualities)}")
    
    @staticmethod
    def validate_security(file: str, mode: str, password: str = None) -> None:
        """Valida operación de seguridad"""
        if mode in ['encrypt', 'decrypt']:
            if not password:
                raise ValidationError("Debe proporcionar una contraseña")
            
            if mode == 'encrypt' and len(password) < 4:
                raise ValidationError("La contraseña debe tener al menos 4 caracteres")
    
    @staticmethod
    def validate_ocr(files: List[str], language: str) -> None:
        """Valida operación de OCR"""
        if not files:
            raise ValidationError("Debe seleccionar al menos un archivo")
        
        valid_languages = ['spa', 'eng', 'por', 'fra', 'deu', 'ita']
        if language not in valid_languages:
            raise ValidationError(f"Idioma no soportado: {language}")
```

### Manejo de Errores

#### Tipos de Errores

```python
class PDFError(Exception):
    """Error base para operaciones PDF"""
    pass

class PDFProcessingError(PDFError):
    """Error durante el procesamiento"""
    pass

class PDFSecurityError(PDFError):
    """Error relacionado con seguridad"""
    pass

class OCRError(PDFError):
    """Error durante OCR"""
    pass

class ConversionError(PDFError):
    """Error durante conversión"""
    pass
```

#### Wrapper de Manejo de Errores

```python
def safe_pdf_operation(operation_func: Callable, 
                       error_callback: Callable = None) -> Callable:
    """
    Decorador para manejo seguro de errores
    
    Usage:
        @safe_pdf_operation
        def my_operation(file):
            # ... código ...
    """
    def wrapper(*args, **kwargs):
        try:
            return operation_func(*args, **kwargs)
        
        except ValidationError as e:
            error_msg = f"Error de validación: {str(e)}"
            if error_callback:
                error_callback(error_msg)
            raise
        
        except PDFSecurityError as e:
            error_msg = f"Error de seguridad: {str(e)}"
            if error_callback:
                error_callback(error_msg)
            raise
        
        except PDFProcessingError as e:
            error_msg = f"Error de procesamiento: {str(e)}"
            if error_callback:
                error_callback(error_msg)
            raise
        
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            if error_callback:
                error_callback(error_msg)
            raise PDFError(error_msg)
    
    return wrapper

# Uso
@safe_pdf_operation
def merge_pdfs(files, output):
    # ... implementación ...
    pass
```

---

## Sistema de Notificaciones

### Librería: Sonner (Toast Notifications)

#### Tipos de Notificaciones

```typescript
import { toast } from 'sonner';

// Éxito
toast.success('¡PDFs combinados exitosamente!');

// Error
toast.error('Por favor selecciona un archivo PDF');

// Información
toast.info('Analizando estructura del documento...');

// Advertencia
toast.warning('Se recomienda usar al menos 8 caracteres');

// Cargando (con promise)
toast.promise(
  asyncOperation(),
  {
    loading: 'Procesando...',
    success: '¡Completado!',
    error: 'Error al procesar'
  }
);
```

#### Posicionamiento

```typescript
<Toaster position="top-right" />
```

Posiciones disponibles:
- `top-left`
- `top-center`
- `top-right` ✓ (usado)
- `bottom-left`
- `bottom-center`
- `bottom-right`

#### Implementación en PySide6

```python
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt, QPropertyAnimation, QPoint

class ToastNotification(QLabel):
    """Notificación toast estilo Sonner"""
    
    def __init__(self, message: str, type: str, parent=None):
        super().__init__(message, parent)
        
        # Estilo según tipo
        styles = {
            'success': 'background: #10b981; color: white;',
            'error': 'background: #ef4444; color: white;',
            'info': 'background: #3b82f6; color: white;',
            'warning': 'background: #f59e0b; color: white;',
        }
        
        self.setStyleSheet(f"""
            {styles.get(type, styles['info'])}
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
        """)
        
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Posicionar en top-right
        parent_rect = parent.rect()
        self.adjustSize()
        x = parent_rect.width() - self.width() - 20
        y = 20
        self.move(x, y)
        
        # Animación de entrada
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(300)
        self.animation.setStartValue(QPoint(x, -self.height()))
        self.animation.setEndValue(QPoint(x, y))
        self.animation.start()
        
        # Auto-hide después de 3 segundos
        QTimer.singleShot(3000, self.hide_toast)
    
    def hide_toast(self):
        """Oculta el toast con animación"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()

# Uso
def show_toast(message: str, type: str = 'info'):
    """Muestra una notificación toast"""
    toast = ToastNotification(message, type, main_window)
    toast.show()
```

---

## Componentes Compartidos

### OperationHeader (No implementado en el código actual, pero útil)

```typescript
interface OperationHeaderProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export function OperationHeader({ icon: Icon, title, description }: OperationHeaderProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-8"
    >
      <div className="flex items-center gap-4 mb-4">
        <div className="w-14 h-14 bg-black rounded-2xl flex items-center justify-center">
          <Icon className="w-7 h-7 text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
          <p className="text-gray-600">{description}</p>
        </div>
      </div>
    </motion.div>
  );
}

// Uso
<OperationHeader
  icon={Combine}
  title="Combinar PDFs"
  description="Une múltiples archivos PDF en uno solo"
/>
```

---

## Integración con Bibliotecas

### Bibliotecas Python Requeridas

```
# Manipulación de PDFs
PyPDF2==3.0.1          # Merge, split, metadata
pikepdf==8.10.1        # Compress, security, advanced
pypdf==3.17.4          # Alternativa moderna a PyPDF2

# Conversión
pdf2docx==0.5.6        # PDF → Word (Layout Engine)
python-docx==1.1.0     # Crear/modificar DOCX
docx2pdf==0.1.8        # Word → PDF (requiere MS Word/LibreOffice)
pdf2image==1.16.3      # PDF → Imágenes
Pillow==10.1.0         # Manipulación de imágenes

# OCR
pytesseract==0.3.10    # Binding de Tesseract
tesseract-ocr          # Motor OCR (instalación del sistema)

# Procesamiento
watchdog==3.0.0        # Watch folder
tqdm==4.66.1           # Progress bars

# GUI (PySide6)
PySide6==6.6.1         # Qt for Python
```

### Instalación de Tesseract

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-spa  # Español
sudo apt-get install tesseract-ocr-eng  # Inglés

# macOS
brew install tesseract
brew install tesseract-lang  # Todos los idiomas

# Windows
# Descargar instalador desde: https://github.com/UB-Mannheim/tesseract/wiki
# Agregar al PATH: C:\Program Files\Tesseract-OCR
```

### Configuración de Tesseract

```python
import pytesseract

# Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Verificar instalación
def check_tesseract():
    """Verifica que Tesseract esté instalado"""
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract version: {version}")
        return True
    except Exception as e:
        print(f"Tesseract no encontrado: {e}")
        return False

# Listar idiomas disponibles
def list_languages():
    """Lista idiomas OCR disponibles"""
    return pytesseract.get_languages()
```

---

## Flujos de Usuario Completos

### Flujo 1: Combinar PDFs

```
1. Usuario hace clic en "Combinar" desde Dashboard o Sidebar
   └─> App.currentView = 'merge'
   └─> Se renderiza <MergePDF />

2. Usuario arrastra 3 archivos PDF al Dropzone
   └─> handleDrop() captura archivos
   └─> setFiles([file1, file2, file3])
   └─> Se muestra lista reordenable

3. Usuario reordena archivos (arrastra file3 al principio)
   └─> Reorder.Group detecta cambio
   └─> onReorder([file3, file1, file2])
   └─> setFiles actualiza orden

4. Usuario hace clic en "Combinar PDFs"
   └─> handleMerge() se ejecuta
   └─> Validación: 3 archivos >= 2 ✓
   └─> setIsProcessing(true)
   └─> Bucle de progreso 0→100
   └─> setIsComplete(true)
   └─> toast.success('¡PDFs combinados exitosamente!')

5. Usuario hace clic en "Descargar"
   └─> handleDownload()
   └─> toast.success('Descargando archivo combinado...')
   └─> [En implementación real: descarga archivo]
```

### Flujo 2: Asistente Inteligente

```
1. Usuario hace clic en card del Asistente en Dashboard
   └─> onNavigate('wizard')
   └─> Se renderiza <Wizard />

2. Se muestra primera pregunta: "¿Qué quieres hacer?"
   └─> 6 opciones disponibles
   └─> Usuario hace clic en "Convertir a otro formato"

3. handleOptionSelect() se ejecuta
   └─> Opción tiene nextQuestion = 'convert'
   └─> setCurrentQuestion('convert')
   └─> setSelectedPath(['Convertir a otro formato'])
   └─> Animación de transición
   └─> Se muestra segunda pregunta

4. Se muestra segunda pregunta: "¿A qué formato?"
   └─> 4 opciones disponibles
   └─> Usuario hace clic en "PDF a Word (DOCX)"

5. handleOptionSelect() se ejecuta
   └─> Opción tiene result = 'convert'
   └─> setRecommendedAction('convert')
   └─> setIsComplete(true)
   └─> Animación a pantalla de resultado

6. Se muestra pantalla de resultado
   └─> Muestra path: ["Convertir...", "PDF a Word"]
   └─> Usuario hace clic en "Ir a la función"

7. handleGoToAction() se ejecuta
   └─> onNavigate('convert')
   └─> Se renderiza <ConvertPDF />
   └─> Tipo 'pdf-to-word' pre-seleccionado
```

### Flujo 3: OCR con Progreso Detallado

```
1. Usuario navega a OCR
   └─> Se renderiza <OCRPdf />

2. Usuario carga 1 PDF de 15 páginas
   └─> setFiles([file])
   └─> Se muestra selector de idioma

3. Usuario selecciona "Español"
   └─> setLanguage('spa')

4. Usuario hace clic en "Aplicar OCR"
   └─> handleOCR() se ejecuta
   └─> setDetectedPages(15) [simulado]
   └─> setIsProcessing(true)
   └─> Bucle de progreso con mensajes:

   Progreso 10%:
   └─> toast.info('Detectando páginas escaneadas...')
   └─> processedPages = 1 / 15

   Progreso 30%:
   └─> toast.info('Aplicando OCR con Tesseract...')
   └─> processedPages = 4 / 15

   Progreso 60%:
   └─> toast.info('Extrayendo texto...')
   └─> processedPages = 9 / 15

   Progreso 90%:
   └─> toast.info('Generando PDF con capa de texto...')
   └─> processedPages = 13 / 15

   Progreso 100%:
   └─> setIsComplete(true)
   └─> toast.success('¡OCR completado exitosamente!')
   └─> processedPages = 15 / 15

5. Se muestra card de éxito
   └─> "15 páginas procesadas con texto reconocido"
   └─> Lista de beneficios
   └─> Botón "Descargar"
```

### Flujo 4: Procesamiento por Lotes

```
1. Usuario navega a Lotes
   └─> Se renderiza <BatchProcessing />

2. Usuario selecciona operación "Comprimir cada uno"
   └─> setOperation('compress')

3. Usuario carga 5 archivos PDF
   └─> setFiles([file1, file2, file3, file4, file5])

4. Usuario hace clic en "Iniciar Procesamiento"
   └─> handleProcess() se ejecuta
   └─> Inicializa fileStatuses:
       [
         {name: 'file1.pdf', status: 'pending', progress: 0},
         {name: 'file2.pdf', status: 'pending', progress: 0},
         {name: 'file3.pdf', status: 'pending', progress: 0},
         {name: 'file4.pdf', status: 'pending', progress: 0},
         {name: 'file5.pdf', status: 'pending', progress: 0}
       ]

5. Procesamiento de file1:
   └─> fileStatuses[0].status = 'processing'
   └─> Progreso individual: 0→20→40→60→80→100
   └─> fileStatuses[0].status = 'completed'
   └─> overallProgress = 20% (1/5)

6. Procesamiento de file2:
   └─> fileStatuses[1].status = 'processing'
   └─> Progreso individual: 0→100
   └─> fileStatuses[1].status = 'completed'
   └─> overallProgress = 40% (2/5)

   [... continúa con file3, file4, file5 ...]

7. Todos completados:
   └─> overallProgress = 100%
   └─> setIsComplete(true)
   └─> toast.success('¡5 archivos procesados exitosamente!')

8. Usuario hace clic en "Descargar Todo"
   └─> handleDownload()
   └─> [En implementación real: descarga ZIP con todos]
```

---

## Resumen de Arquitectura para Implementación PySide6

### Estructura Recomendada

```
localpdf_v5/
│
├── main.py                    # Punto de entrada
├── ui/
│   ├── main_window.py         # Ventana principal
│   ├── sidebar.py             # Sidebar widget
│   ├── dashboard.py           # Dashboard widget
│   ├── wizard.py              # Wizard widget
│   └── operations/
│       ├── merge_widget.py
│       ├── split_widget.py
│       ├── compress_widget.py
│       ├── convert_widget.py
│       ├── security_widget.py
│       ├── ocr_widget.py
│       └── batch_widget.py
│
├── components/
│   ├── file_dropzone.py       # Dropzone reutilizable
│   ├── progress_bar.py        # Barra de progreso custom
│   └── toast.py               # Sistema de notificaciones
│
├── processors/
│   ├── pdf_merger.py          # Lógica de combinar
│   ├── pdf_splitter.py        # Lógica de dividir
│   ├── pdf_compressor.py      # Lógica de comprimir
│   ├── pdf_converter.py       # Lógica de convertir
│   ├── pdf_security.py        # Lógica de seguridad
│   ├── pdf_ocr.py             # Lógica de OCR
│   └── batch_processor.py     # Lógica de lotes
│
├── utils/
│   ├── validators.py          # Validaciones
│   ├── file_utils.py          # Utilidades de archivos
│   └── errors.py              # Excepciones custom
│
└── resources/
    ├── icons/                 # Iconos SVG
    └── styles.qss            # Estilos Qt
```

### MainWindow

```python
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QHBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LocalPDF v5.0")
        self.setMinimumSize(1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.setFixedWidth(264)
        self.sidebar.view_changed.connect(self.navigate_to_view)
        main_layout.addWidget(self.sidebar)
        
        # Stacked widget para vistas
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Agregar todas las vistas
        self.views = {
            'dashboard': DashboardWidget(),
            'wizard': WizardWidget(),
            'merge': MergeWidget(),
            'split': SplitWidget(),
            'compress': CompressWidget(),
            'convert': ConvertWidget(),
            'security': SecurityWidget(),
            'ocr': OCRWidget(),
            'batch': BatchWidget(),
        }
        
        for name, widget in self.views.items():
            self.stacked_widget.addWidget(widget)
        
        # Vista inicial
        self.navigate_to_view('dashboard')
    
    def navigate_to_view(self, view_name: str):
        """Cambia la vista actual"""
        widget = self.views.get(view_name)
        if widget:
            self.stacked_widget.setCurrentWidget(widget)
            self.sidebar.set_current_view(view_name)
```

---

Esta documentación técnica completa proporciona toda la lógica funcional, algoritmos, flujos de datos y patrones de implementación del proyecto LocalPDF v5, lista para ser utilizada como referencia en el desarrollo con PySide6.


VISUALMENTE:

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


PRONT DEFINITIVO:
Rol del asistente

Actúa como un arquitecto de software senior con experiencia en:

Aplicaciones de escritorio profesionales

Procesamiento de documentos PDF

Conversión PDF ↔ Word con preservación de layout

Qt 6, Python y C++

Tu tarea es crear un proyecto completo desde cero, estable y funcional.

Objetivo del proyecto

Desarrollar una aplicación de escritorio local llamada LocalPDF, similar a iLovePDF, que funcione 100% offline y permita trabajar con PDFs de forma profesional.

Debe ser un proyecto realista, usable y extensible, no un demo.

Funcionalidades OBLIGATORIAS
1. Gestión de PDFs

Unir múltiples PDFs en uno solo

Dividir un PDF por páginas o rangos

Reordenar páginas (estructura preparada, aunque UI simple)

2. Conversión

PDF → Word (prioridad máxima)

Preservar:

Texto

Tablas

Columnas

Márgenes razonables

Word → PDF (básico)

3. Flujo guiado (asistente)

Antes de ejecutar cualquier acción:

Detectar el tipo de archivo cargado

Preguntar al usuario:

“¿Qué deseas hacer con este archivo?”

Opciones según contexto (unir, convertir, dividir, etc.)

Confirmar antes de generar y descargar el archivo final

4. Interfaz de usuario

Ventana principal clara y simple

Área central con Drag & Drop

Botones claros por acción

Barra de progreso real (no simulada)

Mensajes de error comprensibles

5. Drag & Drop (CRÍTICO)

Arrastrar archivos desde el explorador de Windows

Soporte para:

Múltiples PDFs

Rutas con espacios y acentos

Validación automática de tipo de archivo

Stack tecnológico (OBLIGATORIO)
Lenguajes

Python 3.10+ → aplicación principal

C++17 → motor PDF (preparado para futuro)

UI

Qt 6

Python bindings: PySide6

Procesamiento PDF

MuPDF

Uso de mutool.exe vía subprocess

PyMuPDF (fitz) → análisis de estructura

pdf2docx → base para PDF → Word

Empaquetado

PyInstaller (Windows)

Arquitectura requerida (DESDE CERO)
Estructura del proyecto esperada
LocalPDF/
├── app/
│   ├── main.py
│   ├── main_window.py
│   ├── workflow_controller.py
│   ├── workers.py
│   └── widgets/
│       └── drop_zone.py
│
├── engines/
│   ├── pdf_merge.py
│   ├── pdf_split.py
│   ├── pdf_to_word.py
│   ├── word_to_pdf.py
│   └── layout_engine/
│       └── structure_detector.py
│
├── cpp_core/
│   ├── mupdf_bridge.py
│   └── vendor/
│       └── mupdf/
│           └── mutool.exe
│
├── assets/
├── tests/
├── requirements.txt
├── pyinstaller.spec
└── README.md

Reglas técnicas IMPORTANTES
Concurrencia

No bloquear la UI

Usar un solo sistema de workers

Progreso real por señales

Manejo correcto de errores (try/except + señales)

Separación de responsabilidades

UI no procesa PDFs

UI solo llama al controlador

Engines no conocen la UI

mupdf_bridge.py (OBLIGATORIO)

Crear un wrapper claro para MuPDF con funciones como:

get_page_count(pdf_path)

extract_text(pdf_path)

render_page(pdf_path, page_index)

Debe manejar:

Errores de ejecución

Encoding UTF-8

Paths de Windows correctamente

Conversión PDF → Word (CRÍTICO)

Implementar un pipeline real:

Analizar estructura con PyMuPDF

Convertir con pdf2docx

Ajustar layout:

Detectar tablas

Respetar columnas

Generar un .docx usable

Si algo falla:

Mostrar error claro

No colgar la aplicación

Empaquetado final

Generar un .exe único

No requerir Python instalado

Incluir:

Qt

mutool

DLLs necesarias

Qué NO hacer

No usar Electron

No usar servicios web

No simular procesos

No dejar botones que “no hacen nada”

No dejar funciones incompletas sin avisar

Resultado esperado

Al finalizar, el proyecto debe:

Abrir correctamente

Aceptar PDFs por Drag & Drop

Unir PDFs sin colgarse

Convertir PDF → Word de forma razonable

Mostrar progreso real

Estar listo para compilar y distribuir

Prioridad absoluta

La estabilidad y la claridad del flujo son más importantes que “muchas funciones”.

Si alguna funcionalidad es compleja:

Implementa una versión estable

Documenta cómo mejorarla


Recomendación ÓPTIMA (arquitectura por capas)
🧠 Visión general
Capa	Lenguaje	Motivo
UI / UX	C++ (Qt 6)	Máximo control, rendimiento y calidad nativa
Motor PDF	C++17 / C++20	Manipulación avanzada de PDFs sin límites
Lógica avanzada / IA	Python	OCR, NLP, layout, ML
Automatización / plugins	Python	Extensibilidad futura
Integraciones	C / C++ bindings	Interoperabilidad

👉 Este stack es el mismo enfoque que usan Adobe, Foxit, PDF-XChange.

Lenguaje por lenguaje (con razones reales)
1️⃣ C++ — EL CORAZÓN DEL PROYECTO

C++ debe ser el núcleo.

Por qué C++ es obligatorio para un proyecto ambicioso

Acceso directo a:

MuPDF

Poppler

PDFium

Máximo rendimiento

Control total de memoria

PDFs grandes (500–2000 páginas)

Renderizado preciso

OCR por lotes

Multithreading real

Qué debe hacerse en C++

✔ Motor PDF
✔ Renderizado
✔ Manipulación de páginas
✔ Layout engine
✔ Pipeline PDF → Word avanzado
✔ Plugins nativos

Librerías clave

MuPDF

Poppler

ICU (Unicode)

HarfBuzz (texto complejo)

OpenCV (preprocesado OCR)

Tesseract (C++ API)

📌 Conclusión:

Si no usas C++, el proyecto tendrá un techo técnico.

2️⃣ Qt 6 (C++) — UI PROFESIONAL

Qt 6 + C++ es la única opción seria si quieres ambición real.

Ventajas

UI nativa (no web disfrazada)

Drag & Drop robusto

Accesibilidad

DPI scaling real

Multiplataforma (Windows / Linux / macOS)

Integración directa con C++

Por qué no Electron / Flutter

PDFs grandes → lag

Consumo absurdo de RAM

Limitaciones de render

No controlas el pipeline

📌 Conclusión:

Qt es el estándar industrial para software técnico.

3️⃣ Python — EL CEREBRO FLEXIBLE

Python NO debe ser el núcleo, pero SÍ es vital.

Usos ideales de Python

OCR avanzado

Post-procesado de texto

IA (layout detection)

NLP (detección de títulos, tablas)

Plugins

Automatizaciones

Testing rápido

Cómo integrarlo correctamente

Python embebido

Comunicación vía:

pybind11

C API

subprocess controlado

📌 Regla de oro:

Python acelera el desarrollo, C++ garantiza calidad.

4️⃣ Lenguajes que NO recomiendo para un proyecto ambicioso
Lenguaje	Motivo
JavaScript	PDFs grandes = desastre
Electron	Pesado, lento
Flutter	PDFs complejos = limitaciones
C#	Bueno, pero ecosistema PDF inferior
Java	UI pobre para desktop moderno
Arquitectura FINAL recomendada
LocalPDF
│
├── ui/
│   └── Qt 6 (C++)
│
├── core/
│   ├── pdf_engine/        (C++)
│   ├── layout_engine/    (C++)
│   ├── render_engine/    (C++)
│
├── python/
│   ├── ocr/
│   ├── nlp/
│   └── plugins/
│
├── bindings/
│   └── pybind11
│
└── installer/

Si quieres el MÁXIMO nivel (nivel Adobe-lite)

Añadir:

Rust

Para módulos críticos de seguridad

Sandboxing

Parsing seguro

Pero esto es nivel experto y no obligatorio al inicio.

Recomendación FINAL (sin rodeos)

C++ + Qt 6 como base
Python como cerebro flexible
Bindings limpios entre ambos

Ese combo:

No tiene techo

Escala a producto comercial

Permite IA, OCR, cloud híbrido si quieres

Te prepara para vender licencias

