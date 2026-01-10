"""
Widget de OCR (Reconocimiento Óptico de Caracteres)
Extrae texto de PDFs escaneados
"""
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel,
    QComboBox, QSpinBox, QCheckBox
)
from PySide6.QtCore import Qt, QThread, Signal
from .base_operation import BaseOperationWidget
from backend.services.ocr_service import OCRService
from utils.file_handler import FileHandler
from config.settings import settings
import os


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
                progress_callback=progress_callback
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class OCRWidget(BaseOperationWidget):
    """Widget de OCR"""
    
    def __init__(self):
        super().__init__(
            "🔍 OCR (Reconocimiento de Texto)",
            "Convierte documentos escaneados en texto buscable"
        )
        self.current_file = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Selector de archivo
        file_layout = QHBoxLayout()
        self.file_btn = QPushButton("📄 Seleccionar PDF Escaneado")
        self.file_btn.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_btn)
        
        self.file_label = QLabel("Ningún archivo seleccionado")
        self.file_label.setStyleSheet("color: #6b7280; font-style: italic;")
        file_layout.addWidget(self.file_label, 1)
        self.config_layout.addLayout(file_layout)
        
        # Opciones
        opts_layout = QHBoxLayout()
        
        # Idioma
        opts_layout.addWidget(QLabel("Idioma:"))
        self.lang_combo = QComboBox()
        # Mapeo de nombres amigables a códigos Tesseract
        self.langs = {
            "Español + Inglés": "spa+eng",
            "Español": "spa",
            "Inglés": "eng"
        }
        self.lang_combo.addItems(self.langs.keys())
        opts_layout.addWidget(self.lang_combo)
        
        # DPI
        opts_layout.addWidget(QLabel("Calidad (DPI):"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(150, 600)
        self.dpi_spin.setValue(300)
        self.dpi_spin.setSingleStep(50)
        self.dpi_spin.setSuffix(" dpi")
        opts_layout.addWidget(self.dpi_spin)
        
        opts_layout.addStretch()
        self.config_layout.addLayout(opts_layout)
        
        # Nota informativa
        note = QLabel("Nota: El proceso puede tardar dependiendo del número de páginas y la resolución.")
        note.setStyleSheet("color: #6b7280; font-size: 11px; margin-top: 10px;")
        note.setWordWrap(True)
        self.config_layout.addWidget(note)
        
    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar PDF", "", "PDF (*.pdf)")
        if file:
            self.current_file = file
            self.file_label.setText(os.path.basename(file))
            
    def start_processing(self):
        if not self.current_file:
            return self.show_error("Selecciona un archivo PDF")
            
        lang_code = self.langs[self.lang_combo.currentText()]
        dpi = self.dpi_spin.value()
        
        output_dir = settings.get_output_directory()
        input_name = FileHandler.get_filename(self.current_file)
        default_name = output_dir / f"ocr_{input_name}"
        
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar PDF con OCR",
            str(default_name),
            "Archivos PDF (*.pdf)"
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
