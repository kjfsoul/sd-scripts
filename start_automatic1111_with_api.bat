@echo off
echo Starting Automatic1111 with API enabled
echo ======================================

cd /d "C:\Users\kjfsw\sd-scripts"

REM Temporarily modify webui-user.bat to include the API flag
echo Creating a temporary copy of webui-user.bat with API flag...

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
call webui-user.bat

echo Restoring original webui-user.bat...
move /y webui-user.bat.backup webui-user.bat > nul

echo.
echo Automatic1111 has been closed.
pause
