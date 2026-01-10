"""
Widget de combinación de PDFs
Permite combinar múltiples archivos PDF en uno solo
"""
import os
import subprocess
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QVBoxLayout, QListWidget, QPushButton, QFileDialog, QHBoxLayout, QLabel, QAbstractItemView, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDesktopServices
from .base_operation import BaseOperationWidget
from backend.services.pdf_merger import PDFMerger
from utils.file_handler import FileHandler
from config.settings import settings
from utils.logger import get_logger

# Configurar logger para este módulo
logger = get_logger(__name__)



class DragDropListWidget(QListWidget):
    """Lista personalizada con soporte completo de drag-and-drop"""
    
    files_dropped = Signal(list)  # Señal cuando se sueltan archivos
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Acepta archivos arrastrados desde el explorador"""
        if event.mimeData().hasUrls():
            # Verificar que sean archivos PDF
            urls = event.mimeData().urls()
            pdf_files = [url.toLocalFile() for url in urls if url.toLocalFile().lower().endswith('.pdf')]
            if pdf_files:
                event.acceptProposedAction()
        else:
            # Permite reordenamiento interno
            super().dragEnterEvent(event)
    
    def dragMoveEvent(self, event):
        """Permite mover durante el arrastre"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)
    
    def dropEvent(self, event: QDropEvent):
        """Maneja archivos soltados"""
        if event.mimeData().hasUrls():
            # Archivos desde el explorador
            urls = event.mimeData().urls()
            files = [url.toLocalFile() for url in urls if url.toLocalFile().lower().endswith('.pdf')]
            if files:
                self.files_dropped.emit(files)
                event.acceptProposedAction()
        else:
            # Reordenamiento interno
            super().dropEvent(event)


