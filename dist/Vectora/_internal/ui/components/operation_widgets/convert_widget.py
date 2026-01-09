"""
Widget de conversión de formatos
Soporta PDF ↔ Word, PDF ↔ Imágenes
"""
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel,
    QComboBox, QListWidget, QSpinBox, QCheckBox, QStackedWidget, QWidget
)
from PySide6.QtCore import Qt, QThread, Signal
from .base_operation import BaseOperationWidget
from backend.services.pdf_converter import PDFConverter
from utils.file_handler import FileHandler
from config.settings import settings
import os


class ConvertWorker(QThread):
    """Worker para conversiones"""
    progress_updated = Signal(int)
    status_updated = Signal(str) # Para mensajes de texto en progreso
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, mode, **kwargs):
        super().__init__()
        self.mode = mode
        self.kwargs = kwargs
    
    def run(self):
        try:
            result = {}
            # Wrapper para manejar callback que acepta (int, str) o (int)
            def progress_callback(val, msg=None):
                self.progress_updated.emit(val)
                if msg:
                    self.status_updated.emit(msg)

            if self.mode == 'pdf_to_word':
                result = PDFConverter.pdf_to_word(
                    self.kwargs['input_path'],
                    self.kwargs['output_path'],
                    progress_callback=progress_callback
                )
            elif self.mode == 'pdf_to_images':
                result = PDFConverter.pdf_to_images(
                    self.kwargs['input_path'],
                    self.kwargs['output_dir'],
                    dpi=self.kwargs['dpi'],
                    image_format=self.kwargs['format'],
                    progress_callback=lambda v: self.progress_updated.emit(v)
                )
            elif self.mode == 'images_to_pdf':
                result = PDFConverter.images_to_pdf(
                    self.kwargs['image_paths'],
                    self.kwargs['output_path'],
                    progress_callback=lambda v: self.progress_updated.emit(v)
                )
            elif self.mode == 'word_to_pdf':
                result = PDFConverter.word_to_pdf(
                    self.kwargs['input_path'],
                    self.kwargs['output_path'],
                    progress_callback=lambda v: self.progress_updated.emit(v)
                )
                
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ConvertWidget(BaseOperationWidget):
    """Widget de conversión multifuncional"""
    
    def __init__(self):
        super().__init__(
            "🔄 Convertir Formatos",
            "Transforma tus documentos entre PDF, Word e Imágenes"
        )
        self.files = []
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Selector de Modo
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Modo de Conversión:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "PDF a Word (.docx)",
            "PDF a Imágenes",
            "Imágenes a PDF",
            "Word a PDF"
        ])
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo, 1)
        self.config_layout.addLayout(mode_layout)
        
        # Área dinámica de configuración
        self.options_stack = QStackedWidget()
        
        # 1. Opciones comunes (solo archivo)
        self.single_file_widget = QWidget()
        sf_layout = QVBoxLayout(self.single_file_widget)
        sf_layout.setContentsMargins(0, 10, 0, 0)
        
        self.file_btn = QPushButton("📄 Seleccionar Archivo")
        self.file_btn.clicked.connect(self.select_single_file)
        self.file_label = QLabel("Ningún archivo seleccionado")
        self.file_label.setStyleSheet("color: #6b7280;")
        
        sf_layout.addWidget(self.file_btn)
        sf_layout.addWidget(self.file_label)
        sf_layout.addStretch()
        
        # 2. Opciones PDF a Imágenes (DPI, Formato)
        self.pdf_img_widget = QWidget()
        pi_layout = QVBoxLayout(self.pdf_img_widget)
        pi_layout.setContentsMargins(0, 10, 0, 0)
        
        # Reusamos los controles de archivo
        self.pi_file_btn = QPushButton("📄 Seleccionar PDF")
        self.pi_file_btn.clicked.connect(self.select_single_file)
        self.pi_file_label = QLabel("Ningún archivo seleccionado")
        
        opts_layout = QHBoxLayout()
        opts_layout.addWidget(QLabel("DPI:"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(72, 600)
        self.dpi_spin.setValue(150)
        self.dpi_spin.setSingleStep(50)
        opts_layout.addWidget(self.dpi_spin)
        
        opts_layout.addWidget(QLabel("Formato:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPEG"])
        opts_layout.addWidget(self.format_combo)
        
        pi_layout.addWidget(self.pi_file_btn)
        pi_layout.addWidget(self.pi_file_label)
        pi_layout.addLayout(opts_layout)
        pi_layout.addStretch()
        
        # 3. Opciones Imágenes a PDF (Lista de archivos)
        self.img_pdf_widget = QWidget()
        ip_layout = QVBoxLayout(self.img_pdf_widget)
        ip_layout.setContentsMargins(0, 10, 0, 0)
        
        self.imgs_btn = QPushButton("🖼️ Agregar Imágenes")
        self.imgs_btn.clicked.connect(self.select_images)
        
        self.imgs_list = QListWidget()
        self.imgs_list.setFixedHeight(100)
        
        ip_layout.addWidget(self.imgs_btn)
        ip_layout.addWidget(self.imgs_list)
        
        # Agregar widgets al stack
        self.options_stack.addWidget(self.single_file_widget) # 0: PDF->Word y Word->PDF
        self.options_stack.addWidget(self.pdf_img_widget)    # 1: PDF->Images
        self.options_stack.addWidget(self.img_pdf_widget)    # 2: Images->PDF
        
        self.config_layout.addWidget(self.options_stack)
        
        # Inicializar estado
        self.current_file = None
        self.image_files = []
        
    def on_mode_changed(self, index):
        """Cambia la interfaz según el modo"""
        self.reset_inputs()
        if index == 0: # PDF -> Word
            self.options_stack.setCurrentIndex(0)
            self.file_btn.setText("📄 Seleccionar PDF")
        elif index == 1: # PDF -> Images
            self.options_stack.setCurrentIndex(1)
        elif index == 2: # Images -> PDF
            self.options_stack.setCurrentIndex(2)
        elif index == 3: # Word -> PDF
            self.options_stack.setCurrentIndex(0)
            self.file_btn.setText("📄 Seleccionar Word")

    def reset_inputs(self):
        self.current_file = None
        self.image_files = []
        self.file_label.setText("Ningún archivo seleccionado")
        self.pi_file_label.setText("Ningún archivo seleccionado")
        self.imgs_list.clear()

    def select_single_file(self):
        mode = self.mode_combo.currentIndex()
        if mode == 0 or mode == 1: # PDF input
            file, _ = QFileDialog.getOpenFileName(self, "Seleccionar PDF", "", "PDF (*.pdf)")
        else: # Word input
            file, _ = QFileDialog.getOpenFileName(self, "Seleccionar Word", "", "Word (*.docx)")
            
        if file:
            self.current_file = file
            label = self.file_label if mode == 0 or mode == 3 else self.pi_file_label
            label.setText(f"📄 {os.path.basename(file)}")

    def select_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Imágenes", "", "Imágenes (*.png *.jpg *.jpeg)")
        if files:
            for f in files:
                if f not in self.image_files:
                    self.image_files.append(f)
                    self.imgs_list.addItem(os.path.basename(f))
    
    def start_processing(self):
        mode_idx = self.mode_combo.currentIndex()
        kwargs = {}
        worker_mode = ""
        output_dir = settings.get_output_directory()
        
        if mode_idx == 0: # PDF -> Word
            if not self.current_file: return self.show_error("Selecciona un archivo")
            worker_mode = 'pdf_to_word'
            
            default_name = output_dir / f"{os.path.basename(self.current_file)[:-4]}.docx"
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Guardar como Word", str(default_name), "Word (*.docx)"
            )
            if not output_file: return
            
            self.last_output_file = output_file
            kwargs = {'input_path': self.current_file, 'output_path': output_file}
            
        elif mode_idx == 1: # PDF -> Images
            if not self.current_file: return self.show_error("Selecciona un archivo")
            worker_mode = 'pdf_to_images'
            
            # Para imágenes, pedimos un directorio
            out_dir = QFileDialog.getExistingDirectory(
                self, "Seleccionar Carpeta de Salida", str(output_dir)
            )
            if not out_dir: return
            
            # Crear subcarpeta con nombre del archivo para orden
            folder_name = os.path.basename(self.current_file)[:-4] + "_images"
            final_out_dir = os.path.join(out_dir, folder_name)
            if not os.path.exists(final_out_dir):
                os.makedirs(final_out_dir)
                
            self.last_output_file = final_out_dir
            kwargs = {
                'input_path': self.current_file, 
                'output_dir': final_out_dir,
                'dpi': self.dpi_spin.value(),
                'format': self.format_combo.currentText()
            }
            
        elif mode_idx == 2: # Images -> PDF
            if not self.image_files: return self.show_error("Selecciona imágenes")
            worker_mode = 'images_to_pdf'
            
            default_name = output_dir / "images_combined.pdf"
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Guardar PDF", str(default_name), "PDF (*.pdf)"
            )
            if not output_file: return
            
            self.last_output_file = output_file
            kwargs = {'image_paths': self.image_files, 'output_path': output_file}
            
        elif mode_idx == 3: # Word -> PDF
            if not self.current_file: return self.show_error("Selecciona un archivo")
            worker_mode = 'word_to_pdf'
            
            default_name = output_dir / f"{os.path.basename(self.current_file)[:-5]}.pdf"
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Guardar como PDF", str(default_name), "PDF (*.pdf)"
            )
            if not output_file: return
            
            self.last_output_file = output_file
            kwargs = {'input_path': self.current_file, 'output_path': output_file}

        self.set_processing_state(True)
        self.update_progress(0, "Iniciando conversión...")
        
        self.worker = ConvertWorker(worker_mode, **kwargs)
        self.worker.progress_updated.connect(lambda v: self.update_progress(v))
        self.worker.status_updated.connect(lambda msg: self.update_progress(self.progress_bar.value(), msg))
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_success(self, result):
        self.set_processing_state(False)
        self.show_success(result.get('message', 'Conversión completada'))
        self.show_success_dialog(self.last_output_file, "Conversión Exitosa")

    def on_error(self, error):
        self.set_processing_state(False)
        self.show_error(f"Error: {error}")

    def reset_operation(self):
        self.reset_inputs()
        self.progress_bar.setValue(0)
