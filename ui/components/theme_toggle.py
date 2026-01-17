"""
Toggle de Tema Mejorado - Estilo iOS Apple
Componente animado con sun/moon icons y transición spring
"""

from PySide6.QtCore import QPropertyAnimation, QSize, Qt, QTimer, QEasingCurve, QRect, Property
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout


class AnimatedThemeToggle(QPushButton):
    """
    Toggle de tema animado estilo iOS Apple
    - Spring animation del knob
    - Iconos sun/moon que cambian
    - Transición suave de 300ms
    """
    
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.setFixedSize(64, 36)
        self.setCursor(Qt.PointingHandCursor)
        
        # Estado
        self.is_dark = theme_manager.is_dark
        self._knob_x = 28 if self.is_dark else 4  # Posición del knob
        
        # Animación
        self.animation = QPropertyAnimation(self, b"knobPosition")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Conectar cambios de tema
        self.clicked.connect(self._on_clicked)
        theme_manager.theme_changed.connect(self._on_theme_changed)
        
        # Actualizar estilo
        self._update_style()
    
    def mousePressEvent(self, event):
        """Cambiar tema al hacer click"""
        self.theme_manager.toggle_theme()
    
    def _on_clicked(self):
        """Callback cuando se hace click"""
        pass
    
    def _on_theme_changed(self, theme_name):
        """Callback cuando cambia el tema"""
        self.is_dark = (theme_name == "dark")
        self._animate_knob()
        self._update_style()
    
    def _animate_knob(self):
        """Anima el movimiento del knob"""
        start_x = self._knob_x
        end_x = 28 if self.is_dark else 4
        
        self.animation.setStartValue(start_x)
        self.animation.setEndValue(end_x)
        self.animation.start()
    
    @Property(float)
    def knobPosition(self):
        return self._knob_x
    
    @knobPosition.setter
    def knobPosition(self, value):
        self._knob_x = value
        self.update()
    
    def _update_style(self):
        """Actualiza el estilo según tema"""
        # No es necesario setStyleSheet para este widget personalizado
        # Se dibuja en paintEvent
        pass
    
    def paintEvent(self, event):
        """Dibuja el toggle personalizado"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Colores según tema
        if self.is_dark:
            track_color = QColor("#374151")
            knob_color = QColor("#111827")
            icon_color = QColor("#D1D5DB")
        else:
            track_color = QColor("#E5E7EB")
            knob_color = QColor("#FFFFFF")
            icon_color = QColor("#6B7280")
        
        # Track (fondo del toggle)
        painter.setBrush(track_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, 64, 36, 18, 18)
        
        # Knob (el círculo móvil)
        painter.setBrush(knob_color)
        knob_rect = QRect(int(self._knob_x), 4, 28, 28)
        painter.drawRoundedRect(knob_rect, 8, 8)
        
        # Shadow del knob
        painter.setPen(QPen(QColor(0, 0, 0, 30)))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(int(self._knob_x) - 1, 3, 30, 30, 8, 8)
        
        # Iconos dentro del knob
        # Moon icon (dark mode)
        if self.is_dark:
            self._draw_moon_icon(painter, knob_rect, icon_color)
        else:
            # Sun icon (light mode)
            self._draw_sun_icon(painter, knob_rect, icon_color)
        
        # Iconos de fondo sutiles
        self._draw_background_icons(painter, track_color, icon_color)
    
    def _draw_sun_icon(self, painter, rect, color):
        """Dibuja icono del sol (light mode)"""
        painter.setPen(QPen(color, 1.5))
        painter.setBrush(Qt.NoBrush)
        
        cx = rect.center().x()
        cy = rect.center().y()
        
        # Círculo central
        painter.drawEllipse(cx - 2, cy - 2, 4, 4)
        
        # Rayos (sin dibujar, solo círculo)
        painter.drawEllipse(cx - 5, cy - 5, 10, 10)
    
    def _draw_moon_icon(self, painter, rect, color):
        """Dibuja icono de la luna (dark mode)"""
        painter.setPen(QPen(color, 1.5))
        painter.setBrush(color)
        
        cx = rect.center().x()
        cy = rect.center().y()
        
        # Luna creciente
        painter.drawEllipse(cx - 4, cy - 4, 8, 8)
        painter.setBrush(QColor("#111827") if not self.is_dark else QColor("#374151"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(cx - 2, cy - 4, 8, 8)
    
    def _draw_background_icons(self, painter, track_color, icon_color):
        """Dibuja iconos sutiles de fondo"""
        # Sun icon - lado izquierdo
        painter.setPen(QPen(icon_color, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(8, 8, 8, 8)
        
        # Moon icon - lado derecho  
        painter.drawEllipse(48, 8, 8, 8)


class ThemeToggleWidget(QWidget):
    """
    Widget completo con toggle y label
    """
    
    def __init__(self, theme_manager, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Label
        label = QLabel("Tema")
        label.setFont(QFont("Segoe UI", 10))
        label.setStyleSheet(f"color: {theme_manager.get_color('TEXT_PRIMARY')};")
        
        # Toggle
        toggle = AnimatedThemeToggle(theme_manager, self)
        
        layout.addWidget(label)
        layout.addWidget(toggle)
        layout.addStretch()
        
        self.setFixedHeight(40)