class MergeWorker(QThread):
    """Worker thread para combinar PDFs"""
    progress_updated = Signal(int)
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, input_files, output_file):
        super().__init__()
        self.input_files = input_files
        self.output_file = output_file
    
    def run(self):
        try:
            result = PDFMerger.merge_pdfs(
                self.input_files,
                self.output_file,
                progress_callback=self.progress_updated.emit
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MergeWidget(BaseOperationWidget):
    """Widget para combinar PDFs"""
    
    def __init__(self):
        super().__init__(
            "📑 Combinar PDFs",
            "Une múltiples archivos PDF en un solo documento"
        )
        self.files = []
        self.output_file = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz específica - Modern Look"""
        # Cambiar icono de la base
        icon = IconHelper.get_icon("combine", color="#FFFFFF")
        if not icon.isNull():
            self.icon_lbl.setPixmap(icon.pixmap(36, 36))
            
        # Lista de archivos con drag-drop completo - Estilizada como Dropzone
        self.file_list = DragDropListWidget()
        self.file_list.files_dropped.connect(self.on_files_dropped)
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 2px dashed {{BORDER}};
                border-radius: 16px;
                background-color: {{HOVER}};
                padding: 12px;
                min-height: 240px;
                outline: none;
            }
            QListWidget:hover {
                border-color: {{ACCENT}};
            }
        """)
        self.config_layout.addWidget(self.file_list)
        
        # Action Bar para la lista
        action_bar = QHBoxLayout()
        add_btn = QPushButton("+ Agregar PDFs")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: {{ACCENT}};
                border: 1px solid {{ACCENT}};
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: {{ACCENT}};
                color: {{ACCENT_TEXT}};
            }
        """)
        add_btn.clicked.connect(self.add_files)
        
        clear_btn = QPushButton("Limpiar")
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("border: none; color: {{TEXT_SECONDARY}}; font-size: 13px;")
        clear_btn.clicked.connect(self.reset_operation)
        
        action_bar.addWidget(add_btn)
        action_bar.addStretch()
        action_bar.addWidget(clear_btn)
        self.config_layout.addLayout(action_bar)
        
        # Información
        self.info_label = QLabel("Arrastra tus archivos PDF o usa el botón para agregar")
        self.info_label.setFont(QFont("Inter", 10))
        self.info_label.setStyleSheet("color: {{TEXT_SECONDARY}};")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(self.info_label)
    
    def add_files(self):
        """Abre diálogo para seleccionar archivos"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar PDFs",
            str(Path.home()),
            "Archivos PDF (*.pdf)"
        )
        
        if files:
            self.on_files_dropped(files)
    
    def on_files_dropped(self, files):
        """Maneja archivos agregados (por drag-drop o diálogo)"""
        logger.info(f"Archivos recibidos: {len(files)}")
        logger.debug(f"Archivos: {[Path(f).name for f in files]}")
        
        added = 0
        for file in files:
            if file not in self.files:
                self.files.append(file)
                # Extraer nombre del archivo
                filename = file.split('/')[-1].split('\\')[-1]
                self.file_list.addItem(f"📄 {filename}")
                added += 1
                logger.debug(f"Archivo agregado: {filename}")
        
        if added > 0:
            total = len(self.files)
            self.info_label.setText(f"{total} archivo(s) seleccionado(s) - Arrastra para reordenar")
            logger.info(f"Total de archivos en lista: {total} ({added} nuevos)")

    
    def start_processing(self):
        """Inicia la combinación de PDFs"""
        logger.info("Iniciando procesamiento de combinación")
        
        if len(self.files) < 2:
            logger.warning("Validación fallida: menos de 2 archivos seleccionados")
            self.show_error("Necesitas al menos 2 archivos PDF para combinar")
            return
        
        # Preguntar dónde guardar el archivo
        output_dir = settings.get_output_directory()
        default_name = output_dir / "combined.pdf"
        
        logger.debug(f"Abriendo diálogo de guardado - Directorio: {output_dir}")
        
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar PDF Combinado",
            str(default_name),
            "Archivos PDF (*.pdf)"
        )
        
        if not output_file:
            # Usuario canceló
            logger.info("Operación cancelada por el usuario")
            return
        
        self.output_file = output_file
        logger.info(f"Archivo de salida seleccionado: {output_file}")
        
        # Crear y ejecutar worker
        self.set_processing_state(True)
        self.update_progress(0, "Iniciando combinación...")
        
        logger.info("Iniciando worker thread para combinación")
        self.worker = MergeWorker(self.files, self.output_file)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_success(self, result):
        """Maneja el resultado exitoso"""
        logger.info(f"Combinación exitosa: {result.get('message')}")
        logger.info(f"Archivo guardado en: {result.get('output_path')}")
        
        self.set_processing_state(False)
        self.show_success(f"¡PDFs combinados exitosamente!")
        
        # Mostrar diálogo con opciones
        msg = QMessageBox(self)
        msg.setWindowTitle("Operación Exitosa")
        msg.setText(f"El archivo se guardó en:\n{self.output_file}")
        msg.setIcon(QMessageBox.Information)
        
        # Botones personalizados
        open_btn = msg.addButton("Abrir Archivo", QMessageBox.AcceptRole)
        folder_btn = msg.addButton("Abrir Carpeta", QMessageBox.ActionRole)
        close_btn = msg.addButton("Cerrar", QMessageBox.RejectRole)
        
        msg.exec()
        
        clicked = msg.clickedButton()
        if clicked == open_btn:
            logger.info("Usuario eligió abrir el archivo")
            self.open_file(self.output_file)
        elif clicked == folder_btn:
            logger.info("Usuario eligió abrir la carpeta")
            self.open_folder(self.output_file)
    
    def on_error(self, error):
        """Maneja errores"""
        logger.error(f"Error durante la combinación: {error}")
        self.set_processing_state(False)
        self.show_error(f"Error: {error}")

    
    def open_file(self, file_path):
        """Abre el archivo con la aplicación predeterminada"""
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
        """Abre la carpeta contenedora y selecciona el archivo"""
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
    
    def reset_operation(self):
        """Reinicia la operación"""
        self.files = []
        self.output_file = None
        self.file_list.clear()
        self.info_label.setText("Arrastra archivos PDF aquí o usa el botón para agregar")
        self.progress_bar.setValue(0)
