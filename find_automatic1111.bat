@echo off
echo Finding Automatic1111 Installation
echo =================================

echo Please enter the full path to your Automatic1111 installation directory:
echo (For example: C:\path\to\stable-diffusion-webui)
set /p sd_path="Path: "

if not exist "%sd_path%" (
    echo The path "%sd_path%" does not exist.
    pause
    exit /b
)

echo.
echo Found directory: %sd_path%
echo.

if exist "%sd_path%\webui-user.bat" (
    echo Found webui-user.bat
) else (
    echo webui-user.bat not found in this directory.
)

if exist "%sd_path%\webui.bat" (
    echo Found webui.bat
) else (
    echo webui.bat not found in this directory.
)

if exist "%sd_path%\launch.py" (
    echo Found launch.py
) else (
    echo launch.py not found in this directory.
)

echo.
echo Please confirm this is your Automatic1111 installation directory.
echo If it is, we'll create a script to start it with the API enabled.
echo.
pause
