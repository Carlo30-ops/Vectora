"""
Gestor de temas y estilos dinámicos
"""
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal
from .themes import THEMES
from config.settings import settings

class ThemeManager(QObject):
    theme_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        
    def toggle_theme(self):
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)
        
    def apply_theme(self, theme_name: str):
        if theme_name not in THEMES:
            return
            
        self.current_theme = theme_name
        
        # Cargar plantilla QSS desde memoria (evita errores en EXE)
        try:
            from .style_content import STYLES_QSS
            qss_content = STYLES_QSS
                
            # Reemplazar variables
            palette = THEMES[theme_name]
            for key, value in palette.items():
                qss_content = qss_content.replace(f"{{{{{key}}}}}", value)
                
            # Aplicar a la app global
            if QApplication.instance():
                QApplication.instance().setStyleSheet(qss_content)
                self.theme_changed.emit(theme_name)
                
        except Exception as e:
            print(f"Error aplicando tema: {e}")

# Global instance
theme_manager = ThemeManager()
