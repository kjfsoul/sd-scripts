@echo off
echo Checking Automatic1111 API
echo =======================

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python 3.8 or higher.
    pause
    exit /b
)

REM Check if requirements are installed
pip show requests > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requirements...
    pip install requests
)

REM Run the API check
python src\tarot_creator.py --check-api

echo.
echo If the API is not accessible, please make sure:
echo 1. Automatic1111 is running
echo 2. It was started with the --api flag
echo 3. It's running on the default port (7860)
echo.
echo You can enable the API by adding --api to the COMMANDLINE_ARGS in webui-user.bat
echo.
pause
