@echo off
echo Enhanced Tarot Card Generator
echo ===========================
echo.
echo This program will help you create custom tarot card images
echo with your own style and descriptions.
echo.

REM Check if Automatic1111 is running
powershell -Command "if ((Get-NetTCPConnection -LocalPort 7860 -ErrorAction SilentlyContinue).Count -gt 0) { exit 0 } else { exit 1 }" > nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Automatic1111 does not appear to be running on port 7860.
    echo Please make sure Automatic1111 is running with the API enabled.
    echo.
    echo Would you like to continue anyway? (Y/N)
    set /p continue="> "
    if /i not "%continue%"=="Y" exit /b
)

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

echo.
echo Starting the tarot card generator...
echo.
echo You will be asked to:
echo 1. Define your artistic style
echo 2. Choose whether to provide custom descriptions
echo 3. Select how many variations to generate for each card
echo.
echo Press any key to continue...
pause > nul

REM Run the enhanced generator
python simple_generator.py

echo.
echo If you're seeing errors, please run diagnose_api.bat to troubleshoot.
echo.
echo Press any key to open the images folder...
pause > nul

REM Open the images folder
start explorer "%~dp0images\cards"

echo.
pause
