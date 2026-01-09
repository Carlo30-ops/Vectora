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
    
    # Cargar estilos globales (opcional)
    try:
        with open('ui/styles/styles.qss', 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Advertencia: No se encontró el archivo de estilos")
    
    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
