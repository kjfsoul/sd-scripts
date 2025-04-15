@echo off
echo Basic Tarot Card Generator
echo ========================
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

REM Check if required packages are installed
echo Checking required packages...
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
echo Starting the basic tarot card generator...
echo.
echo Make sure Automatic1111 is running with the API enabled.
echo.
echo Press any key to continue...
pause > nul

REM Run the basic generator script
python basic_tarot_generator.py

echo.
echo Press any key to open the images folder...
pause > nul

REM Open the images folder if it exists
if exist "images\cards" (
    start explorer "images\cards"
) else (
    echo.
    echo WARNING: The images folder does not exist.
    echo This may indicate that no images were generated.
)

echo.
echo Press any key to exit...
pause > nul
