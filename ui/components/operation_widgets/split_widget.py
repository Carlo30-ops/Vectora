"""
Widget para dividir PDFs
Permite extraer rangos, páginas específicas o dividir cada N páginas
"""

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)

from backend.services.pdf_splitter import PDFSplitter
from config.settings import settings
from utils.file_handler import FileHandler

from .base_operation import BaseOperationWidget


class SplitWorker(QThread):
    """Worker thread para dividir PDFs"""

    progress_updated = Signal(int)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, input_file, mode, config, output_path):
        super().__init__()
        self.input_file = input_file
        self.mode = mode
        self.config = config
        self.output_path = output_path

    def run(self):
        try:
            if self.mode == "range":
                result = PDFSplitter.split_by_range(
                    self.input_file,
                    self.output_path,
                    self.config["start"],
                    self.config["end"],
                    self.progress_updated.emit,
                )
            elif self.mode == "pages":
                result = PDFSplitter.split_by_pages(
                    self.input_file,
                    self.output_path,
                    self.config["pages"],
                    self.progress_updated.emit,
                )
            else:  # every
                result = PDFSplitter.split_every_n_pages(
                    self.input_file, self.output_path, self.config["n"], self.progress_updated.emit
                )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class SplitWidget(BaseOperationWidget):
    """Widget para dividir PDFs"""

    def __init__(self):
        super().__init__("✂️ Dividir PDF", "Extrae páginas específicas de un documento PDF")
        self.input_file = None
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz - Look Premium"""
        # Cambiar icono de la base
        icon = IconHelper.get_icon("scissors", color="#FFFFFF")
        if not icon.isNull():
            self.icon_lbl.setPixmap(icon.pixmap(36, 36))

        # Selección de archivo - Dropzone simple
        drop_area = QFrame()
        drop_area.setObjectName("glassContainer")
        drop_area.setMinimumHeight(120)
        drop_area.setStyleSheet(
            """
            QFrame {
                border: 2px dashed {{BORDER}};
                background-color: {{HOVER}};
            }
            QFrame:hover {
                border-color: {{ACCENT}};
            }
        """
        )

        dal = QVBoxLayout(drop_area)
        dal.setAlignment(Qt.AlignCenter)

        self.file_label = QLabel("Arrastra tu PDF aquí o haz clic para seleccionar")
        self.file_label.setFont(QFont("Inter", 11))
        self.file_label.setStyleSheet("color: {{TEXT_SECONDARY}};")
        dal.addWidget(self.file_label)

        btn = QPushButton("Seleccionar PDF")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
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
        btn.clicked.connect(self.select_file)
        dal.addWidget(btn, 0, Qt.AlignCenter)

        self.config_layout.addWidget(drop_area)

        # Opciones en Horizontal para mejor uso de espacio
        options_layout = QHBoxLayout()
        options_layout.setSpacing(20)

        # Modos de división
        mode_box = QGroupBox("Opciones de División")
        mode_box.setFont(QFont("Inter", 10, QFont.Bold))
        ml = QVBoxLayout(mode_box)
        ml.setSpacing(12)

        self.mode_group = QButtonGroup()
        self.range_radio = QRadioButton("Por Rango (ej: 5-10)")
        self.pages_radio = QRadioButton("Páginas (ej: 1,3,5-8)")
        self.every_radio = QRadioButton("Cada N páginas")
        self.range_radio.setChecked(True)

        self.mode_group.addButton(self.range_radio, 0)
        self.mode_group.addButton(self.pages_radio, 1)
        self.mode_group.addButton(self.every_radio, 2)

        ml.addWidget(self.range_radio)
        ml.addWidget(self.pages_radio)
        ml.addWidget(self.every_radio)

        options_layout.addWidget(mode_box, 1)

        # Campos de configuración - Dynamic stack
        config_box = QGroupBox("Parámetros")
        config_box.setFont(QFont("Inter", 10, QFont.Bold))
        cl = QVBoxLayout(config_box)
        cl.setSpacing(10)

        hl_range = QHBoxLayout()
        self.range_start = QLineEdit()
        self.range_start.setPlaceholderText("Inicio")
        self.range_end = QLineEdit()
        self.range_end.setPlaceholderText("Fin")
        hl_range.addWidget(self.range_start)
        hl_range.addWidget(self.range_end)
        cl.addLayout(hl_range)

        self.pages_spec = QLineEdit()
        self.pages_spec.setPlaceholderText("Ej: 1, 3, 5-8")
        cl.addWidget(self.pages_spec)

        self.every_n = QLineEdit()
        self.every_n.setPlaceholderText("Ej: 1")
        cl.addWidget(self.every_n)

        options_layout.addWidget(config_box, 1)
        self.config_layout.addLayout(options_layout)

    def select_file(self):
        """Seleccionar archivo PDF"""
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar PDF", "", "PDF (*.pdf)")
        if file:
            self.input_file = file
            self.file_label.setText(f"📄 {file.split('/')[-1]}")

    def start_processing(self):
        """Inicia la división"""
        if not self.input_file:
            self.show_error("Selecciona un archivo PDF primero")
            return

        mode_id = self.mode_group.checkedId()
        config = {}

        # Determinar nombre por defecto
        input_name = FileHandler.get_filename(self.input_file)
        if hasattr(input_name, "removesuffix"):
            input_base = input_name.removesuffix(".pdf")
        else:
            input_base = input_name[:-4] if input_name.lower().endswith(".pdf") else input_name

        output_dir = settings.get_output_directory()
        default_name = output_dir / f"{input_base}_split.pdf"

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Guardar PDF Dividido", str(default_name), "Archivos PDF (*.pdf)"
        )

        if not output_file:
            return  # Cancelado

        self.last_output_file = output_file

        if mode_id == 0:  # Range
            try:
                config["start"] = int(self.range_start.text())
                config["end"] = int(self.range_end.text())
                mode = "range"
            except:
                self.show_error("Ingresa valores numéricos válidos")
                return
        elif mode_id == 1:  # Pages
            config["pages"] = self.pages_spec.text()
            mode = "pages"
        else:  # Every
            try:
                config["n"] = int(self.every_n.text())
                mode = "every"
                # Para split every, la salida suele ser una carpeta o sufijos
                # En este caso asumimos que el backend maneja sufijos si es un solo archivo
                # O podríamos pedir un directorio si split_every genera múltiples archivos
                # Revisemos la implementación de SplitWorker/PDFSplitter para 'every'
                # El worker usa settings.OUTPUT_DIR original... debemos pasar el directorio de salida del archivo seleccionado
                # Si output_file es "C:/.../doc.pdf", el splitter seguramente usará eso como base
            except:
                self.show_error("Ingresa un número válido")
                return

        # Ajuste específico para 'every' que necesita un directorio base
        if mode == "every":
            # En este caso, output_file será el patrón base
            pass

        self.set_processing_state(True)
        # Note: SplitWorker for 'every' takes settings.OUTPUT_DIR in the original code
        # We should probably pass the directory of the selected file
        output_path_arg = output_file if mode != "every" else str(Path(output_file).parent)

        self.worker = SplitWorker(self.input_file, mode, config, output_path_arg)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_success(self, result):
        """Maneja éxito"""
        self.set_processing_state(False)
        self.show_success(result.get("message", "¡Operación completada!"))

        # Mostrar diálogo con opciones
        # Si fue 'every', result seguramente tiene info de los archivos o carpeta
        # Usamos self.last_output_file como referencia
        self.show_success_dialog(self.last_output_file, "División Completada")

    def on_error(self, error):
        """Maneja error"""
        self.set_processing_state(False)
        self.show_error(f"Error: {error}")

    def reset_operation(self):
        """Reinicia"""
        self.input_file = None
        self.file_label.setText("Ningún archivo seleccionado")
        self.range_start.clear()
        self.range_end.clear()
        self.pages_spec.clear()
        self.every_n.clear()
