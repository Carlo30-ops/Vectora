@echo off
echo ==========================================
echo   Vectora v5 - Builder Mejorado
echo ==========================================

echo 1. Instalando/actualizando pip...
venv\Scripts\python.exe -m pip install --upgrade pip --quiet

echo.
echo 2. Instalando dependencias desde requirements.txt...
venv\Scripts\pip.exe install -r requirements.txt --quiet

echo.
echo 3. Asegurando sistema de iconos...
venv\Scripts\python.exe setup_icons.py

echo.
echo 4. Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo 5. Creando directorios necesarios...
if not exist output mkdir output
if not exist temp mkdir temp
if not exist logs mkdir logs

echo.
echo 6. Generando ejecutable con PyInstaller...
venv\Scripts\pyinstaller.exe Vectora.spec --noconfirm

echo.
echo ==========================================
if exist dist\Vectora\Vectora.exe (
    echo [EXITO] Ejecutable generado correctamente:
    echo    dist\Vectora\Vectora.exe
    echo.
    echo 7. Copiando directorios y archivos necesarios...
    
    REM Copiar directorios de trabajo
    if not exist dist\Vectora\output mkdir dist\Vectora\output
    if not exist dist\Vectora\temp mkdir dist\Vectora\temp
    if not exist dist\Vectora\logs mkdir dist\Vectora\logs
    
    REM Copiar archivo .env si existe
    if exist .env (
        copy /Y .env dist\Vectora\.env > nul
        echo    [OK] Archivo .env copiado
    )
    
    REM Crear archivo README en dist
    (
    echo Vectora v5.0.0 - Editor de PDFs
    echo.
    echo Ubicaciones importantes:
    echo - Logs: %%USERPROFILE%%\Documents\Vectora\logs\
    echo - Salida: output\
    echo - Temporales: temp\
    echo.
    echo Ejecuta: Vectora.exe
    ) > dist\Vectora\README.txt
    
    echo    [OK] Directorios creados
    echo    [OK] Estructura completa
    echo.
    echo ==========================================
    echo Build completado exitosamente!
    echo ==========================================
) else (
    echo [ERROR] Fallo la generacion del ejecutable.
    echo Revisa los errores arriba.
)
echo.
pause

