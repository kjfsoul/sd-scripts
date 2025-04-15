@echo off
echo Modifying webui-user.bat to Enable API
echo ====================================

set SD_PATH=C:\Users\kjfsw\stable-diffusion-webui

echo.
echo Step 1: Checking if webui-user.bat exists...
if not exist "%SD_PATH%\webui-user.bat" (
    echo Could not find webui-user.bat at %SD_PATH%
    echo Please enter the correct path to your Automatic1111 installation:
    set /p sd_path="Path: "
    
    if not exist "%sd_path%\webui-user.bat" (
        echo webui-user.bat not found at %sd_path%
        pause
        exit /b
    )
    
    set SD_PATH=%sd_path%
)

echo Found webui-user.bat at %SD_PATH%

echo.
echo Step 2: Creating backup of webui-user.bat...
copy "%SD_PATH%\webui-user.bat" "%SD_PATH%\webui-user.bat.backup" > nul
if %errorlevel% neq 0 (
    echo Failed to create backup of webui-user.bat
    pause
    exit /b
)
echo Created backup at %SD_PATH%\webui-user.bat.backup

echo.
echo Step 3: Modifying webui-user.bat to enable API...
(for /f "tokens=*" %%a in ('type "%SD_PATH%\webui-user.bat"') do (
    echo %%a | findstr /C:"set COMMANDLINE_ARGS=" > nul
    if errorlevel 1 (
        echo %%a
    ) else (
        echo set COMMANDLINE_ARGS=--api
    )
)) > "%SD_PATH%\webui-user.bat.new"

move /y "%SD_PATH%\webui-user.bat.new" "%SD_PATH%\webui-user.bat" > nul
if %errorlevel% neq 0 (
    echo Failed to update webui-user.bat
    echo Restoring backup...
    move /y "%SD_PATH%\webui-user.bat.backup" "%SD_PATH%\webui-user.bat" > nul
    pause
    exit /b
)

echo Successfully modified webui-user.bat to enable API

echo.
echo Step 4: Verifying the changes...
type "%SD_PATH%\webui-user.bat"

echo.
echo webui-user.bat has been modified to enable the API.
echo You can now start Automatic1111 normally using webui-user.bat.
echo After it starts, you can access the API documentation at http://127.0.0.1:7860/docs
echo.
echo Would you like to start Automatic1111 now? (Y/N)
set /p choice="Your choice: "
if /i "%choice%"=="Y" (
    echo.
    echo Starting Automatic1111...
    start "" "%SD_PATH%\webui-user.bat"
    echo.
    echo Automatic1111 is starting in a new window.
    echo Please wait for it to fully load before generating tarot cards.
)

echo.
echo Once Automatic1111 is fully loaded, you can run manual_generate_tarot.bat to generate the tarot cards.
pause
