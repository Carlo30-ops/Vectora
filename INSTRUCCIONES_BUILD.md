# 📋 Instrucciones para Generar el .exe

**Fecha**: 2026-01-10  
**Versión**: Vectora v5.0.0

---

## 🚀 Pasos para Generar el Ejecutable

### Opción 1: Usando `vectora.bat` (Recomendado)

1. **Abrir `vectora.bat`** (doble clic o desde línea de comandos)

2. **Seleccionar opción [4] BUILD**

3. **Elegir tipo de build**:
   - **[1] RELEASE** - Para distribución (sin consola)
   - **[2] DEBUG** - Para depuración (con consola para ver errores)

4. **Esperar a que compile** (puede tardar varios minutos)

5. **Ubicación del .exe**:
   - RELEASE: `dist\Vectora\Vectora.exe`
   - DEBUG: `dist\Vectora_debug\Vectora_debug.exe`

---

### Opción 2: Manualmente desde Línea de Comandos

#### Para RELEASE (sin consola):
```cmd
venv\Scripts\activate
pyinstaller Vectora.spec --noconfirm
```

#### Para DEBUG (con consola):
```cmd
venv\Scripts\activate
pyinstaller Vectora_debug.spec --noconfirm
```

---

## ⚠️ Si el .exe No Abre

### Paso 1: Compilar Versión DEBUG
1. Ejecutar `vectora.bat`
2. Seleccionar **[4] BUILD**
3. Seleccionar **[2] DEBUG**
4. Ejecutar `dist\Vectora_debug\Vectora_debug.exe` desde línea de comandos
5. Ver errores en la consola

### Paso 2: Revisar Logs
- **En desarrollo**: `logs\vectora_YYYY-MM-DD.log`
- **En .exe**: `%USERPROFILE%\Documents\Vectora\logs\vectora_YYYY-MM-DD.log`

### Paso 3: Verificar Errores Comunes
- Archivos faltantes en `dist/Vectora/`
- DLLs de PySide6 no incluidas
- Rutas incorrectas en modo frozen

---

## ✅ Verificaciones Pre-Build

El script `vectora.bat` ahora ejecuta automáticamente:
- ✅ Verificación de imports (`test_imports.py`)
- ✅ Actualización de pip
- ✅ Verificación de PyInstaller
- ✅ Limpieza de builds anteriores
- ✅ Creación de directorios necesarios

---

## 📦 Contenido del .exe

El ejecutable incluye:
- ✅ Todos los módulos Python necesarios
- ✅ Carpetas: `config/`, `ui/`, `backend/`, `utils/`
- ✅ Carpetas opcionales: `assets/`, `icons/` (si existen)
- ✅ Archivo `.env` (si existe)
- ✅ Todas las DLLs de PySide6
- ✅ Dependencias de procesamiento PDF

---

## 🎯 Cambios Incluidos en Esta Versión

- ✅ Drag & Drop implementado en todos los widgets
- ✅ Validaciones mejoradas
- ✅ Manejo de errores mejorado
- ✅ `settings.get_output_directory()` corregido
- ✅ Mejor logging y manejo de errores

---

## 📝 Notas Importantes

1. **Primera compilación**: Puede tardar 5-10 minutos
2. **Tamaño del .exe**: ~50-100 MB (incluye PySide6 y dependencias)
3. **Versión DEBUG**: Úsala solo para depuración, no para distribución
4. **Logs**: Siempre revisa los logs si hay problemas

---

**Listo para compilar** ✅
