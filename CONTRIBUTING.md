# Guía de Contribución para Vectora

¡Gracias por tu interés en contribuir a Vectora! Este documento establece las pautas para asegurar un desarrollo de alta calidad y un flujo de trabajo eficiente.

## Estándares de Código

### 1. Estilo y Formato

Utilizamos herramientas estándar para mantener la consistencia:

- **Formato**: `black` (line-length 100)
- **Imports**: `isort`
- **Tipado**: `mypy`

Antes de realizar un commit, ejecuta:

```batch
maintenance\clean_code.bat
```

### 2. Estructura de Docstrings

Todos los módulos, clases y funciones públicas deben tener docstrings siguiendo el estilo de Google:

```python
def function(arg1: int, arg2: str) -> bool:
    """
    Descripción breve de la función.

    Args:
        arg1: Descripción del argumento 1.
        arg2: Descripción del argumento 2.

    Returns:
        bool: Descripción del valor de retorno.

    Raises:
        ValueError: Si los argumentos son inválidos.
    """
```

### 3. Manejo de Errores y Logging

- **NO** usar `print()`. Utiliza siempre el sistema de logging:
  ```python
  from utils.logger import get_logger
  logger = get_logger(__name__)
  logger.info("Mensaje")
  ```
- Retornar siempre `OperationResult` en servicios del backend.

## Flujo de Trabajo

1. **Ramas**: Crea una rama para tu feature o fix (`feature/nueva-funcionalidad` o `fix/bug-descripcion`).
2. **Tests**: Asegúrate de que los tests existentes pasen y agrega nuevos si es necesario.
   ```batch
   vectora.bat -> Opcion 3 (Tests)
   ```
3. **Commit**: Usa mensajes claros y descriptivos.

## Reporte de Bugs

Al reportar un bug, incluye:

- Pasos para reproducir.
- Comportamiento esperado vs actual.
- Logs relevantes (`Documents/Vectora/logs`).

## Estructura del Proyecto

- `backend/`: Lógica de negocio y servicios.
- `ui/`: Interfaz gráfica (PySide6).
- `utils/`: Utilidades transversales.
- `docs/`: Documentación técnica.
- `tests/`: Tests unitarios e integración.
