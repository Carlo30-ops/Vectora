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
            
            # Instanciar servicio
            converter = PDFConverter()

            if self.mode == 'pdf_to_word':
                result = converter.pdf_to_word(
                    self.kwargs['input_path'],
                    self.kwargs['output_path'],
                    progress_callback=progress_callback
                )
            elif self.mode == 'pdf_to_images':
                result = converter.pdf_to_images(
                    self.kwargs['input_path'],
                    self.kwargs['output_dir'],
                    dpi=self.kwargs['dpi'],
                    image_format=self.kwargs['format'],
                    progress_callback=lambda v: self.progress_updated.emit(v)
                )
            elif self.mode == 'images_to_pdf':
                result = converter.images_to_pdf(
                    self.kwargs['image_paths'],
                    self.kwargs['output_path'],
                    progress_callback=lambda v: self.progress_updated.emit(v)
                )
            elif self.mode == 'word_to_pdf':
                result = converter.word_to_pdf(
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
        """Configura la interfaz - Look Premium"""
        # Cambiar icono de la base
        icon = IconHelper.get_icon("refresh-cw", color="#FFFFFF")
        if not icon.isNull():
            self.icon_lbl.setPixmap(icon.pixmap(36, 36))
            
        # Global Mode Selector
        mode_panel = QFrame()
        mode_panel.setObjectName("glassContainer")
        mode_panel.setStyleSheet("padding: 16px;")
        mpl = QHBoxLayout(mode_panel)
        
        mode_lbl = QLabel("Seleccione modo")
        mode_lbl.setFont(QFont("Inter", 11, QFont.Bold))
        mpl.addWidget(mode_lbl)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "PDF a Word (.docx)",
            "PDF a Imágenes",
            "Imágenes a PDF",
            "Word a PDF"
        ])
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        mpl.addWidget(self.mode_combo, 1)
        self.config_layout.addWidget(mode_panel)
        
        # Área dinámica de configuración
        self.options_stack = QStackedWidget()
        
        # 1. Single File Dropzone (PDF->Word, Word->PDF)
        self.single_file_widget = QWidget()
        sf_layout = QVBoxLayout(self.single_file_widget)
        sf_layout.setContentsMargins(0, 0, 0, 0)
        
        self.sf_dropzone = QFrame()
        self.sf_dropzone.setObjectName("glassContainer")
        self.sf_dropzone.setMinimumHeight(150)
        self.sf_dropzone.setStyleSheet("border: 2px dashed {{BORDER}}; background-color: {{HOVER}};")
        
        dzl = QVBoxLayout(self.sf_dropzone)
        dzl.setAlignment(Qt.AlignCenter)
        
        self.file_label = QLabel("Arrastra tu archivo aquí para comenzar")
        self.file_label.setFont(QFont("Inter", 11))
        self.file_label.setStyleSheet("color: {{TEXT_SECONDARY}};")
        dzl.addWidget(self.file_label)
        
        self.file_btn = QPushButton("Seleccionar Archivo")
        self.file_btn.setCursor(Qt.PointingHandCursor)
        self.file_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: {{ACCENT}};
                border: 1px solid {{ACCENT}};
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: {{ACCENT}}; color: {{ACCENT_TEXT}}; }
        """)
        self.file_btn.clicked.connect(self.select_single_file)
        dzl.addWidget(self.file_btn, 0, Qt.AlignCenter)
        sf_layout.addWidget(self.sf_dropzone)
        
        # 2. PDF to Images (DPI, Format)
        self.pdf_img_widget = QWidget()
        pi_layout = QVBoxLayout(self.pdf_img_widget)
        pi_layout.setContentsMargins(0, 0, 0, 0)
        pi_layout.setSpacing(16)
        
        # Reusamos dropzone visualmente (solo info)
        self.pi_info_box = QFrame()
        self.pi_info_box.setObjectName("glassContainer")
        self.pi_info_box.setStyleSheet("border: 2px dashed {{BORDER}}; background-color: {{HOVER}}; padding: 20px;")
        pil = QVBoxLayout(self.pi_info_box)
        pil.setAlignment(Qt.AlignCenter)
        
        self.pi_file_label = QLabel("PDF para extraer imágenes")
        self.pi_file_label.setFont(QFont("Inter", 11))
        self.pi_file_label.setStyleSheet("color: {{TEXT_SECONDARY}};")
        pil.addWidget(self.pi_file_label)
        
        self.pi_file_btn = QPushButton("Cargar PDF")
        self.pi_file_btn.setCursor(Qt.PointingHandCursor)
        self.pi_file_btn.setStyleSheet("background: transparent; border: 1px solid {{ACCENT}}; color: {{ACCENT}}; border-radius: 8px; padding: 6px 16px;")
        self.pi_file_btn.clicked.connect(self.select_single_file)
        pil.addWidget(self.pi_file_btn, 0, Qt.AlignCenter)
        pi_layout.addWidget(self.pi_info_box)
        
        # Quality Settings
        pi_opts = QFrame()
        pi_opts.setObjectName("glassContainer")
        pi_opts.setStyleSheet("padding: 16px;")
        phol = QHBoxLayout(pi_opts)
        
        phol.addWidget(QLabel("DPI"))
        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(72, 600)
        self.dpi_spin.setValue(150)
        phol.addWidget(self.dpi_spin)
        
        phol.addSpacing(20)
        phol.addWidget(QLabel("Formato"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPEG"])
        phol.addWidget(self.format_combo)
        pi_layout.addWidget(pi_opts)
        
        # 3. Images to PDF (List)
        self.img_pdf_widget = QWidget()
        ip_layout = QVBoxLayout(self.img_pdf_widget)
        ip_layout.setContentsMargins(0, 0, 0, 0)
        ip_layout.setSpacing(16)
        
        self.imgs_btn = QPushButton("+ Agregar Imágenes")
        self.imgs_btn.setCursor(Qt.PointingHandCursor)
        self.imgs_btn.setStyleSheet("background: transparent; border: 1px solid {{ACCENT}}; color: {{ACCENT}}; border-radius: 10px; padding: 10px 20px; font-weight: 600;")
        self.imgs_btn.clicked.connect(self.select_images)
        ip_layout.addWidget(self.imgs_btn)
        
        self.imgs_list = QListWidget()
        self.imgs_list.setStyleSheet("border-radius: 12px; border: 1px solid {{BORDER}}; padding: 8px;")
        self.imgs_list.setFixedHeight(140)
        ip_layout.addWidget(self.imgs_list)
        
        # Agregar widgets al stack
        self.options_stack.addWidget(self.single_file_widget) 
        self.options_stack.addWidget(self.pdf_img_widget)    
        self.options_stack.addWidget(self.img_pdf_widget)    
        
        self.config_layout.addWidget(self.options_stack)
        
        self.current_file = None
        self.image_files = []
        
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
