@echo off
echo Direct Run of webui.bat with API Flag
echo ==================================

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
echo Step 2: Setting API flag...
set COMMANDLINE_ARGS=--api

echo.
echo Step 3: Running webui.bat directly...
echo This will run in a new window. Do not close that window until you're done.
echo.
echo Press any key to start Automatic1111...
pause > nul

start "Automatic1111" cmd /k "cd /d "%SD_PATH%" && call webui.bat"

echo.
echo Automatic1111 should now be starting in a new window with the API enabled.
echo Please wait for it to fully load before running the tarot card generation script.
echo.
echo Once Automatic1111 is fully loaded, you can run manual_generate_tarot.bat to generate the tarot cards.
pause
