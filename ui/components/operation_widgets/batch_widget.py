"""
Widget de procesamiento por lotes
Aplica una operación a múltiples archivos
"""

import os

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QSlider,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from backend.services.batch_processor import BatchProcessor
from backend.services.pdf_compressor import PDFCompressor
from backend.services.pdf_converter import PDFConverter
from backend.services.pdf_security import PDFSecurity
from config.settings import settings

from .base_operation import BaseOperationWidget


class BatchWorker(QThread):
    """Worker para procesamiento por lotes"""

    progress_updated = Signal(int)
    item_processed = Signal(str, bool)  # file, success
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, operation_type, files, config, output_dir=None):
        super().__init__()
        self.op_type = operation_type
        self.files = files
        self.config = config
        self.output_dir = output_dir or str(settings.OUTPUT_DIR / "batch")

    def run(self):
        try:
            func = None
            kw_config = {}

            # Mapear operación a función y config
            if self.op_type == "Comprimir PDF":
                func = PDFCompressor.compress_pdf
                kw_config = {"quality_level": self.config["quality"]}

            elif self.op_type == "PDF a Word":
                func = PDFConverter.pdf_to_word

            elif self.op_type == "Word a PDF":
                func = PDFConverter.word_to_pdf

            elif self.op_type == "Encriptar":
                func = PDFSecurity.encrypt_pdf
                kw_config = {"password": self.config["password"]}

            elif self.op_type == "Desencriptar":
                func = PDFSecurity.decrypt_pdf
                kw_config = {"password": self.config["password"]}

            # Callback para BatchProcessor
            def batch_callback(p, msg, res):
                self.progress_updated.emit(p)
                self.item_processed.emit(res["file"], res["success"])

            # Ejecutar
            result = BatchProcessor.process_batch(
                self.files, func, kw_config, str(self.output_dir), progress_callback=batch_callback
            )
            self.finished.emit(result)

        except Exception as e:
            self.error.emit(str(e))


