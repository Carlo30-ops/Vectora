@echo off
echo ==========================================
echo   TODO EN UNO - Completar Fase 1 Rapida
echo ==========================================
echo.
echo Este script ejecuta todas las tareas rapidas de la Fase 1:
echo 1. Instalar PyInstaller
echo 2. Generar requirements.txt completo
echo 3. Verificar salud del proyecto
echo.
pause

REM 1. Instalar PyInstaller
echo.
echo ==========================================
echo PASO 1: Instalando PyInstaller
echo ==========================================
call install_pyinstaller.bat

if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de PyInstaller
    pause
    exit /b 1
)

REM 2. Generar requirements.txt
echo.
echo ==========================================
echo PASO 2: Generando requirements.txt
echo ==========================================
call generate_requirements.bat

REM 3. Verificar salud
echo.
echo ==========================================
echo PASO 3: Verificando salud del proyecto
echo ==========================================
call check_project_health.bat

echo.
echo ==========================================
echo FASE 1 (TAREAS RAPIDAS) COMPLETADA
echo ==========================================
echo.
echo Proximos pasos sugeridos:
echo - Implementar sistema de logging
echo - Crear suite de tests
echo - Agregar icono al ejecutable
echo - Actualizar README
echo.
pause
