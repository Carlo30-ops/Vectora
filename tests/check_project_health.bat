@echo off
setlocal enabledelayedexpansion
title Vectora V5 - Diagnostico de Salud

:: Obtener la ruta raiz del proyecto
set "ROOT_DIR=%~dp0.."
pushd "%ROOT_DIR%"

echo ===================================================
echo    VECTORA V5 - DIAGNOSTICO DE SALUD
echo ===================================================
echo.

set "BAD_COUNT=0"

:: 1. Entorno
echo [1/5] Verificando Entorno...
if exist venv (
    echo [OK] Entorno virtual detectado.
) else (
    echo [MISSING] venv no encontrado.
    set /a BAD_COUNT+=1
)

:: 2. Backend (Actualizado post Fase 1)
echo.
echo [2/5] Servicios Backend (V5)...
for %%s in (pdf_merger.py pdf_splitter.py pdf_compressor.py pdf_converter.py pdf_security.py ocr_service.py batch_processor.py) do (
    set "FILE=backend\services\%%s"
    if exist "!FILE!" (
        findstr "OperationResult" "!FILE!" >nul
        if !ERRORLEVEL! EQU 0 (
            echo [OK] %%s: V5 Standard
        ) else (
            echo [LEGACY] %%s: Requiere migrar
            set /a BAD_COUNT+=1
        )
    ) else (
        echo [MISSING] %%s: No encontrado
        set /a BAD_COUNT+=1
    )
)

:: 3. UI Widgets
echo.
echo [3/5] Widgets UI...
for %%w in (merge_widget.py split_widget.py compress_widget.py convert_widget.py security_widget.py ocr_widget.py batch_widget.py) do (
    if not exist "ui\components\operation_widgets\%%w" set /a BAD_COUNT+=1
)
echo [INFO] Analisis de widgets completado.

:: Result Message
echo.
if !BAD_COUNT! EQU 0 (
    set "MSG=Proyecto en perfecto estado (10/10). Todo estandarizado."
    set "ICON=Information"
) else (
    set "MSG=Se han detectado !BAD_COUNT! problemas o componentes pendientes. Revisa la consola."
    set "ICON=Warning"
)

powershell -Command "[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('!MSG!', 'Vectora V5 - Diagnostico', 'OK', '!ICON!')"

echo ===================================================
echo    DIAGNOSTICO FINALITADO
echo ===================================================
popd
pause
