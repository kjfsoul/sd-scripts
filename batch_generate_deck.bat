@echo off
echo Batch Tarot Deck Generator
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

echo This tool will generate a complete tarot deck in batches.
echo.
echo What would you like to do?
echo 1. Configure batch settings
echo 2. Generate Major Arcana only
echo 3. Generate full deck
echo 4. Generate custom range
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    python batch_generate_deck.py --configure
) else if "%choice%"=="2" (
    python batch_generate_deck.py --major-only
) else if "%choice%"=="3" (
    python batch_generate_deck.py
) else if "%choice%"=="4" (
    echo.
    set /p start="Enter start index (0-77): "
    set /p end="Enter end index (%start%-77): "
    python batch_generate_deck.py --start %start% --end %end%
) else (
    echo Exiting.
    exit /b
)

echo.
echo Press any key to open the images folder...
pause > nul

REM Open the images folder if it exists
if exist "images\cards" (
    start explorer "images\cards"
) else (
    echo.
    echo WARNING: The images folder does not exist.
    echo This may indicate that no images were generated.
)

echo.
echo Press any key to exit...
pause > nul
