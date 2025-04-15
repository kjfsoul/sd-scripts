@echo off
mode con: cols=80 lines=30
color 0A

echo ========================================================
echo             TAROT DECK CREATION SYSTEM
echo ========================================================
echo.
echo Welcome to the Tarot Deck Creation System!
echo.
echo This system allows you to create your own tarot card deck
echo using Stable Diffusion and a guided workflow.
echo.
echo Please choose a mode:
echo.
echo [1] Guided Mode
echo     - Step-by-step workflow with clear instructions
echo     - Opens documentation automatically
echo     - Ideal for first-time users
echo.
echo [2] Manual Mode
echo     - Access to all tools through the Master Control Panel
echo     - More flexibility for experienced users
echo     - Choose your own workflow
echo.
echo [3] View Documentation
echo     - Open the Tarot Creation Guide
echo     - Learn about the recommended workflow
echo     - Get tips for effective prompt refinement
echo.
echo [4] Create Desktop Shortcuts
echo     - Create shortcuts for all modes
echo     - Quick access from your desktop
echo     - Includes Simple Guided Mode shortcut
echo.
echo [5] Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    cls
    echo Starting Guided Mode...
    call simple_guided_mode.bat
) else if "%choice%"=="2" (
    cls
    echo Starting Manual Mode...
    call one_click_tarot_improved.bat
) else if "%choice%"=="3" (
    cls
    echo Opening Documentation...
    start "" "TAROT_CREATION_GUIDE.md"
    timeout /t 2 /nobreak > nul
    call tarot_launcher.bat
) else if "%choice%"=="4" (
    cls
    echo Creating Desktop Shortcuts...
    call create_guided_shortcut.bat
    call create_improved_shortcut.bat
    call create_simple_guided_shortcut.bat
    call create_launcher_shortcut.bat
    echo.
    echo Shortcuts created successfully!
    echo.
    echo Press any key to return to the launcher...
    pause > nul
    call tarot_launcher.bat
) else if "%choice%"=="5" (
    cls
    echo Thank you for using the Tarot Deck Creation System!
    echo.
    echo Exiting...
    timeout /t 2 /nobreak > nul
    exit /b
) else (
    cls
    echo Invalid choice. Please try again.
    echo.
    timeout /t 2 /nobreak > nul
    call tarot_launcher.bat
)
