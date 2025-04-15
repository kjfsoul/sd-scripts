@echo off
echo Tarot Card Prompt Refiner
echo ======================
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
pip show Pillow > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Pillow...
    pip install Pillow
)

echo This tool provides a comprehensive interface to create and refine prompts for tarot cards:
echo.
echo Features:
echo - Select from 22 Major Arcana cards with keywords
echo - Choose from pre-defined style templates
echo - Add suggestions from different categories (Art Style, Color Palette, etc.)
echo - Add artist influences
echo - Edit and customize negative prompts
echo - Preview the final prompt with composition guidance
echo - Save prompts for each card
echo.
echo Press any key to launch the Prompt Refiner...
pause > nul

REM Run the prompt refiner
python prompt_refiner.py

echo.
echo Press any key to exit...
pause > nul
