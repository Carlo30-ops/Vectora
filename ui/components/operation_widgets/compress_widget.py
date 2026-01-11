"""
Widget de compresión de PDFs
Permite reducir el tamaño de archivos PDF
"""

from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSlider,
    QVBoxLayout,
)

from backend.services.pdf_compressor import PDFCompressor
from config.settings import settings
from utils.file_handler import FileHandler

from .base_operation import BaseOperationWidget


class CompressWorker(QThread):
    """Worker thread para comprimir PDFs"""

    progress_updated = Signal(int)
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, input_file, output_file, quality_level):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.quality_level = quality_level

    def run(self):
        try:
            # Instanciar servicio
            compressor = PDFCompressor()

            result = compressor.compress_pdf(
                self.input_file,
                self.output_file,
                self.quality_level,
                progress_callback=self.progress_updated.emit,
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class CompressWidget(BaseOperationWidget):
    """Widget de compresión"""

    def __init__(self):
        super().__init__("🗜️ Comprimir PDF", "Reduce el tamaño del archivo optimizando recursos")
        self.input_file = None
        self.quality_level = settings.DEFAULT_COMPRESSION_QUALITY
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz - Look Premium"""
        # Cambiar icono de la base
        icon = IconHelper.get_icon("compress", color="#FFFFFF")
        if not icon.isNull():
            self.icon_lbl.setPixmap(icon.pixmap(36, 36))

        # Dropzone para archivo
        drop_area = QFrame()
        drop_area.setObjectName("glassContainer")
        drop_area.setMinimumHeight(120)
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

        # Panel de Opciones - Glass look
        opt_panel = QFrame()
        opt_panel.setObjectName("glassContainer")
        opt_panel.setStyleSheet("padding: 24px;")

        ol = QVBoxLayout(opt_panel)
        ol.setSpacing(16)

        header_layout = QHBoxLayout()
        hl_label = QLabel("Nivel de Compresión")
        hl_label.setFont(QFont("Inter", 11, QFont.Bold))
        header_layout.addWidget(hl_label)

        self.level_label = QLabel("Media (Recomendado)")
        self.level_label.setFont(QFont("Inter", 10, QFont.Bold))
        self.level_label.setStyleSheet("color: {{ACCENT}};")
        header_layout.addWidget(self.level_label)
        header_layout.addStretch()
        ol.addLayout(header_layout)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setFixedHeight(30)
        self.slider.setCursor(Qt.PointingHandCursor)
        self.slider.valueChanged.connect(self.update_compression_level)
        ol.addWidget(self.slider)

        # Etiquetas del slider
        labels_layout = QHBoxLayout()
        l_low = QLabel("Baja")
        l_mid = QLabel("Media")
        l_high = QLabel("Extrema")
        for l in [l_low, l_mid, l_high]:
            l.setFont(QFont("Inter", 9))
            l.setStyleSheet("color: {{TEXT_SECONDARY}};")

        labels_layout.addWidget(l_low)
        labels_layout.addStretch()
        labels_layout.addWidget(l_mid)
        labels_layout.addStretch()
        labels_layout.addWidget(l_high)
        ol.addLayout(labels_layout)

        self.info_label = QLabel("Reduce ~40% el tamaño manteniendo buena calidad")
        self.info_label.setFont(QFont("Inter", 10))
        self.info_label.setStyleSheet("color: {{TEXT_SECONDARY}}; font-style: italic;")
        ol.addWidget(self.info_label)

        self.config_layout.addWidget(opt_panel)

    def select_file(self):
        """Selecciona el archivo a comprimir"""
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar PDF", "", "Archivos PDF (*.pdf)")
        if file:
            self.input_file = file
            self.file_label.setText(f"📄 {file.split('/')[-1]}")

    def update_compression_level(self, value):
        """Actualiza la etiqueta e información según el slider"""
        level_key = settings.get_compression_level(value)
        self.quality_level = level_key

        info = settings.COMPRESSION_LEVELS[level_key]
        self.level_label.setText(info["label"])
        self.info_label.setText(f"Reduce {info['reduction']} el tamaño. {info['description']}")

    def start_processing(self):
        """Inicia la compresión"""
        if not self.input_file:
            self.show_error("Por favor selecciona un archivo PDF primero")
            return

        # Preguntar dónde guardar
        output_dir = settings.get_output_directory()
        input_name = FileHandler.get_filename(self.input_file)
        default_name = output_dir / f"compressed_{input_name}"

        output_file, _ = QFileDialog.getSaveFileName(
            self, "Guardar PDF Comprimido", str(default_name), "Archivos PDF (*.pdf)"
        )

        if not output_file:
            return  # Usuario canceló

        self.last_output_file = output_file

        self.set_processing_state(True)
        self.update_progress(0, "Iniciando compresión...")

        self.worker = CompressWorker(self.input_file, output_file, self.quality_level)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_success(self, result):
        """Maneja el éxito de la operación"""
        self.set_processing_state(False)
        self.show_success("¡Compresión exitosa!")

        # Mostrar diálogo con opciones
        self.show_success_dialog(self.last_output_file, "PDF Comprimido")

    def on_error(self, error):
        """Maneja errores"""
        self.set_processing_state(False)
        self.show_error(f"Error: {error}")

    def reset_operation(self):
        """Reinicia el widget"""
        self.input_file = None
        self.file_label.setText("Ningún archivo seleccionado")
        self.slider.setValue(50)
        self.progress_bar.setValue(0)
