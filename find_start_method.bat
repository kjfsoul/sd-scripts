@echo off
echo Finding Automatic1111 Start Method
echo ===============================

set SD_PATH=C:\Users\kjfsw\stable-diffusion-webui

echo Looking for possible start methods in %SD_PATH%...
echo.

echo Batch files:
dir /b "%SD_PATH%\*.bat"

echo.
echo Python files that might be entry points:
dir /b "%SD_PATH%\webui.py" 2>nul
dir /b "%SD_PATH%\launch.py" 2>nul
dir /b "%SD_PATH%\run.py" 2>nul
dir /b "%SD_PATH%\start.py" 2>nul

echo.
echo Based on the files found, here are possible ways to start Automatic1111:

if exist "%SD_PATH%\webui-user.bat" (
    echo 1. Run webui-user.bat directly
)

if exist "%SD_PATH%\webui.py" (
    echo 2. Run: python webui.py --api
)

if exist "%SD_PATH%\launch.py" (
    echo 3. Run: python launch.py --api
)

if exist "%SD_PATH%\run.py" (
    echo 4. Run: python run.py --api
)

if exist "%SD_PATH%\start.py" (
    echo 5. Run: python start.py --api
)

echo.
echo Please try one of these methods to start Automatic1111.
echo After it starts, you can run manual_generate_tarot.bat to generate the tarot cards.
echo.
pause
