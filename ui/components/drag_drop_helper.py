"""
Helper para habilitar drag & drop en widgets existentes
Permite agregar funcionalidad de drag & drop sin reescribir widgets
"""

from pathlib import Path
from typing import List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PySide6.QtWidgets import QFrame, QWidget


class DragDropMixin:
    """
    Mixin para agregar drag & drop a cualquier QWidget/QFrame
    
    Uso:
        class MyWidget(QFrame, DragDropMixin):
            def __init__(self):
                super().__init__()
                self.enable_drag_drop(['.pdf'], multiple=False)
                self.file_dropped.connect(self.on_files_dropped)
    """
    
    file_dropped = Signal(list)  # Emite lista de archivos
    
    def enable_drag_drop(
        self,
        accepted_extensions: Optional[List[str]] = None,
        multiple: bool = False
    ):
        """
        Habilita drag & drop en el widget
        
        Args:
            accepted_extensions: Lista de extensiones aceptadas (ej: ['.pdf', '.docx'])
            multiple: Si True, acepta múltiples archivos
        """
        self.setAcceptDrops(True)
        self._accepted_extensions = accepted_extensions or []
        self._multiple = multiple
        self._original_style = self.styleSheet()
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Acepta el evento si contiene archivos válidos"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            valid_files = self._filter_valid_files([url.toLocalFile() for url in urls])
            
            if valid_files:
                event.acceptProposedAction()
                self._set_drag_style(True)
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event: QDragMoveEvent):
        """Permite mover durante el arrastre si es válido"""
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
        """Restaura el estilo cuando sale el drag"""
        self._set_drag_style(False)
        if hasattr(super(), 'dragLeaveEvent'):
            super().dragLeaveEvent(event)
    
    def dropEvent(self, event: QDropEvent):
        """Maneja archivos soltados"""
        self._set_drag_style(False)
        
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            files = [url.toLocalFile() for url in urls]
            valid_files = self._filter_valid_files(files)
            
            if valid_files:
                if not self._multiple and len(valid_files) > 1:
                    # Si no acepta múltiples, tomar solo el primero
                    valid_files = [valid_files[0]]
                
                event.acceptProposedAction()
                self.file_dropped.emit(valid_files)
            else:
                event.ignore()
        else:
            event.ignore()
    
    def _filter_valid_files(self, files: List[str]) -> List[str]:
        """Filtra archivos válidos según extensiones aceptadas"""
        if not self._accepted_extensions:
            return [f for f in files if Path(f).is_file()]
        
        valid = []
        for file_path in files:
            if not Path(file_path).is_file():
                continue
            
            ext = Path(file_path).suffix.lower()
            if ext in [e.lower() for e in self._accepted_extensions]:
                valid.append(file_path)
        
        return valid
    
    def _set_drag_style(self, is_dragging: bool):
        """Cambia el estilo visual cuando se arrastra sobre la zona"""
        if is_dragging:
            # Agregar estilo de drag activo
            current = self.styleSheet()
            # Buscar y reemplazar border dashed por solid
            new_style = current.replace(
                "border: 2px dashed {{BORDER}}",
                "border: 2px solid {{ACCENT}}"
            )
            if new_style == current:
                # Si no tiene el patrón, agregar al final
                new_style = current + "\nborder: 2px solid {{ACCENT}} !important; background-color: {{ACCENT}}20;"
            else:
                # También cambiar background
                new_style = new_style.replace(
                    "background-color: {{HOVER}}",
                    "background-color: {{ACCENT}}20"
                )
            self.setStyleSheet(new_style)
        else:
            # Restaurar estilo original (el tema lo manejará automáticamente)
            pass


def enable_drag_drop_on_frame(
    frame: QFrame,
    accepted_extensions: Optional[List[str]] = None,
    multiple: bool = False,
    file_dropped_callback=None
):
    """
    Función helper para habilitar drag & drop en un QFrame existente
    
    Args:
        frame: QFrame al que agregar drag & drop
        accepted_extensions: Lista de extensiones aceptadas
        multiple: Si acepta múltiples archivos
        file_dropped_callback: Función a llamar cuando se sueltan archivos
    
    Returns:
        Signal que emite cuando se sueltan archivos
    """
    # Crear una clase dinámica que herede de QFrame y el mixin
    class DragDropFrame(QFrame, DragDropMixin):
        def __init__(self, parent_frame):
            QFrame.__init__(self, parent_frame)
            DragDropMixin.__init__(self)
            # Copiar propiedades del frame original
            self.setObjectName(parent_frame.objectName())
            self.setStyleSheet(parent_frame.styleSheet())
            self.setMinimumHeight(parent_frame.minimumHeight())
            self.setMaximumHeight(parent_frame.maximumHeight())
            self.setMinimumWidth(parent_frame.minimumWidth())
            self.setMaximumWidth(parent_frame.maximumWidth())
            self.setGeometry(parent_frame.geometry())
            # Copiar layout
            if parent_frame.layout():
                self.setLayout(parent_frame.layout())
    
    # En lugar de crear nueva clase, agregar métodos directamente al frame
    frame.setAcceptDrops(True)
    frame._accepted_extensions = accepted_extensions or []
    frame._multiple = multiple
    frame._original_style = frame.styleSheet()
    
    # Agregar métodos del mixin directamente
    def dragEnterEvent(event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            valid_files = _filter_valid_files(frame, [url.toLocalFile() for url in urls])
            if valid_files:
                event.acceptProposedAction()
                _set_drag_style(frame, True)
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragMoveEvent(event: QDragMoveEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            valid_files = _filter_valid_files(frame, [url.toLocalFile() for url in urls])
            if valid_files:
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragLeaveEvent(event):
        _set_drag_style(frame, False)
    
    def dropEvent(event: QDropEvent):
        _set_drag_style(frame, False)
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            files = [url.toLocalFile() for url in urls]
            valid_files = _filter_valid_files(frame, files)
            if valid_files:
                if not frame._multiple and len(valid_files) > 1:
                    valid_files = [valid_files[0]]
                event.acceptProposedAction()
                if file_dropped_callback:
                    file_dropped_callback(valid_files)
            else:
                event.ignore()
        else:
            event.ignore()
    
    # Reemplazar métodos del frame
    frame.dragEnterEvent = dragEnterEvent
    frame.dragMoveEvent = dragMoveEvent
    frame.dragLeaveEvent = dragLeaveEvent
    frame.dropEvent = dropEvent
    
    return frame


def _filter_valid_files(frame: QFrame, files: List[str]) -> List[str]:
    """Helper interno para filtrar archivos"""
    if not frame._accepted_extensions:
        return [f for f in files if Path(f).is_file()]
    
    valid = []
    for file_path in files:
        if not Path(file_path).is_file():
            continue
        ext = Path(file_path).suffix.lower()
        if ext in [e.lower() for e in frame._accepted_extensions]:
            valid.append(file_path)
    return valid


def _set_drag_style(frame: QFrame, is_dragging: bool):
    """Helper interno para cambiar estilo"""
    if is_dragging:
        current = frame.styleSheet()
        new_style = current.replace(
            "border: 2px dashed {{BORDER}}",
            "border: 2px solid {{ACCENT}}"
        )
        if new_style == current:
            new_style = current + "\nborder: 2px solid {{ACCENT}} !important; background-color: {{ACCENT}}20;"
        else:
            new_style = new_style.replace(
                "background-color: {{HOVER}}",
                "background-color: {{ACCENT}}20"
            )
        frame.setStyleSheet(new_style)
