"""
Plantilla de estilos QSS embebida para evitar problemas de rutas en ejecutables.
"""

STYLES_QSS = """
/* 
 * Vectora - Estilos Globales Dinámicos
 * Usa variables que ThemeManager reemplaza en tiempo de ejecución
 */

/* === COLORES GLOBALES === */
* {
    font-family: 'Segoe UI', 'San Francisco', 'Roboto', sans-serif;
    outline: none;
}

QMainWindow {
    background-color: {{APP_BG}};
}

QWidget {
    color: {{TEXT_PRIMARY}};
}

/* === LABELS === */
QLabel {
    color: {{TEXT_PRIMARY}};
}

QLabel#sidebarTitle {
    color: {{TEXT_PRIMARY}};
    font-weight: 800;
}

/* === SIDEBAR === */
QWidget#sidebar {
    background-color: {{SURFACE_BG}};
    border-right: 1px solid {{BORDER}};
}

QPushButton#sidebarBtn {
    text-align: left;
    padding: 12px 16px;
    border: none;
    border-radius: 12px;
    background-color: transparent;
    color: {{TEXT_SECONDARY}}; /* Visible Text */
    font-weight: 500;
    outline: none;
}

QPushButton#sidebarBtn:hover {
    background-color: {{HOVER}};
    color: {{TEXT_PRIMARY}};
}

QPushButton#sidebarBtn:checked {
    background-color: {{ACCENT}};
    color: {{ACCENT_TEXT}};
    font-weight: 700;
    border: none;
}

/* === BOTONES PRIMARIOS (Action) === */
QPushButton[primary="true"], QPushButton#primaryButton {
    background-color: {{ACCENT}};
    color: {{ACCENT_TEXT}};
    border: 1px solid {{ACCENT}};
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton[primary="true"]:hover, QPushButton#primaryButton:hover {
    background-color: {{TEXT_SECONDARY}}; /* Fallback hover logic or opacit */
    opacity: 0.9;
}

QPushButton[primary="true"]:pressed, QPushButton#primaryButton:pressed {
    background-color: {{BORDER}}; 
}

QPushButton[primary="true"]:disabled, QPushButton#primaryButton:disabled {
    background-color: {{BORDER}};
    color: {{TEXT_SECONDARY}};
    border-color: {{BORDER}};
}

/* === BOTONES SECUNDARIOS / GENERALES === */
QPushButton {
    background-color: {{SURFACE_BG}};
    color: {{TEXT_PRIMARY}};
    border: 1px solid {{BORDER}};
    border-radius: 10px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: {{HOVER}};
    border-color: {{TEXT_SECONDARY}};
}

QPushButton:disabled {
    color: {{TEXT_SECONDARY}};
    background-color: {{APP_BG}};
    border-color: {{BORDER}};
}

/* === INPUTS === */
QLineEdit, QSpinBox, QTextEdit {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 8px;
    padding: 10px;
    color: {{TEXT_PRIMARY}};
    font-size: 14px;
    selection-background-color: {{ACCENT}};
    selection-color: {{ACCENT_TEXT}};
}

QLineEdit:focus, QSpinBox:focus, QTextEdit:focus {
    border: 1px solid {{ACCENT}};
    background-color: {{SURFACE_BG}};
}

/* === COMBOBOX === */
QComboBox {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 8px;
    padding: 10px;
    color: {{TEXT_PRIMARY}};
    font-size: 14px;
}

QComboBox:hover {
    border-color: {{TEXT_SECONDARY}};
}

QComboBox:focus {
    border: 1px solid {{ACCENT}};
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

/* Removed arrow image dependency for robustness - use unicode or native */
QComboBox::down-arrow {
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 8px;
    selection-background-color: {{HOVER}};
    selection-color: {{TEXT_PRIMARY}};
    padding: 4px;
    color: {{TEXT_PRIMARY}};
    outline: none;
}

/* === LISTS === */
QListWidget {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 12px;
    padding: 10px;
    outline: none;
    color: {{TEXT_PRIMARY}};
}

QListWidget::item {
    padding: 8px;
    border-radius: 6px;
    color: {{TEXT_PRIMARY}};
}

QListWidget::item:selected {
    background-color: {{HOVER}};
    color: {{TEXT_PRIMARY}};
    border: 1px solid {{BORDER}};
}

QListWidget::item:hover {
    background-color: {{HOVER}};
}

/* === PROGRESS BAR === */
QProgressBar {
    border: none;
    background-color: {{BORDER}};
    border-radius: 5px;
    text-align: center;
    height: 8px;
    color: transparent; 
}

QProgressBar::chunk {
    background-color: {{SUCCESS}};
    border-radius: 5px;
}

/* === SLIDERS === */
QSlider::groove:horizontal {
    background: {{BORDER}};
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: {{SURFACE_BG}};
    border: 2px solid {{ACCENT}};
    width: 18px;
    height: 18px;
    margin: -7px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background: {{HOVER}};
}

/* === CHECKBOXES === */
QCheckBox {
    spacing: 12px;
    color: {{TEXT_PRIMARY}}; /* Ensure visibility */
    font-size: 14px;
    background: transparent;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid {{BORDER}};
    background-color: {{SURFACE_BG}};
}

QCheckBox::indicator:hover {
    border-color: {{ACCENT}};
}

QCheckBox::indicator:checked {
    background-color: {{ACCENT}};
    border-color: {{ACCENT}};
}

/* === RADIO BUTTONS === */
QRadioButton {
    spacing: 8px;
    color: {{TEXT_PRIMARY}};
    font-size: 14px;
    background: transparent;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 1px solid {{BORDER}};
    background-color: {{SURFACE_BG}};
}

QRadioButton::indicator:checked {
    background-color: {{ACCENT}};
    border: 4px solid {{SURFACE_BG}}; /* Inner dot effect */
    outline: 1px solid {{ACCENT}};
}

/* === GROUPBOX === */
QGroupBox {
    border: 1px solid {{BORDER}};
    border-radius: 12px;
    margin-top: 12px;
    padding: 24px 16px 16px 16px;
    background-color: {{SURFACE_BG}};
    font-weight: 600;
    color: {{TEXT_PRIMARY}};
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    left: 10px;
    color: {{TEXT_PRIMARY}};
}

/* === SCROLLBARS === */
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: {{BORDER}};
    border-radius: 5px;
    min-height: 40px;
}

QScrollBar::handle:vertical:hover {
    background: {{TEXT_SECONDARY}};
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
    height: 0px;
}

/* === TEXTOS === */
QLabel#labelTitle {
    font-size: 28px;
    font-weight: 800;
    color: {{TEXT_PRIMARY}};
    letter-spacing: -0.5px;
}

QLabel#labelSubtitle {
    font-size: 16px;
    color: {{TEXT_SECONDARY}};
    font-weight: 400;
}

QLabel#labelSection {
    font-size: 18px;
    font-weight: 700;
    color: {{TEXT_PRIMARY}};
    margin-bottom: 8px;
}

/* === Cards Specific Overrides === */
/* Ensure default bg is right */
QFrame#dashboardCard, QWidget#dashboardCard {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
}
"""
