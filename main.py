"""
Vectora - Aplicación de Escritorio
Punto de entrada principal
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
from config.settings import settings


def main():
    """Función principal de la aplicación"""
    
    # Crear aplicación
    app = QApplication(sys.argv)
    app.setApplicationName(settings.APP_NAME)
    app.setApplicationVersion(settings.APP_VERSION)
    app.setOrganizationName(settings.APP_AUTHOR)
    
    # Cargar tema inicial
    from ui.styles.theme_manager import theme_manager
    theme_manager.apply_theme("light")
    
    # Crear y mostrar ventana principal
    initial_file = sys.argv[1] if len(sys.argv) > 1 else None
    window = MainWindow(initial_file)
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
