@echo off
echo Creating Desktop Shortcut for Simple Guided Tarot Creator
echo ==================================================
echo.

REM Get the current directory
set CURRENT_DIR=%~dp0
set SHORTCUT_NAME=Simple Guided Tarot Creator

REM Create a temporary VBScript to create the shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\%SHORTCUT_NAME%.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%CURRENT_DIR%simple_guided_mode.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Start Simple Guided Tarot Deck Creation Workflow" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%SystemRoot%\System32\imageres.dll,76" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM Run the VBScript to create the shortcut
cscript //nologo "%TEMP%\CreateShortcut.vbs"

REM Delete the temporary VBScript
del "%TEMP%\CreateShortcut.vbs"

echo.
echo Desktop shortcut created successfully!
echo You can now start the Simple Guided Tarot Creation Workflow by double-clicking the "%SHORTCUT_NAME%" icon on your desktop.
echo.
echo The simple guided mode will:
echo 1. Present a menu of steps to follow
echo 2. Allow you to perform each step in order
echo 3. Return to the menu after each step
echo 4. Never close unexpectedly
echo.
echo Press any key to exit...
pause > nul
