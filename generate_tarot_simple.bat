@echo off
echo Tarot Card Generation via API
echo ===========================

echo This script will generate tarot card images using the Automatic1111 API.
echo It will first check if the API is accessible.
echo.

REM Check if the API is accessible
echo Checking if Automatic1111 API is running...
python check_a1111_api.py

if %errorlevel% neq 0 (
    echo.
    echo Would you like to start Automatic1111 with the API enabled? (Y/N)
    set /p choice="Your choice: "
    if /i "%choice%"=="Y" (
        echo.
        call start_a1111_api.bat
        echo.
        echo Please wait for Automatic1111 to fully load, then press any key to continue...
        pause > nul
    ) else (
        echo Please start Automatic1111 with the API enabled, then run this script again.
        pause
        exit /b
    )
)

echo.
echo Generating tarot card images...
python generate_tarot_api.py --lora "fool_hypernetwork"

if %errorlevel% equ 0 (
    echo.
    echo Done! Images have been saved to the tarot_output folder.
    echo.
    echo Press any key to open the output folder...
    pause > nul
    start explorer "%~dp0tarot_output"
) else (
    echo.
    echo There was an error generating the images. Please check the error messages above.
)

pause
