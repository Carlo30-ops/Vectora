@echo off
setlocal
echo ==========================================
echo Vectora Backend Cleanup Script
echo ==========================================

set "BACKUP_DIR=backup_legacy_%date:~-4,4%%date:~-7,2%%date:~-10,2%"
set "TARGET_DIR=Vectora\Vectora"

echo [1/3] Creando respaldo de seguridad en %BACKUP_DIR%...
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
xcopy /E /I /Y "Vectora\Vectora" "%BACKUP_DIR%"

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo al crear respaldo. Abortando limpieza.
    exit /b 1
)

echo [2/3] Eliminando directorio duplicado %TARGET_DIR%...
rmdir /S /Q "Vectora\Vectora"

if exist "Vectora\Vectora" (
    echo [ERROR] No se pudo eliminar el directorio completamente.
    exit /b 1
) else (
    echo [OK] Directorio eliminado exitosamente.
)

echo [3/3] Limpieza completada.
echo La carpeta duplicada ha sido movida a: %BACKUP_DIR%
echo Por favor verifica que la aplicacion sigue funcionando correctamente.
pause
