@echo off
echo ==================================================
echo CLEANING UP PYCACHE
echo ==================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo.

echo ==================================================
echo RUNNING PDF MERGER TEST
echo ==================================================
python test_merger.py
echo.
echo ==================================================
pause
