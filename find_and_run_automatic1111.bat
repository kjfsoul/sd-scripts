@echo off
echo Finding and Running Automatic1111
echo ================================

echo Please enter the full path to your Automatic1111 installation directory:
echo (For example: C:\path\to\stable-diffusion-webui)
set /p sd_path="Path: "

if not exist "%sd_path%" (
    echo The path "%sd_path%" does not exist.
    pause
    exit /b
)

cd /d "%sd_path%"

echo Looking for startup files in %sd_path%...

if exist "webui-user.bat" (
    echo Found webui-user.bat
    
    REM Create a backup of the original file
    copy webui-user.bat webui-user.bat.backup > nul
    
    REM Read the original file and create a modified version
    (for /f "tokens=*" %%a in (webui-user.bat) do (
        echo %%a | findstr /C:"set COMMANDLINE_ARGS=" > nul
        if errorlevel 1 (
            echo %%a
        ) else (
            echo set COMMANDLINE_ARGS=--api
        )
    )) > webui-user.bat.temp
    
    REM Replace the original with the modified version
    move /y webui-user.bat.temp webui-user.bat > nul
    
    echo Starting Automatic1111 with API enabled...
    start "Automatic1111" cmd /c "webui-user.bat && pause"
    
    echo Waiting 5 seconds before restoring original file...
    timeout /t 5 /nobreak > nul
    
    echo Restoring original webui-user.bat...
    move /y webui-user.bat.backup webui-user.bat > nul
    
    echo Automatic1111 should now be starting with API enabled.
    echo Please wait for it to fully load before running the tarot card generation script.
    
) else if exist "webui.bat" (
    echo Found webui.bat
    
    echo Starting Automatic1111 with API enabled...
    start "Automatic1111" cmd /c "webui.bat --api && pause"
    
    echo Automatic1111 should now be starting with API enabled.
    echo Please wait for it to fully load before running the tarot card generation script.
    
) else if exist "launch.py" (
    echo Found launch.py
    
    echo Starting Automatic1111 with API enabled...
    start "Automatic1111" cmd /c "python launch.py --api && pause"
    
    echo Automatic1111 should now be starting with API enabled.
    echo Please wait for it to fully load before running the tarot card generation script.
    
) else (
    echo Could not find any known startup files for Automatic1111.
    echo Please start Automatic1111 manually with the --api flag.
    pause
)

cd /d "%~dp0"
echo.
echo You can now run generate_tarot_api.bat to generate the tarot card images.
echo.
pause
