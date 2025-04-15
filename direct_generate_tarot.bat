@echo off
echo Direct Tarot Card Generation
echo ==========================

echo This script will:
echo 1. Start Automatic1111 with API enabled
echo 2. Wait for it to load
echo 3. Generate the tarot card images
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause > nul

echo.
echo Step 1: Starting Automatic1111...
call direct_start_a1111.bat

echo.
echo Step 2: Waiting for Automatic1111 to load (60 seconds)...
timeout /t 60 /nobreak

echo.
echo Step 3: Checking if API is accessible...
python check_a1111_api.py

if %errorlevel% neq 0 (
    echo.
    echo API is still not accessible. Please:
    echo 1. Make sure Automatic1111 is fully loaded
    echo 2. Check that it was started with the --api flag
    echo 3. Try running direct_install_dependencies.bat if you see missing module errors
    echo.
    echo Once Automatic1111 is running, run generate_tarot_simple.bat to generate the images.
    pause
    exit /b
)

echo.
echo Step 4: Generating tarot card images...
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
