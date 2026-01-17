"""
Vectora - Aplicación de Escritorio
Punto de entrada principal
"""

import sys

from PySide6.QtWidgets import QApplication

from config.settings import settings
from ui.main_window import MainWindow
from utils.logger import get_logger


def main():
    """Función principal de la aplicación"""

    # Wrapper para capturar errores incluso antes del logger
    try:
        # 0. Inicializar Logger PRIMERO (antes de cualquier otra cosa)
        logger = get_logger("main")
        logger.info("=" * 60)
        logger.info("Iniciando Vectora...")
        logger.info(f"Python: {sys.version}")
        logger.info(f"Plataforma: {sys.platform}")
        logger.info(f"Frozen: {getattr(sys, 'frozen', False)}")
        if getattr(sys, "frozen", False):
            logger.info(f"Ejecutable: {sys.executable}")
            logger.info(f"MEIPASS: {getattr(sys, '_MEIPASS', 'N/A')}")
        logger.info("=" * 60)

        # 1. Asegurar directorios (Lazy initialization)
        logger.debug("Asegurando directorios...")
        settings.ensure_directories()
        logger.debug(f"Directorio base: {settings.BASE_DIR}")
        logger.debug(f"Directorio de salida: {settings.OUTPUT_DIR}")
        logger.debug(f"Directorio temporal: {settings.TEMP_DIR}")

        # 2. Crear aplicación Qt
        logger.debug("Creando QApplication...")
        app = QApplication(sys.argv)
        app.setApplicationName(settings.APP_NAME)
        app.setApplicationVersion(settings.APP_VERSION)
        app.setOrganizationName(settings.APP_AUTHOR)
        logger.debug("QApplication creada exitosamente")

        # 3. Cargar tema inicial
        logger.debug("Cargando tema inicial...")
        from ui.styles.theme_manager import theme_manager

        # El tema se aplica automáticamente en el constructor de ThemeManager
        logger.debug("Tema cargado exitosamente")

        # 4. Crear y mostrar ventana principal
        logger.debug("Creando ventana principal...")
        initial_file = sys.argv[1] if len(sys.argv) > 1 else None
        if initial_file:
            logger.info(f"Archivo inicial: {initial_file}")

        window = MainWindow(initial_file)
        logger.debug("Ventana principal creada exitosamente")

        window.show()
        logger.info("Ventana principal mostrada")
        logger.info("Ejecutando aplicación...")

        # 5. Ejecutar aplicación
        exit_code = app.exec()
        logger.info(f"Aplicación terminada con código: {exit_code}")
        sys.exit(exit_code)

    except KeyboardInterrupt:
        logger = get_logger("main") if "logger" not in locals() else logger
        logger.warning("Aplicación interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        # Intentar loggear incluso si el logger falló
        try:
            logger = get_logger("main") if "logger" not in locals() else logger
            logger.critical(f"Error fatal en la aplicación: {e}", exc_info=True)
        except:
            # Si el logger falla, escribir a stderr y archivo
            error_msg = f"Error fatal antes de inicializar logger: {e}\n"
            import traceback

            error_msg += traceback.format_exc()

            # Intentar escribir a archivo directamente
            try:
                from pathlib import Path

                log_dir = Path.home() / "Documents" / "Vectora" / "logs"
                log_dir.mkdir(exist_ok=True, parents=True)
                from datetime import datetime

                error_log = (
                    log_dir / f"vectora_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                )
                with open(error_log, "w", encoding="utf-8") as f:
                    f.write(error_msg)
                print(f"Error guardado en: {error_log}", file=sys.stderr)
            except:
                pass

            print(error_msg, file=sys.stderr)

        sys.exit(1)


if __name__ == "__main__":
    main()
