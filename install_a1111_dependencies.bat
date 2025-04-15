@echo off
echo Installing Automatic1111 Dependencies
echo ===================================

echo Please enter the full path to your Automatic1111 installation:
echo Example: C:\path\to\stable-diffusion-webui
set /p sd_path="Path: "

if not exist "%sd_path%" (
    echo The path "%sd_path%" does not exist.
    pause
    exit /b
)

cd /d "%sd_path%"

echo Installing pytorch_lightning and other dependencies...

if exist "venv" (
    echo Using virtual environment in venv folder...
    call venv\Scripts\activate.bat
    pip install pytorch_lightning
    pip install -r requirements.txt
    deactivate
) else (
    echo No virtual environment found, installing globally...
    pip install pytorch_lightning
    
    if exist "requirements.txt" (
        pip install -r requirements.txt
    ) else (
        echo requirements.txt not found, installing common dependencies...
        pip install torch torchvision torchaudio diffusers transformers accelerate safetensors
    )
)

echo.
echo Dependencies installed. You can now try running Automatic1111 again.
echo.
pause
