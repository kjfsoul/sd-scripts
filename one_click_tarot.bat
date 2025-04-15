@echo off
setlocal enabledelayedexpansion

echo Tarot Deck Creation System - True One-Click Startup
echo ================================================
echo.

REM Set paths
set SD_PATH=C:\Users\kjfsw\sd-scripts
set WEBUI_PATH=%SD_PATH%\webui.bat
set WEBUI_USER_PATH=%SD_PATH%\webui-user.bat
set BROWSER_URL=http://127.0.0.1:7860

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in your PATH.
    echo Please install Python 3.8 or higher.
    echo.
    pause
    exit /b
)

echo Step 1: Checking for running Automatic1111 instances...
echo.

REM Check if the API is already accessible (meaning an instance is running)
curl -s %BROWSER_URL%/sdapi/v1/sd-models > nul 2>&1
if %errorlevel% equ 0 (
    echo Automatic1111 is already running at %BROWSER_URL%
    echo Using the existing instance.
    
    REM Open the browser to the existing instance
    echo Opening browser to Automatic1111...
    start "" %BROWSER_URL%
    
    REM Wait a moment for the browser to open
    timeout /t 3 /nobreak > nul
) else (
    echo No running Automatic1111 instance found.
    echo Starting Automatic1111...
    
    REM Check if webui-user.bat exists
    if not exist "%WEBUI_USER_PATH%" (
        echo ERROR: webui-user.bat not found at %WEBUI_USER_PATH%
        echo Please make sure Automatic1111 is installed correctly.
        echo.
        pause
        exit /b
    )
    
    REM Check if API is enabled in webui-user.bat
    findstr /i "--api" "%WEBUI_USER_PATH%" > nul
    if %errorlevel% neq 0 (
        echo API not enabled in webui-user.bat. Adding --api flag...
        
        REM Backup original file
        copy "%WEBUI_USER_PATH%" "%WEBUI_USER_PATH%.bak"
        
        REM Add --api flag to COMMANDLINE_ARGS
        powershell -Command "(Get-Content '%WEBUI_USER_PATH%') -replace 'set COMMANDLINE_ARGS=', 'set COMMANDLINE_ARGS=--api --autolaunch ' | Set-Content '%WEBUI_USER_PATH%'"
        
        echo API flag and autolaunch added to webui-user.bat.
    ) else (
        REM Check if autolaunch is enabled
        findstr /i "--autolaunch" "%WEBUI_USER_PATH%" > nul
        if %errorlevel% neq 0 (
            echo Adding autolaunch flag to webui-user.bat...
            
            REM Backup original file if not already backed up
            if not exist "%WEBUI_USER_PATH%.bak" (
                copy "%WEBUI_USER_PATH%" "%WEBUI_USER_PATH%.bak"
            )
            
            REM Add --autolaunch flag to COMMANDLINE_ARGS
            powershell -Command "(Get-Content '%WEBUI_USER_PATH%') -replace '--api', '--api --autolaunch' | Set-Content '%WEBUI_USER_PATH%'"
            
            echo Autolaunch flag added to webui-user.bat.
        ) else (
            echo API and autolaunch are already enabled in webui-user.bat.
        )
    )
    
    REM Start Automatic1111 in a new window
    echo Starting Automatic1111 with browser auto-launch...
    start cmd /c "cd /d %SD_PATH% && call webui.bat"
    
    echo Waiting for Automatic1111 to start...
    echo This may take a minute or two...
    
    REM Wait for the API to become available
    set MAX_ATTEMPTS=60
    set ATTEMPT=0
    set API_READY=0
    
    :check_api
    set /a ATTEMPT+=1
    echo Checking API (attempt %ATTEMPT% of %MAX_ATTEMPTS%)...
    timeout /t 5 /nobreak > nul
    
    REM Check if API is responding
    curl -s %BROWSER_URL%/sdapi/v1/sd-models > nul 2>&1
    if %errorlevel% equ 0 (
        set API_READY=1
        goto api_ready
    )
    
    if %ATTEMPT% lss %MAX_ATTEMPTS% goto check_api
    
    :api_ready
    if %API_READY% equ 1 (
        echo.
        echo Automatic1111 API is ready!
        
        REM Open the browser to the new instance (in case autolaunch didn't work)
        echo Opening browser to Automatic1111...
        start "" %BROWSER_URL%
        
        REM Wait a moment for the browser to open
        timeout /t 3 /nobreak > nul
    ) else (
        echo.
        echo WARNING: Automatic1111 API did not respond within the expected time.
        echo The process will continue, but you may need to check if Automatic1111 is running correctly.
        echo Try opening %BROWSER_URL% in your browser manually.
    )
)

echo.
echo Step 2: Installing dependencies and setting up directories...
echo.

REM Create necessary directories
python create_directory_structure.py

REM Setup style templates
python setup_style_templates.py

REM Setup tarot reference database
python setup_tarot_reference_db.py

echo.
echo Step 3: Starting Tarot Deck Creation System...
echo.

REM Start the Tarot Master Control Panel
start cmd /c "call tarot_master.bat"

echo.
echo Tarot Deck Creation System has been started!
echo.
echo You can now:
echo 1. Use the Master Control Panel to create your tarot deck
echo 2. Access Automatic1111 in your browser at %BROWSER_URL%
echo 3. Follow the step-by-step process from reference images to final cards
echo.
echo Press any key to exit this startup script...
pause > nul
