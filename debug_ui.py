"""
Script de depuración para probar componentes de la UI individualmente
"""
import sys
import os

# Añadir el directorio raíz al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.styles.theme_manager import theme_manager

def run_app():
    app = QApplication(sys.argv)
    
    # Aplicar tema inicial
    theme_manager.apply_theme(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()
