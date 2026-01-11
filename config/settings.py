"""
Configuración centralizada de LocalPDF v5
Lee variables de entorno del archivo .env y proporciona valores por defecto
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env (si existe)
load_dotenv()

class Settings:
    """Clase de configuración global de la aplicación"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa los valores de configuración"""
        self.IS_FROZEN = getattr(sys, 'frozen', False)
        self.IS_WINDOWS = sys.platform.startswith('win')
        
        # ==================== PATHS PRINCIPALES ====================
        if self.IS_FROZEN:
            # En ejecutable: sys.executable es la app, _MEIPASS es temp
            self.BASE_DIR = Path(sys.executable).parent
            self._MEIPASS = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
            self.LIBS_DIR = Path(self._MEIPASS) / 'libs'
        else:
            # En desarrollo
            self.BASE_DIR = Path(__file__).parent.parent
            self.LIBS_DIR = self.BASE_DIR.parent / 'libs'  # Ajustar según estructura real

        # ==================== PATHS EXTERNOS (OCR/Tools) ====================
        self._configure_external_tools()

        # ==================== DIRECTORIOS DE DATOS ====================
        self.TEMP_DIR = self.BASE_DIR / os.getenv('TEMP_DIR', 'temp')
        self.ASSETS_DIR = self.BASE_DIR / 'assets'
        
        # Output dir depende del contexto
        if self.IS_FROZEN:
            self.OUTPUT_DIR = Path.home() / "Documents" / "Vectora"
        else:
            self.OUTPUT_DIR = self.BASE_DIR / os.getenv('OUTPUT_DIR', 'output')

        # ==================== CONFIGURACIONES ====================
        self.APP_NAME = "Vectora"
        self.APP_VERSION = "5.0.0"
        self.APP_AUTHOR = "Vectora"
        
        # OCR
        self.TESSERACT_LANG = os.getenv('TESSERACT_LANG', 'spa+eng')
        self.OCR_DPI = int(os.getenv('OCR_DPI', 300))
        
        # Conversión
        self.PDF_TO_IMAGE_DPI = int(os.getenv('PDF_TO_IMAGE_DPI', 300))
        self.IMAGE_FORMAT = os.getenv('IMAGE_FORMAT', 'PNG')
        self.WORD_CONVERSION_AVAILABLE = os.getenv('WORD_CONVERSION_AVAILABLE', 'True').lower() == 'true'
        
        # Límites
        self.MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 100))
        self.MAX_BATCH_FILES = int(os.getenv('MAX_BATCH_FILES', 50))
        
        self.COMPRESSION_LEVELS = {
            'low': {'value': 25, 'quality': 90, 'label': 'Baja', 'reduction': '~20%', 'description': 'Alta calidad'},
            'medium': {'value': 50, 'quality': 70, 'label': 'Media', 'reduction': '~40%', 'description': 'Calidad equilibrada'},
            'high': {'value': 75, 'quality': 50, 'label': 'Alta', 'reduction': '~60%', 'description': 'Compresión fuerte'},
            'extreme': {'value': 100, 'quality': 30, 'label': 'Extrema', 'reduction': '~80%', 'description': 'Máxima compresión'}
        }

    def _configure_external_tools(self):
        """Configura rutas de Tesseract y Poppler"""
        if self.IS_FROZEN:
            self.TESSERACT_PATH = os.path.join(self.LIBS_DIR, 'tesseract', 'tesseract.exe')
            self.POPPLER_PATH = os.path.join(self.LIBS_DIR, 'poppler')
        else:
            # Intentar buscar en libs local primero
            local_tess = self.LIBS_DIR / 'tesseract' / 'tesseract.exe'
            local_pop = self.LIBS_DIR / 'poppler'
            
            # Tesseract
            if local_tess.exists():
                self.TESSERACT_PATH = str(local_tess)
            else:
                self.TESSERACT_PATH = os.getenv('TESSERACT_PATH', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
            
            # Poppler
            if local_pop.exists():
                self.POPPLER_PATH = str(local_pop)
            else:
                self.POPPLER_PATH = os.getenv('POPPLER_PATH', r'C:\Program Files\poppler-24.02.0\Library\bin')

    def ensure_directories(self):
        """Crea los directorios necesarios (Lazy Creation)"""
        try:
            self.TEMP_DIR.mkdir(exist_ok=True, parents=True)
            self.OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
            self.ASSETS_DIR.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            print(f"Error creando directorios: {e}")

    def get_compression_level(self, value: int) -> str:
        """Determina el nivel de compresión según el valor del slider"""
        if value <= 25: return 'low'
        elif value <= 50: return 'medium'
        elif value <= 75: return 'high'
        else: return 'extreme'

# Instancia singleton de configuración
settings = Settings()
# Nota: ensure_directories() ya no se llama automáticamente al importar
# para evitar efectos secundarios. Debe llamarse en el main.py
