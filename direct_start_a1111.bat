@echo off
echo Direct Start of Automatic1111 with API Enabled
echo ============================================

REM Set the path to your Automatic1111 installation
set SD_PATH=C:\Users\kjfsw\stable-diffusion-webui

echo Starting Automatic1111 from %SD_PATH% with API enabled...
echo This will open in a new window.

cd /d "%SD_PATH%"

REM Check if there's a venv folder and use it if available
if exist "venv\Scripts\activate.bat" (
    echo Using virtual environment...
    call venv\Scripts\activate.bat
    
    if exist "webui.py" (
        start "Automatic1111" cmd /k "python webui.py --api --listen"
    ) else if exist "launch.py" (
        start "Automatic1111" cmd /k "python launch.py --api --listen"
    ) else (
        echo Could not find webui.py or launch.py in the specified directory.
        pause
        exit /b
    )
    
    call deactivate
) else (
    echo No virtual environment found, using system Python...
    
    if exist "webui.py" (
        start "Automatic1111" cmd /k "python webui.py --api --listen"
    ) else if exist "launch.py" (
        start "Automatic1111" cmd /k "python launch.py --api --listen"
    ) else (
        echo Could not find webui.py or launch.py in the specified directory.
        pause
        exit /b
    )
)

cd /d "%~dp0"

echo Automatic1111 should now be starting with API enabled.
echo Please wait for it to fully load before running the tarot card generation script.
echo.
echo Once Automatic1111 is fully loaded, you can run check_a1111_api.bat to verify
echo that the API is accessible, then run generate_tarot_simple.bat to generate the tarot cards.
pause
