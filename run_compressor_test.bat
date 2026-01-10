@echo off
echo ==================================================
echo CLEANING UP PYCACHE
echo ==================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo.

echo ==================================================
echo RUNNING PDF COMPRESSOR TEST
echo ==================================================
python test_compressor.py
echo.
echo ==================================================
pause
