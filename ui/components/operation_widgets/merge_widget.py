"""
Widget de combinación de PDFs
Permite combinar múltiples archivos PDF en uno solo
"""
from PySide6.QtWidgets import (
    QVBoxLayout, QListWidget, QPushButton, QFileDialog, QHBoxLayout
)
from PySide6.QtCore import Qt, QThread, Signal
from .base_operation import BaseOperationWidget
from backend.services.pdf_merger import PDFMerger
from utils.file_handler import FileHandler
from config.settings import settings


class MergeWorker(QThread):
    """Worker thread para combinar PDFs"""
    progress_updated = Signal(int)
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, input_files, output_file):
        super().__init__()
        self.input_files = input_files
        self.output_file = output_file
    
    def run(self):
        try:
            result = PDFMerger.merge_pdfs(
                self.input_files,
                self.output_file,
                progress_callback=self.progress_updated.emit
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MergeWidget(BaseOperationWidget):
    """Widget para combinar PDFs"""
    
    def __init__(self):
        super().__init__(
            "📑 Combinar PDFs",
            "Une múltiples archivos PDF en un solo documento"
        )
        self.files = []
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz específica"""
        # Botón para agregar archivos
        add_btn = QPushButton("+ Agregar PDFs")
        add_btn.clicked.connect(self.add_files)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 10px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f9fafb;
                border-color: #000000;
            }
        """)
        self.config_layout.addWidget(add_btn)
        
        # Lista de archivos
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 2px dashed #d1d5db;
                border-radius: 8px;
                background-color: #f9fafb;
                padding: 8px;
                min-height: 200px;
            }
        """)
        self.config_layout.addWidget(self.file_list)
        
        # Información
        self.info_label = QLabel("Arrastra archivos o usa el botón para agregar")
        self.info_label.setStyleSheet("color: #6b7280; font-size: 12px; margin-top: 8px;")
        self.config_layout.addWidget(self.info_label)
    
    def add_files(self):
        """Abre diálogo para seleccionar archivos"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar PDFs",
            "",
            "Archivos PDF (*.pdf)"
        )
        
        if files:
            for file in files:
                if file not in self.files:
                    self.files.append(file)
                    self.file_list.addItem(f"📄 {file.split('/')[-1]}")
            
            self.info_label.setText(f"{len(self.files)} archivo(s) seleccionado(s)")
    
    def start_processing(self):
        """Inicia la combinación de PDFs"""
        if len(self.files) < 2:
            self.show_error("Necesitas al menos 2 archivos PDF para combinar")
            return
        
        # Generar archivo de salida
        output_file = str(settings.OUTPUT_DIR / "combined.pdf")
        output_file = FileHandler.ensure_unique_filename(output_file)
        
        # Crear y ejecutar worker
        self.set_processing_state(True)
        self.update_progress(0, "Iniciando combinación...")
        
        self.worker = MergeWorker(self.files, output_file)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_success(self, result):
        """Maneja el resultado exitoso"""
        self.set_processing_state(False)
        self.show_success(f"¡PDFs combinados! Archivo: {result['output_path']}")
    
    def on_error(self, error):
        """Maneja errores"""
        self.set_processing_state(False)
        self.show_error(f"Error: {error}")
    
    def reset_operation(self):
        """Reinicia la operación"""
        self.files = []
        self.file_list.clear()
        self.info_label.setText("Arrastra archivos o usa el botón para agregar")
        self.progress_bar.setValue(0)


from PySide6.QtWidgets import QLabel
