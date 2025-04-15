@echo off
echo Manual Start of Automatic1111
echo ===========================

echo This script will attempt to start Automatic1111 in the most direct way possible.

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
echo Step 2: Checking for Python...
python --version
if %errorlevel% neq 0 (
    echo Python not found in PATH
    echo Please make sure Python is installed and in your PATH.
    pause
    exit /b
)

echo.
echo Step 3: Starting Automatic1111 with API enabled...
echo This will run in the current window. Do not close this window until you're done.
echo.
echo If you see any error messages, please note them down.
echo.
echo Press any key to start Automatic1111...
pause > nul

if exist "webui.py" (
    echo Running: python webui.py --api --listen
    python webui.py --api --listen
) else if exist "launch.py" (
    echo Running: python launch.py --api --listen
    python launch.py --api --listen
) else (
    echo Could not find webui.py or launch.py
    echo Please make sure you're in the correct Automatic1111 directory.
    pause
    exit /b
)

echo.
echo Automatic1111 has stopped running.
pause
