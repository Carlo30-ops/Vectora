"""
Componente reutilizable de Drag & Drop para archivos
Permite arrastrar y soltar archivos en widgets de operación
"""

from pathlib import Path
from typing import List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout


class DragDropZone(QFrame):
    """
    Zona de drop reutilizable para un solo archivo o múltiples

    Uso:
        zone = DragDropZone(
            accepted_extensions=['.pdf'],
            multiple=False
        )
        zone.file_dropped.connect(self.on_file_dropped)
    """

    file_dropped = Signal(list)  # Emite lista de archivos (aunque sea uno)

    def __init__(
        self, accepted_extensions: Optional[List[str]] = None, multiple: bool = False, parent=None
    ):
        """
        Args:
            accepted_extensions: Lista de extensiones aceptadas (ej: ['.pdf', '.docx'])
            multiple: Si True, acepta múltiples archivos
            parent: Widget padre
        """
        super().__init__(parent)
        self.accepted_extensions = accepted_extensions or []
        self.multiple = multiple
        self.setAcceptDrops(True)
        self._setup_ui()

    def _setup_ui(self):
        """Configura la UI básica (puede ser personalizada por hijos)"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)

        # Label y botón serán configurados por el widget padre
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.button = QPushButton()
        layout.addWidget(self.button, 0, Qt.AlignCenter)

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
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent):
        """Maneja archivos soltados"""
        self._set_drag_style(False)

        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            files = [url.toLocalFile() for url in urls]
            valid_files = self._filter_valid_files(files)

            if valid_files:
                if not self.multiple and len(valid_files) > 1:
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
        if not self.accepted_extensions:
            return files  # Si no hay restricciones, acepta todos

        valid = []
        for file_path in files:
            if not Path(file_path).is_file():
                continue

            ext = Path(file_path).suffix.lower()
            if ext in [e.lower() for e in self.accepted_extensions]:
                valid.append(file_path)

        return valid

    def _set_drag_style(self, is_dragging: bool):
        """Cambia el estilo visual cuando se arrastra sobre la zona"""
        # Obtener estilo actual y modificar border-color
        current_style = self.styleSheet()

        if is_dragging:
            # Cambiar border a sólido y color accent
            new_style = current_style.replace(
                "border: 2px dashed {{BORDER}}", "border: 2px solid {{ACCENT}}"
            )
            new_style = new_style.replace(
                "background-color: {{HOVER}}",
                "background-color: {{ACCENT}}20",  # Accent con 20% opacidad
            )
            # Si no tiene reemplazos, agregar estilo directamente
            if new_style == current_style:
                self.setStyleSheet(
                    current_style
                    + "\nborder: 2px solid {{ACCENT}}; background-color: {{ACCENT}}20;"
                )
            else:
                self.setStyleSheet(new_style)
        else:
            # Restaurar estilo original (solo si se modificó)
            # En la práctica, el estilo se restaura automáticamente por el tema
            # Pero podemos forzar una actualización
            pass
