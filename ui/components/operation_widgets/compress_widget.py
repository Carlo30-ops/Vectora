"""
Widget de compresión de PDFs
Permite reducir el tamaño de archivos PDF
"""
from pathlib import Path
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel,
    QSlider, QProgressBar, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal
from .base_operation import BaseOperationWidget
from backend.services.pdf_compressor import PDFCompressor
from utils.file_handler import FileHandler
from config.settings import settings


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
                progress_callback=self.progress_updated.emit
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class CompressWidget(BaseOperationWidget):
    """Widget de compresión"""
    
    def __init__(self):
        super().__init__(
            "🗜️ Comprimir PDF", 
            "Reduce el tamaño del archivo optimizando recursos"
        )
        self.input_file = None
        self.quality_level = settings.DEFAULT_COMPRESSION_QUALITY
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz específica"""
        # Selección de archivo
        btn_layout = QHBoxLayout()
        select_btn = QPushButton("📄 Seleccionar PDF")
        select_btn.clicked.connect(self.select_file)
        select_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()
        
        self.config_layout.addLayout(btn_layout)
        
        self.file_label = QLabel("Ningún archivo seleccionado")
        self.file_label.setStyleSheet("color: #6b7280; margin: 8px 0 16px 0;")
        self.config_layout.addWidget(self.file_label)
        
        # Slider de nivel de compresión
        slider_container = QFrame()
        slider_container.setStyleSheet(".QFrame { background-color: #f3f4f6; border-radius: 8px; padding: 16px; }")
        slider_layout = QVBoxLayout(slider_container)
        
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Nivel de Compresión:"))
        self.level_label = QLabel("Media (Recomendado)")
        self.level_label.setStyleSheet("font-weight: bold; color: #2563eb;")
        header_layout.addWidget(self.level_label)
        header_layout.addStretch()
        slider_layout.addLayout(header_layout)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(25)
        self.slider.valueChanged.connect(self.update_compression_level)
        slider_layout.addWidget(self.slider)
        
        # Etiquetas del slider
        labels_layout = QHBoxLayout()
        labels_layout.addWidget(QLabel("Baja"))
        labels_layout.addStretch()
        labels_layout.addWidget(QLabel("Media"))
        labels_layout.addStretch()
        labels_layout.addWidget(QLabel("Extrema"))
        slider_layout.addLayout(labels_layout)
        
        self.info_label = QLabel("Reduce ~40% el tamaño manteniendo buena calidad")
        self.info_label.setStyleSheet("color: #6b7280; font-style: italic; margin-top: 8px;")
        slider_layout.addWidget(self.info_label)
        
        self.config_layout.addWidget(slider_container)

    def select_file(self):
        """Selecciona el archivo a comprimir"""
        file, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar PDF", "", "Archivos PDF (*.pdf)"
        )
        if file:
            self.input_file = file
            self.file_label.setText(f"📄 {file.split('/')[-1]}")
    
    def update_compression_level(self, value):
        """Actualiza la etiqueta e información según el slider"""
        level_key = settings.get_compression_level(value)
        self.quality_level = level_key
        
        info = settings.COMPRESSION_LEVELS[level_key]
        self.level_label.setText(info['label'])
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
            self,
            "Guardar PDF Comprimido",
            str(default_name),
            "Archivos PDF (*.pdf)"
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
