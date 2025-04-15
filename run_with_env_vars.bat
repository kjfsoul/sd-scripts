@echo off
echo Run webui.bat with Environment Variables
echo ====================================

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
echo Step 2: Setting environment variables...
set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS=--api

echo.
echo Step 3: Running webui.bat directly...
echo This will run in the current window. Do not close this window until you're done.
echo.
echo Press any key to start Automatic1111...
pause > nul

call "%SD_PATH%\webui.bat"

echo.
echo Automatic1111 has stopped running.
pause
