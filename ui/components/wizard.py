"""
Wizard - Asistente Inteligente Conversacional (Vector v5)
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget,
    QGridLayout, QFrame
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap
from .ui_helpers import AnimatedCard, IconHelper, FadingStackedWidget
from ui.styles.themes import THEMES
from ui.styles.theme_manager import theme_manager

# --- Datos del Asistente ---
WIZARD_QUESTIONS = {
    'start': {
        'question': '¿Qué quieres hacer con tus PDFs?',
        'options': [
            {'text': 'Combinar varios archivos', 'desc': 'Unir múltiples PDFs en uno solo', 'icon': 'merge', 'result': 'merge'},
            {'text': 'Separar páginas', 'desc': 'Extraer o dividir un documento', 'icon': 'split', 'result': 'split'},
            {'text': 'Reducir tamaño', 'desc': 'Compresión inteligente', 'icon': 'compress', 'result': 'compress'},
            {'text': 'Convertir formato', 'desc': 'PDF a Word, Imágenes, etc.', 'icon': 'convert', 'next': 'convert'},
            {'text': 'Proteger', 'desc': 'Encriptar con contraseña', 'icon': 'security', 'result': 'security'},
            {'text': 'Reconocer texto (OCR)', 'desc': 'Hacer buscable un escaneado', 'icon': 'ocr', 'result': 'ocr'}
        ]
    },
    'convert': {
        'question': '¿A qué formato quieres convertir?',
        'options': [
            {'text': 'PDF a Word', 'desc': 'Editar documento en Word', 'icon': 'file-text', 'result': 'convert', 'mode': 0}, # 0 = PDF->Word
            {'text': 'PDF a Imágenes', 'desc': 'Extraer páginas como fotos', 'icon': 'image', 'result': 'convert', 'mode': 1}, # 1 = PDF->Img
            {'text': 'Imágenes a PDF', 'desc': 'Crear PDF de fotos', 'icon': 'image', 'result': 'convert', 'mode': 2}, # 2 = Img->PDF
            {'text': 'Word a PDF', 'desc': 'Documento a PDF', 'icon': 'file-text', 'result': 'convert', 'mode': 3}  # 3 = Word->PDF
        ]
    }
}

class Wizard(QWidget):
    operation_selected = Signal(str) # Emite el ID de la operación (ej: 'merge')
    
    def __init__(self):
        super().__init__()
        self.history = [] # Pila de navegación
        self.init_ui()
        
        # Conectar temas
        theme_manager.theme_changed.connect(self.update_theme)
        
        # Iniciar
        self.show_question('start')
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Stack principal con animación
        self.stack = FadingStackedWidget()
        self.layout.addWidget(self.stack)

    def show_question(self, q_id):
        """Crea y muestra una pantalla de pregunta"""
        if q_id not in WIZARD_QUESTIONS: return
        
        data = WIZARD_QUESTIONS[q_id]
        
        # Crear widget contenedor
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        # Header
        header = QWidget()
        hl = QVBoxLayout(header)
        hl.setContentsMargins(0,0,0,0)
        hl.setSpacing(10)
        
        # Botón Atrás (si no es start)
        if q_id != 'start':
            back_btn = QPushButton("← Volver")
            back_btn.setCursor(Qt.PointingHandCursor)
            back_btn.setStyleSheet("border: none; text-align: left; font-size: 14px; color: #6b7280;")
            back_btn.clicked.connect(self.go_back)
            hl.addWidget(back_btn)

        # Título
        title = QLabel(data['question'])
        title.setObjectName("wizardTitle") # ID para theming
        title.setWordWrap(True)
        hl.addWidget(title)
        
        layout.addWidget(header)
        
        # Grid de Opciones
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(20)
        grid.setContentsMargins(0,0,0,0)
        
        # Crear arjetas
        row, col = 0, 0
        for opt in data['options']:
            card = self.create_option_card(opt)
            grid.addWidget(card, row, col)
            
            col += 1
            if col > 1: # 2 columnas
                col = 0
                row += 1
                
        layout.addWidget(grid_widget)
        layout.addStretch()
        
        # Añadir al stack y mostrar
        self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)
        
        # Actualizar tema para este nuevo widget
        self.update_theme(theme_manager.current_theme)

    def create_option_card(self, opt):
        card = AnimatedCard()
        card.setProperty("icon_name", opt.get('icon', 'circle'))
        
        l = QVBoxLayout(card)
        l.setSpacing(15)
        l.setContentsMargins(24, 24, 24, 24)
        
        # Icono
        icon_box = QLabel()
        icon_box.setObjectName("iconBox")
        icon_box.setFixedSize(48, 48)
        icon_box.setAlignment(Qt.AlignCenter)
        l.addWidget(icon_box)
        
        # Textos
        t = QLabel(opt['text'])
        t.setObjectName("optionTitle")
        t.setWordWrap(True)
        l.addWidget(t)
        
        d = QLabel(opt['desc'])
        d.setObjectName("optionDesc")
        d.setWordWrap(True)
        l.addWidget(d)
        
        # Acción
        if 'result' in opt:
            # Si tiene modo específico (ej: convert 0), podríamos pasarlo
            # Por ahora simplificamos navegando a la vista
            card.clicked.connect(lambda: self.finish_wizard(opt['result']))
        elif 'next' in opt:
            card.clicked.connect(lambda: self.next_step(opt['next']))
            
        return card

    def next_step(self, next_q_id):
        self.history.append(self.stack.currentWidget()) # Guardar widget actual para volver?
        # Mejor guardar ID
        # Simplificación: Recreamos widgets, no guardamos estado complejo
        self.show_question(next_q_id)

    def go_back(self):
        # Volver al inicio por ahora (simple)
        self.show_question('start')

    def finish_wizard(self, result_id):
        self.operation_selected.emit(result_id)
        # Resetear wizard para la próxima
        self.show_question('start')

    def update_theme(self, theme_name=None):
        if not theme_name:
            theme_name = theme_manager.current_theme
            
        t = THEMES.get(theme_name, THEMES['light'])
        
        # Colores
        bg_s = t.get('SURFACE_BG', '#ffffff')
        txt_p = t.get('TEXT_PRIMARY', '#111827')
        txt_s = t.get('TEXT_SECONDARY', '#6b7280')
        accent = t.get('ACCENT', '#000000')
        border = t.get('BORDER', '#e5e7eb')
        hover = t.get('HOVER', '#f3f4f6')
        
        # Icon BG logic
        icon_bg = '#f3f4f6' if theme_name == 'light' else '#374151'
        
        # Estilo Global del Widget actual
        current = self.stack.currentWidget()
        if not current: return
        
        # Títulos
        for lbl in current.findChildren(QLabel, "wizardTitle"):
            lbl.setStyleSheet(f"font-size: 32px; font-weight: 800; color: {txt_p};")
            
        # Cards
        card_style = f"""
            QPushButton {{
                background-color: {bg_s};
                border: 1px solid {border};
                border-radius: 20px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {hover};
                border: 1px solid {accent};
                transform: scale(1.02);
            }}
        """
        
        for card in current.findChildren(AnimatedCard):
            card.setStyleSheet(card_style)
            
            # Icon Box
            ibox = card.findChild(QLabel, "iconBox")
            if ibox:
                ibox.setStyleSheet(f"background-color: {icon_bg}; border-radius: 12px;")
                # Update Icon Pixmap
                iname = card.property("icon_name")
                if iname:
                    icon = IconHelper.get_icon(iname, color=txt_p)
                    if not icon.isNull():
                        ibox.setPixmap(icon.pixmap(24, 24))
            
            # Textos
            t_lbl = card.findChild(QLabel, "optionTitle")
            if t_lbl:
                t_lbl.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {txt_p}; border: none; background: transparent;")
                
            d_lbl = card.findChild(QLabel, "optionDesc")
            if d_lbl:
                 d_lbl.setStyleSheet(f"font-size: 14px; color: {txt_s}; border: none; background: transparent;")