class BatchWidget(BaseOperationWidget):
    """Widget de procesamiento por lotes"""

    file_detected = Signal(str)

    def __init__(self):
        super().__init__(
            "⚡ Procesamiento por Lotes", "Aplica la misma operación a múltiples archivos a la vez"
        )
        self.files = []
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz - Look Premium"""
        # Cambiar icono de la base
        icon = IconHelper.get_icon("zap", color="#FFFFFF")
        if not icon.isNull():
            self.icon_lbl.setPixmap(icon.pixmap(36, 36))

        # Top Panel: Files & Operation Select
        top_panel = QFrame()
        top_panel.setObjectName("glassContainer")
        top_panel.setStyleSheet("padding: 24px;")
        tpl = QVBoxLayout(top_panel)
        tpl.setSpacing(16)

        # Files Header
        fl = QHBoxLayout()
        f_title = QLabel("Archivos en el lote")
        f_title.setFont(QFont("Inter", 11, QFont.Bold))
        fl.addWidget(f_title)
        fl.addStretch()

        add_btn = QPushButton("+ Agregar")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet(
            "color: {{ACCENT}}; font-weight: 600; border: none; background: transparent;"
        )
        add_btn.clicked.connect(self.add_files)
        fl.addWidget(add_btn)

        clear_btn = QPushButton("Limpiar")
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet(
            "color: {{TEXT_SECONDARY}}; font-size: 13px; border: none; background: transparent;"
        )
        clear_btn.clicked.connect(self.clear_files)
        fl.addWidget(clear_btn)
        tpl.addLayout(fl)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet(
            "border-radius: 12px; border: 1px solid {{BORDER}}; padding: 8px;"
        )
        self.file_list.setFixedHeight(120)
        tpl.addWidget(self.file_list)

        # Operation Selector
        tpl.addSpacing(10)
        tpl.addWidget(QLabel("Operación a realizar"))
        self.op_combo = QComboBox()
        self.op_combo.addItems(
            ["Comprimir PDF", "PDF a Word", "Word a PDF", "Encriptar", "Desencriptar"]
        )
        self.op_combo.currentIndexChanged.connect(self.on_op_changed)
        tpl.addWidget(self.op_combo)

        self.config_layout.addWidget(top_panel)

        # Config Area - Stacked
        self.config_stack = QStackedWidget()

        # 0. Config Compresión
        self.compress_config = QFrame()
        self.compress_config.setObjectName("glassContainer")
        self.compress_config.setStyleSheet("padding: 16px;")
        c_layout = QVBoxLayout(self.compress_config)
        c_layout.addWidget(QLabel("Nivel de compresión"))
        self.c_slider = QSlider(Qt.Horizontal)
        self.c_slider.setRange(0, 100)
        self.c_slider.setValue(50)
        c_layout.addWidget(self.c_slider)
        self.config_stack.addWidget(self.compress_config)

        # 1 y 2. Sin config
        self.empty_config = QWidget()
        self.config_stack.addWidget(self.empty_config)

        # 3. Config Seguridad
        self.sec_config = QFrame()
        self.sec_config.setObjectName("glassContainer")
        self.sec_config.setStyleSheet("padding: 16px;")
        s_layout = QVBoxLayout(self.sec_config)
        s_layout.addWidget(QLabel("Contraseña maestra"))
        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setPlaceholderText("Se usará para todos los archivos")
        s_layout.addWidget(self.pwd_input)
        self.config_stack.addWidget(self.sec_config)

        self.config_layout.addWidget(self.config_stack)

        # Automation Panel
        auto_panel = QFrame()
        auto_panel.setObjectName("glassContainer")
        auto_panel.setStyleSheet(
            f"background-color: {{HOVER}}; padding: 16px; border: 1px dashed {{BORDER}};"
        )
        al = QHBoxLayout(auto_panel)

        self.watch_btn = QPushButton("👁️ Activar Carpeta Vigilada")
        self.watch_btn.setCheckable(True)
        self.watch_btn.setCursor(Qt.PointingHandCursor)
        self.watch_btn.setStyleSheet(
            """
            QPushButton { background: transparent; color: {{TEXT_PRIMARY}}; border-radius: 8px; padding: 8px 16px; }
            QPushButton:checked { background-color: {{SUCCESS}}; color: white; }
        """
        )
        self.watch_btn.clicked.connect(self.toggle_watch)
        al.addWidget(self.watch_btn)

        self.watch_status = QLabel("Modo pasivo")
        self.watch_status.setFont(QFont("Inter", 9))
        self.watch_status.setStyleSheet("color: {{TEXT_SECONDARY}};")
        al.addWidget(self.watch_status)
        al.addStretch()

        self.config_layout.addWidget(auto_panel)

        # Inicializar vista de config
        self.on_op_changed(0)

        # Signals
        self.file_detected.connect(self.process_new_file)

        # Watcher Service
        from backend.services.pdf_watcher import PDFWatchService

        self.watcher = PDFWatchService()

    # Define signal outside init (class level) but dynamically bound inside
    # Wait, Signals must be class attributes.
    # To fix this without re-writing the whole class header, we add the attribute dynamically
    # BUT PySide Signal must be defined at class level.
    # I will modify the class definition start below.

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivos")
        if files:
            for f in files:
                if f not in self.files:
                    self.files.append(f)
                    self.file_list.addItem(os.path.basename(f))

    def clear_files(self):
        self.files = []
        self.file_list.clear()

    def on_op_changed(self, idx):
        if idx == 0:  # Comprimir
            self.config_stack.setCurrentWidget(self.compress_config)
        elif idx == 1 or idx == 2:  # Conversiones simples
            self.config_stack.setCurrentWidget(self.empty_config)
        else:  # Seguridad
            self.config_stack.setCurrentWidget(self.sec_config)

    def start_processing(self):
        if not self.files:
            return self.show_error("Agrega archivos primero")

        self.run_batch(self.files)

    def run_batch(self, file_list):
        op = self.op_combo.currentText()
        config = {}

        # Output logic
        default_dir = settings.get_output_directory() / "batch_output"

        if not os.path.exists(default_dir):
            os.makedirs(default_dir)

        # If running from button, maybe ask?
        # For watch folder, we use default without asking
        # Let's simple use default_dir always for now to avoid blocking prompts
        output_dir = default_dir
        self.last_output_file = output_dir

        if op == "Comprimir PDF":
            val = self.c_slider.value()
            level = settings.get_compression_level(val)
            config["quality"] = level
        elif op in ["Encriptar", "Desencriptar"]:
            pwd = self.pwd_input.text()
            if not pwd:
                # Solo error si es manual
                if self.sender() == self.start_btn:
                    return self.show_error("Ingresa una contraseña")
                return  # Skip silently in watch mode?
            config["password"] = pwd

        self.set_processing_state(True)
        self.update_progress(0, f"Procesando {len(file_list)} archivos...")

        self.worker = BatchWorker(op, file_list, config, output_dir)
        self.worker.progress_updated.connect(lambda v: self.update_progress(v))
        self.worker.item_processed.connect(self.on_item_processed)
        self.worker.finished.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def toggle_watch(self, checked):
        if checked:
            # Seleccionar carpeta a vigilar
            watch_dir = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta a Vigilar")
            if not watch_dir:
                self.watch_btn.setChecked(False)
                return

            self.watch_status.setText(f"Vigilando: {os.path.basename(watch_dir)}")
            self.watch_status.setStyleSheet("color: #10b981; font-weight: bold;")

            # Start watcher
            self.watcher.start(watch_dir, self.on_watch_event)
            self.start_btn.setEnabled(False)  # Deshabilitar manual mientras vigila

        else:
            self.watch_status.setText("Inactivo")
            self.watch_status.setStyleSheet("")
            self.watcher.stop()
            self.start_btn.setEnabled(True)

    def on_watch_event(self, filepath):
        """Callback desde hilo secundario"""
        self.file_detected.emit(filepath)

    def process_new_file(self, filepath):
        """Slot en hilo principal"""
        self.file_list.addItem(f"DETECTADO: {os.path.basename(filepath)}")
        # Ejecutar lote unitario
        # Note: If a batch is running, this might conflict.
        # For v5, simple implementation: run separate batch per file
        # Queueing would be better but complex.
        self.run_batch([filepath])

    def on_item_processed(self, filename, success):
        status = "✅" if success else "❌"
        # Actualizar lista visualmente si es posible
        print(f"{status} {filename}")

    def on_success(self, result):
        self.set_processing_state(False)
        # En watch mode, no mostrar popup bloqueante
        if not self.watch_btn.isChecked():
            self.show_success(f"Lote finalizado.\n{result['message']}")
            self.show_success_dialog(self.last_output_file, "Procesamiento Finalizado")
        else:
            # Solo actualizar estado
            self.status_label.setText("Esperando archivos...")
            self.progress_bar.setValue(0)

    def on_error(self, error):
        self.set_processing_state(False)
        self.show_error(f"Error: {error}")

    def reset_operation(self):
        self.clear_files()
        self.progress_bar.setValue(0)
