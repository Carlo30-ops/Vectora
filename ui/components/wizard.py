"""
Wizard - Asistente Inteligente (Rediseño Black/White)
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon
from .ui_helpers import AnimatedCard, IconHelper

class Wizard(QWidget):
    operation_selected = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        # Header
        header = QWidget()
        hl = QVBoxLayout(header)
        hl.setContentsMargins(0,0,0,0)
        hl.setSpacing(8)
        
        t = QLabel("¿Qué quieres hacer hoy?")
        t.setObjectName("labelTitle")
        t.setStyleSheet("font-size: 28px; font-weight: 800; color: #111827;")
        hl.addWidget(t)
        
        s = QLabel("Selecciona una operación para comenzar")
        s.setObjectName("labelSubtitle")
        s.setStyleSheet("font-size: 16px; color: #6b7280;")
        hl.addWidget(s)
        
        layout.addWidget(header)
        
        # Options Grid
        grid = QVBoxLayout()
        grid.setSpacing(16)
        
        options = [
            ("Combinar archivos", "Unir varios PDFs en uno solo", "merge", "combine"),
            ("Extraer páginas", "Separar páginas de un documento", "split", "split"),
            ("Reducir tamaño", "Comprimir archivos para envío", "compress", "minimize-2"),
            ("Convertir formato", "PDF a Word o Imágenes", "convert", "refresh-cw"),
            ("Proteger documento", "Añadir contraseña o permisos", "security", "lock")
        ]
        
        for title, desc, op_id, icon_name in options:
            btn = self.create_option(title, desc, op_id, icon_name)
            grid.addWidget(btn)
            
        layout.addLayout(grid)
        layout.addStretch()
        
    def create_option(self, title, desc, op_id, icon_name):
        btn = AnimatedCard()
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
                padding: 24px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #f9fafb;
                border: 1px solid #000000;
            }
        """)
        
        layout = QHBoxLayout(btn)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(20)
        
        # Icon placeholder
        icon_box = QLabel()
        icon_box.setFixedSize(48, 48)
        icon_box.setStyleSheet("background-color: #f3f4f6; border-radius: 12px;")
        icon_box.setAlignment(Qt.AlignCenter)
        
        icon = IconHelper.get_icon(icon_name)
        if not icon.isNull():
            icon_box.setPixmap(icon.pixmap(24, 24))
            
        layout.addWidget(icon_box)
        
        vl = QVBoxLayout()
        vl.setSpacing(4)
        
        t = QLabel(title)
        t.setFont(QFont("Segoe UI", 14, QFont.Bold))
        t.setStyleSheet("color: #111827; background: transparent; border: none;")
        vl.addWidget(t)
        
        d = QLabel(desc)
        d.setFont(QFont("Segoe UI", 11))
        d.setStyleSheet("color: #6b7280; background: transparent; border: none;")
        vl.addWidget(d)
        
        layout.addLayout(vl)
        layout.addStretch()
        
        arrow = QLabel("→")
        arrow.setFont(QFont("Segoe UI", 20))
        arrow.setStyleSheet("color: #d1d5db; background: transparent; border: none;")
        layout.addWidget(arrow)
        
        btn.clicked.connect(lambda: self.operation_selected.emit(op_id))
        return btn
