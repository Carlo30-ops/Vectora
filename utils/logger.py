"""
Sistema de Logging Profesional para Vectora
Proporciona logging configurado con rotación de archivos, niveles y formato consistente
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional


class VectoraLogger:
    """
    Gestor centralizado de logging para Vectora
    
    Características:
    - Logging a archivo con rotación automática
    - Logging a consola con colores (opcional)
    - Formato consistente
    - Niveles configurables
    - Archivos de log organizados por fecha
    """
    
    _instance: Optional['VectoraLogger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Patrón Singleton para tener una única instancia"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa el sistema de logging si no está inicializado"""
        if not VectoraLogger._initialized:
            self._setup_logging()
            VectoraLogger._initialized = True
    
    def _setup_logging(self):
        """Configura el sistema de logging"""
        # Detectar si estamos en ejecutable o desarrollo
        if getattr(sys, 'frozen', False):
            # Ejecutable: logs en Documents/Vectora/logs
            log_dir = Path.home() / 'Documents' / 'Vectora' / 'logs'
        else:
            # Desarrollo: logs en carpeta del proyecto
            log_dir = Path(__file__).parent.parent / 'logs'
        
        # Crear directorio de logs
        log_dir.mkdir(exist_ok=True, parents=True)
        
        # Nombre del archivo de log con fecha
        log_filename = f"vectora_{datetime.now().strftime('%Y-%m-%d')}.log"
        log_path = log_dir / log_filename
        
        # Configurar formato de logging
        log_format = logging.Formatter(
            fmt='[%(asctime)s] [%(levelname)-8s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configurar handler de archivo con rotación
        # Máximo 10 MB por archivo, mantener 5 backups
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        
        # Configurar handler de consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_format)
        
        # Configurar logger raíz
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Limpiar handlers existentes
        root_logger.handlers.clear()
        
        # Agregar handlers
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        # Log de inicio
        root_logger.info("=" * 60)
        root_logger.info(f"Vectora v5.0.0 - Sistema de Logging Iniciado")
        root_logger.info(f"Archivo de log: {log_path}")
        root_logger.info("=" * 60)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Obtiene un logger con el nombre especificado
        
        Args:
            name: Nombre del logger (normalmente __name__ del módulo)
            
        Returns:
            Logger configurado
            
        Ejemplo:
            logger = VectoraLogger.get_logger(__name__)
            logger.info("Operación iniciada")
        """
        # Asegurar que el sistema está inicializado
        VectoraLogger()
        return logging.getLogger(name)


# Función de conveniencia para obtener logger
def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado
    
    Args:
        name: Nombre del logger (usa __name__)
        
    Returns:
        Logger configurado
        
    Ejemplo:
        from utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Mensaje informativo")
        logger.warning("Advertencia")
        logger.error("Error", exc_info=True)
    """
    return VectoraLogger.get_logger(name)


# Inicializar el sistema al importar
_vectora_logger = VectoraLogger()


# Ejemplos de uso (para documentación)
if __name__ == '__main__':
    # Ejemplo 1: Logger básico
    logger = get_logger(__name__)
    
    logger.debug("Mensaje de debug (solo en archivo)")
    logger.info("Mensaje informativo")
    logger.warning("Mensaje de advertencia")
    logger.error("Mensaje de error")
    logger.critical("Mensaje crítico")
    
    # Ejemplo 2: Logging con contexto
    logger.info(f"Procesando archivo: ejemplo.pdf")
    logger.info(f"Operación completada en 2.5s")
    
    # Ejemplo 3: Logging de excepciones
    try:
        result = 1 / 0
    except Exception as e:
        logger.error(f"Error al procesar: {e}", exc_info=True)
    
    # Ejemplo 4: Logger por módulo
    merger_logger = get_logger('backend.services.pdf_merger')
    merger_logger.info("Combinando 3 archivos PDF...")
    merger_logger.info("Progreso: 33%")
    merger_logger.info("Progreso: 66%")
    merger_logger.info("Progreso: 100%")
    merger_logger.info("¡PDFs combinados exitosamente!")
