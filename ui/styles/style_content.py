"""
Plantilla de estilos QSS embebida para evitar problemas de rutas en ejecutables.
"""

STYLES_QSS = """
/* 
 * Vectora - Estilos Globales Premium
 * Usa variables que ThemeManager reemplaza en tiempo de ejecución
 */

/* === COLORES GLOBALES === */
* {
    font-family: 'Inter', 'Segoe UI', sans-serif;
    outline: none;
}

QMainWindow {
    background-color: {{APP_BG}};
}

QWidget {
    color: {{TEXT_PRIMARY}};
}

/* === GLASS CONTAINERS === */
QFrame#glassContainer, QWidget#glassContainer {
    background-color: {{GLASS_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 16px;
}

/* === SIDEBAR === */
QWidget#sidebar {
    background-color: {{SURFACE_BG}};
    border-right: 1px solid {{BORDER}};
}

QLabel#sidebarTitle {
    color: {{TEXT_PRIMARY}};
    font-weight: 800;
    font-size: 18px;
}

QPushButton#sidebarBtn {
    text-align: left;
    padding: 12px 16px;
    border: none;
    border-radius: 12px;
    background-color: transparent;
    color: {{TEXT_SECONDARY}};
    font-weight: 500;
    font-size: 14px;
}

QPushButton#sidebarBtn:hover {
    background-color: {{HOVER}};
    color: {{TEXT_PRIMARY}};
}

QPushButton#sidebarBtn:checked {
    background-color: {{ACCENT}};
    color: {{ACCENT_TEXT}};
    font-weight: 700;
}

/* === BOTONES PRIMARIOS === */
QPushButton#primaryButton, QPushButton[primary="true"] {
    background-color: {{ACCENT}};
    color: {{ACCENT_TEXT}};
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#primaryButton:hover, QPushButton[primary="true"]:hover {
    opacity: 0.9;
}

/* === DASHBOARD CARDS === */
QFrame#dashboardCard, QPushButton#dashboardCard {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 20px;
}

QFrame#dashboardCard:hover {
    border: 1px solid {{ACCENT}};
}

/* === INPUTS & COMBOBOX === */
QLineEdit, QSpinBox, QComboBox {
    background-color: {{SURFACE_BG}};
    border: 1px solid {{BORDER}};
    border-radius: 10px;
    padding: 10px 14px;
    color: {{TEXT_PRIMARY}};
}

QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid {{ACCENT}};
}

/* === PROGRESS BAR === */
QProgressBar {
    border: none;
    background-color: {{BORDER}};
    border-radius: 6px;
    text-align: center;
    height: 10px;
    color: transparent;
}

QProgressBar::chunk {
    background-color: {{ACCENT}};
    border-radius: 6px;
}

/* === SCROLLBARS === */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: {{BORDER}};
    border-radius: 4px;
    min-height: 40px;
}

QScrollBar::handle:vertical:hover {
    background: {{TEXT_SECONDARY}};
}

/* === TITLES === */
QLabel#labelTitle {
    font-size: 32px;
    font-weight: 800;
    color: {{TEXT_PRIMARY}};
    letter-spacing: -1px;
}

QLabel#labelSubtitle {
    font-size: 16px;
    color: {{TEXT_SECONDARY}};
}

"""
