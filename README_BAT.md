# Scripts y Herramientas - Vectora

## Script Principal: `vectora.bat`

**Vectora** ahora tiene un único script maestro que consolida todas las funcionalidades anteriores.

### Ejecutar el Panel de Control

```cmd
vectora.bat
```

### Opciones Disponibles

1. **SETUP** - Configurar entorno inicial
   - Crea entorno virtual si no existe
   - Instala dependencias desde requirements.txt
   - Crea directorios necesarios (temp, output, assets, logs)
   - Genera archivo .env básico si no existe

2. **RUN** - Ejecutar aplicación (modo desarrollo)
   - Ejecuta `main.py` usando el entorno virtual

3. **TEST** - Ejecutar suite de tests
   - Instala pytest si es necesario
   - Ejecuta todos los tests con verbose
   - Genera reporte de coverage en HTML

4. **BUILD** - Generar ejecutable (.exe)
   - Verifica/instala PyInstaller
   - Prepara sistema de iconos
   - Limpia builds anteriores
   - Genera ejecutable usando Vectora.spec
   - Configura estructura final en dist/

5. **VERIFY** - Verificar entorno y salud del proyecto
   - Verifica Python instalado
   - Verifica entorno virtual
   - Lista dependencias instaladas
   - Verifica estructura del proyecto

6. **TOOLS** - Herramientas adicionales
   - Generar requirements.txt
   - Instalar/actualizar PyInstaller
   - Verificar entorno Python
   - Generar iconos

7. **CLEAN** - Limpiar archivos temporales
   - Elimina build/ y dist/
   - Limpia __pycache__ y *.pyc
   - Limpia cache de pytest
   - Limpia logs antiguos (más de 7 días)

## Scripts Python de Herramientas

### En la raíz del proyecto

- `main.py` - Punto de entrada de la aplicación
- `setup_icons.py` - Configuración de iconos SVG (usado en build)
- `generate_icons.py` - Generación de iconos SVG

### En `tools/`

- `apply_backend_refactor.py` - Herramientas de refactorización (si necesario)
- `create_icon.py` - Generación de iconos .ico desde PNG
- `fix_icons.py` - Generación de icono .ico básico (sin PNG)

## Notas

- Todos los scripts .bat obsoletos han sido eliminados
- El script maestro `vectora.bat` consolida todas las funciones
- Los scripts de herramientas Python se mantienen según necesidad