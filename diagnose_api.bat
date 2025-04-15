@echo off
echo Diagnosing Automatic1111 API
echo =========================

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python 3.8 or higher.
    pause
    exit /b
)

REM Check if requests is installed
pip show requests > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requests...
    pip install requests
)

REM Run the diagnostic script
python diagnose_api.py

echo.
echo If you're seeing 500 server errors, it could be due to:
echo 1. The model is still loading in Automatic1111
echo 2. There's not enough VRAM/RAM available
echo 3. The prompt is too complex or contains problematic elements
echo 4. There's an issue with the Automatic1111 installation
echo.
echo Try restarting Automatic1111 and waiting a few minutes before running this script again.
echo.
pause
