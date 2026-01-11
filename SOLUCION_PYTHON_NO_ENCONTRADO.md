# 🔧 Solución: Python No Encontrado

**Problema**: El comando `python` no está en el PATH, pero Python está instalado.

**Error**:
```
no se encontró Python; ejecutar sin argumentos para instalar desde el Microsoft Store
```

---

## ✅ Solución Implementada

### Cambios en Scripts

Los scripts ahora usan **`py` (Python Launcher)** que funciona mejor en Windows:

1. **`maintenance/reinstall_env.bat`**:
   - ✅ Detecta Python usando `py -3` primero
   - ✅ Si falla, intenta con `python`
   - ✅ Muestra mensajes claros de error

2. **`vectora.bat`** (opción SETUP):
   - ✅ Usa `py -3` para crear el venv
   - ✅ Fallback a `python` si `py` no funciona
   - ✅ Mensajes de error mejorados

---

## 🚀 Cómo Usar

### Opción 1: Usar el Script de Reparación (Actualizado)

```cmd
maintenance\reinstall_env.bat
```

El script ahora:
1. Detecta Python automáticamente (`py -3` o `python`)
2. Crea el venv con el Python correcto
3. Instala todas las dependencias

### Opción 2: Crear Venv Manualmente

```cmd
REM Usar py (recomendado en Windows)
py -3 -m venv venv
venv\Scripts\pip.exe install -r requirements.txt
```

O si `python` funciona:
```cmd
python -m venv venv
venv\Scripts\pip.exe install -r requirements.txt
```

---

## 🔍 Verificar Python

### Verificar que Python está instalado:
```cmd
py -3 --version
```

Debería mostrar: `Python 3.14.2` (o similar)

### Ver todas las versiones disponibles:
```cmd
py -0
```

### Verificar ubicación:
```cmd
py -3 -c "import sys; print(sys.executable)"
```

---

## ⚠️ Si Python No Está Instalado

### Opción 1: Instalar desde python.org (Recomendado)
1. Ir a https://www.python.org/downloads/
2. Descargar Python 3.10 o superior
3. **IMPORTANTE**: Marcar "Add Python to PATH" durante la instalación
4. Reiniciar terminal

### Opción 2: Instalar desde Microsoft Store
1. Abrir Microsoft Store
2. Buscar "Python 3.14" o "Python 3.12"
3. Instalar
4. El comando `py` debería funcionar automáticamente

---

## 📋 Estado

- ✅ Scripts actualizados para usar `py -3`
- ✅ Detección automática de Python
- ✅ Mensajes de error claros
- ✅ Fallback a `python` si `py` no funciona

---

**Próximo Paso**: Ejecutar `maintenance\reinstall_env.bat` nuevamente
