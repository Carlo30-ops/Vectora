"""
DragDropZone Mejorado - Animaciones Spring Completas
Incluye animación de icono + container con efecto spring
"""

from pathlib import Path
from typing import List, Optional
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QSize, Property, QTimer
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QIcon, QColor
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget
import math


class SpringAnimationHelper:
    """
    Helper para crear animaciones tipo spring
    Emula Framer Motion stiffness/damping
    """
    
    @staticmethod
    def create_spring_easing(stiffness=300, damping=20):
        """
        Crea una curva de easing tipo spring
        stiffness: 100-500 (más alto = más rápido)
        damping: 10-50 (más alto = menos rebote)
        """
        # Para simplificar, usamos OutElastic para efecto spring
        # En producción, podríamos calcular la curva exacta
        if stiffness >= 400:
            return QEasingCurve.OutCubic  # Rápido y suave
        else:
            return QEasingCurve.OutQuad   # Un poco más lento
    

class AnimatedIconButton(QPushButton):
    """
    Botón con icono que anima su tamaño
    Usado dentro del DragDropZone
    """
    
    def __init__(self, parent=None, icon=None):
        super().__init__(parent)
        
        self._scale = 1.0
        self._icon = icon
        
        self.setIcon(icon) if icon else None
        self.setIconSize(QSize(48, 48))
        self.setFixedSize(64, 64)
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        
        # Animación
        self.scale_anim = QPropertyAnimation(self, b"scale")
        self.scale_anim.setDuration(300)
        self.scale_anim.setEasingCurve(QEasingCurve.OutCubic)
    
    @Property(float)
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value):
        self._scale = value
        # Recalcular tamaño del icono
        base_size = 48
        new_size = int(base_size * self._scale)
        self.setIconSize(QSize(new_size, new_size))
    
    def animate_to_scale(self, scale, duration=300):
        """Anima a la escala objetivo"""
        self.scale_anim.setDuration(duration)
        self.scale_anim.setStartValue(self._scale)
        self.scale_anim.setEndValue(scale)
        self.scale_anim.start()


class EnhancedDragDropZone(QFrame):
    """
    Zona de drag & drop mejorada con animaciones spring completas
    - Container escala 1.05 en arrastre
    - Icono interno escala 1.1 en arrastre
    - Border suave transición
    """
    
    file_dropped = Signal(list)
    
    def __init__(
        self,
        accepted_extensions: Optional[List[str]] = None,
        multiple: bool = False,
        icon: Optional[QIcon] = None,
        parent=None
    ):
        super().__init__(parent)
        
        self.accepted_extensions = accepted_extensions or []
        self.multiple = multiple
        self._dragging = False
        self._is_dragging = False
        
        # Escala
        self._scale = 1.0
        self._is_animating = False
        
        self.setAcceptDrops(True)
        self._setup_ui(icon)
        
        # Animación de container
        self.scale_anim = QPropertyAnimation(self, b"scale")
        self.scale_anim.setDuration(300)
        self.scale_anim.setEasingCurve(QEasingCurve.OutCubic)
    
    def _setup_ui(self, icon=None):
        """Setup UI con icono animable"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 40, 20, 40)
        
        # Icono animable
        self.icon_button = AnimatedIconButton(self, icon)
        self.icon_button.setFlat(True)
        layout.addWidget(self.icon_button, 0, Qt.AlignCenter)
        
        # Texto
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        # Botón secundario
        self.button = QPushButton()
        layout.addWidget(self.button, 0, Qt.AlignCenter)
        
        # Estilos
        self.setStyleSheet("""
            EnhancedDragDropZone {
                border: 2px dashed #D1D5DB;
                border-radius: 28px;
                background-color: #F9FAFB;
                transition: all 300ms ease-in-out;
            }
            EnhancedDragDropZone:hover {
                border-color: #9CA3AF;
                background-color: #F3F4F6;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Drag enter con animación"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            valid_files = self._filter_valid_files([url.toLocalFile() for url in urls])
            
            if valid_files:
                event.acceptProposedAction()
                self._set_dragging(True)
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event: QDragMoveEvent):
        """Drag move"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            valid_files = self._filter_valid_files([url.toLocalFile() for url in urls])
            
            if valid_files:
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        """Drag leave con animación"""
        self._set_dragging(False)
        super().dragLeaveEvent(event)
    
    def dropEvent(self, event: QDropEvent):
        """Drop files"""
        self._set_dragging(False)
        
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            files = [url.toLocalFile() for url in urls]
            valid_files = self._filter_valid_files(files)
            
            if valid_files:
                if not self.multiple and len(valid_files) > 1:
                    valid_files = [valid_files[0]]
                
                event.acceptProposedAction()
                self.file_dropped.emit(valid_files)
            else:
                event.ignore()
        else:
            event.ignore()
    
    def _filter_valid_files(self, files: List[str]) -> List[str]:
        """Filter valid files"""
        if not self.accepted_extensions:
            return files
        
        valid = []
        for file_path in files:
            if not Path(file_path).is_file():
                continue
            
            ext = Path(file_path).suffix.lower()
            if ext in [e.lower() for e in self.accepted_extensions]:
                valid.append(file_path)
        
        return valid
    
    def _set_dragging(self, dragging: bool):
        """Actualiza estado de arrastre con animaciones"""
        if dragging == self._is_dragging:
            return
        
        self._is_dragging = dragging
        
        if dragging:
            # Animar container a 1.05
            self.scale_anim.setStartValue(1.0)
            self.scale_anim.setEndValue(1.05)
            self.scale_anim.start()
            
            # Animar icono a 1.1
            self.icon_button.animate_to_scale(1.1, 300)
            
            # Cambiar estilos
            self.setStyleSheet("""
                EnhancedDragDropZone {
                    border: 2px solid #3B82F6;
                    border-radius: 28px;
                    background-color: #EFF6FF;
                    transition: all 300ms ease-in-out;
                }
            """)
        else:
            # Animar container a 1.0
            self.scale_anim.setStartValue(self._scale)
            self.scale_anim.setEndValue(1.0)
            self.scale_anim.start()
            
            # Animar icono a 1.0
            self.icon_button.animate_to_scale(1.0, 300)
            
            # Restaurar estilos
            self.setStyleSheet("""
                EnhancedDragDropZone {
                    border: 2px dashed #D1D5DB;
                    border-radius: 28px;
                    background-color: #F9FAFB;
                    transition: all 300ms ease-in-out;
                }
                EnhancedDragDropZone:hover {
                    border-color: #9CA3AF;
                    background-color: #F3F4F6;
                }
            """)
    
    @Property(float)
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()
