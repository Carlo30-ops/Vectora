# Changelog

Todas las mejoras notables de este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.0] - 2026-01-10

### 🚀 Novedades

- **Sistema de Logging Profesional**: Implementado módulo `utils/logger.py` con rotación automática de logs, múltiples niveles y formateo consistente. Integrado en servicios backend y UI.
- **Suite de Tests Automatizados**: 27 tests implementados cubriendo `PDFMerger` y `PDFSplitter`. Incluye fixtures reutilizables y reportes de cobertura.
- **Build System Mejorado**: Scripts `.bat` optimizados para instalación (`quick_setup.bat`), verificación (`check_project_health.bat`) y compilación (`build_exe.bat`).
- **Gestión de Dependencias**: `requirements.txt` con versiones exactas y script de generación automática.

### 🔧 Mejoras Técnicas

- **Estructura del Proyecto**: Limpieza de archivos y organización estándar (`backend/`, `ui/`, `utils/`, `tests/`).
- **Configuración**: Archivo `.gitignore` optimizado para Python, PyInstaller y entornos virtuales.
- **Instalador**: Solución de problemas en `setup_icons.py` (dependencia opcional) y `Vectora.spec` (rutas corregidas).

### 🐛 Correcciones

- Corregido error de referencia a carpeta `libs/` inexistente en el spec de PyInstaller.
- Corregido manejo de dependencia `requests` para descarga de iconos.

## [Pre-5.0.0] - Versiones Anteriores

- Funcionalidades base: Combinar, Dividir, Comprimir, Convertir, OCR.
- Interfaz gráfica base con PySide6.
