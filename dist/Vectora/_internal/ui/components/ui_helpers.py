"""
Componentes UI comunes: Animaciones, Iconos, Botones estilizados
"""
from PySide6.QtWidgets import QPushButton, QFrame, QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve, QSize, Qt, QParallelAnimationGroup, QPoint
from PySide6.QtGui import QIcon, QColor, QPixmap, QPainter
import os
import sys

class IconHelper:
    @staticmethod
    def get_icon(name, color=None, active_color=None):
        """
        Carga iconos usando el sistema embebido.
        Si se provee active_color, el icono tendrá estado Normal/On distinto.
        """
        try:
            from icons.icons import get_icon_qicon
            
            icon = get_icon_qicon(name, color)
            
            if active_color:
                # Generar pixmap para estado activo (Checked/On)
                active_icon = get_icon_qicon(name, active_color)
                # Extraer pixmap y añadirlo al icono original como estado 'On'
                # QIcon.Mode.Normal, QIcon.State.On
                pixmap_on = active_icon.pixmap(24, 24)
                icon.addPixmap(pixmap_on, QIcon.Normal, QIcon.On)
                
            return icon
        except Exception as e:
            print(f"Error cargando icono '{name}': {e}")
            return QIcon()


class AnimatedButton(QPushButton):
    """Botón sin animaciones problemáticas"""
    def __init__(self, text="", parent=None, is_primary=False):
        super().__init__(text, parent)
        self.is_primary = is_primary
        self.setCursor(Qt.PointingHandCursor)

class AnimatedCard(QPushButton):
    """Card seleccionable sin animaciones de posición"""
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
        self.animation_type = "fade" # fade, slide

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
        if hasattr(self, 'overlay_label'):
            self.overlay_label.hide()
            self.overlay_label.deleteLater()
            del self.overlay_label
