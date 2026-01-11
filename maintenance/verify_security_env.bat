@echo off
setlocal

:: ==========================================
::   Vectora Verification Script
:: ==========================================

:: 1. Define Root Directory (One level up from maintenance)
set "PROJECT_ROOT=%~dp0.."
set "PYTHONPATH=%PROJECT_ROOT%"
cd /d "%PROJECT_ROOT%"

echo [INFO] PYTHONPATH set to: %PYTHONPATH%

:: 2. Run Unit Tests via Pytest
echo.
echo ==========================================
echo   Running Unit Tests...
echo ==========================================
python -m pytest tests/test_pdf_security.py -v

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Tests failed!
    pause
    exit /b 1
)

:: 3. Create Temporary UI Launcher
echo.
echo ==========================================
echo   Launching Security Widget Preview...
echo ==========================================
set "LAUNCHER=debug_security_launch.py"

(
echo import sys
echo from PySide6.QtWidgets import QApplication
echo from ui.components.operation_widgets.security_widget import SecurityWidget
echo.
echo if __name__ == "__main__":
echo     app = QApplication(sys.argv^)
echo     try:
echo         window = SecurityWidget(^)
echo         window.resize(800, 600^)
echo         window.show(^)
echo         print("[INFO] Widget launched successfully."^)
echo         sys.exit(app.exec(document^)^) # Using 'document' is a typo in echo, careful. sys.exit(app.exec())
echo     except Exception as e:
echo         print(f"[ERROR] Launch failed: {e}"^)
echo         sys.exit(1^)
) > "%LAUNCHER%"

:: Fix typo in the echo above for app.exec
(
echo import sys
echo from PySide6.QtWidgets import QApplication
echo from ui.components.operation_widgets.security_widget import SecurityWidget
echo.
echo if __name__ == "__main__":
echo     app = QApplication(sys.argv^)
echo     try:
echo         window = SecurityWidget(^)
echo         window.resize(800, 600^)
echo         window.show(^)
echo         print("[INFO] Widget launched successfully."^)
echo         sys.exit(app.exec(^) ^)
echo     except Exception as e:
echo         print(f"[ERROR] Launch failed: {e}"^)
echo         sys.exit(1^)
) > "%LAUNCHER%"

:: 4. Run Launcher
python "%LAUNCHER%"

:: 5. Cleanup
if exist "%LAUNCHER%" del "%LAUNCHER%"

echo.
echo [DONE] Verification completed.
pause
