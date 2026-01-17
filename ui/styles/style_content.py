"""
Plantilla de estilos QSS embebida - LocalPDF v5 Design System
Basado en documentación de diseño minimalista iOS con Glassmorphism
Usa variables que ThemeManager reemplaza en tiempo de ejecución
MEJORADO: Sombras elevadas, bordes redondeados Apple, transiciones suaves
"""

STYLES_QSS = """
/*
 * LocalPDF v5 - Design System Completo (APPLE iOS Style)
 * Colores, espaciado y efectos según especificación Apple Design
 * Todas las variables se reemplazan en tiempo de ejecución
 * VERSIÓN: 5.0.0 - Glassmorphism + Elevated Design
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
    transition: all 300ms ease-in-out;
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

/* Dashboard Cards - General (Glassmorphism + Elevated) */
QFrame#dashboardCard, QWidget#dashboardCard, QPushButton#dashboardCardBtn {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 24px;
    padding: 28px;
    text-align: left;
    transition: all 300ms ease-in-out;
}

QFrame#dashboardCard:hover, QWidget#dashboardCard:hover, QPushButton#dashboardCardBtn:hover {
    background-color: {{HOVER}};
    border: 1px solid {{ACCENT}};
}

/* Card Icon Container (56x56px como especifica PROYECTO_EJEMPLO) */
QFrame#cardIcon, QWidget#cardIcon {
    background-color: {{ACCENT}};
    border-radius: 16px;
    min-width: 56px;
    max-width: 56px;
    min-height: 56px;
    max-height: 56px;
    transition: all 300ms ease-in-out;
}

/* Card Titles and Text */
QLabel#cardTitle {
    font-weight: 600;
    font-size: 16px;
    color: {{TEXT_PRIMARY}};
}

QLabel#cardDescription {
    font-size: 13px;
    color: {{TEXT_SECONDARY}};
    margin-top: 8px;
}

/* Special Card - Asistente (Black Background con Glassmorphism) */
QFrame#assistantCard, QPushButton#assistantCard {
    background-color: {{ACCENT}};
    border: none;
    border-radius: 28px;
    padding: 40px;
    transition: all 300ms ease-in-out;
}

QFrame#assistantCard:hover, QPushButton#assistantCard:hover {
    background-color: {{ACCENT}};
}

QLabel#assistantTitle {
    font-size: 28px;
    font-weight: 700;
    color: {{ACCENT_TEXT}};
}

QLabel#assistantDescription {
    font-size: 15px;
    color: rgba(255, 255, 255, 0.85);
    margin-top: 12px;
}

/* === BUTTONS & INTERACTIONS (Apple Hover Effects) === */
QPushButton#primaryButton, QPushButton#actionButton {
    background-color: {{ACCENT}};
    color: {{ACCENT_TEXT}};
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 15px;
    font-weight: 600;
    min-height: 44px;
    transition: all 300ms ease-in-out;
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
    transition: all 300ms ease-in-out;
}

QPushButton#secondaryButton:hover {
    background-color: {{HOVER}};
    border: 1px solid {{ACCENT}};
}

/* === INPUTS & FIELDS (Apple Style) === */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 12px;
    padding: 12px 14px;
    color: {{TEXT_PRIMARY}};
    selection-background-color: {{ACCENT}};
    font-size: 14px;
    transition: all 300ms ease-in-out;
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

/* === DROPZONE / FILE AREA (Glassmorphism) === */
QFrame#dropZone, QWidget#dropZone {
    background-color: {{SURFACE_BG}};
    border: 2px dashed {{BORDER}};
    border-radius: 28px;
    padding: 56px 40px;
    text-align: center;
    transition: all 300ms ease-in-out;
}

QFrame#dropZone:hover, QWidget#dropZone:hover {
    background-color: {{HOVER}};
    border: 2px dashed {{ACCENT}};
}

QLabel#dropZoneTitle {
    font-size: 20px;
    font-weight: 600;
    color: {{TEXT_PRIMARY}};
}

QLabel#dropZoneDescription {
    font-size: 15px;
    color: {{TEXT_SECONDARY}};
    margin-top: 8px;
}

/* === PROGRESS BAR === */
QProgressBar {
    border: none;
    background-color: {{BORDER}};
    border-radius: 8px;
    text-align: center;
    height: 10px;
    margin: 0px;
    padding: 0px;
}

QProgressBar::chunk {
    background-color: {{ACCENT}};
    border-radius: 8px;
    transition: width 300ms ease-in-out;
}

QLabel#progressLabel {
    font-size: 13px;
    color: {{TEXT_SECONDARY}};
}

/* === SUCCESS / RESULT CARDS === */
QFrame#successCard, QWidget#successCard {
    background-color: {{ACCENT}};
    border: none;
    border-radius: 24px;
    padding: 32px;
    transition: all 300ms ease-in-out;
}

QLabel#successTitle {
    font-size: 20px;
    font-weight: 700;
    color: {{ACCENT_TEXT}};
}

QLabel#successMessage {
    font-size: 15px;
    color: rgba(255, 255, 255, 0.85);
    margin-top: 8px;
}

/* === SCROLLBARS (Apple Style) === */
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 0px;
    padding: 0px;
}

QScrollBar::handle:vertical {
    background: {{BORDER}};
    border-radius: 5px;
    min-height: 40px;
    margin: 4px 0px;
    transition: all 300ms ease-in-out;
}

QScrollBar::handle:vertical:hover {
    background: {{TEXT_SECONDARY}};
}

QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: transparent;
    height: 10px;
}

QScrollBar::handle:horizontal {
    background: {{BORDER}};
    border-radius: 5px;
    min-width: 40px;
    transition: all 300ms ease-in-out;
}

QScrollBar::handle:horizontal:hover {
    background: {{TEXT_SECONDARY}};
}

QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal {
    width: 0px;
}

/* === TABS === */
QTabBar::tab {
    background-color: {{HOVER}};
    color: {{TEXT_SECONDARY}};
    padding: 12px 20px;
    border-radius: 10px;
    margin-right: 4px;
    font-weight: 500;
    font-size: 14px;
    transition: all 300ms ease-in-out;
}

QTabBar::tab:hover {
    background-color: {{ACTIVE}};
}

QTabBar::tab:selected {
    background-color: {{SURFACE_BG}};
    color: {{TEXT_PRIMARY}};
    font-weight: 600;
    border: 1px solid {{BORDER}};
}

QTabWidget::pane {
    border: none;
}

/* === CHECKBOXES & RADIO BUTTONS === */
QCheckBox, QRadioButton {
    color: {{TEXT_PRIMARY}};
    spacing: 10px;
    padding: 4px;
    transition: all 300ms ease-in-out;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 20px;
    height: 20px;
    border-radius: 6px;
}

QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
    background-color: {{SURFACE_BG}};
    border: 1.5px solid {{BORDER}};
}

QCheckBox::indicator:unchecked:hover, QRadioButton::indicator:unchecked:hover {
    border: 1.5px solid {{ACCENT}};
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: {{ACCENT}};
    border: none;
}

QCheckBox::indicator:checked:hover, QRadioButton::indicator:checked:hover {
    background-color: {{ACCENT}};
    opacity: 0.9;
}

/* === TOOLTIPS === */
QToolTip {
    background-color: {{ACCENT}};
    color: {{ACCENT_TEXT}};
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 12px;
    font-weight: 500;
}

/* === GROUPBOX === */
QGroupBox {
    color: {{TEXT_PRIMARY}};
    border: 1px solid {{BORDER}};
    border-radius: 12px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: 500;
    transition: all 300ms ease-in-out;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0px 6px;
}

"""
