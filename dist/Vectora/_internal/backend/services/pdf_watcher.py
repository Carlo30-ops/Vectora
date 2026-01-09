"""
Servicio de vigilancia de carpetas para nuevos PDFs
"""
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class PDFWatcherHandler(FileSystemEventHandler):
    """Manejador de eventos de archivo"""
    def __init__(self, callback):
        self.callback = callback
        self.processed = set()
    
    def on_created(self, event):
        if event.is_directory: return
        
        path = event.src_path
        if not path.lower().endswith('.pdf'): return
        
        # Debounce simple
        if path in self.processed: return
        
        # Esperar a que el archivo se libere (copia terminada)
        # Esto es bloqueante, idealmente se maneja mejor, pero para v5 simple sirve
        self.wait_for_file(path)
        
        self.processed.add(path)
        self.callback(path)
        
    def wait_for_file(self, path, retries=5):
        """Espera a que el archivo deje de crecer/estar bloqueado"""
        size = -1
        for _ in range(retries):
            try:
                new_size = os.path.getsize(path)
                if new_size == size: # Estable
                    return
                size = new_size
                time.sleep(0.5)
            except:
                time.sleep(0.5)

class PDFWatchService:
    """Servicio de monitoreo"""
    def __init__(self):
        self.observer = None
        
    def start(self, path: str, callback):
        """Inicia el monitoreo en path, llamando a callback(filepath)"""
        self.stop() # Asegurar limpieza anterior
        
        handler = PDFWatcherHandler(callback)
        self.observer = Observer()
        self.observer.schedule(handler, path, recursive=False)
        self.observer.start()
        
    def stop(self):
        """Detiene el monitoreo"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
