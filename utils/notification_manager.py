"""
Sistema de notificaciones (toasts/snackbars) para la interfaz
"""

from typing import Optional

from PySide6.QtCore import QPropertyAnimation, Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QGraphicsOpacityEffect, QLabel, QVBoxLayout


class NotificationManager:
    """Gestor de notificaciones visuales tipo toast"""

    # Tipos de notificación
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

    # Estilos para cada tipo
    STYLES = {
        SUCCESS: """
            background-color: #10b981;
            color: white;
            border-radius: 8px;
            padding: 16px 24px;
            font-size: 14px;
        """,
        ERROR: """
            background-color: #ef4444;
            color: white;
            border-radius: 8px;
            padding: 16px 24px;
            font-size: 14px;
        """,
        WARNING: """
            background-color: #f59e0b;
            color: white;
            border-radius: 8px;
            padding: 16px 24px;
            font-size: 14px;
        """,
        INFO: """
            background-color: #3b82f6;
            color: white;
            border-radius: 8px;
            padding: 16px 24px;
            font-size: 14px;
        """,
    }

    @staticmethod
    def show_notification(
        parent, message: str, notification_type: str = INFO, duration: int = 3000
    ):
        """
        Muestra una notificación temporal

        Args:
            parent: Widget padre
            message: Mensaje a mostrar
            notification_type: Tipo de notificación (SUCCESS, ERROR, WARNING, INFO)
            duration: Duración en milisegundos
        """
        # Crear diálogo de notificación
        notification = QDialog(parent)
        notification.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        notification.setAttribute(Qt.WA_TranslucentBackground)
        notification.setAttribute(Qt.WA_DeleteOnClose)

        # Layout
        layout = QVBoxLayout(notification)
        layout.setContentsMargins(0, 0, 0, 0)

        # Label con el mensaje
        label = QLabel(message)
        label.setWordWrap(True)
        label.setStyleSheet(
            NotificationManager.STYLES.get(
                notification_type, NotificationManager.STYLES[NotificationManager.INFO]
            )
        )
        label.setFont(QFont("Segoe UI", 10))

        layout.addWidget(label)

        # Posicionar en la parte superior derecha
        notification.adjustSize()
        parent_rect = parent.geometry()
        x = parent_rect.x() + parent_rect.width() - notification.width() - 20
        y = parent_rect.y() + 20
        notification.move(x, y)

        # Mostrar
        notification.show()

        # Auto-cerrar después de la duración
        QTimer.singleShot(duration, notification.close)

    @staticmethod
    def show_success(parent, message: str, duration: int = 3000):
        """Muestra notificación de éxito"""
        NotificationManager.show_notification(
            parent, f"✓ {message}", NotificationManager.SUCCESS, duration
        )

    @staticmethod
    def show_error(parent, message: str, duration: int = 4000):
        """Muestra notificación de error"""
        NotificationManager.show_notification(
            parent, f"✗ {message}", NotificationManager.ERROR, duration
        )

    @staticmethod
    def show_warning(parent, message: str, duration: int = 3500):
        """Muestra notificación de advertencia"""
        NotificationManager.show_notification(
            parent, f"⚠ {message}", NotificationManager.WARNING, duration
        )

    @staticmethod
    def show_info(parent, message: str, duration: int = 3000):
        """Muestra notificación informativa"""
        NotificationManager.show_notification(
            parent, f"ℹ {message}", NotificationManager.INFO, duration
        )
