@echo off
echo Direct Installation of Automatic1111 Dependencies
echo =============================================

REM Set the path to your Automatic1111 installation
set SD_PATH=C:\Users\kjfsw\stable-diffusion-webui

echo Installing dependencies for Automatic1111 at %SD_PATH%...

cd /d "%SD_PATH%"

REM Check if there's a venv folder and use it if available
if exist "venv\Scripts\activate.bat" (
    echo Using virtual environment...
    call venv\Scripts\activate.bat
    
    echo Installing pytorch_lightning...
    pip install pytorch_lightning
    
    echo Installing other dependencies...
    if exist "requirements.txt" (
        pip install -r requirements.txt
    ) else (
        echo requirements.txt not found, installing common dependencies...
        pip install torch torchvision torchaudio diffusers transformers accelerate safetensors
    )
    
    call deactivate
) else (
    echo No virtual environment found, using system Python...
    
    echo Installing pytorch_lightning...
    pip install pytorch_lightning
    
    echo Installing other dependencies...
    if exist "requirements.txt" (
        pip install -r requirements.txt
    ) else (
        echo requirements.txt not found, installing common dependencies...
        pip install torch torchvision torchaudio diffusers transformers accelerate safetensors
    )
)

cd /d "%~dp0"

echo.
echo Dependencies installed. You can now try running Automatic1111 again.
echo.
pause
