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
        
        # Conectar a cambios de tema
        from ui.styles.theme_manager import theme_manager
        theme_manager.theme_changed.connect(lambda t: self.update_icons())
        
        # Inicializar iconos
        self.update_icons()
    
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
        sep.setStyleSheet("background-color: transparent; max-height: 10px;") # Managed by QSS mostly
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
    
    def update_icons(self):
        """Actualiza el color de los iconos y estilos según el tema actual"""
        from ui.styles.theme_manager import theme_manager
        from ui.styles.themes import THEMES
        
        current_theme = theme_manager.current_theme
        if current_theme not in THEMES: return
        
        theme = THEMES[current_theme]
        color_normal = theme.get('ICON_COLOR', '#6b7280') # Fallback Gray
        color_active = theme.get('ACCENT_TEXT', '#ffffff')
        
        # Colores para estilos inyectados (Failsafe)
        text_primary = theme.get('TEXT_PRIMARY', '#000000')
        text_secondary = theme.get('TEXT_SECONDARY', '#6b7280')
        accent = theme.get('ACCENT', '#000000')
        hover_bg = theme.get('HOVER', '#f3f4f6')
        
        # Actualizar estilo del título
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"color: {text_primary}; font-weight: 800; border: none;")
            
        # Actualizar botón de tema
        if hasattr(self, 'theme_btn'):
            # Lógica invertida: Si estoy en Light, muestro Luna (ir a Dark). Si Dark, Sol.
            icon_name = "moon" if current_theme == "light" else "sun"
            icon = IconHelper.get_icon(icon_name, color=color_normal)
            self.theme_btn.setIcon(icon)
            self.theme_btn.setIconSize(QSize(20, 20))
        
        # Estilo base para botones (inyectado para garantizar visualización)
        btn_style_template = """
            QPushButton {{
                text-align: left;
                padding: 12px 16px;
                border: none;
                border-radius: 12px;
                background-color: transparent;
                color: {text_color};
                font-weight: 500;
                outline: none;
            }}
            QPushButton:hover {{
                background-color: {hover};
                color: {text_hover};
            }}
            QPushButton:checked {{
                background-color: {accent};
                color: {active_text};
                font-weight: 700;
                border: none;
            }}
        """
        
        style_sheet = btn_style_template.format(
            text_color=text_secondary,
            hover=hover_bg,
            text_hover=text_primary,
            accent=accent,
            active_text=color_active
        )
        
        for view_id, btn in self.buttons.items():
            # Aplicar estilo directo
            btn.setStyleSheet(style_sheet)
            
            icon_name = btn.property("icon_name")
            if icon_name:
                # Usar helper para crear icono con estado Normal y Active
                icon = IconHelper.get_icon(icon_name, color=color_normal, active_color=color_active)
                btn.setIcon(icon)
                btn.setIconSize(QSize(20, 20))
                
    def create_header(self) -> QWidget:
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 40, 24, 24)
        header_layout.setSpacing(12)
        
        # Icono Logo - Diseño Premium tipo Glass
        logo_container = QFrame()
        logo_container.setFixedSize(42, 42)
        logo_container.setObjectName("glassContainer")
        logo_container.setStyleSheet("""
            QFrame#glassContainer {
                background-color: #000000;
                border-radius: 12px;
            }
        """)
        
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignCenter)
        
        logo_label = QLabel()
        icon = IconHelper.get_icon("file-text", color="#FFFFFF")
        if not icon.isNull():
            logo_label.setPixmap(icon.pixmap(24, 24))
        else:
            logo_label.setText("V")
            logo_label.setStyleSheet("color: white; font-weight: bold; font-size: 18px;")
        
        logo_layout.addWidget(logo_label)
        header_layout.addWidget(logo_container)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        
        self.title_label = QLabel("VECTORA")
        self.title_label.setObjectName("sidebarTitle")
        self.title_label.setFont(QFont("Inter", 14, QFont.ExtraBold))
        self.title_label.setStyleSheet("letter-spacing: 1px;")
        text_layout.addWidget(self.title_label)
        
        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        
        # Theme Toggle
        from ui.styles.theme_manager import theme_manager
        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(36, 36)
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.setStyleSheet("background: transparent; border-radius: 18px;")
        self.theme_btn.clicked.connect(theme_manager.toggle_theme)
        
        header_layout.addWidget(self.theme_btn)
        
        return header
    
    def create_nav_button(self, view_id: str, label: str, icon_name: str, has_badge: bool = False) -> QPushButton:
        btn = AnimatedButton(label)
        btn.setObjectName("sidebarBtn")
        btn.setProperty("view_id", view_id)
        btn.setProperty("icon_name", icon_name)
        
        btn.setCheckable(True)
        btn.setChecked(view_id == 'dashboard')
        btn.clicked.connect(lambda: self.on_nav_clicked(view_id))
        btn.setFont(QFont("Segoe UI", 10, QFont.Medium))
        btn.setCursor(Qt.PointingHandCursor)
        
        # Styles removed - handled by QSS
        
        if has_badge:
            pass # TODO: Implementar badge visual si es necesario
            
        return btn
        
    def create_footer(self) -> QWidget:
        # (Footer creation remains same, skipping detail here for brevity if replace handles chunks, 
        # but replace targets 5-227 so I must provide full file or correct chunk)
        # Assuming replacement of TOP part and METHODS up to create_footer...
        # Wait, I am replacing practically the whole file except footer implementation details?
        # NO, create_footer logic needs to remain. I'll include it.
        
        footer = QWidget()
        layout = QVBoxLayout(footer)
        layout.setContentsMargins(20, 16, 20, 32)
        
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: transparent; 
                border-radius: 16px; 
                padding: 16px;
                border: 1px solid #e5e7eb;
            }
        """) # Simple override
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
        vl.addWidget(t)
        
        d = QLabel("Privacidad total")
        d.setFont(QFont("Segoe UI", 9))
        d.setStyleSheet("color: #6b7280;") # Keep explicit or use placeholder? Placeholder better but specific file.
        vl.addWidget(d)
        
        l.addLayout(vl)
        l.addStretch()
        
        layout.addWidget(card)
        return footer
        
    def on_nav_clicked(self, view_id: str):
        self.current_view = view_id
        self.navigation_requested.emit(view_id)
    
    def set_active_item(self, view_id: str):
        self.current_view = view_id
        if view_id in self.buttons:
            self.buttons[view_id].setChecked(True)
