@echo off
echo Manual Tarot Card Generation
echo ==========================

echo This script will generate tarot card images using the Automatic1111 API.
echo Please make sure Automatic1111 is already running with the API enabled.
echo The API should be accessible at http://127.0.0.1:7860/docs
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause > nul

cd /d "%~dp0"

echo.
echo Step 1: Checking if API is accessible...
python -c "import requests; exit(0 if requests.get('http://127.0.0.1:7860/sdapi/v1/sd-models', timeout=5).status_code == 200 else 1)" 2>nul

if %errorlevel% neq 0 (
    echo.
    echo API is not accessible. Please make sure Automatic1111 is running with the API enabled.
    echo You need to:
    echo 1. Run modify_webui_user.bat to enable the API
    echo 2. Start Automatic1111 using webui-user.bat
    echo 3. Wait for it to fully load
    echo 4. Run this script again
    pause
    exit /b
)

echo API is accessible! Proceeding with image generation...

echo.
echo Step 2: Generating tarot card images...
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
