"""
ScalableIconButton - Botón con icono que escala en hover
Emula el comportamiento de scale(1.1) de Tailwind en React
"""

from PySide6.QtCore import QPropertyAnimation, Qt, QEasingCurve, QSize, Property, QRect
from PySide6.QtGui import QPainter, QIcon, QColor
from PySide6.QtWidgets import QPushButton


class ScalableIconButton(QPushButton):
    """
    Botón que escala el icono al 110% en hover
    Mantiene el tamaño del botón, anima solo el icono
    """
    
    def __init__(self, parent=None, icon=None, size=48):
        super().__init__(parent)
        
        self.base_size = size  # Tamaño base (48px típico)
        self._scale = 1.0      # Escala actual (1.0 = 100%, 1.1 = 110%)
        self._icon = icon
        
        # Configurar botón
        self.setFixedSize(size, size)
        self.setIcon(icon) if icon else None
        self.setIconSize(QSize(size - 8, size - 8))  # 8px de padding
        self.setCursor(Qt.PointingHandCursor)
        
        # Animación de escala
        self.scale_animation = QPropertyAnimation(self, b"scale")
        self.scale_animation.setDuration(300)
        self.scale_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Estilos
        self.setStyleSheet("""
            ScalableIconButton {
                border: none;
                background-color: transparent;
                border-radius: 12px;
                padding: 4px;
            }
            ScalableIconButton:hover {
                background-color: rgba(0, 0, 0, 0.05);
            }
            ScalableIconButton:pressed {
                background-color: rgba(0, 0, 0, 0.10);
            }
        """)
    
    def enterEvent(self, event):
        """Al pasar mouse, animar icono a 1.1"""
        super().enterEvent(event)
        self._animate_scale(1.1)
    
    def leaveEvent(self, event):
        """Al salir mouse, animar icono a 1.0"""
        super().leaveEvent(event)
        self._animate_scale(1.0)
    
    def _animate_scale(self, target_scale):
        """Anima el icono a la escala objetivo"""
        self.scale_animation.setStartValue(self._scale)
        self.scale_animation.setEndValue(target_scale)
        self.scale_animation.start()
    
    @Property(float)
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()
    
    def paintEvent(self, event):
        """Dibuja el botón con icono escalado"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Dibujar fondo hover si está dentro
        if self.underMouse():
            painter.fillRect(self.rect(), QColor(0, 0, 0, 10))
        
        # Calcular rect del icono escalado
        base_w = self.width() - 8
        base_h = self.height() - 8
        
        # Aplicar escala
        scaled_w = int(base_w * self._scale)
        scaled_h = int(base_h * self._scale)
        
        # Centrar el icono escalado
        x = (self.width() - scaled_w) // 2
        y = (self.height() - scaled_h) // 2
        
        # Dibuja el icono
        if self.icon() and not self.icon().isNull():
            pixmap = self.icon().pixmap(scaled_w, scaled_h)
            painter.drawPixmap(x, y, pixmap)


class ScalableCardIcon(QPushButton):
    """
    Icono mejorado para cards del dashboard
    Escala a 1.1 en hover con transición smooth
    """
    
    def __init__(self, parent=None, icon=None, bg_color="#000000", size=56):
        super().__init__(parent)
        
        self.base_size = size
        self._scale = 1.0
        self._icon = icon
        self.bg_color = bg_color
        
        # Configurar botón
        self.setFixedSize(size, size)
        self.setIcon(icon) if icon else None
        self.setIconSize(QSize(size - 12, size - 12))
        self.setCursor(Qt.PointingHandCursor)
        
        # Animación
        self.scale_animation = QPropertyAnimation(self, b"scale")
        self.scale_animation.setDuration(300)
        self.scale_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Estilo base - fondo oscuro como en ejemplo
        self.setStyleSheet(f"""
            ScalableCardIcon {{
                border: none;
                background-color: {bg_color};
                border-radius: {size // 2}px;
                padding: 0px;
            }}
            ScalableCardIcon:hover {{
                background-color: {self._darken_color(bg_color)};
            }}
        """)
    
    def _darken_color(self, color_hex):
        """Oscurece el color un poco en hover"""
        # Convertir hex a RGB
        hex_color = color_hex.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Reducir brightness en 10%
        r = max(0, int(r * 0.9))
        g = max(0, int(g * 0.9))
        b = max(0, int(b * 0.9))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def enterEvent(self, event):
        """Scale a 1.1 en hover"""
        super().enterEvent(event)
        self._animate_scale(1.1)
    
    def leaveEvent(self, event):
        """Scale a 1.0 al salir"""
        super().leaveEvent(event)
        self._animate_scale(1.0)
    
    def _animate_scale(self, target_scale):
        """Anima escala"""
        self.scale_animation.setStartValue(self._scale)
        self.scale_animation.setEndValue(target_scale)
        self.scale_animation.start()
    
    @Property(float)
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()
    
    def paintEvent(self, event):
        """Dibuja card con icono escalado"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo redondeado
        painter.fillRect(self.rect(), QColor(self.bg_color))
        
        # Dibuja icono escalado
        base_w = self.width() - 12
        base_h = self.height() - 12
        
        scaled_w = int(base_w * self._scale)
        scaled_h = int(base_h * self._scale)
        
        x = (self.width() - scaled_w) // 2
        y = (self.height() - scaled_h) // 2
        
        if self.icon() and not self.icon().isNull():
            pixmap = self.icon().pixmap(scaled_w, scaled_h)
            painter.drawPixmap(x, y, pixmap)
