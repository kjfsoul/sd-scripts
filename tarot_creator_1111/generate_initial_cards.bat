@echo off
echo Generating Initial Cards
echo =====================

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python 3.8 or higher.
    pause
    exit /b
)

REM Check if requirements are installed
pip show requests > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requirements...
    pip install -r requirements.txt
)

pip show Pillow > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Pillow...
    pip install Pillow
)

REM Run the script
python src\tarot_creator.py --initial

echo.
echo If you encountered any errors, please try running:
echo pip install requests Pillow
echo.
pause
