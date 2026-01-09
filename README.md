# Vectora v5 - Editor de PDFs Profesional

![Vectora v5](https://img.shields.io/badge/version-5.0.0-black.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-Qt%20for%20Python-green.svg)

## 📋 Descripción

**Vectora v5** es un editor de PDFs profesional y gratuito construido con PySide6 (Qt para Python). Permite realizar operaciones avanzadas sobre archivos PDF de forma local, sin necesidad de internet y protegiendo tu privacidad.

### ✨ Características Principales

- **📑 Combinar PDFs**: Une múltiples archivos PDF en uno solo
- **✂️ Dividir PDFs**: Extrae rangos de páginas o páginas específicas
- **🗜️ Comprimir PDFs**: Reduce el tamaño de archivos
- **🔄 Convertir**: PDF ↔ Word, PDF ↔ Imágenes
- **🔒 Seguridad**: Protege archivos con contraseña
- **🔍 OCR**: Extrae texto de PDFs escaneados
- **⚡ Procesamiento por Lotes**: Aplica operaciones a múltiples archivos
- **🧙 Asistente Inteligente**: Te guía paso a paso

## 🚀 Instalación

### Requisitos Previos

1. **Python 3.8+**
2. **Tesseract OCR** (para funcionalidad OCR)

   - Windows: Descargar desde [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
   - Instalar en `C:\Program Files\Tesseract-OCR` o actualizar la ruta en `.env`

3. **Poppler** (para conversión PDF ↔ Imágenes)
   - Descomprimir `poppler-25.12.0.zip` en `C:\Program Files\poppler-25.12.0`
   - O actualizar la ruta en `.env`

### Instalación de Dependencias

```bash
# Clonar o descargar el repositorio
cd Vectora

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Configuración

1. Editar el archivo `.env` con las rutas correctas:

```env
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
POPPLER_PATH=C:\Program Files\poppler-25.12.0\Library\bin
```

2. Verificar que los directorios `temp` y `output` existen (se crean automáticamente)

## 🎯 Uso

### Iniciar la Aplicación

```bash
python main.py
```

### Operaciones Disponibles

#### 1. Combinar PDFs

1. Navega a **Combinar PDFs**
2. Agrega 2 o más archivos PDF
3. Haz clic en **Procesar**
4. El archivo combinado se guardará en la carpeta `output/`

#### 2. Dividir PDFs

1. Navega a **Dividir PDF**
2. Selecciona un archivo PDF
3. Elige el modo de división:
   - **Por Rango**: Páginas 5-10
   - **Páginas Específicas**: 1,3,5-8,12
   - **Cada N páginas**: Divide en chunks
4. Configura los parámetros y procesa

#### 3. Asistente Inteligente

1. Haz clic en **Asistente Inteligente** desde el Dashboard
2. Responde las preguntas
3. El asistente te recomendará la herramienta adecuada

## 📁 Estructura del Proyecto

```
Vectora/
├── main.py                      # Punto de entrada
├── .env                         # Configuración (variables de entorno)
├── requirements.txt             # Dependencias Python
│
├── config/                      # Configuración
│   ├── __init__.py
│   └── settings.py              # Settings centralizados
│
├── backend/                     # Lógica de negocio
│   └── services/                # Servicios de procesamiento PDF
│       ├── pdf_merger.py        # Combinar PDFs
│       ├── pdf_splitter.py      # Dividir PDFs
│       ├── pdf_compressor.py    # Comprimir PDFs
│       ├── pdf_converter.py     # Convertir formatos
│       ├── pdf_security.py      # Seguridad
│       ├── ocr_service.py       # OCR
│       └── batch_processor.py   # Procesamiento por lotes
│
├── ui/                          # Interfaz PySide6
│   ├── main_window.py           # Ventana principal
│   ├── components/
│   │   ├── sidebar.py           # Navegación
│   │   ├── dashboard.py         # Pantalla principal
│   │   ├── wizard.py            # Asistente
│   │   └── operation_widgets/   # Widgets de operaciones
│   └── styles/
│       └── styles.qss           # Estilos Qt
│
├── utils/                       # Utilidades
│   ├── file_handler.py          # Manejo de archivos
│   ├── validators.py            # Validaciones
│   └── notification_manager.py  # Notificaciones
│
├── temp/                        # Archivos temporales
└── output/                      # Archivos procesados
```

## 🛠️ Tecnologías Utilizadas

- **PySide6**: Framework de interfaz gráfica (Qt para Python)
- **PyPDF2**: Manipulación de PDFs
- **pikepdf**: Operaciones avanzadas (compresión, seguridad)
- **pdf2docx**: Conversión PDF → Word con Layout Engine
- **pdf2image**: Conversión PDF ↔ Imágenes
- **pytesseract**: OCR (reconocimiento de texto)
- **Pillow**: Procesamiento de imágenes

## 📝 Notas Importantes

### Estado de Desarrollo

- ✅ **Completamente funcional**: Combinar PDFs, Dividir PDFs
- ⚙️ **Backend implementado, UI en desarrollo**: Comprimir, Convertir, Seguridad, OCR, Lotes

### Limitaciones Conocidas

- **Conversión Word → PDF**: Requiere Microsoft Word instalado en Windows
- **PDFs muy grandes**: Pueden tener problemas de rendimiento (>500 páginas)
- **OCR**: Requiere idiomas de Tesseract instalados (español e inglés por defecto)

## 🔧 Desarrollo Futuro

### Próximas Características

- [ ] Completar UI para todas las operaciones
- [ ] Vista previa de PDFs
- [ ] Edición de metadatos
- [ ] Marcas de agua
- [ ] Firma digital
- [ ] Modo oscuro

### Optimizaciones Planificadas

- [ ] Migración del motor PDF a C++ para mejor rendimiento
- [ ] Caché de miniaturas
- [ ] Procesamiento paralelo mejorado

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama de feature (`git checkout -b feature/MejoraNueva`)
3. Commit tus cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/MejoraNueva`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 👤 Autor

**Vectora Team**

- Versión: 5.0.0
- Arquitectura: PySide6 (Python)

## 🙏 Agradecimientos

- Equipo de Qt/PySide6
- Desarrolladores de PyPDF2, pikepdf, pdf2docx
- Comunidad de Tesseract OCR
- Poppler developers

---

**💡 Tip**: Si tienes problemas, verifica que Tesseract y Poppler estén correctamente instalados y configurados en el archivo `.env`

**🔒 Privacidad**: Todos los archivos se procesan localmente en tu computadora. No se envía ningún dato a internet.
