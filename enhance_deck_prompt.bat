@echo off
echo Tarot Deck Prompt Enhancer
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

echo This tool will enhance and refine your deck style prompt by:
echo - Removing redundant terms
echo - Organizing terms into categories (art styles, artists, descriptors, subjects)
echo - Creating a more coherent and usable prompt
echo.

REM Check if deck style file exists
if not exist "deck_style.txt" (
    echo No deck_style.txt file found.
    echo Please run the style analyzer first to generate a deck style.
    echo.
    echo Would you like to enter a prompt manually? (Y/N)
    set /p manual_prompt="Enter Y or N: "
    
    if /i "%manual_prompt%"=="Y" (
        echo.
        echo Enter your prompt below:
        set /p prompt="Prompt: "
        
        echo.
        echo Enhancing prompt...
        python enhance_deck_prompt.py --prompt "%prompt%"
    ) else (
        echo Exiting.
        pause
        exit /b
    )
) else (
    echo Found deck_style.txt file.
    echo Enhancing the prompt...
    python enhance_deck_prompt.py
)

REM Check if the script ran successfully
if %errorlevel% neq 0 (
    echo.
    echo ERROR: The enhancer script encountered an error.
    echo.
    pause
    exit /b
)

echo.
echo Press any key to open the enhanced prompt file...
pause > nul

REM Open the enhanced prompt file if it exists
if exist "enhanced_deck_style.txt" (
    start notepad "enhanced_deck_style.txt"
) else (
    echo.
    echo WARNING: The enhanced prompt file was not created.
)

echo.
echo Press any key to exit...
pause > nul
