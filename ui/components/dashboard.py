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
from utils.history_manager import HistoryManager

class Dashboard(QWidget):
    operation_selected = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.history_layout = None
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
        
        # Historial (Nuevo)
        hist_label = QLabel("Historial Reciente")
        hist_label.setObjectName("labelTitle")
        hist_label.setStyleSheet("font-size: 20px; font-weight: 700; margin-top: 10px; color: #111827;")
        layout.addWidget(hist_label)
        
        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        self.history_layout.setContentsMargins(0,0,0,0)
        self.history_layout.setSpacing(10)
        layout.addWidget(self.history_container)
        
        self.update_history()
        
        # Quick Actions
        actions_label = QLabel("Acciones Rápidas")
        actions_label.setObjectName("labelTitle")
        actions_label.setStyleSheet("font-size: 20px; font-weight: 700; margin-top: 10px; color: #111827;")
        layout.addWidget(actions_label)
        
        grid = self.create_grid()
        layout.addWidget(grid)
        
        # Advanced
        adv_label = QLabel("Características Avanzadas")
        adv_label.setObjectName("labelTitle")
        adv_label.setStyleSheet("font-size: 20px; font-weight: 700; margin-top: 10px; color: #111827;")
        layout.addWidget(adv_label)
        
        # Usar un contenedor horizontal para características avanzadas (Batch + Layout Engine)
        adv_container = QWidget()
        adv_layout = QHBoxLayout(adv_container)
        adv_layout.setContentsMargins(0,0,0,0)
        adv_layout.setSpacing(20)
        
        batch = self.create_batch_card()
        adv_layout.addWidget(batch)
        
        layout_engine = self.create_layout_engine_card()
        adv_layout.addWidget(layout_engine)
        
        layout.addWidget(adv_container)

        layout.addStretch()
        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area)
        
    def showEvent(self, event):
        """Actualizar historial al mostrar"""
        super().showEvent(event)
        self.update_history()
        
    def update_history(self):
        """Carga y muestra el historial"""
        if not self.history_layout: return
        
        # Limpiar
        while self.history_layout.count():
            child = self.history_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        history = HistoryManager.load_history()
        # Mostrar solo los últimos 5
        recent = history[:5]
        
        if not recent:
            lbl = QLabel("No hay operaciones recientes")
            lbl.setStyleSheet("color: #9ca3af; font-style: italic;")
            self.history_layout.addWidget(lbl)
            return

        for item in recent:
            # Simple row: [Time] Operation - File
            row = QFrame()
            row.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #e5e7eb;")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(15, 10, 15, 10)
            
            # Timestamp
            ts = QLabel(item['timestamp'].split(' ')[1]) # Solo hora
            ts.setStyleSheet("color: #6b7280; font-family: monospace;")
            rl.addWidget(ts)
            
            # Op
            op = QLabel(item['operation'])
            op.setStyleSheet("font-weight: bold; color: #111827;")
            rl.addWidget(op)
            
            # File
            fname = "Desconocido"
            if item['input'] != "N/A":
                # Intenta extraer nombre base si es ruta
                fname = item['input'].replace("\\", "/").split("/")[-1]
            
            f = QLabel(fname)
            f.setStyleSheet("color: #4b5563;")
            rl.addWidget(f)
            
            rl.addStretch()
            
            # Status icon
            st = QLabel("✅")
            rl.addWidget(st)
            
            self.history_layout.addWidget(row)

        
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
        # Estilos actualizados para look Premium
        card.setStyleSheet("""
            QPushButton {
                background-color: {{SURFACE_BG}};
                border: 1px solid {{BORDER}};
                border-radius: 20px;
                padding: 24px;
                text-align: left;
            }
            QPushButton:hover {
                border: 1px solid {{ACCENT}};
                background-color: {{HOVER}};
            }
        """)
        
        l = QVBoxLayout(card)
        l.setSpacing(15)
        l.setContentsMargins(0,0,0,0)
        
        # Header con icono y flecha
        hl = QHBoxLayout()
        
        # Icon box - Glass effect
        ibox = QFrame()
        ibox.setFixedSize(50, 50)
        ibox.setObjectName("glassContainer")
        ibox.setStyleSheet(f"background-color: #000000; border-radius: 12px;")
        
        il = QVBoxLayout(ibox)
        il.setContentsMargins(0,0,0,0)
        il.setAlignment(Qt.AlignCenter)
        
        icon_lbl = QLabel()
        icon = IconHelper.get_icon(icon_name, color="#FFFFFF")
        if not icon.isNull():
             icon_lbl.setPixmap(icon.pixmap(24, 24))
        il.addWidget(icon_lbl)
        
        hl.addWidget(ibox)
        hl.addStretch()
        l.addLayout(hl)
        
        # Textos
        vl = QVBoxLayout()
        vl.setSpacing(6)
        
        t = QLabel(title)
        t.setFont(QFont("Inter", 16, QFont.Bold))
        t.setStyleSheet("color: {{TEXT_PRIMARY}}; background: transparent; border: none;")
        vl.addWidget(t)
        
        d = QLabel(desc)
        d.setFont(QFont("Inter", 11))
        d.setStyleSheet("color: {{TEXT_SECONDARY}}; background: transparent; border: none;")
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
        
        icon = IconHelper.get_icon("layers", color="#ffffff") 
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

    def create_layout_engine_card(self):
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
        
        icon = IconHelper.get_icon("layout", color="#ffffff") 
        if not icon.isNull():
            ibox.setPixmap(icon.pixmap(28, 28))
        else:
            # Fallback icon if layout not exists
            icon = IconHelper.get_icon("file-text", color="#ffffff") 
            if not icon.isNull(): ibox.setPixmap(icon.pixmap(28, 28))
            
        l.addWidget(ibox)
        
        vl = QVBoxLayout()
        vl.setSpacing(2)
        t = QLabel("Layout Engine")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet("color: #111827; border: none; background: transparent;")
        vl.addWidget(t)
        
        d = QLabel("Análisis de estructura para conversiones precisas")
        d.setFont(QFont("Segoe UI", 12))
        d.setStyleSheet("color: #6b7280; border: none; background: transparent;")
        vl.addWidget(d)
        
        l.addLayout(vl)
        l.addStretch()
        
        # Info Badge instead of arrow
        badge = QLabel("INFO")
        badge.setStyleSheet("""
            background-color: #eff6ff; color: #3b82f6; 
            padding: 4px 8px; border-radius: 6px; font-weight: bold; font-size: 10px;
        """)
        l.addWidget(badge)
        
        # No action yet, just informative as per spec (it's integrated in Convert)
        # card.clicked.connect(...) 
        return card
