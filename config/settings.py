"""
Configuración centralizada de LocalPDF v5
Lee variables de entorno del archivo .env y proporciona valores por defecto
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

class Settings:
    """Clase de configuración global de la aplicación"""
    
    # ==================== PATHS EXTERNOS ====================
    TESSERACT_PATH = os.getenv('TESSERACT_PATH', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    POPPLER_PATH = os.getenv('POPPLER_PATH', r'C:\Program Files\poppler-25.12.0\Library\bin')
    
    # ==================== CONFIGURACIÓN OCR ====================
    TESSERACT_LANG = os.getenv('TESSERACT_LANG', 'spa+eng')
    OCR_DPI = int(os.getenv('OCR_DPI', 300))
    
    # ==================== CONFIGURACIÓN DE CONVERSIÓN ====================
    PDF_TO_IMAGE_DPI = int(os.getenv('PDF_TO_IMAGE_DPI', 300))
    IMAGE_FORMAT = os.getenv('IMAGE_FORMAT', 'PNG')
    WORD_CONVERSION_AVAILABLE = os.getenv('WORD_CONVERSION_AVAILABLE', 'True').lower() == 'true'
    
    # ==================== CONFIGURACIÓN DE COMPRESIÓN ====================
    DEFAULT_COMPRESSION_QUALITY = os.getenv('DEFAULT_COMPRESSION_QUALITY', 'medium')
    
    COMPRESSION_LEVELS = {
        'low': {
            'value': 25,
            'quality': 90,
            'label': 'Baja',
            'reduction': '~20%',
            'description': 'Alta calidad'
        },
        'medium': {
            'value': 50,
            'quality': 70,
            'label': 'Media',
            'reduction': '~40%',
            'description': 'Calidad equilibrada'
        },
        'high': {
            'value': 75,
            'quality': 50,
            'label': 'Alta',
            'reduction': '~60%',
            'description': 'Compresión fuerte'
        },
        'extreme': {
            'value': 100,
            'quality': 30,
            'label': 'Extrema',
            'reduction': '~80%',
            'description': 'Máxima compresión'
        }
    }
    
    # ==================== DIRECTORIOS ====================
    # Detectar si se ejecuta desde PyInstaller
    if getattr(sys, 'frozen', False):
        # Ejecutable: usar carpeta del ejecutable como base
        BASE_DIR = Path(sys.executable).parent
    else:
        # Desarrollo: usar carpeta del proyecto
        BASE_DIR = Path(__file__).parent.parent
    
    TEMP_DIR = BASE_DIR / os.getenv('TEMP_DIR', 'temp')
    OUTPUT_DIR = BASE_DIR / os.getenv('OUTPUT_DIR', 'output')
    ASSETS_DIR = BASE_DIR / 'assets'
    
    # ==================== LÍMITES ====================
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 100))
    MAX_BATCH_FILES = int(os.getenv('MAX_BATCH_FILES', 50))
    
    # ==================== INFORMACIÓN DE LA APP ====================
    APP_NAME = "Vectora"
    APP_VERSION = "5.0.0"
    APP_AUTHOR = "Vectora Team"
    
    @classmethod
    def get_output_directory(cls):
        """
        Retorna el directorio de salida apropiado según el contexto
        
        En desarrollo: usa carpeta 'output' del proyecto
        En ejecutable: usa carpeta 'Vectora' en Documentos del usuario
        """
        if getattr(sys, 'frozen', False):
            # Ejecutable: usar Documentos del usuario
            user_docs = Path.home() / "Documents" / "Vectora"
            user_docs.mkdir(exist_ok=True, parents=True)
            return user_docs
        else:
            # Desarrollo: usar carpeta del proyecto
            return cls.OUTPUT_DIR
    
    @classmethod
    def ensure_directories(cls):
        """Crea los directorios necesarios si no existen"""
        cls.TEMP_DIR.mkdir(exist_ok=True, parents=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
        cls.ASSETS_DIR.mkdir(exist_ok=True, parents=True)
        
        # Asegurar que existe el directorio de salida apropiado
        cls.get_output_directory().mkdir(exist_ok=True, parents=True)
    
    @classmethod
    def get_compression_level(cls, value: int) -> str:
        """
        Determina el nivel de compresión según el valor del slider
        
        Args:
            value: Valor del slider (0-100)
            
        Returns:
            Clave del nivel de compresión ('low', 'medium', 'high', 'extreme')
        """
        if value <= 25:
            return 'low'
        elif value <= 50:
            return 'medium'
        elif value <= 75:
            return 'high'
        else:
            return 'extreme'

# Instancia singleton de configuración
settings = Settings()

# Asegurar que los directorios existen al importar
settings.ensure_directories()
