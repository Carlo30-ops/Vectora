"""
Vectora - Aplicación de Escritorio
Punto de entrada principal
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from config.settings import settings
from utils.logger import get_logger

def main():
    """Función principal de la aplicación"""
    
    # 0. Inicializar Logger
    logger = get_logger("main")
    logger.info("Iniciando Vectora...")

    # 1. Asegurar directorios (Lazy initialization)
    settings.ensure_directories()

    # 2. Crear aplicación
    app = QApplication(sys.argv)
    app.setApplicationName(settings.APP_NAME)
    app.setApplicationVersion(settings.APP_VERSION)
    app.setOrganizationName(settings.APP_AUTHOR)
    
    # 3. Cargar tema inicial
    from ui.styles.theme_manager import theme_manager
    theme_manager.apply_theme("light")
    
    # 4. Crear y mostrar ventana principal
    try:
        initial_file = sys.argv[1] if len(sys.argv) > 1 else None
        window = MainWindow(initial_file)
        window.show()
        
        # 5. Ejecutar aplicación
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"Error fatal en la aplicación: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
