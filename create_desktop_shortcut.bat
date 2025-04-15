@echo off
echo Creating Desktop Shortcut for Tarot Deck Creation System
echo ===================================================
echo.

REM Get the current directory
set CURRENT_DIR=%~dp0
set SHORTCUT_NAME=Tarot Deck Creator

REM Create a temporary VBScript to create the shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\%SHORTCUT_NAME%.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%CURRENT_DIR%start_tarot_project.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Start Tarot Deck Creation System" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%SystemRoot%\System32\imageres.dll,76" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM Run the VBScript to create the shortcut
cscript //nologo "%TEMP%\CreateShortcut.vbs"

REM Delete the temporary VBScript
del "%TEMP%\CreateShortcut.vbs"

echo.
echo Desktop shortcut created successfully!
echo You can now start the Tarot Deck Creation System by double-clicking the "%SHORTCUT_NAME%" icon on your desktop.
echo.
echo Press any key to exit...
pause > nul
