@echo off
echo Tarot Card Generation via API
echo ===========================

REM Check if Automatic1111 is running
echo Checking if Automatic1111 is running...

REM Try to connect to the API
python -c "import requests; exit(0 if requests.get('http://127.0.0.1:7860/sdapi/v1/sd-models', timeout=2).status_code == 200 else 1)" 2>nul

if %errorlevel% equ 0 (
    echo Automatic1111 API is running. Proceeding with image generation...
) else (
    echo Automatic1111 API is not running or not accessible.
    echo.
    echo Would you like to start Automatic1111 with API enabled? (Y/N)
    set /p choice="Your choice: "
    if /i "%choice%"=="Y" (
        echo.
        echo Please enter the full path to your Automatic1111 installation:
        set /p sd_path="Path: "

        if not exist "%sd_path%" (
            echo The path "%sd_path%" does not exist.
            pause
            exit /b
        )

        echo Starting Automatic1111 with API enabled...
        start "Automatic1111" python run_automatic1111_api.py --path "%sd_path%"

        echo Waiting for Automatic1111 to start (30 seconds)...
        timeout /t 30 /nobreak > nul

        REM Check if it's running now
        python -c "import requests; exit(0 if requests.get('http://127.0.0.1:7860/sdapi/v1/sd-models', timeout=2).status_code == 200 else 1)" 2>nul

        if %errorlevel% neq 0 (
            echo Automatic1111 API did not start successfully.
            echo Please start it manually with the --api flag and try again.
            pause
            exit /b
        )
    ) else (
        echo Please start Automatic1111 manually with the --api flag.
        echo Then run this script again.
        pause
        exit /b
    )
)

echo.
echo Generating tarot card images...
python generate_tarot_api.py --lora "fool_hypernetwork"

echo.
echo Done! Images have been saved to the tarot_output folder.
echo.
echo Press any key to open the output folder...
pause > nul
start explorer "%~dp0tarot_output"
pause
