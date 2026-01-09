"""
Ventana principal de LocalPDF v5
Contiene la barra lateral de navegación y el área de contenido con las diferentes vistas
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QVBoxLayout
)
import os
from PySide6.QtCore import Qt
from ui.components.sidebar import Sidebar
from ui.components.dashboard import Dashboard
from ui.components.wizard import Wizard
from ui.components.operation_widgets.merge_widget import MergeWidget
from ui.components.operation_widgets.split_widget import SplitWidget
from ui.components.operation_widgets.compress_widget import CompressWidget
from ui.components.operation_widgets.convert_widget import ConvertWidget
from ui.components.operation_widgets.security_widget import SecurityWidget
from ui.components.operation_widgets.ocr_widget import OCRWidget
from ui.components.operation_widgets.batch_widget import BatchWidget
from config.settings import settings


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self, initial_file=None):
        super().__init__()
        self.current_view = 'dashboard'
        self.initial_file = initial_file
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        # Configuración de la ventana
        self.setWindowTitle(f"{settings.APP_NAME} - Editor de PDFs")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal (Sidebar | Contenido)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crear sidebar
        self.sidebar = Sidebar()
        self.sidebar.navigation_requested.connect(self.navigate_to_view)
        
        from ui.components.ui_helpers import FadingStackedWidget
        
        # Crear stacked widget para las vistas
        self.stacked_widget = FadingStackedWidget()
        
        # Crear todas las vistas
        self.views = {
            'dashboard': Dashboard(),
            'wizard': Wizard(),
            'merge': MergeWidget(),
            'split': SplitWidget(),
            'compress': CompressWidget(),
            'convert': ConvertWidget(),
            'security': SecurityWidget(),
            'ocr': OCRWidget(),
            'batch': BatchWidget()
        }
        
        # Conectar señales del dashboard
        self.views['dashboard'].operation_selected.connect(self.navigate_to_view)
        
        # Conectar señales del wizard
        self.views['wizard'].operation_selected.connect(self.navigate_to_view)
        
        # Agregar vistas al stacked widget
        for view_name, view_widget in self.views.items():
            self.stacked_widget.addWidget(view_widget)
        
        # Agregar widgets al layout principal
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget, 1)  # stretch factor 1
        
        # Mostrar vista inicial
        self.navigate_to_view('dashboard')
        
        # Aplicar estilos de fondo - Eliminado para permitir temas globales
        # self.setStyleSheet(...)
        
        if self.initial_file and os.path.exists(self.initial_file):
            if self.initial_file.lower().endswith('.pdf'):
                # Default to Convert widget for PDFs
                target = self.views['convert']
                target.current_file = self.initial_file
                target.file_label.setText(f"📄 {os.path.basename(self.initial_file)}")
                self.navigate_to_view('convert')
    
    def navigate_to_view(self, view_name: str):
        """
        Cambia la vista actual
        
        Args:
            view_name: Nombre de la vista ('dashboard', 'merge', 'split', etc.)
        """
        if view_name in self.views:
            self.current_view = view_name
            self.stacked_widget.setCurrentWidget(self.views[view_name])
            self.sidebar.set_active_item(view_name)
    
    def get_current_view(self) -> str:
        """Retorna el nombre de la vista actual"""
        return self.current_view

    def keyPressEvent(self, event):
        """Manejar atajos globales"""
        from PySide6.QtGui import QKeySequence
        
        # Ctrl+T: Alternar Tema
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_T:
            from ui.styles.theme_manager import theme_manager
            theme_manager.toggle_theme()
            event.accept()
        else:
            super().keyPressEvent(event)
