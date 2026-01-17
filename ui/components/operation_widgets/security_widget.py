"""
Widget de seguridad para PDFs
Permite encriptar, desencriptar y gestionar permisos
"""

import os

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QFont
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)

from backend.services.pdf_security import PDFSecurity
from config.settings import settings
from ui.components.ui_helpers import IconHelper
from utils.file_handler import FileHandler

from .base_operation import BaseOperationWidget


class SecurityWorker(QThread):
    """Worker para operaciones de seguridad"""

    progress_updated = Signal(int, str)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, mode, **kwargs):
        super().__init__()
        self.mode = mode
        self.kwargs = kwargs

    def run(self):
        try:
            # Instanciar servicio
            security = PDFSecurity()

            if self.mode == "encrypt":
                result = security.encrypt_pdf(
                    self.kwargs["input_path"],
                    self.kwargs["output_path"],
                    self.kwargs["password"],
                    self.kwargs["permissions"],
                    progress_callback=self.progress_updated.emit,
                )
            elif self.mode == "decrypt":
                result = security.decrypt_pdf(
                    self.kwargs["input_path"],
                    self.kwargs["output_path"],
                    self.kwargs["password"],
                    progress_callback=self.progress_updated.emit,
                )
            self.finished.emit(result.to_dict())
        except Exception as e:
            self.error.emit(str(e))


