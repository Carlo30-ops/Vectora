"""
Sistema de animaciones Apple-style para Vectora
Proporciona transiciones suaves, fade in/out, y efectos hover
"""

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer, Qt
from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtGui import QColor


class AnimationHelper:
    """Ayudante para crear animaciones Apple-style consistentes"""
    
    DURATION_FAST = 150      # ms - Click/press
    DURATION_NORMAL = 300    # ms - Hover/state change
    DURATION_SLOW = 500      # ms - Page transitions
    
    @staticmethod
    def create_fade_in(widget: QWidget, duration: int = DURATION_NORMAL) -> QPropertyAnimation:
        """
        Crea una animación de fade in suave
        
        Args:
            widget: Widget a animar
            duration: Duración en ms
            
        Returns:
            QPropertyAnimation configurada
        """
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutCubic)
        return animation
    
    @staticmethod
    def create_fade_out(widget: QWidget, duration: int = DURATION_NORMAL) -> QPropertyAnimation:
        """
        Crea una animación de fade out suave
        
        Args:
            widget: Widget a animar
            duration: Duración en ms
            
        Returns:
            QPropertyAnimation configurada
        """
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.InOutCubic)
        return animation
    
    @staticmethod
    def create_slide_in_left(widget: QWidget, distance: int = 50, 
                             duration: int = DURATION_NORMAL) -> QPropertyAnimation:
        """
        Crea una animación de slide in desde la izquierda
        
        Args:
            widget: Widget a animar
            distance: Distancia en px
            duration: Duración en ms
            
        Returns:
            QPropertyAnimation configurada
        """
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        
        current_geom = widget.geometry()
        animation.setStartValue(
            current_geom.translated(-distance, 0)
        )
        animation.setEndValue(current_geom)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        return animation
    
    @staticmethod
    def create_smooth_color_transition(widget: QWidget, 
                                      start_color: str, 
                                      end_color: str,
                                      duration: int = DURATION_NORMAL) -> QPropertyAnimation:
        """
        Crea una transición de color suave
        
        Args:
            widget: Widget a animar
            start_color: Color inicial (hex string)
            end_color: Color final (hex string)
            duration: Duración en ms
            
        Returns:
            QPropertyAnimation configurada
        """
        animation = QPropertyAnimation(widget, b"styleSheet")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.InOutCubic)
        
        # Las animaciones de stylesheet requieren manejo especial
        # Esto es una simplificación - para casos complejos usar custom properties
        return animation


class HoverEffect:
    """Efecto hover Apple-style para botones"""
    
    def __init__(self, button: QPushButton):
        self.button = button
        self.original_opacity = 1.0
        self.normal_opacity = 1.0
        self.hover_opacity = 0.95
        self.press_opacity = 0.85
        
        # Conectar eventos
        self.button.enterEvent = lambda event: self.on_enter()
        self.button.leaveEvent = lambda event: self.on_leave()
        self.button.mousePressEvent = lambda event: self.on_press()
        self.button.mouseReleaseEvent = lambda event: self.on_release()
    
    def on_enter(self):
        """Cuando el mouse entra al botón"""
        self._animate_opacity(self.hover_opacity)
    
    def on_leave(self):
        """Cuando el mouse sale del botón"""
        self._animate_opacity(self.normal_opacity)
    
    def on_press(self):
        """Cuando presiona el botón"""
        self._animate_opacity(self.press_opacity)
    
    def on_release(self):
        """Cuando suelta el botón"""
        self._animate_opacity(self.hover_opacity if self.button.underMouse() 
                            else self.normal_opacity)
    
    def _animate_opacity(self, target_opacity: float, duration: int = 150):
        """Anima la opacidad del botón"""
        animation = QPropertyAnimation(self.button, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(self.button.windowOpacity())
        animation.setEndValue(target_opacity)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()


class TransitionManager:
    """Gestor de transiciones entre vistas"""
    
    @staticmethod
    def transition_between_widgets(from_widget: QWidget, 
                                  to_widget: QWidget,
                                  duration: int = AnimationHelper.DURATION_NORMAL):
        """
        Realiza una transición suave entre dos widgets
        
        Args:
            from_widget: Widget actual
            to_widget: Widget destino
            duration: Duración en ms
        """
        # Fade out del widget actual
        fade_out = AnimationHelper.create_fade_out(from_widget, duration)
        
        # Fade in del nuevo widget
        to_widget.setWindowOpacity(0.0)
        fade_in = AnimationHelper.create_fade_in(to_widget, duration)
        
        fade_out.start()
        fade_in.start()
    
    @staticmethod
    def staggered_animation(widgets: list, duration: int = AnimationHelper.DURATION_FAST,
                          stagger_delay: int = 50):
        """
        Anima múltiples widgets con retardo escalonado
        
        Args:
            widgets: Lista de widgets a animar
            duration: Duración de cada animación en ms
            stagger_delay: Retardo entre cada widget en ms
        """
        for index, widget in enumerate(widgets):
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(
                lambda w=widget, d=duration: 
                AnimationHelper.create_fade_in(w, d).start()
            )
            timer.start(index * stagger_delay)
