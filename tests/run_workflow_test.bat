@echo off
echo ==================================================
echo CLEANING UP PYCACHE
echo ==================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo.

echo ==================================================
echo RUNNING CORE WORKFLOW TEST
echo ==================================================
python test_workflow.py
echo.
echo ==================================================
pause
