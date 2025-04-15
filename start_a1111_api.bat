@echo off
echo Starting Automatic1111 with API enabled
echo ======================================

echo Please enter the full path to your Automatic1111 installation:
echo Example: C:\path\to\stable-diffusion-webui
set /p sd_path="Path: "

if not exist "%sd_path%" (
    echo The path "%sd_path%" does not exist.
    pause
    exit /b
)

cd /d "%sd_path%"

echo Starting Automatic1111 with API enabled...
echo This will open in a new window.

REM Check if there's a venv folder and use it if available
if exist "venv\Scripts\activate.bat" (
    echo Using virtual environment...
    set PYTHON_CMD=venv\Scripts\python.exe
) else (
    echo Using system Python...
    set PYTHON_CMD=python
)

if exist "webui.py" (
    start "Automatic1111" cmd /k "%PYTHON_CMD% webui.py --api --listen"
) else if exist "launch.py" (
    start "Automatic1111" cmd /k "%PYTHON_CMD% launch.py --api --listen"
) else (
    echo Could not find webui.py or launch.py in the specified directory.
    echo Please make sure you entered the correct path to your Automatic1111 installation.
    pause
    exit /b
)

cd /d "%~dp0"

echo Automatic1111 should now be starting with API enabled.
echo Please wait for it to fully load before running the tarot card generation script.
echo.
echo Once Automatic1111 is fully loaded, you can run check_a1111_api.bat to verify
echo that the API is accessible, then run generate_tarot_simple.bat to generate the tarot cards.
pause
