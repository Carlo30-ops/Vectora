"""
Dashboard - Diseño Minimalista Negro/Gris/Blanco
Pantalla principal con accesos rápidos
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap
from .ui_helpers import IconHelper, AnimatedCard

class Dashboard(QWidget):
    operation_selected = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background: transparent;")
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(40)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Wizard Card
        wizard = self.create_wizard_card()
        layout.addWidget(wizard)
        
        # Quick Actions
        actions_label = QLabel("Acciones Rápidas")
        actions_label.setObjectName("labelTitle")
        actions_label.setStyleSheet("font-size: 20px; font-weight: 700; margin-top: 10px;")
        layout.addWidget(actions_label)
        
        grid = self.create_grid()
        layout.addWidget(grid)
        
        # Advanced
        adv_label = QLabel("Características Avanzadas")
        adv_label.setObjectName("labelTitle")
        adv_label.setStyleSheet("font-size: 20px; font-weight: 700; margin-top: 10px;")
        layout.addWidget(adv_label)
        
        # Usar un contenedor para el card de batch para evitar que se estire demasiado
        batch_container = QWidget()
        batch_layout = QHBoxLayout(batch_container)
        batch_layout.setContentsMargins(0,0,0,0)
        batch = self.create_batch_card()
        batch_layout.addWidget(batch)
        layout.addWidget(batch_container)

        layout.addStretch()
        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area)
        
    def create_header(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0,0,0,0)
        l.setSpacing(8)
        
        t = QLabel("Bienvenido a Vectora")
        t.setObjectName("labelTitle")
        # El estilo ya está en QSS, pero podemos forzar overrides si es necesario
        l.addWidget(t)
        
        s = QLabel("Herramienta profesional para manipulación de PDFs")
        s.setObjectName("labelSubtitle")
        l.addWidget(s)
        return w
        
    def create_wizard_card(self):
        card = AnimatedCard()
        card.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                border: 1px solid #000000;
                border-radius: 20px;
                padding: 30px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #111827;
            }
        """)
        
        l = QHBoxLayout(card)
        l.setSpacing(25)
        
        # Icon
        icon_box = QLabel()
        icon_box.setFixedSize(64, 64)
        icon_box.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1); 
            border-radius: 16px;
        """)
        icon_box.setAlignment(Qt.AlignCenter)
        
        # Icono wand en blanco
        icon = IconHelper.get_icon("wand-2", color="#ffffff")
        if not icon.isNull():
            icon_box.setPixmap(icon.pixmap(32, 32))
        
        l.addWidget(icon_box)
        
        vl = QVBoxLayout()
        vl.setSpacing(4)
        
        t = QLabel("Asistente Inteligente")
        t.setFont(QFont("Segoe UI", 22, QFont.Bold))
        t.setStyleSheet("color: white; background: transparent; border: none;")
        vl.addWidget(t)
        
        d = QLabel("Déjanos ayudarte a elegir la mejor operación para tus archivos")
        d.setFont(QFont("Segoe UI", 13))
        d.setStyleSheet("color: #9ca3af; background: transparent; border: none;")
        vl.addWidget(d)
        
        l.addLayout(vl)
        l.addStretch()
        
        arrow = QLabel("→")
        arrow.setFont(QFont("Segoe UI", 28))
        arrow.setStyleSheet("color: white; background: transparent; border: none;")
        l.addWidget(arrow)
        
        card.clicked.connect(lambda: self.operation_selected.emit("wizard"))
        return card

    def create_grid(self):
        w = QWidget()
        g = QGridLayout(w)
        g.setSpacing(20)
        g.setContentsMargins(0,0,0,0)
        
        ops = [
            ('merge', 'Combinar', 'combine', 'Unir varios archivos'),
            ('split', 'Dividir', 'split', 'Separar páginas'),
            ('compress', 'Comprimir', 'compress', 'Reducir tamaño'),
            ('convert', 'Convertir', 'convert', 'Cambiar formato'),
            ('security', 'Seguridad', 'security', 'Proteger/Desbloquear'),
            ('ocr', 'OCR', 'ocr', 'Reconocimiento texto'),
        ]
        
        row, col = 0, 0
        for pid, title, icon_name, desc in ops:
            card = self.create_card(pid, title, icon_name, desc)
            g.addWidget(card, row, col)
            col += 1
            if col > 2: # 3 columnas
                col = 0
                row += 1
        return w
        
    def create_card(self, pid, title, icon_name, desc):
        card = AnimatedCard()
        card.setObjectName("dashboardCard")
        # Estilos específicos para cards del dashboard se pueden poner aquí o en QSS
        # Usamos estilos inline para asegurar la personalización sin conflictos globales
        card.setStyleSheet("""
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
        
        l = QVBoxLayout(card)
        l.setSpacing(15)
        l.setContentsMargins(0,0,0,0)
        
        # Header con icono y flecha (invisible por defecto en hover quizas?)
        hl = QHBoxLayout()
        
        # Icon box
        ibox = QLabel()
        ibox.setFixedSize(50, 50)
        ibox.setStyleSheet("background-color: #f3f4f6; border-radius: 12px;")
        ibox.setAlignment(Qt.AlignCenter)
        
        # Force Black icon
        icon = IconHelper.get_icon(icon_name, color="#000000")
        if not icon.isNull():
             ibox.setPixmap(icon.pixmap(24, 24))
        
        hl.addWidget(ibox)
        hl.addStretch()
        l.addLayout(hl)
        
        # Textos
        vl = QVBoxLayout()
        vl.setSpacing(4)
        
        t = QLabel(title)
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet("color: #111827; background: transparent; border: none;")
        t.setWordWrap(True)
        vl.addWidget(t)
        
        d = QLabel(desc)
        d.setFont(QFont("Segoe UI", 11))
        d.setStyleSheet("color: #6b7280; background: transparent; border: none;")
        d.setWordWrap(True)
        vl.addWidget(d)
        
        l.addLayout(vl)
        
        card.clicked.connect(lambda chk=False, p=pid: self.operation_selected.emit(p))
        return card
        
    def create_batch_card(self):
        card = AnimatedCard()
        card.setStyleSheet("""
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
        
        l = QHBoxLayout(card)
        l.setSpacing(20)
        
        ibox = QLabel()
        ibox.setFixedSize(56, 56)
        ibox.setStyleSheet("background-color: #111827; border-radius: 12px;")
        ibox.setAlignment(Qt.AlignCenter)
        
        icon = IconHelper.get_icon("layers", color="#ffffff") # Icono layers/batch (keep white on black bg)
        if not icon.isNull():
            ibox.setPixmap(icon.pixmap(28, 28))
            
        l.addWidget(ibox)
        
        vl = QVBoxLayout()
        vl.setSpacing(2)
        t = QLabel("Procesamiento por Lotes")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet("color: #111827; border: none; background: transparent;")
        vl.addWidget(t)
        
        d = QLabel("Automatiza tareas múltiples en una sola ejecución")
        d.setFont(QFont("Segoe UI", 12))
        d.setStyleSheet("color: #6b7280; border: none; background: transparent;")
        vl.addWidget(d)
        
        l.addLayout(vl)
        l.addStretch()
        
        # Arrow
        arrow = QLabel("→")
        arrow.setFont(QFont("Segoe UI", 20))
        arrow.setStyleSheet("color: #d1d5db; background: transparent; border: none;")
        l.addWidget(arrow)
        
        card.clicked.connect(lambda: self.operation_selected.emit("batch"))
        return card
