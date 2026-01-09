"""
Barra lateral de navegación - Diseño Minimalista
Paleta: Negro, Gris, Blanco
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QButtonGroup, QAbstractButton
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QIcon
from .ui_helpers import IconHelper, AnimatedButton

class Sidebar(QWidget):
    """Barra lateral de navegación con diseño minimalista"""
    
    navigation_requested = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.current_view = 'dashboard'
        self.buttons = {}
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        self.setFixedWidth(280)
        self.setObjectName("sidebar")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # === HEADER ===
        header = self.create_header()
        layout.addWidget(header)
        
        # Separator (invisible spacer or subtle line)
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #f3f4f6; max-height: 1px; margin: 0 20px;")
        layout.addWidget(sep)
        
        # === NAVEGACIÓN ===
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(16, 24, 16, 16)
        nav_layout.setSpacing(8)
        
        # Items: (id, label, icon_name, has_badge)
        menu_items = [
            ('dashboard', 'Dashboard', 'layout-dashboard', False),
            ('wizard', 'Asistente', 'wand-2', True),
            ('merge', 'Combinar', 'combine', False),
            ('split', 'Dividir', 'split', False),
            ('compress', 'Comprimir', 'minimize-2', False),
            ('convert', 'Convertir', 'refresh-cw', False),
            ('security', 'Seguridad', 'lock', False),
            ('ocr', 'OCR', 'scan-text', False),
            ('batch', 'Lotes', 'layers', False),
        ]
        
        for item in menu_items:
            view_id, label, icon_name, has_badge = item
            btn = self.create_nav_button(view_id, label, icon_name, has_badge)
            self.buttons[view_id] = btn
            self.btn_group.addButton(btn)
            nav_layout.addWidget(btn)
        
        nav_layout.addStretch()
        layout.addWidget(nav_container)
        
        # === FOOTER ===
        footer = self.create_footer()
        layout.addWidget(footer)
        
        self.setStyleSheet("""
            QWidget#sidebar {
                background-color: #ffffff;
                border-right: 1px solid #e5e7eb;
            }
        """)
    
    def create_header(self) -> QWidget:
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 32, 24, 24)
        header_layout.setSpacing(12)
        
        # Icono Logo
        logo_label = QLabel()
        logo_label.setFixedSize(40, 40)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("background-color: #000000; border-radius: 10px;")
        
        # Intentar cargar icono blanco
        icon = IconHelper.get_icon("file-text", color="#ffffff")
        if not icon.isNull():
            logo_label.setPixmap(icon.pixmap(24, 24))
        else:
             logo_label.setText("V") 
             logo_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
             logo_label.setStyleSheet("color: white; background-color: black; border-radius: 10px;")

        header_layout.addWidget(logo_label)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        text_layout.setContentsMargins(0, 4, 0, 4)
        
        title = QLabel("Vectora")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #111827; border: none; background: transparent;")
        text_layout.addWidget(title)
        
        # version = QLabel("v5.0")
        # version.setFont(QFont("Segoe UI", 10))
        # version.setStyleSheet("color: #9ca3af; border: none; background: transparent;")
        # text_layout.addWidget(version)
        
        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        
        return header
    
    def create_nav_button(self, view_id: str, label: str, icon_name: str, has_badge: bool = False) -> QPushButton:
        btn = AnimatedButton(label)
        btn.setCheckable(True)
        btn.setChecked(view_id == 'dashboard')
        btn.clicked.connect(lambda: self.on_nav_clicked(view_id))
        btn.setFont(QFont("Segoe UI", 10, QFont.Medium))
        btn.setCursor(Qt.PointingHandCursor)
        
        # Icono
        # Use dark gray for icons to contrast with white background
        icon = IconHelper.get_icon(icon_name, color="#4b5563") 
        if not icon.isNull():
            btn.setIcon(icon)
            btn.setIconSize(QSize(20, 20))
        
        # Estilo
        # Usamos CSS para manejar active states vs hover
        btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 12px 16px;
                border: none;
                border-radius: 12px;
                background-color: transparent;
                color: #4b5563; /* gray-600 */
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #f9fafb;
                color: #111827;
            }}
            QPushButton:checked {{
                background-color: #f3f4f6; /* gray-100 */
                color: #000000;
                font-weight: 700;
            }}
        """)
        
        if has_badge:
            pass # TODO: Implementar badge visual si es necesario
            
        return btn
        
    def create_footer(self) -> QWidget:
        footer = QWidget()
        layout = QVBoxLayout(footer)
        layout.setContentsMargins(20, 16, 20, 32)
        
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #f9fafb; 
                border-radius: 16px; 
                padding: 16px;
                border: 1px solid #f3f4f6;
            }
        """)
        l = QHBoxLayout(card)
        l.setSpacing(12)
        l.setContentsMargins(0,0,0,0)
        
        icon_box = QLabel()
        icon_box.setFixedSize(32, 32)
        icon_box.setStyleSheet("background-color: #e5e7eb; border-radius: 8px;")
        icon_box.setAlignment(Qt.AlignCenter)
        shield = IconHelper.get_icon("shield")
        if not shield.isNull():
            icon_box.setPixmap(shield.pixmap(16, 16))
        l.addWidget(icon_box)
        
        vl = QVBoxLayout()
        vl.setSpacing(2)
        t = QLabel("100% Offline")
        t.setFont(QFont("Segoe UI", 9, QFont.Bold))
        t.setStyleSheet("color: #111827; border:none;")
        vl.addWidget(t)
        
        d = QLabel("Privacidad total")
        d.setFont(QFont("Segoe UI", 9))
        d.setStyleSheet("color: #6b7280; border:none;")
        vl.addWidget(d)
        
        l.addLayout(vl)
        l.addStretch()
        
        layout.addWidget(card)
        return footer
        
    def on_nav_clicked(self, view_id: str):
        self.current_view = view_id
        # Force styles update if needed, but QButtonGroup handles exclusion
        self.navigation_requested.emit(view_id)
    
    def set_active_item(self, view_id: str):
        self.current_view = view_id
        if view_id in self.buttons:
            self.buttons[view_id].setChecked(True)
