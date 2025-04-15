@echo off
echo Enhanced Tarot Card Generator
echo ===========================
echo.
echo This program will help you create custom tarot card images
echo with your own style and descriptions.
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
echo Starting the tarot card generator...
echo.
echo You will be asked to:
echo 1. Define your artistic style
echo 2. Choose whether to provide custom descriptions
echo 3. Select how many variations to generate for each card
echo.
echo Press any key to continue...
pause > nul

REM Run the generator script
echo Running generator script...
python simple_generator.py

REM Check if the script ran successfully
if %errorlevel% neq 0 (
    echo.
    echo ERROR: The generator script encountered an error.
    echo Please check if Automatic1111 is running with the API enabled.
    echo You can run diagnose_api.bat to troubleshoot API issues.
    echo.
    pause
    exit /b
)

echo.
echo If you're seeing errors, please run diagnose_api.bat to troubleshoot.
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
