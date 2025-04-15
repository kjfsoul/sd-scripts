@echo off
echo Tarot Deck Style Analyzer
echo =======================
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

echo This tool will analyze your prompt files to suggest a cohesive style for your entire tarot deck.
echo.
echo It will:
echo - Scan all prompt files in the reference/prompts directory
echo - Identify common art styles, phrases, and descriptive words
echo - Detect artist names mentioned in the prompts
echo - Generate a suggested style prompt for your entire deck
echo.

REM Check if prompt directory exists and has files
if not exist "reference\prompts\*.txt" (
    echo No prompt files found in reference\prompts directory.
    echo Please run the image scanner first to generate prompts.
    echo.
    pause
    exit /b
)

echo Press any key to analyze your deck style...
pause > nul

REM Run the analyzer script
python analyze_deck_style.py

REM Check if the script ran successfully
if %errorlevel% neq 0 (
    echo.
    echo ERROR: The analyzer script encountered an error.
    echo.
    pause
    exit /b
)

echo.
echo Press any key to open the generated style file...
pause > nul

REM Open the style file if it exists
if exist "deck_style.txt" (
    start notepad "deck_style.txt"
) else (
    echo.
    echo WARNING: The style file was not created.
)

echo.
echo Press any key to exit...
pause > nul
