"""
Widget de procesamiento por lotes
Aplica una operación a múltiples archivos
"""
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel,
    QListWidget, QComboBox, QStackedWidget, QWidget, QSlider,
    QLineEdit, QGroupBox
)
from PySide6.QtCore import Qt, QThread, Signal
from .base_operation import BaseOperationWidget
from backend.services.batch_processor import BatchProcessor
from backend.services.pdf_compressor import PDFCompressor
from backend.services.pdf_converter import PDFConverter
from backend.services.pdf_security import PDFSecurity
from config.settings import settings
import os


class BatchWorker(QThread):
    """Worker para procesamiento por lotes"""
    progress_updated = Signal(int)
    item_processed = Signal(str, bool) # file, success
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, operation_type, files, config):
        super().__init__()
        self.op_type = operation_type
        self.files = files
        self.config = config
    
    def run(self):
        try:
            func = None
            kw_config = {}
            
            # Mapear operación a función y config
            if self.op_type == "Comprimir PDF":
                func = PDFCompressor.compress_pdf
                kw_config = {'quality_level': self.config['quality']}
                
            elif self.op_type == "PDF a Word":
                func = PDFConverter.pdf_to_word
                
            elif self.op_type == "Word a PDF":
                func = PDFConverter.word_to_pdf
                
            elif self.op_type == "Encriptar":
                func = PDFSecurity.encrypt_pdf
                kw_config = {'password': self.config['password']}
                
            elif self.op_type == "Desencriptar":
                func = PDFSecurity.decrypt_pdf
                kw_config = {'password': self.config['password']}

            # Callback para BatchProcessor
            def batch_callback(p, msg, res):
                self.progress_updated.emit(p)
                self.item_processed.emit(res['file'], res['success'])

            # Ejecutar
            result = BatchProcessor.process_batch(
                self.files,
                func,
                kw_config,
                str(settings.OUTPUT_DIR / "batch"),
                progress_callback=batch_callback
            )
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))


class BatchWidget(BaseOperationWidget):
    """Widget de procesamiento por lotes"""
    
    def __init__(self):
        super().__init__(
            "⚡ Procesamiento por Lotes",
            "Aplica la misma operación a múltiples archivos a la vez"
        )
        self.files = []
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # --- Lista de Archivos ---
        self.config_layout.addWidget(QLabel("1. Selecciona Archivos:"))
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Agregar Archivos")
        add_btn.clicked.connect(self.add_files)
        clear_btn = QPushButton("🗑️ Limpiar")
        clear_btn.clicked.connect(self.clear_files)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        self.config_layout.addLayout(btn_layout)
        
        self.file_list = QListWidget()
        self.file_list.setFixedHeight(150)
        self.config_layout.addWidget(self.file_list)
        
        # --- Selección de Operación ---
        self.config_layout.addWidget(QLabel("2. Elige Operación:"))
        self.op_combo = QComboBox()
        self.op_combo.addItems([
            "Comprimir PDF",
            "PDF a Word",
            "Word a PDF",
            "Encriptar",
            "Desencriptar"
        ])
        self.op_combo.currentIndexChanged.connect(self.on_op_changed)
        self.config_layout.addWidget(self.op_combo)
        
        # --- Configuración Específica ---
        self.config_stack = QStackedWidget()
        self.config_layout.addWidget(self.config_stack)
        
        # 0. Config Compresión
        self.compress_config = QWidget()
        c_layout = QVBoxLayout(self.compress_config)
        c_layout.addWidget(QLabel("Nivel de compresión:"))
        self.c_slider = QSlider(Qt.Horizontal)
        self.c_slider.setRange(0, 100)
        self.c_slider.setValue(50)
        c_layout.addWidget(self.c_slider)
        self.config_stack.addWidget(self.compress_config)
        
        # 1 y 2. Sin config (PDF->Word, Word->PDF)
        self.empty_config = QWidget()
        self.config_stack.addWidget(self.empty_config) # Para índice 1 y 2
        
        # 3. Config Seguridad (Password)
        self.sec_config = QWidget()
        s_layout = QVBoxLayout(self.sec_config)
        s_layout.addWidget(QLabel("Contraseña:"))
        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setPlaceholderText("Contraseña para todos los archivos")
        s_layout.addWidget(self.pwd_input)
        self.config_stack.addWidget(self.sec_config) # Para índice 3 y 4

        # Inicializar vista de config
        self.on_op_changed(0)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivos")
        if files:
            for f in files:
                if f not in self.files:
                    self.files.append(f)
                    self.file_list.addItem(os.path.basename(f))
                    
    def clear_files(self):
        self.files = []
        self.file_list.clear()
        
    def on_op_changed(self, idx):
        if idx == 0: # Comprimir
            self.config_stack.setCurrentWidget(self.compress_config)
        elif idx == 1 or idx == 2: # Conversiones simples
            self.config_stack.setCurrentWidget(self.empty_config)
        else: # Seguridad
            self.config_stack.setCurrentWidget(self.sec_config)
            
    def start_processing(self):
        if not self.files:
            return self.show_error("Agrega archivos primero")
            
        op = self.op_combo.currentText()
        config = {}
        
        if op == "Comprimir PDF":
            # Convertir slider a nivel string usando settings
            # Importante: reutilizar logica o hardcodear mapeo simple aquí
            val = self.c_slider.value()
            level = settings.get_compression_level(val)
            config['quality'] = level
            
        elif op in ["Encriptar", "Desencriptar"]:
            pwd = self.pwd_input.text()
            if not pwd: return self.show_error("Ingresa una contraseña")
            config['password'] = pwd
            
        self.set_processing_state(True)
        self.update_progress(0, "Iniciando lote...")
        
        self.worker = BatchWorker(op, self.files, config)
        self.worker.progress_updated.connect(lambda v: self.update_progress(v))
        self.worker.item_processed.connect(self.on_item_processed)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()
        
    def on_item_processed(self, filename, success):
        status = "✅" if success else "❌"
        # Podríamos actualizar un log visual aquí
        print(f"{status} {filename}")

    def on_success(self, result):
        self.set_processing_state(False)
        self.show_success(f"Lote finalizado.\n{result['message']}")
        
    def on_error(self, error):
        self.set_processing_state(False)
        self.show_error(f"Error: {error}")
        
    def reset_operation(self):
        self.clear_files()
        self.progress_bar.setValue(0)
