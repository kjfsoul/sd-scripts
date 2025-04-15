@echo off
echo Installing Dependencies
echo ====================

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python 3.8 or higher.
    pause
    exit /b
)

echo Installing required packages...
pip install requests Pillow

echo.
echo Dependencies installed successfully.
echo.
pause
