@echo off
echo Generating Tarot Cards (No LoRA)
echo =============================

echo This script will generate tarot card images without using a LoRA model.
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause > nul

python generate_tarot_no_lora.py

echo.
echo Done! Images have been saved to the tarot_output folder.
echo.
echo Press any key to open the output folder...
pause > nul
start explorer "%~dp0tarot_output"
pause
