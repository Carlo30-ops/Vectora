"""
Widget de seguridad para PDFs
Permite encriptar, desencriptar y gestionar permisos
"""
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel,
    QLineEdit, QCheckBox, QGroupBox, QRadioButton, QButtonGroup, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal
from .base_operation import BaseOperationWidget
from backend.services.pdf_security import PDFSecurity
from utils.file_handler import FileHandler
from config.settings import settings
import os


class SecurityWorker(QThread):
    """Worker para operaciones de seguridad"""
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, mode, **kwargs):
        super().__init__()
        self.mode = mode
        self.kwargs = kwargs
    
    def run(self):
        try:
            if self.mode == 'encrypt':
                result = PDFSecurity.encrypt_pdf(
                    self.kwargs['input_path'],
                    self.kwargs['output_path'],
                    self.kwargs['password'],
                    self.kwargs['permissions']
                )
            elif self.mode == 'decrypt':
                result = PDFSecurity.decrypt_pdf(
                    self.kwargs['input_path'],
                    self.kwargs['output_path'],
                    self.kwargs['password']
                )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class SecurityWidget(BaseOperationWidget):
    """Widget de seguridad"""
    
    def __init__(self):
        super().__init__(
            "🔒 Seguridad PDF",
            "Protege tus documentos con contraseña y permisos"
        )
        self.current_file = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Selector de archivo
        file_layout = QHBoxLayout()
        self.file_btn = QPushButton("📄 Seleccionar PDF")
        self.file_btn.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_btn)
        
        self.file_label = QLabel("Ningún archivo seleccionado")
        self.file_label.setStyleSheet("color: #6b7280; font-style: italic;")
        file_layout.addWidget(self.file_label, 1)
        self.config_layout.addLayout(file_layout)
        
        # Selección de Modo (Radio Buttons)
        mode_group = QGroupBox("Operación")
        mode_layout = QHBoxLayout()
        self.mode_bg = QButtonGroup()
        
        self.rb_encrypt = QRadioButton("Encriptar (Proteger)")
        self.rb_decrypt = QRadioButton("Desencriptar (Quitar protección)")
        self.rb_encrypt.setChecked(True)
        self.rb_encrypt.toggled.connect(self.toggle_mode)
        
        self.mode_bg.addButton(self.rb_encrypt, 0)
        self.mode_bg.addButton(self.rb_decrypt, 1)
        
        mode_layout.addWidget(self.rb_encrypt)
        mode_layout.addWidget(self.rb_decrypt)
        mode_group.setLayout(mode_layout)
        self.config_layout.addWidget(mode_group)
        
        # --- Área de Contraseña ---
        pwd_group = QGroupBox("Contraseña")
        pwd_layout = QVBoxLayout()
        
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Ingresa la contraseña")
        self.pwd_input.setEchoMode(QLineEdit.Password)
        
        self.pwd_confirm = QLineEdit()
        self.pwd_confirm.setPlaceholderText("Confirma la contraseña")
        self.pwd_confirm.setEchoMode(QLineEdit.Password)
        
        # Toggle visibilidad
        self.show_pwd = QCheckBox("Mostrar contraseña")
        self.show_pwd.stateChanged.connect(self.toggle_pwd_visibility)
        
        pwd_layout.addWidget(self.pwd_input)
        pwd_layout.addWidget(self.pwd_confirm)
        pwd_layout.addWidget(self.show_pwd)
        pwd_group.setLayout(pwd_layout)
        self.config_layout.addWidget(pwd_group)
        
        # --- Área de Permisos (Solo Encriptar) ---
        self.perm_group = QGroupBox("Permisos Permitidos")
        perm_layout = QVBoxLayout()
        
        self.chk_print = QCheckBox("Impresión")
        self.chk_print.setChecked(True)
        self.chk_copy = QCheckBox("Copiar texto/imágenes")
        self.chk_copy.setChecked(True)
        self.chk_modify = QCheckBox("Modificar contenido")
        self.chk_modify.setChecked(False)
        self.chk_notes = QCheckBox("Agregar notas/formularios")
        self.chk_notes.setChecked(True)
        
        perm_layout.addWidget(self.chk_print)
        perm_layout.addWidget(self.chk_copy)
        perm_layout.addWidget(self.chk_modify)
        perm_layout.addWidget(self.chk_notes)
        self.perm_group.setLayout(perm_layout)
        self.config_layout.addWidget(self.perm_group)
        
    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar PDF", "", "PDF (*.pdf)")
        if file:
            self.current_file = file
            self.file_label.setText(os.path.basename(file))
            
    def toggle_mode(self):
        is_encrypt = self.rb_encrypt.isChecked()
        self.perm_group.setVisible(is_encrypt)
        self.pwd_confirm.setVisible(is_encrypt)
        self.start_btn.setText("🔒 Proteger PDF" if is_encrypt else "🔓 Desbloquear PDF")
        
    def toggle_pwd_visibility(self, state):
        mode = QLineEdit.Normal if state == Qt.Checked else QLineEdit.Password
        self.pwd_input.setEchoMode(mode)
        self.pwd_confirm.setEchoMode(mode)
        
    def start_processing(self):
        if not self.current_file:
            return self.show_error("Selecciona un archivo PDF")
            
        pwd = self.pwd_input.text()
        if not pwd:
            return self.show_error("Ingresa una contraseña")
            
        # Preparar argumentos
        kwargs = {}
        mode = 'encrypt' if self.rb_encrypt.isChecked() else 'decrypt'
        
        output_dir = settings.get_output_directory()
        input_name = FileHandler.get_filename(self.current_file)
        
        if mode == 'encrypt':
            if pwd != self.pwd_confirm.text():
                return self.show_error("Las contraseñas no coinciden")
            
            default_name = output_dir / f"protected_{input_name}"
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Guardar PDF Protegido", str(default_name), "PDF (*.pdf)"
            )
            if not output_file: return
            
            self.last_output_file = output_file
            kwargs = {
                'input_path': self.current_file,
                'output_path': output_file,
                'password': pwd,
                'permissions': {
                    'allow_print': self.chk_print.isChecked(),
                    'allow_copy': self.chk_copy.isChecked(),
                    'allow_modify': self.chk_modify.isChecked(),
                    'allow_annotations': self.chk_notes.isChecked()
                }
            }
        else:
            default_name = output_dir / f"unlocked_{input_name}"
            output_file, _ = QFileDialog.getSaveFileName(
                self, "Guardar PDF Desbreloqueado", str(default_name), "PDF (*.pdf)"
            )
            if not output_file: return
            
            self.last_output_file = output_file
            kwargs = {
                'input_path': self.current_file,
                'output_path': output_file,
                'password': pwd
            }
            
        self.set_processing_state(True)
        self.update_progress(0, "Procesando seguridad...")
        
        self.worker = SecurityWorker(mode, **kwargs)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()
        
    def on_success(self, result):
        self.set_processing_state(False)
        self.show_success(result.get('message', 'Operación completada'))
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
