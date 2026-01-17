"""
Definición de paletas de colores para temas - LocalPDF v5 Design System
Basado en esquema minimalista iOS con blancos, negros y grises
Implementa Dark Mode profesional estilo Apple
"""

THEMES = {
    "light": {
        # Colores Principales - Light Mode
        "APP_BG": "#f9fafb",  # gray-50 - Fondo global
        "SURFACE_BG": "#ffffff",  # white - Fondos principales
        "TEXT_PRIMARY": "#111827",  # gray-900 - Textos principales (label-primary)
        "TEXT_SECONDARY": "#6b7280",  # gray-500 - Textos secundarios (label-secondary 60%)
        "TEXT_TERTIARY": "#9ca3af",  # gray-400 - Textos terciarios (label-tertiary 30%)
        "TEXT_QUATERNARY": "#d1d5db",  # gray-300 - Textos cuaternarios (label-quaternary 18%)
        
        # Elementos de Interfaz
        "ACCENT": "#000000",  # Negro principal - Buttons, elementos destacados
        "ACCENT_TEXT": "#ffffff",  # Texto en elementos oscuros
        "BORDER": "#e5e7eb",  # gray-200 - Bordes
        "BORDER_DASHED": "#d1d5db",  # gray-300 - Bordes punteados
        "HOVER": "#f3f4f6",  # gray-100 - Estados hover
        "ICON_COLOR": "#4b5563",  # gray-600 - Iconos
        "ICON_CONTAINER_BG": "#000000",  # Icon containers - negro
        "ICON_CONTAINER_FG": "#ffffff",  # Icon - blanco
        
        # Estados de Color
        "SUCCESS": "#10b981",  # emerald-500 - Éxito
        "SUCCESS_LIGHT": "#d1fae5",  # emerald-100
        "ERROR": "#ef4444",  # red-500 - Error
        "ERROR_LIGHT": "#fee2e2",  # red-100
        "WARNING": "#f59e0b",  # amber-500 - Advertencia
        "WARNING_LIGHT": "#fef3c7",  # amber-100
        "INFO": "#6366f1",  # indigo-500 - Información
        "INFO_LIGHT": "#e0e7ff",  # indigo-100
        
        # Efectos Especiales
        "GLASS_BG": "rgba(255, 255, 255, 0.6)",  # Glassmorphism light
        "SHADOW": "rgba(0, 0, 0, 0.05)",  # Sombra suave
        "SHADOW_MD": "rgba(0, 0, 0, 0.1)",  # Sombra media
        "SHADOW_LG": "rgba(0, 0, 0, 0.15)",  # Sombra grande
    },
    "dark": {
        # Apple Dark Mode Profesional
        # Colores Principales - Negro base con elevaciones
        "APP_BG": "#000000",  # Negro puro - Fondo global (black-base)
        "SURFACE_BG": "#1c1c1e",  # Primer nivel de elevación (elevated-1)
        "TEXT_PRIMARY": "#ffffff",  # Blanco - Textos principales (label-primary)
        "TEXT_SECONDARY": "#98989d",  # Gris claro - Textos secundarios (label-secondary 60%)
        "TEXT_TERTIARY": "#76767a",  # Gris medio - Textos terciarios (label-tertiary 30%)
        "TEXT_QUATERNARY": "#5a5a5e",  # Gris oscuro - Textos cuaternarios (label-quaternary 18%)
        
        # Elementos de Interfaz - Elevaciones Apple
        "HOVER": "#2c2c2e",  # Segundo nivel (elevated-2) - Para hover
        "ACTIVE": "#3a3a3c",  # Tercer nivel (elevated-3) - Para active
        "BORDER": "#38383a",  # Separadores y bordes (separator)
        "BORDER_DASHED": "#3a3a3c",  # Bordes punteados
        "ACCENT": "#ffffff",  # Blanco para elementos destacados
        "ACCENT_TEXT": "#000000",  # Texto negro en elementos blancos
        "ICON_COLOR": "#98989d",  # Iconos en gris claro
        "ICON_CONTAINER_BG": "#ffffff",  # Icon containers - blanco (INVERTIDO)
        "ICON_CONTAINER_FG": "#000000",  # Icon - negro (INVERTIDO)
        
        # Estados de Color - Más vibrantes en dark mode (Apple Style)
        "SUCCESS": "#32d74b",  # green-500 Apple - Muy brillante
        "SUCCESS_LIGHT": "#064e3b",  # emerald-900
        "ERROR": "#ff453a",  # red-500 Apple - Muy brillante
        "ERROR_LIGHT": "#7f1d1d",  # red-900
        "WARNING": "#ff9500",  # orange-500 Apple - Muy brillante
        "WARNING_LIGHT": "#78350f",  # amber-900
        "INFO": "#0a84ff",  # blue-500 Apple - Muy brillante
        "INFO_LIGHT": "#312e81",  # indigo-900
        
        # Efectos Especiales - Adaptados para dark mode
        "GLASS_BG": "rgba(255, 255, 255, 0.1)",  # Glassmorphism dark (muy sutil)
        "SHADOW": "rgba(0, 0, 0, 0.3)",  # Sombra más oscura
        "SHADOW_MD": "rgba(0, 0, 0, 0.4)",  # Sombra media más oscura
        "SHADOW_LG": "rgba(0, 0, 0, 0.5)",  # Sombra grande más oscura
    },
}
