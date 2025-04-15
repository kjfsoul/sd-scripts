@echo off
echo Tarot Deck Style Guide Generator
echo =============================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in your PATH.
    echo Please install Python 3.8 or higher.
    echo.
    pause
    exit /b
)

REM Check if required packages are installed
pip show Pillow > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Pillow...
    pip install Pillow
)

echo This tool will generate a comprehensive style guide for your tarot deck project.
echo.
echo Please enter the following information:
echo.

set /p project_name="Project Name: "
set /p client_name="Client Name (optional): "

echo.
echo Available style templates:
echo 1. Fantasy
echo 2. Vintage
echo 3. Minimalist
echo 4. Watercolor
echo 5. Cyberpunk
echo 6. None (use analyzed style only)
echo.
set /p template_choice="Choose a template (1-6): "

if "%template_choice%"=="1" (
    set template=fantasy
) else if "%template_choice%"=="2" (
    set template=vintage
) else if "%template_choice%"=="3" (
    set template=minimalist
) else if "%template_choice%"=="4" (
    set template=watercolor
) else if "%template_choice%"=="5" (
    set template=cyberpunk
) else (
    set template=
)

echo.
echo Generating style guide...
echo.

if "%template%"=="" (
    python generate_style_guide.py --project "%project_name%" --client "%client_name%"
) else (
    python generate_style_guide.py --project "%project_name%" --client "%client_name%" --template %template%
)

echo.
echo Press any key to exit...
pause > nul
