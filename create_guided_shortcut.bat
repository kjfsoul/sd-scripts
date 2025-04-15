@echo off
echo Creating Desktop Shortcut for Guided Tarot Creator
echo =============================================
echo.

REM Get the current directory
set CURRENT_DIR=%~dp0
set SHORTCUT_NAME=Guided Tarot Creator

REM Create a temporary VBScript to create the shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\%SHORTCUT_NAME%.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%CURRENT_DIR%guided_tarot_creator.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Start Guided Tarot Deck Creation Workflow" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%SystemRoot%\System32\imageres.dll,76" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM Run the VBScript to create the shortcut
cscript //nologo "%TEMP%\CreateShortcut.vbs"

REM Delete the temporary VBScript
del "%TEMP%\CreateShortcut.vbs"

echo.
echo Desktop shortcut created successfully!
echo You can now start the Guided Tarot Creation Workflow by double-clicking the "%SHORTCUT_NAME%" icon on your desktop.
echo.
echo The guided mode will:
echo 1. Open the Tarot Creation Guide for reference
echo 2. Walk you through each step of the recommended workflow
echo 3. Automatically launch the appropriate tools at each step
echo 4. Provide clear instructions and guidance throughout the process
echo.
echo Press any key to exit...
pause > nul
