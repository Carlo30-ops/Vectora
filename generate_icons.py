#!/usr/bin/env python3
"""
Generador de Iconos SVG para LocalPDF v5
Genera todos los iconos necesarios para la aplicación

Uso:
    python generate_icons.py

Los iconos se guardarán en la carpeta ./icons/
"""

import os
from pathlib import Path

# Directorio de salida
OUTPUT_DIR = Path("icons")

# Definiciones SVG de los iconos (basados en lucide-react)
ICONS = {
    # Logo principal
    "file-text": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
  <polyline points="14 2 14 8 20 8"/>
  <line x1="16" y1="13" x2="8" y2="13"/>
  <line x1="16" y1="17" x2="8" y2="17"/>
  <line x1="10" y1="9" x2="8" y2="9"/>
</svg>''',

    # Navegación principal
    "home": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
  <polyline points="9 22 9 12 15 12 15 22"/>
</svg>''',

    "wand-2": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72Z"/>
  <path d="m14 7 3 3"/>
  <path d="M5 6v4"/>
  <path d="M19 14v4"/>
  <path d="M10 2v2"/>
  <path d="M7 8H3"/>
  <path d="M21 16h-4"/>
  <path d="M11 3H9"/>
</svg>''',

    # Operaciones PDF
    "combine": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 3H5a2 2 0 0 0-2 2v3"/>
  <path d="M21 8V5a2 2 0 0 0-2-2h-3"/>
  <path d="M3 16v3a2 2 0 0 0 2 2h3"/>
  <path d="M16 21h3a2 2 0 0 0 2-2v-3"/>
  <line x1="8" y1="12" x2="16" y2="12"/>
  <line x1="12" y1="8" x2="12" y2="16"/>
</svg>''',

    "scissors": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="6" cy="6" r="3"/>
  <circle cx="6" cy="18" r="3"/>
  <line x1="20" y1="4" x2="8.12" y2="15.88"/>
  <line x1="14.47" y1="14.48" x2="20" y2="20"/>
  <line x1="8.12" y1="8.12" x2="12" y2="12"/>
</svg>''',

    "archive": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="2" y="4" width="20" height="5" rx="2"/>
  <path d="M4 9v9a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9"/>
  <path d="M10 13h4"/>
</svg>''',

    "refresh-cw": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 2v6h-6"/>
  <path d="M3 12a9 9 0 0 1 15-6.7L21 8"/>
  <path d="M3 22v-6h6"/>
  <path d="M21 12a9 9 0 0 1-15 6.7L3 16"/>
</svg>''',

    "shield": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>
</svg>''',

    "scan-text": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 7V5a2 2 0 0 1 2-2h2"/>
  <path d="M17 3h2a2 2 0 0 1 2 2v2"/>
  <path d="M21 17v2a2 2 0 0 1-2 2h-2"/>
  <path d="M7 21H5a2 2 0 0 1-2-2v-2"/>
  <path d="M7 8h8"/>
  <path d="M7 12h10"/>
  <path d="M7 16h6"/>
</svg>''',

    "folder-clock": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="16" cy="16" r="6"/>
  <path d="M7 20H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H20a2 2 0 0 1 2 2"/>
  <path d="M16 14v2l1 1"/>
</svg>''',

    # Acciones comunes
    "upload": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
  <polyline points="17 8 12 3 7 8"/>
  <line x1="12" y1="3" x2="12" y2="15"/>
</svg>''',

    "download": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
  <polyline points="7 10 12 15 17 10"/>
  <line x1="12" y1="15" x2="12" y2="3"/>
</svg>''',

    "x": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="18" y1="6" x2="6" y2="18"/>
  <line x1="6" y1="6" x2="18" y2="18"/>
</svg>''',

    "arrow-right": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="5" y1="12" x2="19" y2="12"/>
  <polyline points="12 5 19 12 12 19"/>
</svg>''',

    "chevron-right": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="9 18 15 12 9 6"/>
</svg>''',

    # Iconos de estado
    "check-circle-2": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <path d="m9 12 2 2 4-4"/>
</svg>''',

    "clock": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <polyline points="12 6 12 12 16 14"/>
</svg>''',

    "play": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="5 3 19 12 5 21 5 3"/>
</svg>''',

    "alert-circle": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="12" y1="8" x2="12" y2="12"/>
  <line x1="12" y1="16" x2="12.01" y2="16"/>
</svg>''',

    # Iconos especiales
    "sparkles": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
  <path d="M5 3v4"/>
  <path d="M19 17v4"/>
  <path d="M3 5h4"/>
  <path d="M17 19h4"/>
</svg>''',

    "grip-vertical": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="9" cy="12" r="1"/>
  <circle cx="9" cy="5" r="1"/>
  <circle cx="9" cy="19" r="1"/>
  <circle cx="15" cy="12" r="1"/>
  <circle cx="15" cy="5" r="1"/>
  <circle cx="15" cy="19" r="1"/>
</svg>''',

    "help-circle": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
  <line x1="12" y1="17" x2="12.01" y2="17"/>
</svg>''',

    # Iconos de seguridad
    "lock": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
</svg>''',

    "unlock": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
  <path d="M7 11V7a5 5 0 0 1 9.9-1"/>
</svg>''',

    "eye": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
  <circle cx="12" cy="12" r="3"/>
</svg>''',

    "eye-off": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
  <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
  <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
  <line x1="2" y1="2" x2="22" y2="22"/>
</svg>''',

    # Iconos de conversión
    "image": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
  <circle cx="9" cy="9" r="2"/>
  <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
</svg>''',

    "file-spreadsheet": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
  <polyline points="14 2 14 8 20 8"/>
  <path d="M8 13h2"/>
  <path d="M8 17h2"/>
  <path d="M14 13h2"/>
  <path d="M14 17h2"/>
</svg>''',

    "file-search": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M4 22h14a2 2 0 0 0 2-2V7.5L14.5 2H6a2 2 0 0 0-2 2v3"/>
  <polyline points="14 2 14 8 20 8"/>
  <path d="M5 17a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
  <path d="m9 18-1.5-1.5"/>
</svg>''',

    "languages": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m5 8 6 6"/>
  <path d="m4 14 6-6 2-3"/>
  <path d="M2 5h12"/>
  <path d="M7 2h1"/>
  <path d="m22 22-5-10-5 10"/>
  <path d="M14 18h6"/>
</svg>''',

    "folder": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>
</svg>''',

    # Nuevos iconos agregados
    "settings": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.38a2 2 0 0 0-.73-2.73l-.15-.1a2 2 0 0 1-1-1.72v-.51a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
  <circle cx="12" cy="12" r="3"/>
</svg>''',

    "trash-2": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 6h18"/>
  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
  <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
  <line x1="10" y1="11" x2="10" y2="17"/>
  <line x1="14" y1="11" x2="14" y2="17"/>
</svg>''',

    "edit-2": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
</svg>''',

    "more-vertical": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="1"/>
  <circle cx="12" cy="5" r="1"/>
  <circle cx="12" cy="19" r="1"/>
</svg>''',

    "layout-dashboard": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="3" width="7" height="9"/>
  <rect x="14" y="3" width="7" height="5"/>
  <rect x="14" y="12" width="7" height="9"/>
  <rect x="3" y="16" width="7" height="5"/>
</svg>''',

    "sun": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="5"/>
  <line x1="12" y1="1" x2="12" y2="3"/>
  <line x1="12" y1="21" x2="12" y2="23"/>
  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
  <line x1="1" y1="12" x2="3" y2="12"/>
  <line x1="21" y1="12" x2="23" y2="12"/>
  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
</svg>''',

    "moon": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
</svg>''',

    "github": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>
</svg>''',

    "info": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="12" y1="16" x2="12" y2="12"/>
  <line x1="12" y1="8" x2="12.01" y2="8"/>
</svg>''',

    "arrow-left": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="19" y1="12" x2="5" y2="12"/>
  <polyline points="12 19 5 12 12 5"/>
</svg>''',

    "layers": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="12 2 2 7 12 12 22 7 12 2"/>
  <polyline points="2 17 12 22 22 17"/>
  <polyline points="2 12 12 17 22 12"/>
</svg>''',

    "minimize-2": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="4 14 10 14 10 20"/>
  <polyline points="20 10 14 10 14 4"/>
  <line x1="14" y1="10" x2="21" y2="3"/>
  <line x1="3" y1="21" x2="10" y2="14"/>
</svg>''',

    "check": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="20 6 9 17 4 12"/>
</svg>''',
    
    "chevron-down": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="6 9 12 15 18 9"/>
</svg>''',

    # Iconos Faltantes Rediseño
    "search": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
</svg>''',

    "zap": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>
</svg>''',

    "plus": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M5 12h14"/><path d="M12 5v14"/>
</svg>''',

    "trash": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>
</svg>''',

    "layout": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/>
</svg>''',

    # Alias para facilidad de uso
    "merge": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="12" y1="8" x2="12" y2="16"/>
</svg>''',
    
    "split": '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/>
</svg>''',
}


