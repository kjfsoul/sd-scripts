@echo off
echo Tarot Card Feedback Interface
echo ==========================
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

echo This tool provides a user-friendly interface to:
echo - View generated tarot cards
echo - Provide detailed feedback on each card
echo - Rate different aspects of each card
echo - Edit prompts and regenerate cards
echo - Quickly accept or reject cards
echo.
echo Keyboard shortcuts:
echo - Left/Right arrows: Navigate between cards
echo - A: Accept current card
echo - R: Reject current card
echo - S: Save feedback
echo.
echo Press any key to launch the feedback interface...
pause > nul

REM Run the feedback interface
python user_feedback_interface.py

echo.
echo Press any key to exit...
pause > nul
