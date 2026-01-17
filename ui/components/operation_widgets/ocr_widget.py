"""
Widget de OCR (Reconocimiento Óptico de Caracteres)
Extrae texto de PDFs escaneados
"""

import os

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from backend.services.ocr_service import OCRService
from config.settings import settings
from ui.components.ui_helpers import IconHelper
from utils.file_handler import FileHandler

from .base_operation import BaseOperationWidget


class OCRWorker(QThread):
    """Worker para proceso de OCR"""

    progress_updated = Signal(int, str)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, input_path, output_path, language, dpi):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.language = language
        self.dpi = dpi

    def run(self):
        try:
            # Wrapper para callback de progreso
            def progress_callback(val, msg=""):
                self.progress_updated.emit(val, msg)

            # Instanciar servicio (Inyección de dependencias)
            ocr_service = OCRService()

            result = ocr_service.pdf_to_searchable_pdf(
                self.input_path,
                self.output_path,
                language=self.language,
                dpi=self.dpi,
                progress_callback=progress_callback,
            )
            self.finished.emit(result.to_dict())
        except Exception as e:
            self.error.emit(str(e))


class OCRWidget(BaseOperationWidget):
    """Widget de OCR"""

    def __init__(self):
        super().__init__(
            "🔍 OCR (Reconocimiento de Texto)", "Convierte documentos escaneados en texto buscable"
        )
        self.current_file = None
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz - Look Premium"""
        # Cambiar icono de la base
        icon = IconHelper.get_icon("search", color="#FFFFFF")
        if not icon.isNull():
            self.icon_lbl.setPixmap(icon.pixmap(36, 36))

        # Dropzone para archivo
        drop_area = QFrame()
        drop_area.setObjectName("glassContainer")
        drop_area.setMinimumHeight(100)
        drop_area.setAcceptDrops(True)  # Habilitar drag & drop
        drop_area.setStyleSheet(
            """
            QFrame {
                border: 2px dashed {{BORDER}};
                background-color: {{HOVER}};
            }
            QFrame:hover { border-color: {{ACCENT}}; }
        """
        )

        dal = QVBoxLayout(drop_area)
        dal.setAlignment(Qt.AlignCenter)

        self.file_label = QLabel("Arrastra tu PDF escaneado aquí o haz clic para seleccionar")
        self.file_label.setFont(QFont("Inter", 11))
        self.file_label.setStyleSheet("color: {{TEXT_SECONDARY}};")
        dal.addWidget(self.file_label)

        select_btn = QPushButton("Seleccionar PDF")
        select_btn.setCursor(Qt.PointingHandCursor)
        select_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: {{ACCENT}};
                border: 1px solid {{ACCENT}};
                border-radius: 8px;
                padding: 6px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: {{ACCENT}};
                color: {{ACCENT_TEXT}};
            }
        """
        )
        select_btn.clicked.connect(self.select_file)
        dal.addWidget(select_btn, 0, Qt.AlignCenter)

        self.config_layout.addWidget(drop_area)

        # Implementar drag & drop
        self._setup_drag_drop(drop_area)

        # Opciones en panel Glass
        opt_panel = QFrame()
        opt_panel.setObjectName("glassContainer")
        opt_panel.setStyleSheet("padding: 20px;")

        ol = QHBoxLayout(opt_panel)
        ol.setSpacing(20)

        # Idioma
        vl_lang = QVBoxLayout()
        vl_lang.addWidget(QLabel("Idioma del Documento"))
        self.lang_combo = QComboBox()
        self.langs = {"Español + Inglés": "spa+eng", "Español": "spa", "Inglés": "eng"}
        self.lang_combo.addItems(self.langs.keys())
        vl_lang.addWidget(self.lang_combo)
        ol.addLayout(vl_lang)

        # DPI
        vl_dpi = QVBoxLayout()
        vl_dpi.addWidget(QLabel("Calidad (DPI)"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(150, 600)
        self.dpi_spin.setValue(300)
        self.dpi_spin.setSuffix(" dpi")
        vl_dpi.addWidget(self.dpi_spin)
        ol.addLayout(vl_dpi)

        self.config_layout.addWidget(opt_panel)

        # Nota informativa
        note_container = QFrame()
        note_container.setStyleSheet(
            f"background-color: {{HOVER}}; border-radius: 8px; padding: 12px;"
        )
        nl = QHBoxLayout(note_container)

        note_icon = QLabel()
        ni = IconHelper.get_icon("info", color="{{TEXT_SECONDARY}}")
        if not ni.isNull():
            note_icon.setPixmap(ni.pixmap(16, 16))
        nl.addWidget(note_icon)

        note = QLabel("El proceso puede tardar según el número de páginas y la resolución.")
        note.setFont(QFont("Inter", 9))
        note.setStyleSheet("color: {{TEXT_SECONDARY}};")
        note.setWordWrap(True)
        nl.addWidget(note, 1)

        self.config_layout.addWidget(note_container)

    def _setup_drag_drop(self, drop_area: QFrame):
        """Configura drag & drop en el área de drop"""
        drop_area._accepted_extensions = [".pdf"]
        drop_area._multiple = False

        def dragEnterEvent(event: QDragEnterEvent):
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                valid_files = [
                    url.toLocalFile() for url in urls if url.toLocalFile().lower().endswith(".pdf")
                ]
                if valid_files:
                    event.acceptProposedAction()
                    drop_area.setStyleSheet(
                        drop_area.styleSheet().replace(
                            "border: 2px dashed {{BORDER}}", "border: 2px solid {{ACCENT}}"
                        )
                        + "\nbackground-color: {{ACCENT}}20;"
                    )
                else:
                    event.ignore()
            else:
                event.ignore()

        def dragMoveEvent(event: QDragMoveEvent):
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                valid_files = [
                    url.toLocalFile() for url in urls if url.toLocalFile().lower().endswith(".pdf")
                ]
                if valid_files:
                    event.acceptProposedAction()
                else:
                    event.ignore()
            else:
                event.ignore()

        def dragLeaveEvent(event):
            drop_area.setStyleSheet(
                """
                QFrame {
                    border: 2px dashed {{BORDER}};
                    background-color: {{HOVER}};
                }
                QFrame:hover { border-color: {{ACCENT}}; }
            """
            )

        def dropEvent(event: QDropEvent):
            drop_area.setStyleSheet(
                """
                QFrame {
                    border: 2px dashed {{BORDER}};
                    background-color: {{HOVER}};
                }
                QFrame:hover { border-color: {{ACCENT}}; }
            """
            )
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                files = [
                    url.toLocalFile() for url in urls if url.toLocalFile().lower().endswith(".pdf")
                ]
                if files:
                    event.acceptProposedAction()
                    self.on_file_dropped(files[0])
                else:
                    event.ignore()
            else:
                event.ignore()

        drop_area.dragEnterEvent = dragEnterEvent
        drop_area.dragMoveEvent = dragMoveEvent
        drop_area.dragLeaveEvent = dragLeaveEvent
        drop_area.dropEvent = dropEvent

    def on_file_dropped(self, file_path: str):
        """Maneja archivo soltado"""
        self.current_file = file_path
        self.file_label.setText(os.path.basename(file_path))

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar PDF", "", "PDF (*.pdf)")
        if file:
            self.on_file_dropped(file)

    def start_processing(self):
        if not self.current_file:
            return self.show_error("Selecciona un archivo PDF")

        # Validar que el archivo existe
        from pathlib import Path

        if not Path(self.current_file).exists():
            return self.show_error("El archivo seleccionado no existe")

        lang_code = self.langs[self.lang_combo.currentText()]
        dpi = self.dpi_spin.value()

        output_dir = settings.get_output_directory()
        input_name = FileHandler.get_filename(self.current_file)
        default_name = output_dir / f"ocr_{input_name}"

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Guardar PDF con OCR", str(default_name), "Archivos PDF (*.pdf)"
        )

        if not output_file:
            return  # Cancelado

        self.last_output_file = output_file

        self.set_processing_state(True)
        self.update_progress(0, "Iniciando motor OCR...")

        self.worker = OCRWorker(self.current_file, output_file, lang_code, dpi)
        self.worker.progress_updated.connect(self.update_progress_message)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def update_progress_message(self, val, msg):
        self.update_progress(val, msg)

    def on_success(self, result):
        self.set_processing_state(False)
        self.show_success(
            f"¡OCR Completado!\n"
            f"Se procesaron {result['total_pages']} páginas.\n"
            f"Caracteres detectados: {result['total_characters']}"
        )
        self.show_success_dialog(self.last_output_file, "OCR Completado")

    def on_error(self, error):
        self.set_processing_state(False)
        self.show_error(f"Error: {error}")

    def reset_operation(self):
        self.current_file = None
        self.file_label.setText("Ningún archivo seleccionado")
        self.progress_bar.setValue(0)
