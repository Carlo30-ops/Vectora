"""
Servicio de vigilancia de carpetas para nuevos PDFs
Utiliza watchdog para detectar archivos y procesarlos automáticamente
"""
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from typing import Optional, Callable
from logging import Logger
from utils.logger import get_logger

class PDFWatcherHandler(FileSystemEventHandler):
    """Manejador de eventos de archivo"""
    
    def __init__(self, callback: Callable[[str], None], logger: Logger, retries: int, interval: float):
        self.callback = callback
        self.logger = logger
        self.processed = set()
        self.stability_retries = retries
        self.stability_interval = interval
    
    def on_created(self, event):
        if event.is_directory: return
        
        path = event.src_path
        if not path.lower().endswith('.pdf'): return
        
        # Debounce simple
        if path in self.processed: return
        
        self.logger.info(f"Archivo detectado: {path}")
        
        # Esperar a que el archivo se libere (copia terminada)
        if self.wait_for_file_stability(path):
            self.processed.add(path)
            self.logger.info(f"Archivo estable, procesando: {path}")
            try:
                self.callback(path)
            except Exception as e:
                self.logger.error(f"Error en callback de watcher para {path}: {e}", exc_info=True)
        else:
            self.logger.warning(f"Timeout esperando estabilidad de archivo: {path}")
        
    def wait_for_file_stability(self, path: str) -> bool:
        """
        Espera a que el archivo deje de crecer (indica fin de copia)
        Uses self.stability_retries and self.stability_interval
        
        Returns:
            bool: True si el archivo es estable, False si hubo timeout
        """
        last_size = -1
        for i in range(self.stability_retries):
            try:
                current_size = os.path.getsize(path)
                if current_size == last_size and current_size > 0:
                    # El tamaño no cambió en el último intervalo
                    return True
                last_size = current_size
                time.sleep(self.stability_interval)
            except OSError:
                # Archivo puede estar bloqueado o no existir aún
                time.sleep(self.stability_interval)
                
        return False

class PDFWatchService:
    """Servicio de monitoreo de carpetas"""
    
    def __init__(self, logger: Optional[Logger] = None, stability_retries: int = 10, stability_interval: float = 0.5):
        """
        Inicializa el servicio de monitoreo
        Args:
            logger: Logger opcional
            stability_retries: Intentos para verificar estabilidad de archivo
            stability_interval: Segundos entre intentos
        """
        self.logger = logger or get_logger(__name__)
        self.observer = None
        self.stability_retries = stability_retries
        self.stability_interval = stability_interval
        
    def start(self, path: str, callback: Callable[[str], None]):
        """
        Inicia el monitoreo en path
        
        Args:
            path: Directorio a vigilar
            callback: Función a llamar cuando llega un PDF nuevo (recibe ruta)
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"La ruta a monitorear no existe: {path}")
            
        self.stop() # Asegurar limpieza anterior
        
        self.logger.info(f"Iniciando vigilancia en: {path}")
        self.logger.info(f"Iniciando vigilancia en: {path}")
        handler = PDFWatcherHandler(callback, self.logger, self.stability_retries, self.stability_interval)
        self.observer = Observer()
        self.observer.schedule(handler, path, recursive=False)
        self.observer.start()
        
    def stop(self):
        """Detiene el monitoreo"""
        if self.observer:
            self.logger.info("Deteniendo vigilancia de carpeta")
            self.observer.stop()
            self.observer.join()
            self.observer = None
