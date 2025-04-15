@echo off
echo Tarot Deck Creation System - One-Click Startup (PowerShell Version)
echo ===========================================================
echo.

REM Launch PowerShell script with elevated privileges
powershell -ExecutionPolicy Bypass -File "%~dp0start_tarot_project.ps1"

echo.
echo Press any key to exit...
pause > nul
