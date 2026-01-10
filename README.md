# 📄 Vectora v5

![Version](https://img.shields.io/badge/version-5.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-27%20passed-success.svg)
![Coverage](https://img.shields.io/badge/coverage-70%25-orange.svg)

**Vectora** (anteriormente LocalPDF) es una potente herramienta de escritorio para la manipulación de archivos PDF. Diseñada con privacidad y eficiencia en mente, procesa todos tus documentos localmente sin subirlos a la nube.

---

## ✨ Características Principales

- **🔒 100% Local y Privado**: Tus archivos nunca salen de tu computadora.
- **📑 Combinar PDFs**: Une múltiples documentos en uno solo con ordenamiento drag-and-drop.
- **✂️ Dividir PDFs**: Extrae rangos, páginas específicas o divide en partes iguales.
- **📉 Compresión**: Reduce el tamaño de tus archivos manteniendo la calidad.
- **🔄 Conversión**: Transforma PDF a Word, Imágenes a PDF y viceversa.
- **👁️ OCR (Reconocimiento de Texto)**: Extrae texto de imágenes y PDFs escaneados.
- **🛡️ Seguridad**: Encripta y desencripta tus documentos.
- **🎨 Tema Dinámico**: Modo claro y oscuro integrados.

---

## 🚀 Instalación y Uso

### Prerrequisitos

- Python 3.10 o superior
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (para funciones de OCR)
- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) (para manipulación de imágenes PDF)

### Configuración Rápida (Desarrollo)

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/tu-usuario/vectora.git
   cd vectora
   ```

2. **Ejecutar Setup Automático** (Windows)

   ```cmd
   quick_setup.bat
   ```

   Este script creará el entorno virtual, instalará dependencias y configurará carpetas.

3. **Ejecutar la Aplicación**
   ```cmd
   venv\Scripts\python main.py
   ```

### Generar Ejecutable (.exe)

Para crear una versión portable de Vectora:

```cmd
build_exe.bat
```

El ejecutable se generará en `dist/Vectora/Vectora.exe`.

---

## 🛠️ Desarrollo y Testing

### Estructura del Proyecto

```
Vectora/
├── backend/          # Lógica de negocio y servicios
├── ui/               # Interfaz gráfica (PySide6)
├── utils/            # Utilidades (Logger, Validadores)
├── config/           # Configuraciones y Settings
├── tests/            # Suite de pruebas automatizadas
├── docs/             # Documentación adicional
└── assets/           # Recursos estáticos (Iconos, imágenes)
```

### Ejecutar Tests

El proyecto cuenta con una suite de tests robusta usando `pytest`.

```cmd
run_tests.bat
```

O directamente:

```bash
venv\Scripts\python -m pytest tests/
```

### Logging

Los logs se guardan automáticamente en:

- Desarrollo: `./logs/`
- Producción: `Documentos/Vectora/logs/`

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) para detalles sobre nuestro código de conducta y el proceso para enviar pull requests.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

_Desarrollado con ❤️ por el equipo Vectora._
