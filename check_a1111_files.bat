@echo off
echo Checking Automatic1111 Files
echo ==========================

set SD_PATH=C:\Users\kjfsw\stable-diffusion-webui

echo Looking for files in %SD_PATH%...
echo.

echo Batch files:
dir /b "%SD_PATH%\*.bat"

echo.
echo Python files:
dir /b "%SD_PATH%\*.py"

echo.
echo Press any key to continue...
pause > nul