def create_icon_file(name: str, svg_content: str, output_dir: Path):
    """Crea un archivo SVG individual"""
    filename = f"{name}.svg"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    return filepath


def create_colored_variant(svg_content: str, color: str) -> str:
    """Crea una variante coloreada del SVG"""
    return svg_content.replace('stroke="currentColor"', f'stroke="{color}"')


def generate_all_icons():
    """Genera todos los iconos SVG"""
    # Crear directorio si no existe
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("  Generador de Iconos SVG - LocalPDF v5")
    print("=" * 60)
    print()
    print(f"Generando {len(ICONS)} iconos en el directorio: {OUTPUT_DIR}")
    print()
    
    created_files = []
    
    # Generar iconos estándar (negro)
    for name, svg_content in ICONS.items():
        filepath = create_icon_file(name, svg_content, OUTPUT_DIR)
        created_files.append(filepath)
        print(f"✓ Creado: {filepath.name}")
    
    print()
    print("=" * 60)
    print("Generando variantes de color...")
    print("=" * 60)
    print()
    
    # Crear subdirectorio para variantes coloreadas
    colored_dir = OUTPUT_DIR / "colored"
    colored_dir.mkdir(exist_ok=True)
    
    # Colores para variantes
    colors = {
        "white": "#ffffff",
        "gray": "#6b7280",
        "black": "#000000",
        "blue": "#3b82f6",
        "green": "#10b981",
        "red": "#ef4444",
    }
    
    # Iconos principales que necesitan variantes de color
    main_icons = ["file-text", "wand-2", "combine", "scissors", "archive", 
                  "refresh-cw", "shield", "scan-text", "folder-clock"]
    
    for icon_name in main_icons:
        if icon_name in ICONS:
            for color_name, color_value in colors.items():
                colored_svg = create_colored_variant(ICONS[icon_name], color_value)
                colored_filename = f"{icon_name}-{color_name}.svg"
                colored_path = colored_dir / colored_filename
                
                with open(colored_path, 'w', encoding='utf-8') as f:
                    f.write(colored_svg)
                
                created_files.append(colored_path)
                print(f"✓ Creado: colored/{colored_filename}")
    
    print()
    print("=" * 60)
    print("Generando iconos en diferentes tamaños...")
    print("=" * 60)
    print()
    
    # Crear subdirectorio para diferentes tamaños
    sizes_dir = OUTPUT_DIR / "sizes"
    sizes_dir.mkdir(exist_ok=True)
    
    sizes = [16, 24, 32, 48, 64, 128]
    important_icons = ["file-text", "wand-2", "combine", "scissors"]
    
    for icon_name in important_icons:
        if icon_name in ICONS:
            for size in sizes:
                sized_svg = ICONS[icon_name].replace('width="24"', f'width="{size}"')
                sized_svg = sized_svg.replace('height="24"', f'height="{size}"')
                sized_filename = f"{icon_name}-{size}px.svg"
                sized_path = sizes_dir / sized_filename
                
                with open(sized_path, 'w', encoding='utf-8') as f:
                    f.write(sized_svg)
                
                created_files.append(sized_path)
    
    print(f"✓ Creados iconos en {len(sizes)} tamaños para {len(important_icons)} iconos principales")
    
    # Generar archivo Python con los iconos embebidos
    print()
    print("=" * 60)
    print("Generando módulo Python...")
    print("=" * 60)
    print()
    
    python_module = generate_python_module()
    python_path = OUTPUT_DIR / "icons.py"
    
    with open(python_path, 'w', encoding='utf-8') as f:
        f.write(python_module)
    
    print(f"✓ Creado: {python_path.name}")
    
    # Generar archivo Qt Resource (QRC)
    print()
    print("=" * 60)
    print("Generando archivo Qt Resource (.qrc)...")
    print("=" * 60)
    print()
    
    qrc_content = generate_qrc_file()
    qrc_path = OUTPUT_DIR / "icons.qrc"
    
    with open(qrc_path, 'w', encoding='utf-8') as f:
        f.write(qrc_content)
    
    print(f"✓ Creado: {qrc_path.name}")
    
    # Resumen final
    print()
    print("=" * 60)
    print("  ¡Generación completada!")
    print("=" * 60)
    print()
    print(f"Total de archivos creados: {len(created_files) + 2}")
    print()
    print("Estructura de archivos:")
    print(f"  {OUTPUT_DIR}/")
    print(f"    ├── *.svg ({len(ICONS)} iconos)")
    print(f"    ├── colored/ ({len(main_icons) * len(colors)} variantes)")
    print(f"    ├── sizes/ ({len(important_icons) * len(sizes)} tamaños)")
    print(f"    ├── icons.py (módulo Python)")
    print(f"    └── icons.qrc (Qt Resource)")
    print()
    print("Uso en PySide6:")
    print()
    print("  # Opción 1: Cargar desde archivo")
    print("  icon = QIcon('icons/scissors.svg')")
    print()
    print("  # Opción 2: Usar módulo Python")
    print("  from icons.icons import get_icon_svg, ICONS")
    print("  svg_content = ICONS['scissors']")
    print()
    print("  # Opción 3: Usar Qt Resources (después de compilar)")
    print("  # pyside6-rcc icons/icons.qrc -o icons_rc.py")
    print("  # import icons_rc")
    print("  # icon = QIcon(':/icons/scissors.svg')")
    print()


