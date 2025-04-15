@echo off
echo Simple Tarot Card Generator
echo ========================

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python 3.8 or higher.
    pause
    exit /b
)

REM Check if required packages are installed
pip show requests > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requests...
    pip install requests
)

pip show Pillow > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Pillow...
    pip install Pillow
)

REM Run the simplified generator
python simple_generator.py

echo.
echo If you're still seeing errors, please run diagnose_api.bat to troubleshoot.
echo.
pause
