@echo off
echo Enhanced Dependencies Installer for Tarot Card Generation
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

echo This tool will install additional Python packages to enhance
echo your tarot card generation project.
echo.
echo These packages will add functionality for:
echo - Advanced image processing and analysis
echo - Data organization and management
echo - Web scraping for tarot card references
echo - Machine learning model integration
echo - User interface improvements
echo.
echo Press any key to continue...
pause > nul

REM Run the enhanced dependencies installer
python install_enhanced_dependencies.py

echo.
echo Press any key to exit...
pause > nul
