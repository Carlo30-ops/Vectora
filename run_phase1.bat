@echo off
echo Iniciando aplicacion de Fase 1...
python apply_phase1.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Fase 1 completada exitosamente.
    echo Se han actualizado los servicios de backend y se ha creado la infraestructura core.
) else (
    echo.
    echo Hubo un error al aplicar la fase 1.
)
pause
