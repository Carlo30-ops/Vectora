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
