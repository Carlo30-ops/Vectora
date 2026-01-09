"""
Widget para dividir PDFs
Permite extraer rangos, páginas específicas o dividir cada N páginas
"""
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel,
    QLineEdit, QRadioButton, QButtonGroup, QGroupBox
)
from PySide6.QtCore import QThread, Signal
from .base_operation import BaseOperationWidget
from backend.services.pdf_splitter import PDFSplitter
from utils.file_handler import FileHandler
from config.settings import settings


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
            if self.mode == 'range':
                result = PDFSplitter.split_by_range(
                    self.input_file,
                    self.output_path,
                    self.config['start'],
                    self.config['end'],
                    self.progress_updated.emit
                )
            elif self.mode == 'pages':
                result = PDFSplitter.split_by_pages(
                    self.input_file,
                    self.output_path,
                    self.config['pages'],
                    self.progress_updated.emit
                )
            else:  # every
                result = PDFSplitter.split_every_n_pages(
                    self.input_file,
                    str(settings.OUTPUT_DIR),
                    self.config['n'],
                    self.progress_updated.emit
                )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class SplitWidget(BaseOperationWidget):
    """Widget para dividir PDFs"""
    
    def __init__(self):
        super().__init__(
            "✂️ Dividir PDF",
            "Extrae páginas específicas de un documento PDF"
        )
        self.input_file = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Selección de archivo
        btn = QPushButton("📄 Seleccionar PDF")
        btn.clicked.connect(self.select_file)
        self.config_layout.addWidget(btn)
        
        self.file_label = QLabel("Ningún archivo seleccionado")
        self.file_label.setStyleSheet("color: #6b7280; margin-bottom: 16px;")
        self.config_layout.addWidget(self.file_label)
        
        # Modos de división
        mode_group = QGroupBox("Modo de División")
        mode_layout = QVBoxLayout(mode_group)
        
        self.mode_group = QButtonGroup()
        self.range_radio = QRadioButton("Por Rango (ej: páginas 5-10)")
        self.pages_radio = QRadioButton("Páginas Específicas (ej: 1,3,5-8)")
        self.every_radio = QRadioButton("Cada N páginas")
        self.range_radio.setChecked(True)
        
        self.mode_group.addButton(self.range_radio, 0)
        self.mode_group.addButton(self.pages_radio, 1)
        self.mode_group.addButton(self.every_radio, 2)
        
        mode_layout.addWidget(self.range_radio)
        mode_layout.addWidget(self.pages_radio)
        mode_layout.addWidget(self.every_radio)
        
        self.config_layout.addWidget(mode_group)
        
        # Campos de configuración
        self.range_start = QLineEdit()
        self.range_start.setPlaceholderText("Página inicial")
        self.range_end = QLineEdit()
        self.range_end.setPlaceholderText("Página final")
        
        self.pages_spec = QLineEdit()
        self.pages_spec.setPlaceholderText("Ej: 1,3,5-8,12")
        
        self.every_n = QLineEdit()
        self.every_n.setPlaceholderText("Número de páginas")
        
        self.config_layout.addWidget(QLabel("Configuración:"))
        self.config_layout.addWidget(self.range_start)
        self.config_layout.addWidget(self.range_end)
        self.config_layout.addWidget(self.pages_spec)
        self.config_layout.addWidget(self.every_n)
    
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
        output_path = str(settings.OUTPUT_DIR / "split.pdf")
        
        if mode_id == 0:  # Range
            try:
                config['start'] = int(self.range_start.text())
                config['end'] = int(self.range_end.text())
                mode = 'range'
            except:
                self.show_error("Ingresa valores numéricos válidos")
                return
        elif mode_id == 1:  # Pages
            config['pages'] = self.pages_spec.text()
            mode = 'pages'
        else:  # Every
            try:
                config['n'] = int(self.every_n.text())
                mode = 'every'
            except:
                self.show_error("Ingresa un número válido")
                return
        
        self.set_processing_state(True)
        self.worker = SplitWorker(self.input_file, mode, config, output_path)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_success(self, result):
        """Maneja éxito"""
        self.set_processing_state(False)
        self.show_success(result.get('message', '¡Operación completada!'))
    
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