class SecurityWidget(BaseOperationWidget):
    """Widget de seguridad"""

    def __init__(self):
        super().__init__("🔒 Seguridad PDF", "Protege tus documentos con contraseña y permisos")
        self.current_file = None
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz - Look Premium"""
        # Cambiar icono de la base
        icon = IconHelper.get_icon("shield", color="#FFFFFF")
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

        self.file_label = QLabel("Arrastra tu PDF aquí o haz clic para seleccionar")
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

        # Opciones en Horizontal
        options_layout = QHBoxLayout()
        options_layout.setSpacing(20)

        # Selección de Modo
        mode_box = QGroupBox("Operación")
        mode_box.setFont(QFont("Inter", 10, QFont.Bold))
        ml = QVBoxLayout(mode_box)
        ml.setSpacing(12)

        self.mode_bg = QButtonGroup()
        self.rb_encrypt = QRadioButton("Encriptar (Proteger)")
        self.rb_decrypt = QRadioButton("Desencriptar (Quitar)")
        self.rb_encrypt.setChecked(True)
        self.rb_encrypt.toggled.connect(self.toggle_mode)

        self.mode_bg.addButton(self.rb_encrypt, 0)
        self.mode_bg.addButton(self.rb_decrypt, 1)

        ml.addWidget(self.rb_encrypt)
        ml.addWidget(self.rb_decrypt)
        options_layout.addWidget(mode_box, 1)

        # --- Área de Contraseña ---
        pwd_box = QGroupBox("Contraseña")
        pwd_box.setFont(QFont("Inter", 10, QFont.Bold))
        pl = QVBoxLayout(pwd_box)
        pl.setSpacing(10)

        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Ingresa la contraseña")
        self.pwd_input.setEchoMode(QLineEdit.Password)

        self.pwd_confirm = QLineEdit()
        self.pwd_confirm.setPlaceholderText("Confirma la contraseña")
        self.pwd_confirm.setEchoMode(QLineEdit.Password)

        self.show_pwd = QCheckBox("Mostrar")
        self.show_pwd.stateChanged.connect(self.toggle_pwd_visibility)

        pl.addWidget(self.pwd_input)
        pl.addWidget(self.pwd_confirm)
        pl.addWidget(self.show_pwd)
        options_layout.addWidget(pwd_box, 1)

        self.config_layout.addLayout(options_layout)

        # --- Área de Permisos (Solo Encriptar) ---
        self.perm_box = QGroupBox("Permisos Permitidos")
        self.perm_box.setFont(QFont("Inter", 10, QFont.Bold))
        perml = QGridLayout(self.perm_box)
        perml.setSpacing(10)

        self.chk_print = QCheckBox("Impresión")
        self.chk_print.setChecked(True)
        self.chk_copy = QCheckBox("Copiar contenido")
        self.chk_copy.setChecked(True)
        self.chk_modify = QCheckBox("Modificar")
        self.chk_modify.setChecked(False)
        self.chk_notes = QCheckBox("Anotaciones")
        self.chk_notes.setChecked(True)

        perml.addWidget(self.chk_print, 0, 0)
        perml.addWidget(self.chk_copy, 0, 1)
        perml.addWidget(self.chk_modify, 1, 0)
        perml.addWidget(self.chk_notes, 1, 1)

        self.config_layout.addWidget(self.perm_box)

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

    def toggle_mode(self):
        is_encrypt = self.rb_encrypt.isChecked()
        self.perm_box.setVisible(is_encrypt)
        self.pwd_confirm.setVisible(is_encrypt)
        self.start_btn.setText("🔒 Proteger PDF" if is_encrypt else "🔓 Desbloquear PDF")

    def toggle_pwd_visibility(self, state):
        # state is an int (0 or 2), convert to bool check
        is_checked = (state == Qt.Checked) if isinstance(state, int) else self.show_pwd.isChecked()
        mode = QLineEdit.Normal if is_checked else QLineEdit.Password
        self.pwd_input.setEchoMode(mode)
        self.pwd_confirm.setEchoMode(mode)

    def start_processing(self):
        if not self.current_file:
            return self.show_error("Selecciona un archivo PDF")

        # Validar que el archivo existe
        from pathlib import Path

        if not Path(self.current_file).exists():
            return self.show_error("El archivo seleccionado no existe")

        pwd = self.pwd_input.text()
        if not pwd:
            return self.show_error("Ingresa una contraseña")

        # Preparar argumentos
        kwargs = {}
        mode = "encrypt" if self.rb_encrypt.isChecked() else "decrypt"

        output_dir = settings.get_output_directory()
        input_name = FileHandler.get_filename(self.current_file)

        if mode == "encrypt":
            if pwd != self.pwd_confirm.text():
                return self.show_error("Las contraseñas no coinciden")

            default_name = output_dir / f"protected_{input_name}"
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Guardar PDF Protegido", str(default_name), "PDF (*.pdf)"
            )
            if not output_file:
                return

            self.last_output_file = output_file
            kwargs = {
                "input_path": self.current_file,
                "output_path": output_file,
                "password": pwd,
                "permissions": {
                    "allow_print": self.chk_print.isChecked(),
                    "allow_copy": self.chk_copy.isChecked(),
                    "allow_modify": self.chk_modify.isChecked(),
                    "allow_annotations": self.chk_notes.isChecked(),
                },
            }
        else:
            default_name = output_dir / f"unlocked_{input_name}"
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Guardar PDF Desbreloqueado", str(default_name), "PDF (*.pdf)"
            )
            if not output_file:
                return

            self.last_output_file = output_file
            kwargs = {"input_path": self.current_file, "output_path": output_file, "password": pwd}

        self.set_processing_state(True)
        self.update_progress(0, "Procesando seguridad...")

        self.worker = SecurityWorker(mode, **kwargs)
        self.worker.progress_updated.connect(self.update_progress_message)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def update_progress_message(self, val, msg):
        self.update_progress(val, msg)

    def on_success(self, result):
        self.set_processing_state(False)
        self.show_success(result.get("message", "Operación completada"))
        self.update_progress(100)
        self.show_success_dialog(self.last_output_file, "Operación de Seguridad Exitosa")

    def on_error(self, error):
        self.set_processing_state(False)
        self.show_error(f"Error: {error}")
        self.update_progress(0)

    def reset_operation(self):
        self.current_file = None
        self.file_label.setText("Ningún archivo seleccionado")
        self.pwd_input.clear()
        self.pwd_confirm.clear()
        self.progress_bar.setValue(0)
