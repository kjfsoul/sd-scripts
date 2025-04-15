@echo off
echo Tarot Reference Database Setup
echo ============================
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

echo This tool will create a comprehensive reference database of tarot card information:
echo - Symbolism for each card (visual elements and their meanings)
echo - Upright and reversed meanings
echo - Color associations
echo - Elemental associations
echo.
echo This database can be used by the prompt refiner to create more accurate
echo and symbolically rich tarot card prompts.
echo.
echo Press any key to continue...
pause > nul

REM Run the tarot reference database setup
python setup_tarot_reference_db.py

echo.
echo Press any key to exit...
pause > nul
