@echo off
echo Tarot Card Element Adder
echo =====================
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

echo This tool will add borders, nameplates, and numerals to your tarot card images.
echo.
echo Before continuing, make sure you have:
echo 1. Generated tarot card images in the images/cards directory
echo 2. Added border images to the elements/borders directory (optional)
echo 3. Added nameplate images to the elements/nameplates directory (optional)
echo 4. Added numeral plate images to the elements/numerals directory (optional)
echo.

REM Create directories if they don't exist
if not exist "elements\borders" mkdir "elements\borders"
if not exist "elements\nameplates" mkdir "elements\nameplates"
if not exist "elements\numerals" mkdir "elements\numerals"
if not exist "images\final" mkdir "images\final"

echo What would you like to do?
echo 1. Configure element settings
echo 2. Process all card images
echo 3. Process a specific card image
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    python add_card_elements.py --configure
) else if "%choice%"=="2" (
    python add_card_elements.py --all
) else if "%choice%"=="3" (
    echo.
    echo Available card images:
    dir /b "images\cards"
    echo.
    set /p filename="Enter filename to process: "
    python add_card_elements.py --file "%filename%"
) else (
    echo Exiting.
    exit /b
)

echo.
echo Press any key to open the final images folder...
pause > nul

REM Open the final images folder if it exists
if exist "images\final" (
    start explorer "images\final"
) else (
    echo.
    echo WARNING: The final images folder does not exist.
    echo This may indicate that no images were processed.
)

echo.
echo Press any key to exit...
pause > nul
