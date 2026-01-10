"""
Gestor de preferencias de usuario
Maneja la persistencia de configuraciones (tema, rutas, opciones)
"""
import json
import os
from pathlib import Path
from typing import Any, Dict
from utils.logger import get_logger

logger = get_logger(__name__)

class PreferencesManager:
    """Singleton para gestionar preferencias persistentes"""
    
    _instance = None
    _preferences: Dict[str, Any] = {}
    
    # Valores por defecto
    DEFAULTS = {
        "theme": "light",
        "last_folder_merge": str(Path.home()),
        "last_folder_split": str(Path.home()),
        "last_folder_compress": str(Path.home()),
        "compression_level": "medium",
        "window_size": [1024, 768],
        "window_position": [100, 100]
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_preferences()
        return cls._instance
    
    def _get_config_path(self) -> Path:
        """Obtiene la ruta del archivo de configuración JSON"""
        if os.getenv('APPDATA'):
            # Windows: AppData/Roaming/Vectora
            base = Path(os.getenv('APPDATA')) / 'Vectora'
        else:
            # Fallback: Home/Vectora
            base = Path.home() / 'Vectora'
            
        base.mkdir(parents=True, exist_ok=True)
        return base / 'preferences.json'
    
    def _load_preferences(self):
        """Carga preferencias desde disco"""
        config_path = self._get_config_path()
        if not config_path.exists():
            self._preferences = self.DEFAULTS.copy()
            return

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                # Merge con defaults para asegurar que existen todas las keys
                self._preferences = {**self.DEFAULTS, **saved}
                logger.info(f"Preferencias cargadas desde {config_path}")
        except Exception as e:
            logger.error(f"Error cargando preferencias: {e}")
            self._preferences = self.DEFAULTS.copy()
            
    def save(self):
        """Guarda preferencias a disco"""
        config_path = self._get_config_path()
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self._preferences, f, indent=4)
                logger.info("Preferencias guardadas exitosamente")
        except Exception as e:
            logger.error(f"Error guardando preferencias: {e}")
            
    def get(self, key: str, default=None) -> Any:
        """Obtiene una preferencia"""
        return self._preferences.get(key, default)
        
    def set(self, key: str, value: Any):
        """Establece una preferencia y guarda"""
        self._preferences[key] = value
        self.save()

# Instancia global
preferences = PreferencesManager()
