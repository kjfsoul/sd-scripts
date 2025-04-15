@echo off
echo Installing Dependencies for Tarot Deck Creation System
echo ================================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in your PATH.
    echo Please install Python 3.8 or higher.
    echo.
    pause
    exit /b
)

echo Installing required packages...
pip install requests Pillow tk

echo.
echo Creating required directories...

REM Create directory structure using Python script
python create_directory_structure.py

echo.
echo Dependencies installed and directories created successfully.
echo.
echo Next steps:
echo 1. Make sure Automatic1111 is running with the API enabled
echo 2. Place reference images in the reference/images directory
echo 3. Run tarot_master.bat to start the system
echo.
pause
