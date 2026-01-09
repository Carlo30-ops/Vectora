"""
Widget Base para Operaciones - Rediseño Minimalista
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from ..ui_helpers import IconHelper

class BaseOperationWidget(QWidget):
    """Clase base para operaciones (Rediseñada)"""
    
    def __init__(self, title, description):
        super().__init__()
        self.title = title
        self.description = description
        self.init_base_ui()
        
    def init_base_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(50, 40, 50, 50)
        self.main_layout.setSpacing(32)
        
        # Header Container
        header = QFrame()
        header.setStyleSheet("background-color: transparent;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(0,0,0,0)
        hl.setSpacing(24)
        
        # Icon
        icon_box = QLabel()
        icon_box.setFixedSize(64, 64)
        icon_box.setStyleSheet("background-color: #000000; border-radius: 18px;")
        icon_box.setAlignment(Qt.AlignCenter)
        
        # Icono visual, puede ser overwriteado por hijos
        icon = IconHelper.get_icon("layers", color="#ffffff") # Default fallback
        if not icon.isNull():
             icon_box.setPixmap(icon.pixmap(32, 32))
        
        hl.addWidget(icon_box)
        
        vl = QVBoxLayout()
        vl.setSpacing(6)
        
        # Clean title
        clean_title = self.title.replace("📑 ", "").replace("✂️ ", "").replace("🗜️ ", "")
        t = QLabel(clean_title)
        t.setFont(QFont("Segoe UI", 26, QFont.Bold))
        t.setStyleSheet("color: #111827; border: none;")
        vl.addWidget(t)
        
        d = QLabel(self.description)
        d.setFont(QFont("Segoe UI", 12))
        d.setStyleSheet("color: #6b7280; border: none;")
        vl.addWidget(d)
        
        hl.addLayout(vl)
        hl.addStretch()
        
        self.main_layout.addWidget(header)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #e5e7eb; max-height: 1px;")
        self.main_layout.addWidget(line)
        
        # Content Area
        self.config_layout = QVBoxLayout()
        self.config_layout.setSpacing(20)
        self.main_layout.addLayout(self.config_layout)
        
        # Progress
        self.progress_container = QWidget()
        pl = QVBoxLayout(self.progress_container)
        pl.setContentsMargins(0, 20, 0, 0)
        pl.setSpacing(10)
        
        self.progress_label = QLabel("Preparado")
        self.progress_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        pl.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        # Apply updated styling
        # self.progress_bar.setStyleSheet(...) # Already global or updated here
        pl.addWidget(self.progress_bar)
        
        self.progress_container.setVisible(False)
        self.main_layout.addWidget(self.progress_container)
        
        self.main_layout.addStretch()
        
        # Action Button Area
        button_area = QWidget()
        bl = QHBoxLayout(button_area)
        bl.setContentsMargins(0, 20, 0, 0)
        
        from ..ui_helpers import AnimatedButton
        self.start_btn = AnimatedButton("Iniciar Operación", is_primary=True)
        self.start_btn.setMinimumHeight(56)
        self.start_btn.setMinimumWidth(200)
        self.start_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.start_btn.clicked.connect(self.start_processing)
        
        bl.addStretch()
        bl.addWidget(self.start_btn)
        
        self.main_layout.addWidget(button_area)

    def start_processing(self):
        pass
        
    def set_processing_state(self, processing):
        self.start_btn.setEnabled(not processing)
        self.progress_container.setVisible(True)
        if processing:
            self.start_btn.setText("Procesando...")
        else:
            self.start_btn.setText("Iniciar Operación")
            
    def update_progress(self, value, message=None):
        self.progress_bar.setValue(value)
        if message:
            self.progress_label.setText(message)
            
    def show_error(self, message):
        self.progress_label.setText(f"❌ Error: {message}")
        self.progress_label.setStyleSheet("color: #ef4444;") # red-500
        
    def show_success(self, message):
        self.progress_label.setText(f"✅ {message}")
        self.progress_label.setStyleSheet("color: #059669;") # green-600
