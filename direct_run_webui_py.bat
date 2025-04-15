@echo off
echo Direct Run of webui.py with API Flag
echo =================================

set SD_PATH=C:\Users\kjfsw\stable-diffusion-webui

echo.
echo Step 1: Navigating to Automatic1111 directory...
cd /d "%SD_PATH%"
if %errorlevel% neq 0 (
    echo Failed to navigate to %SD_PATH%
    echo Please make sure this is the correct path to your Automatic1111 installation.
    pause
    exit /b
)

echo.
echo Step 2: Running webui.py directly with API flag...
echo This will run in the current window. Do not close this window until you're done.
echo.
echo Press any key to start Automatic1111...
pause > nul

if exist "venv\Scripts\activate.bat" (
    echo Using virtual environment...
    call venv\Scripts\activate.bat
    python webui.py --api
    call deactivate
) else (
    echo Using system Python...
    python webui.py --api
)

echo.
echo Automatic1111 has stopped running.
pause
