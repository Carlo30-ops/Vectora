"""
Widget Base para Operaciones - Rediseño Minimalista
"""
import os
import sys
import subprocess
import time
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QKeySequence, QShortcut
from ..ui_helpers import IconHelper
from utils.history_manager import HistoryManager


class BaseOperationWidget(QWidget):
    """Clase base para operaciones (Rediseñada - Premium Look)"""
    
    def __init__(self, title, description):
        super().__init__()
        self.title = title
        self.description = description
        self.last_output_file = None
        self.start_time = None
        self.init_base_ui()
        
    def init_base_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(60, 50, 60, 60)
        self.main_layout.setSpacing(40)
        
        # Header Container
        header = QFrame()
        header.setStyleSheet("background-color: transparent;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(0,0,0,0)
        hl.setSpacing(28)
        
        # Icon - Glass Container look
        icon_box = QFrame()
        icon_box.setFixedSize(72, 72)
        icon_box.setObjectName("glassContainer")
        icon_box.setStyleSheet("background-color: #000000; border-radius: 20px;")
        
        il = QVBoxLayout(icon_box)
        il.setContentsMargins(0, 0, 0, 0)
        il.setAlignment(Qt.AlignCenter)
        
        self.icon_lbl = QLabel()
        icon = IconHelper.get_icon("layers", color="#FFFFFF")
        if not icon.isNull():
             self.icon_lbl.setPixmap(icon.pixmap(36, 36))
        il.addWidget(self.icon_lbl)
        
        hl.addWidget(icon_box)
        
        vl = QVBoxLayout()
        vl.setSpacing(4)
        
        # Clean title
        clean_title = self.title.replace("📑 ", "").replace("✂️ ", "").replace("🗜️ ", "")
        t = QLabel(clean_title)
        t.setFont(QFont("Inter", 28, QFont.ExtraBold))
        t.setStyleSheet("color: {{TEXT_PRIMARY}}; border: none; letter-spacing: -1px;")
        vl.addWidget(t)
        
        d = QLabel(self.description)
        d.setFont(QFont("Inter", 12))
        d.setStyleSheet("color: {{TEXT_SECONDARY}}; border: none;")
        vl.addWidget(d)
        
        hl.addLayout(vl)
        hl.addStretch()
        
        self.main_layout.addWidget(header)
        
        # Content Area - Con scroll si es necesario
        self.config_layout = QVBoxLayout()
        self.config_layout.setSpacing(24)
        self.main_layout.addLayout(self.config_layout)
        
        # Progress Area
        self.progress_container = QFrame()
        self.progress_container.setObjectName("glassContainer")
        self.progress_container.setStyleSheet("padding: 20px;")
        
        pl = QVBoxLayout(self.progress_container)
        pl.setSpacing(12)
        
        self.progress_label = QLabel("Preparado")
        self.progress_label.setFont(QFont("Inter", 10, QFont.Bold))
        pl.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        pl.addWidget(self.progress_bar)
        
        self.progress_container.setVisible(False)
        self.main_layout.addWidget(self.progress_container)
        
        self.main_layout.addStretch()
        
        # Action Button Area
        button_area = QWidget()
        bl = QHBoxLayout(button_area)
        bl.setContentsMargins(0, 0, 0, 0)
        
        from ..ui_helpers import AnimatedButton
        self.start_btn = AnimatedButton("Iniciar Operación", is_primary=True)
        self.start_btn.setMinimumHeight(60)
        self.start_btn.setMinimumWidth(240)
        self.start_btn.setFont(QFont("Inter", 12, QFont.Bold))
        self.start_btn.clicked.connect(self.start_processing)
        
        bl.addStretch()
        bl.addWidget(self.start_btn)
        
        self.main_layout.addWidget(button_area)
        self.setup_shortcuts()

    def setup_shortcuts(self):
        """Configura atajos de teclado comunes"""
        # Ctrl+Enter para iniciar operación
        self.shortcut_start = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.shortcut_start.activated.connect(self.start_btn.animateClick)
        
        # Ctrl+O para abrir archivo (los hijos deben sobreescribir trigger_file_selection)
        self.shortcut_open = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut_open.activated.connect(self.trigger_file_selection)
        
    def trigger_file_selection(self):
        """Método para ser sobreescrito por hijos para Ctrl+O"""
        pass

    def start_processing(self):
        pass
        
    def set_processing_state(self, processing):
        self.start_btn.setEnabled(not processing)
        self.progress_container.setVisible(True)
        if processing:
            self.start_btn.setText("Procesando...")
            self.start_time = time.time()
        else:
            self.start_btn.setText("Iniciar Operación")
            self.start_time = None
            
    def update_progress(self, value, message=None):
        self.progress_bar.setValue(value)
        
        # Lógica de estimación
        eta_msg = ""
        if self.start_time and value > 0 and value < 100:
            elapsed = time.time() - self.start_time
            # Regla de tres: value % -> elapsed
            # 100 % -> total_time
            total_estimated = elapsed * (100 / value)
            remaining = total_estimated - elapsed
            
            if remaining > 60:
                eta_msg = f" (~{int(remaining/60)} min restantes)"
            else:
                eta_msg = f" (~{int(remaining)} seg restantes)"
        
        base_msg = message if message else f"Procesando... {value}%"
        self.progress_label.setText(f"{base_msg}{eta_msg}")
            
    def show_error(self, message):
        self.progress_label.setText(f"❌ Error: {message}")
        self.progress_label.setStyleSheet("color: #ef4444;") # red-500
        
    def show_success(self, message):
        self.progress_label.setText(f"✅ {message}")
        self.progress_label.setStyleSheet("color: #059669;") # green-600
    
    # === MÉTODOS COMUNES PARA FEEDBACK POST-PROCESAMIENTO ===
    
    def show_success_dialog(self, output_file, title="Operación Exitosa"):
        """
        Muestra diálogo de éxito y GUARDA HISTORIAL
        """
        self.last_output_file = output_file
        
        # Guardar en historial
        try:
            # Intentar obtener input file de varias formas
            input_f = getattr(self, 'current_file', "Multiple Input")
            if not input_f and hasattr(self, 'image_files'):
                input_f = "Imágenes Múltiples"
            elif not input_f and hasattr(self, 'files'): # Batch/merge
                input_f = "Lote de Archivos"
                
            HistoryManager.add_entry(self.title, input_f, output_file)
        except Exception as e:
            print(f"Error guardando historial: {e}")
        
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(f"El archivo se guardó en:\n{output_file}")
        msg.setIcon(QMessageBox.Information)
        
        # Botones personalizados
        open_btn = msg.addButton("Abrir Archivo", QMessageBox.AcceptRole)
        folder_btn = msg.addButton("Abrir Carpeta", QMessageBox.ActionRole)
        close_btn = msg.addButton("Cerrar", QMessageBox.RejectRole)
        
        msg.exec()
        
        clicked = msg.clickedButton()
        if clicked == open_btn:
            self.open_file(output_file)
        elif clicked == folder_btn:
            self.open_folder(output_file)
    
    def open_file(self, file_path):
        """Abre el archivo con la aplicación predeterminada (multiplataforma)"""
        try:
            if sys.platform == 'win32':
                os.startfile(file_path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', file_path])
            else:
                subprocess.run(['xdg-open', file_path])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el archivo: {str(e)}")
    
    def open_folder(self, file_path):
        """Abre la carpeta contenedora y selecciona el archivo (multiplataforma)"""
        try:
            folder = str(Path(file_path).parent)
            if sys.platform == 'win32':
                subprocess.run(['explorer', '/select,', file_path])
            elif sys.platform == 'darwin':
                subprocess.run(['open', '-R', file_path])
            else:
                subprocess.run(['xdg-open', folder])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir la carpeta: {str(e)}")
