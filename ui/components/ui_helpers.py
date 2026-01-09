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
    def get_resource_path(relative_path):
        """Obtiene la ruta absoluta al recurso, compatible con PyInstaller"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    @staticmethod
    def get_icon(name, color=None):
        """Carga un icono SVG y opcionalmente lo colorea"""
        # Intentar primero con la ruta de recursos
        path = IconHelper.get_resource_path(f"assets/icons/{name}.svg")
        
        # Si no existe, intentar ruta relativa directa (fallback)
        if not os.path.exists(path):
            path = f"assets/icons/{name}.svg"
            
        if not os.path.exists(path):
            return QIcon()
            
        pixmap = QPixmap(path)
        if color:
            painter = QPainter(pixmap)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), QColor(color))
            painter.end()
            
        return QIcon(pixmap)


class AnimatedButton(QPushButton):
    """Botón con animación de escala sutil al hover"""
    def __init__(self, text="", parent=None, is_primary=False):
        super().__init__(text, parent)
        self.is_primary = is_primary
        self.setCursor(Qt.PointingHandCursor)
        self._default_rect = None
        
        # Animación de geometría
        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def showEvent(self, event):
        super().showEvent(event)
        if not self._default_rect:
            self._default_rect = self.geometry()

    def enterEvent(self, event):
        super().enterEvent(event)
        # Escalar ligeramente (crecer 2px en cada dirección)
        rect = self.geometry()
        target = rect.adjusted(-2, -2, 2, 2)
        self._start_anim(target)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        # Regresar al tamaño original relativo
        if self._default_rect:
             rect = self.geometry()
             target = rect.adjusted(2, 2, -2, -2)
             self._start_anim(target)

    def _start_anim(self, target_rect):
        self._anim.stop()
        self._anim.setStartValue(self.geometry())
        self._anim.setEndValue(target_rect)
        self._anim.start()

class AnimatedCard(QPushButton):
    """Card seleccionable con animación de elevación y color"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(False)
        self.setStyleSheet("text-align: left;")
        
        # Animación de geometría para elevación
        self._anim = QPropertyAnimation(self, b"pos")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self._original_pos = None

    def showEvent(self, event):
        super().showEvent(event)
        if not self._original_pos:
            self._original_pos = self.pos()

    def enterEvent(self, event):
        super().enterEvent(event)
        # Efecto de elevación: mover hacia arriba
        if self._original_pos:
            target = self._original_pos + QPoint(0, -4)
            self._start_anim(target)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        # Volver a posición original
        if self._original_pos:
            self._start_anim(self._original_pos)
            
    def _start_anim(self, target_pos):
        self._anim.stop()
        self._anim.setStartValue(self.pos())
        self._anim.setEndValue(target_pos)
        self._anim.start()

