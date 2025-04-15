@echo off
echo Scan Reference Images
echo ===================
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
echo This tool will scan your reference images and generate prompts.
echo.
echo Before continuing:
echo 1. Make sure Automatic1111 is running with the API enabled
echo 2. Place your reference images in the "reference/images" folder
echo.

REM Create the reference directory if it doesn't exist
if not exist "reference\images" (
    echo Creating reference image directory...
    mkdir "reference\images" 2>nul
    echo.
    echo Please place your reference images in the "reference\images" folder
    echo and then run this script again.
    echo.
    start explorer "reference\images"
    pause
    exit /b
)

echo Press any key to continue...
pause > nul

REM Run the advanced generator script with scan option
python advanced_tarot_generator.py --scan

REM Check if the script ran successfully
if %errorlevel% neq 0 (
    echo.
    echo ERROR: The script encountered an error.
    echo Please check if Automatic1111 is running with the API enabled.
    echo.
    pause
    exit /b
)

echo.
echo Press any key to open the prompts folder...
pause > nul

REM Open the prompts folder if it exists
if exist "reference\prompts" (
    start explorer "reference\prompts"
) else (
    echo.
    echo WARNING: The prompts folder does not exist.
    echo This may indicate that no prompts were generated.
)

echo.
echo Press any key to exit...
pause > nul
