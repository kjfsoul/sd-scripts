@echo off
echo Diagnosing Automatic1111 Installation
echo ===================================

echo This script will check your Automatic1111 installation and provide diagnostic information.

echo.
echo Step 1: Checking if Automatic1111 directory exists...
if exist "C:\Users\kjfsw\stable-diffusion-webui" (
    echo Found Automatic1111 directory at C:\Users\kjfsw\stable-diffusion-webui
) else (
    echo Could not find Automatic1111 directory at C:\Users\kjfsw\stable-diffusion-webui
    echo Please provide the correct path to your Automatic1111 installation:
    set /p sd_path="Path: "
    
    if not exist "%sd_path%" (
        echo The path "%sd_path%" does not exist.
        pause
        exit /b
    )
    
    echo Found Automatic1111 directory at %sd_path%
    set SD_PATH=%sd_path%
) && set SD_PATH=C:\Users\kjfsw\stable-diffusion-webui

echo.
echo Step 2: Checking for key files in %SD_PATH%...
if exist "%SD_PATH%\webui.py" (
    echo Found webui.py
) else (
    echo webui.py not found
)

if exist "%SD_PATH%\launch.py" (
    echo Found launch.py
) else (
    echo launch.py not found
)

if exist "%SD_PATH%\venv" (
    echo Found venv directory
) else (
    echo venv directory not found
)

if exist "%SD_PATH%\models" (
    echo Found models directory
) else (
    echo models directory not found
)

echo.
echo Step 3: Checking Python installation...
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python not found in PATH
) else (
    echo Python found in PATH
)

if exist "%SD_PATH%\venv\Scripts\python.exe" (
    echo Found Python in venv
) else (
    echo Python not found in venv
)

echo.
echo Step 4: Checking network connectivity...
ping -n 1 127.0.0.1 > nul
if %errorlevel% equ 0 (
    echo Local network is working
) else (
    echo Local network is not working
)

echo.
echo Step 5: Checking if Automatic1111 is already running...
netstat -ano | findstr ":7860" > nul
if %errorlevel% equ 0 (
    echo Automatic1111 appears to be running on port 7860
) else (
    echo Automatic1111 does not appear to be running on port 7860
)

echo.
echo Diagnostic information complete.
echo.
echo Based on this information, here are some suggestions:
echo 1. Make sure Python is installed and in your PATH
echo 2. Try starting Automatic1111 manually from its directory
echo 3. Check if there are any error messages when starting Automatic1111
echo 4. Make sure the --api flag is included when starting Automatic1111
echo.
pause
