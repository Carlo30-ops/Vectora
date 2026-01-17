"""
Gestor de temas y estilos dinámicos - Apple Dark Mode Implementation
Maneja el cambio de tema con transiciones suaves y persistencia
"""

import os
from pathlib import Path

from PySide6.QtCore import QObject, Signal, QSettings
from PySide6.QtWidgets import QApplication

from config.settings import settings

from .themes import THEMES


class ThemeManager(QObject):
    """
    Gestor centralizado de temas con soporte para Dark Mode profesional
    Estilo Apple iOS con transiciones suaves y persistencia de preferencias
    """
    
    theme_changed = Signal(str)  # Emitido cuando cambia el tema

    def __init__(self):
        super().__init__()
        self.settings = QSettings("LocalPDF", "Preferences")
        self.current_theme = self._load_saved_theme()
        self._apply_initial_theme()

    def _load_saved_theme(self) -> str:
        """Carga el tema guardado o usa light como default"""
        saved_theme = self.settings.value("theme", "light")
        if saved_theme not in THEMES:
            saved_theme = "light"
        return saved_theme

    def _apply_initial_theme(self):
        """Aplica el tema inicial sin esperar interacción"""
        try:
            from .style_content import STYLES_QSS
            
            qss_content = STYLES_QSS
            palette = THEMES[self.current_theme]
            
            # Reemplazar todas las variables de tema
            for key, value in palette.items():
                qss_content = qss_content.replace(f"{{{{{key}}}}}", value)
            
            app_instance = QApplication.instance()
            if app_instance:
                from typing import cast
                cast(QApplication, app_instance).setStyleSheet(qss_content)
                
        except Exception as e:
            print(f"Error aplicando tema inicial: {e}")

    def toggle_theme(self):
        """Alterna entre light y dark mode"""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.set_theme(new_theme)

    def set_theme(self, theme_name: str):
        """
        Establece un tema específico y aplica los cambios
        Persiste la preferencia en QSettings
        """
        if theme_name not in THEMES:
            return

        if self.current_theme == theme_name:
            return  # Ya está en este tema

        self.current_theme = theme_name
        
        # Guardar preferencia
        self.settings.setValue("theme", theme_name)
        self.settings.sync()

        # Aplicar tema
        self._apply_theme()
        
        # Emitir señal para que los widgets se actualicen
        self.theme_changed.emit(theme_name)

    def _apply_theme(self):
        """Aplica el tema actual a la aplicación completa con transición suave"""
        try:
            from .style_content import STYLES_QSS

            qss_content = STYLES_QSS

            # Reemplazar todas las variables de tema
            palette = THEMES[self.current_theme]
            for key, value in palette.items():
                qss_content = qss_content.replace(f"{{{{{key}}}}}", value)

            # Aplicar a la app global con transición suave
            app_instance = QApplication.instance()
            if app_instance:
                from typing import cast
                cast(QApplication, app_instance).setStyleSheet(qss_content)
                
                # Log del cambio
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f"Tema cambiado a: {self.current_theme}")

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error aplicando tema: {e}", exc_info=True)

    def get_color(self, color_key: str) -> str:
        """
        Obtiene un color del tema actual
        Útil para iconos y componentes personalizados
        
        Args:
            color_key: Clave del color (ej: 'TEXT_PRIMARY', 'ACCENT')
        
        Returns:
            Valor hexadecimal del color
        """
        palette = THEMES[self.current_theme]
        return palette.get(color_key, "#000000")

    @property
    def is_dark(self) -> bool:
        """Retorna True si el tema actual es dark"""
        return self.current_theme == "dark"

    @property
    def is_light(self) -> bool:
        """Retorna True si el tema actual es light"""
        return self.current_theme == "light"


# Instancia global única
theme_manager = ThemeManager()
