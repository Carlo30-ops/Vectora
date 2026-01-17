"""
Componentes UI comunes: Animaciones, Iconos, Botones estilizados
"""

import os
import sys

from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
)
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import QFrame, QGraphicsOpacityEffect, QLabel, QPushButton, QStackedWidget


class IconHelper:
    """
    Helper para manejar iconos con soporte para Dark Mode
    Invierte automáticamente los colores de iconos según el tema actual
    """
    
    @staticmethod
    def get_icon(name, color=None, active_color=None):
        """
        Carga iconos usando el sistema embebido con soporte para Dark Mode.
        Si color es None, obtiene automáticamente el color del tema.
        
        Args:
            name: Nombre del icono (ej: 'combine', 'scissors')
            color: Color hexadecimal personalizado (optional)
            active_color: Color para estado activo/ON (optional)
        
        Returns:
            QIcon con soporte para diferentes estados
        """
        try:
            from icons.icons import get_icon_qicon
            from ui.styles.theme_manager import theme_manager
            
            # Si no se especifica color, usar del tema actual
            if color is None:
                color = theme_manager.get_color("ICON_CONTAINER_FG")
            
            icon = get_icon_qicon(name, color)

            if active_color:
                # Generar pixmap para estado activo (Checked/On)
                active_icon = get_icon_qicon(name, active_color)
                pixmap_on = active_icon.pixmap(24, 24)
                icon.addPixmap(pixmap_on, QIcon.Normal, QIcon.On)

            return icon
        except Exception as e:
            print(f"Error cargando icono '{name}': {e}")
            return QIcon()
    
    @staticmethod
    def get_themed_icon(name, theme_manager_instance=None):
        """
        Obtiene un icono con colores automáticos del tema.
        Invierte iconos automáticamente en dark mode:
        - Light Mode: Icono blanco sobre fondo negro
        - Dark Mode: Icono negro sobre fondo blanco
        
        Args:
            name: Nombre del icono
            theme_manager_instance: Instancia de ThemeManager (optional)
        
        Returns:
            QIcon con colores adaptados al tema actual
        """
        try:
            from icons.icons import get_icon_qicon
            from ui.styles.theme_manager import theme_manager as default_tm
            
            tm = theme_manager_instance or default_tm
            
            # Obtener color de icono según tema actual
            icon_color = tm.get_color("ICON_CONTAINER_FG")
            
            return get_icon_qicon(name, icon_color)
        except Exception as e:
            print(f"Error cargando icono temático '{name}': {e}")
            return QIcon()


class AnimatedButton(QPushButton):
    """Botón con animación de escala sutil"""

    def __init__(self, text="", parent=None, is_primary=False):
        super().__init__(text, parent)
        self.is_primary = is_primary
        self.setCursor(Qt.PointingHandCursor)


class AnimatedCard(QPushButton):
    """Card con efecto de elevación suave"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(False)
        self.setStyleSheet("text-align: left;")


class FadingStackedWidget(QStackedWidget):
    """
    QStackedWidget con animación de desvanecimiento (Fade) al cambiar de página.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fade_duration = 300
        self.animation_type = "fade"  # fade, slide

    def setCurrentIndex(self, index):
        self.fade_transition(index)

    def setCurrentWidget(self, widget):
        index = self.indexOf(widget)
        self.setCurrentIndex(index)

    def fade_transition(self, index):
        if index == self.currentIndex():
            return

        current_widget = self.currentWidget()
        next_widget = self.widget(index)

        if not current_widget:
            super().setCurrentIndex(index)
            return

        # 1. Capturar imagen del widget actual
        pixmap = QPixmap(self.size())
        current_widget.render(pixmap)

        # 2. Crear un Label superpuesto con esa imagen
        self.overlay_label = QLabel(self)
        self.overlay_label.setPixmap(pixmap)
        self.overlay_label.setGeometry(self.rect())
        self.overlay_label.show()

        # 3. Cambiar la página real debajo
        super().setCurrentIndex(index)

        # 4. Configurar efecto de opacidad en el Label
        self.effect = QGraphicsOpacityEffect(self.overlay_label)
        self.overlay_label.setGraphicsEffect(self.effect)

        # 5. Animar opacidad de 1.0 a 0.0
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(self.fade_duration)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)

        # 6. Limpiar al terminar
        self.anim.finished.connect(self.cleanup)
        self.anim.start()

    def cleanup(self):
        if hasattr(self, "overlay_label"):
            self.overlay_label.hide()
            self.overlay_label.deleteLater()
            del self.overlay_label
