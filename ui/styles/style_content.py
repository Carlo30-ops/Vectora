"""
Plantilla de estilos QSS embebida - LocalPDF v5 Design System
Basado en documentación de diseño minimalista iOS
Usa variables que ThemeManager reemplaza en tiempo de ejecución
"""

STYLES_QSS = """
/*
 * LocalPDF v5 - Design System Completo
 * Colores y espaciado según especificación de diseño
 * Todas las variables se reemplazan en tiempo de ejecución
 */

/* === GLOBAL & TYPOGRAPHY === */
* {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
    outline: none;
    margin: 0;
    padding: 0;
}

QMainWindow, QWidget {
    background-color: {{APP_BG}};
    color: {{TEXT_PRIMARY}};
}

/* === WINDOW STYLING === */
QMainWindow {
    background-color: {{APP_BG}};
    border: none;
}

/* === SIDEBAR STYLING === */
QWidget#sidebar, QWidget#sidebarWidget {
    background-color: {{SURFACE_BG}};
    border-right: 1px solid {{BORDER}};
    min-width: 256px;
    max-width: 256px;
}

/* Sidebar Header */
QWidget#sidebarHeader {
    background-color: {{SURFACE_BG}};
    border-bottom: 1px solid {{BORDER}};
    padding: 24px;
}

QLabel#sidebarLogo {
    font-size: 18px;
    font-weight: 600;
    color: {{TEXT_PRIMARY}};
}

QLabel#sidebarVersion {
    font-size: 11px;
    color: {{TEXT_SECONDARY}};
    margin-top: 4px;
}

/* Logo Icon Container */
QFrame#logoIcon, QWidget#logoIcon {
    background-color: {{ACCENT}};
    border-radius: 16px;
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
}

/* Sidebar Navigation Buttons */
QPushButton#sidebarButton, QPushButton#navButton {
    text-align: left;
    padding: 12px 16px;
    margin: 2px 0px;
    border: none;
    border-radius: 12px;
    background-color: transparent;
    color: {{TEXT_PRIMARY}};
    font-weight: 500;
    font-size: 14px;
}

QPushButton#sidebarButton:hover, QPushButton#navButton:hover {
    background-color: {{HOVER}};
    color: {{TEXT_PRIMARY}};
}

QPushButton#sidebarButton:pressed, QPushButton#navButton:pressed {
    background-color: {{ACCENT}};
    color: {{ACCENT_TEXT}};
}

QPushButton#sidebarButton:checked, QPushButton#navButton:checked {
    background-color: {{ACCENT}};
    color: {{ACCENT_TEXT}};
    font-weight: 700;
}

/* Sidebar Footer */
QWidget#sidebarFooter {
    background-color: {{SURFACE_BG}};
    border-top: 1px solid {{BORDER}};
    padding: 16px;
}

QFrame#offlineIndicator {
    background-color: {{HOVER}};
    border-radius: 12px;
    padding: 16px;
}

QLabel#offlineTitle {
    font-weight: 500;
    color: {{TEXT_PRIMARY}};
    font-size: 12px;
}

QLabel#offlineSubtitle {
    color: {{TEXT_SECONDARY}};
    font-size: 11px;
    margin-top: 4px;
}

/* === MAIN CONTENT AREA === */
QWidget#contentArea, QWidget#mainContent {
    background-color: {{APP_BG}};
}

QScrollArea {
    border: none;
    background-color: {{APP_BG}};
}

/* === DASHBOARD STYLING === */
QLabel#dashboardTitle {
    font-size: 36px;
    font-weight: 700;
    color: {{TEXT_PRIMARY}};
}

QLabel#dashboardSubtitle {
    font-size: 16px;
    color: {{TEXT_SECONDARY}};
    margin-top: 8px;
}

/* Dashboard Cards - General */
QFrame#dashboardCard, QWidget#dashboardCard, QPushButton#dashboardCardBtn {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 20px;
    padding: 24px;
    text-align: left;
}

QFrame#dashboardCard:hover, QWidget#dashboardCard:hover, QPushButton#dashboardCardBtn:hover {
    background-color: {{HOVER}};
    border: 1px solid {{BORDER}};
}

/* Card Icon Container */
QFrame#cardIcon, QWidget#cardIcon {
    background-color: {{ACCENT}};
    border-radius: 12px;
    min-width: 48px;
    max-width: 48px;
    min-height: 48px;
    max-height: 48px;
}

/* Card Titles and Text */
QLabel#cardTitle {
    font-weight: 600;
    font-size: 15px;
    color: {{TEXT_PRIMARY}};
}

QLabel#cardDescription {
    font-size: 13px;
    color: {{TEXT_SECONDARY}};
    margin-top: 4px;
}

/* Special Card - Asistente (Black Background) */
QFrame#assistantCard, QPushButton#assistantCard {
    background-color: {{ACCENT}};
    border: none;
    border-radius: 24px;
    padding: 32px;
}

QLabel#assistantTitle {
    font-size: 24px;
    font-weight: 700;
    color: {{ACCENT_TEXT}};
}

QLabel#assistantDescription {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
    margin-top: 8px;
}

/* === BUTTONS & INTERACTIONS === */
QPushButton#primaryButton, QPushButton#actionButton {
    background-color: {{ACCENT}};
    color: {{ACCENT_TEXT}};
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 15px;
    font-weight: 600;
    min-height: 40px;
}

QPushButton#primaryButton:hover, QPushButton#actionButton:hover {
    background-color: {{ACCENT}};
    opacity: 0.9;
}

QPushButton#primaryButton:pressed, QPushButton#actionButton:pressed {
    opacity: 0.8;
}

QPushButton#primaryButton:disabled, QPushButton#actionButton:disabled {
    opacity: 0.5;
}

/* Secondary Button */
QPushButton#secondaryButton {
    background-color: transparent;
    color: {{ACCENT}};
    border: 1px solid {{ACCENT}};
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
}

QPushButton#secondaryButton:hover {
    background-color: {{HOVER}};
}

/* === INPUTS & FIELDS === */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 10px;
    padding: 10px 12px;
    color: {{TEXT_PRIMARY}};
    selection-background-color: {{ACCENT}};
    font-size: 14px;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid {{ACCENT}};
    background-color: {{SURFACE_BG}};
}

QLineEdit::placeholder {
    color: {{TEXT_SECONDARY}};
}

/* ComboBox Dropdown */
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox::down-arrow {
    image: none;
    width: 0px;
}

/* === DROPZONE / FILE AREA === */
QFrame#dropZone, QWidget#dropZone {
    background-color: {{SURFACE_BG}};
    border: 2px dashed {{BORDER}};
    border-radius: 24px;
    padding: 48px 32px;
    text-align: center;
}

QFrame#dropZone:hover, QWidget#dropZone:hover {
    background-color: {{HOVER}};
    border: 2px dashed {{ACCENT}};
}

QLabel#dropZoneTitle {
    font-size: 18px;
    font-weight: 600;
    color: {{TEXT_PRIMARY}};
}

QLabel#dropZoneDescription {
    font-size: 14px;
    color: {{TEXT_SECONDARY}};
    margin-top: 4px;
}

/* === PROGRESS BAR === */
QProgressBar {
    border: none;
    background-color: {{BORDER}};
    border-radius: 6px;
    text-align: center;
    height: 8px;
    margin: 0px;
    padding: 0px;
}

QProgressBar::chunk {
    background-color: {{ACCENT}};
    border-radius: 6px;
}

QLabel#progressLabel {
    font-size: 13px;
    color: {{TEXT_SECONDARY}};
}

/* === SUCCESS / RESULT CARDS === */
QFrame#successCard, QWidget#successCard {
    background-color: {{ACCENT}};
    border: none;
    border-radius: 20px;
    padding: 24px;
}

QLabel#successTitle {
    font-size: 18px;
    font-weight: 700;
    color: {{ACCENT_TEXT}};
}

QLabel#successMessage {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
    margin-top: 4px;
}

/* === SCROLLBARS === */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0px;
    padding: 0px;
}

QScrollBar::handle:vertical {
    background: {{BORDER}};
    border-radius: 4px;
    min-height: 40px;
    margin: 4px 0px;
}

QScrollBar::handle:vertical:hover {
    background: {{TEXT_SECONDARY}};
}

QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
}

QScrollBar::handle:horizontal {
    background: {{BORDER}};
    border-radius: 4px;
    min-width: 40px;
}

QScrollBar::handle:horizontal:hover {
    background: {{TEXT_SECONDARY}};
}

/* === TABS === */
QTabBar::tab {
    background-color: {{HOVER}};
    color: {{TEXT_SECONDARY}};
    padding: 8px 16px;
    border-radius: 8px;
    margin-right: 4px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: {{SURFACE_BG}};
    color: {{TEXT_PRIMARY}};
    font-weight: 600;
}

QTabWidget::pane {
    border: none;
}

/* === CHECKBOXES & RADIO BUTTONS === */
QCheckBox, QRadioButton {
    color: {{TEXT_PRIMARY}};
    spacing: 8px;
    padding: 4px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
}

QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: {{ACCENT}};
    border: none;
}

/* === TOOLTIPS === */
QToolTip {
    background-color: {{ACCENT}};
    color: {{ACCENT_TEXT}};
    border: none;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
}

/* === GROUPBOX === */
QGroupBox {
    color: {{TEXT_PRIMARY}};
    border: 1px solid {{BORDER}};
    border-radius: 12px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 500;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0px 4px;
}

"""
