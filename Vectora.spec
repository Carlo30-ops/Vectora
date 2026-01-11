# -*- mode: python ; coding: utf-8 -*-
# Vectora v5.0.0 - PyInstaller Spec File

import os
from pathlib import Path

block_cipher = None

# Determinar qué carpetas incluir (solo las que existen)
datas_list = []

# Carpetas principales (siempre incluir)
for folder in ['config', 'ui', 'backend', 'utils']:
    if os.path.exists(folder):
        datas_list.append((folder, folder))

# Carpetas opcionales
optional_folders = ['assets', 'icons']
for folder in optional_folders:
    if os.path.exists(folder):
        datas_list.append((folder, folder))

# Archivo .env (opcional)
if os.path.exists('.env'):
    datas_list.append(('.env', '.'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas_list,
    hiddenimports=[
        'pikepdf._cpphelpers',
        'PySide6.QtSvg',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'logging.handlers',
        'utils.logger',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib'],  # Excluir módulos no necesarios
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Icono (opcional)
icon_path = 'assets/vectora.ico'
if not os.path.exists(icon_path):
    icon_path = None  # Si no existe, PyInstaller usará el icono por defecto

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Vectora',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Sin consola para app de escritorio
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    icon=icon_path,  # Icono oficial (opcional)
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Vectora',
)

