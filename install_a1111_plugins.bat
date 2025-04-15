@echo off
echo Automatic1111 Plugin Installer for Tarot Card Generation
echo =====================================================
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

REM Check if Git is installed
git --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in your PATH.
    echo Please install Git and try again.
    echo.
    pause
    exit /b
)

echo This tool will install recommended plugins for Automatic1111 to enhance
echo your tarot card generation project.
echo.
echo These plugins will add functionality for:
echo - Image organization and tagging
echo - Prompt engineering and autocompletion
echo - LoRA and textual inversion support
echo - Dataset building and management
echo - Visual analysis and composition control
echo.
echo Press any key to continue...
pause > nul

REM Run the plugin installer
python install_a1111_plugins.py

echo.
echo Press any key to exit...
pause > nul