def generate_python_module() -> str:
    """Genera un módulo Python con los iconos embebidos"""
    code = '''"""
Módulo de Iconos SVG para LocalPDF v5
Generado automáticamente - No editar manualmente

Uso:
    from icons import ICONS, get_icon_svg, get_icon_qicon
    
    # Obtener SVG como string
    svg = get_icon_svg('scissors')
    
    # Obtener QIcon directamente
    icon = get_icon_qicon('scissors')
"""

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray


# Diccionario de iconos SVG
ICONS = {
'''
    
    for name, svg_content in ICONS.items():
        # Escapar comillas en el SVG
        svg_escaped = svg_content.replace("'", "\\'").replace('\n', ' ')
        code += f"    '{name}': '''{svg_content}''',\n\n"
    
    code += '''}


def get_icon_svg(name: str) -> str:
    """
    Obtiene el contenido SVG de un icono
    
    Args:
        name: Nombre del icono (ej: 'scissors', 'combine')
    
    Returns:
        String con el contenido SVG
    """
    return ICONS.get(name, ICONS['file-text'])


def get_icon_qicon(name: str, color: str = None) -> QIcon:
    """
    Crea un QIcon desde un icono SVG
    
    Args:
        name: Nombre del icono
        color: Color opcional (ej: '#ffffff', '#000000')
    
    Returns:
        QIcon listo para usar
    """
    svg_content = get_icon_svg(name)
    
    # Cambiar color si se especifica
    if color:
        svg_content = svg_content.replace('stroke="currentColor"', f'stroke="{color}"')
    
    # Crear QIcon desde SVG
    byte_array = QByteArray(svg_content.encode('utf-8'))
    renderer = QSvgRenderer(byte_array)
    
    # Renderizar a pixmap
    pixmap = QPixmap(24, 24)
    pixmap.fill(0x00000000)  # Transparente
    
    from PySide6.QtGui import QPainter
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)


def list_available_icons() -> list:
    """
    Lista todos los iconos disponibles
    
    Returns:
        Lista de nombres de iconos
    """
    return sorted(ICONS.keys())


if __name__ == '__main__':
    print("Iconos disponibles:")
    for icon in list_available_icons():
        print(f"  - {icon}")
'''
    
    return code


def generate_qrc_file() -> str:
    """Genera un archivo Qt Resource (.qrc)"""
    qrc = '''<!DOCTYPE RCC>
<RCC version="1.0">
<qresource prefix="/icons">
'''
    
    # Agregar todos los iconos SVG
    for name in ICONS.keys():
        qrc += f'    <file>{name}.svg</file>\n'
    
    qrc += '''</qresource>
</RCC>'''
    
    return qrc


if __name__ == '__main__':
    try:
        generate_all_icons()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
