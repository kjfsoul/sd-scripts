@echo off
echo Tarot Deck Creation System - One-Click Startup
echo ==========================================
echo.

REM Set paths
set SD_PATH=C:\Users\kjfsw\sd-scripts
set WEBUI_PATH=%SD_PATH%\webui.bat
set WEBUI_USER_PATH=%SD_PATH%\webui-user.bat

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
curl -s http://127.0.0.1:7860/sdapi/v1/sd-models > nul 2>&1
if %errorlevel% equ 0 (
    echo Automatic1111 API is already accessible.
    echo Using the existing instance running in Chrome.
    set API_ALREADY_RUNNING=1
    goto skip_a1111_startup
) else (
    echo No accessible Automatic1111 API found.
    set API_ALREADY_RUNNING=0
)

REM Ask user if they want to close any running instances
echo.
echo Would you like to close any running Automatic1111 instances?
echo (This will close any command-line instances, but not browser tabs)
set /p close_instances="Enter Y to close instances or N to keep them running (Y/N): "

if /i "%close_instances%"=="Y" (
    echo Closing running Automatic1111 instances...

    REM Find and kill any running Automatic1111 processes
    tasklist /fi "imagename eq python.exe" /fo csv | findstr /i "webui.py" > nul
    if %errorlevel% equ 0 (
        echo Found running Automatic1111 instance. Terminating...
        for /f "tokens=2 delims=," %%a in ('tasklist /fi "imagename eq python.exe" /fo csv ^| findstr /i "webui.py"') do (
            set PID=%%~a
            taskkill /PID !PID! /F
        )
        echo Automatic1111 processes terminated.
    ) else (
        echo No running Automatic1111 command-line instances found.
    )

    REM Also check for Python processes that might be related
    tasklist /fi "imagename eq python.exe" /fo csv | findstr /i "sd-scripts" > nul
    if %errorlevel% equ 0 (
        echo Found other related Python processes. Terminating...
        for /f "tokens=2 delims=," %%a in ('tasklist /fi "imagename eq python.exe" /fo csv ^| findstr /i "sd-scripts"') do (
            set PID=%%~a
            taskkill /PID !PID! /F
        )
        echo Related Python processes terminated.
    )
) else (
    echo Keeping any running Automatic1111 instances.
)

echo.
echo Step 2: Installing dependencies...
echo.

REM Install dependencies
call install_dependencies.bat

REM Create necessary directories for prompt refiner
python create_directory_structure.py

REM Setup style templates for prompt refiner
python setup_style_templates.py

REM Setup tarot reference database
python setup_tarot_reference_db.py

echo.
echo Step 2.5: Installing enhanced dependencies and plugins...
echo.

REM Ask if user wants to install enhanced dependencies
set /p install_deps="Would you like to install enhanced dependencies for advanced features? (Y/N, default: N): "

if /i "%install_deps%"=="Y" (
    echo Installing enhanced dependencies...
    python install_enhanced_dependencies.py --all
) else (
    echo Skipping enhanced dependencies installation.
)

REM Ask if user wants to install Automatic1111 plugins
set /p install_plugins="Would you like to install recommended Automatic1111 plugins? (Y/N, default: N): "

if /i "%install_plugins%"=="Y" (
    echo Installing Automatic1111 plugins...
    python install_a1111_plugins.py
) else (
    echo Skipping Automatic1111 plugins installation.
)

echo.
echo Step 3: Checking Automatic1111 configuration...
echo.

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
    powershell -Command "(Get-Content '%WEBUI_USER_PATH%') -replace 'set COMMANDLINE_ARGS=', 'set COMMANDLINE_ARGS=--api ' | Set-Content '%WEBUI_USER_PATH%'"

    echo API flag added to webui-user.bat.
) else (
    echo API is already enabled in webui-user.bat.
)

echo.
echo Step 4: Ensuring Automatic1111 is running with API enabled...
echo.

if %API_ALREADY_RUNNING% equ 1 (
    echo Using existing Automatic1111 instance running in Chrome.
    echo API is already accessible at http://127.0.0.1:7860
    set API_READY=1
) else (
    REM Start Automatic1111 in a new window
    echo Starting Automatic1111 in a new window...
    start cmd /c "cd /d %SD_PATH% && call webui.bat"

    echo Waiting for Automatic1111 to start...
    echo This may take a minute or two...

    REM Wait for the API to become available
    set MAX_ATTEMPTS=30
    set ATTEMPT=0
    set API_READY=0

    :check_api
    set /a ATTEMPT+=1
    echo Checking API (attempt %ATTEMPT% of %MAX_ATTEMPTS%)...
    timeout /t 5 /nobreak > nul

    REM Check if API is responding
    curl -s http://127.0.0.1:7860/sdapi/v1/sd-models > nul 2>&1
    if %errorlevel% equ 0 (
        set API_READY=1
        goto api_ready
    )

    if %ATTEMPT% lss %MAX_ATTEMPTS% goto check_api

    :api_ready
    if %API_READY% equ 1 (
        echo.
        echo Automatic1111 API is ready!
    ) else (
        echo.
        echo WARNING: Automatic1111 API did not respond within the expected time.
        echo The process will continue, but you may need to check if Automatic1111 is running correctly.
    )
)

:skip_a1111_startup

echo.
echo Step 5: Starting Tarot Deck Creation System...
echo.

REM Start the Tarot Master Control Panel
start cmd /c "call tarot_master.bat"

echo.
echo Tarot Deck Creation System has been started!
echo.
echo You can now:
echo 1. Use the Master Control Panel to create your tarot deck
echo 2. Follow the step-by-step process from reference images to final cards
echo 3. Check the Automatic1111 interface at http://127.0.0.1:7860 if needed
echo.
echo Press any key to exit this startup script...
pause > nul
