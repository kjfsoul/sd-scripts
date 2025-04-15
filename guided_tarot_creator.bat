@echo off
setlocal enabledelayedexpansion

echo Tarot Deck Creation System - Guided Mode
echo =====================================
echo.

REM Set paths
set SD_PATH=C:\Users\kjfsw\sd-scripts
set WEBUI_PATH=%SD_PATH%\webui.bat
set WEBUI_USER_PATH=%SD_PATH%\webui-user.bat
set BROWSER_URL=http://127.0.0.1:7860
set GUIDE_FILE=TAROT_CREATION_GUIDE.md

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in your PATH.
    echo Please install Python 3.8 or higher.
    echo.
    pause
    exit /b
)

REM Open the guide file
echo Opening Tarot Creation Guide...
start "" "%GUIDE_FILE%"

echo Step 1: Checking for running Automatic1111 instances...
echo.

REM Check if the API is already accessible (meaning an instance is running)
curl -s %BROWSER_URL%/sdapi/v1/sd-models > nul 2>&1
if %errorlevel% equ 0 (
    echo Automatic1111 is already running at %BROWSER_URL%
    echo Using the existing instance.
    
    REM Open the browser to the existing instance
    echo Opening browser to Automatic1111...
    start "" %BROWSER_URL%
    
    REM Wait a moment for the browser to open
    timeout /t 3 /nobreak > nul
) else (
    echo No running Automatic1111 instance found.
    echo Starting Automatic1111...
    
    REM Check if webui-user.bat exists
    if not exist "%WEBUI_USER_PATH%" (
        echo ERROR: webui-user.bat not found at %WEBUI_USER_PATH%
        echo Please make sure Automatic1111 is installed correctly.
        echo.
        pause
        exit /b
    )
    
    REM Check if API is enabled in webui-user.bat
    findstr /i "--api" "%WEBUI_USER_PATH%" > nul
    if %errorlevel% neq 0 (
        echo API not enabled in webui-user.bat. Adding --api flag...
        
        REM Backup original file
        copy "%WEBUI_USER_PATH%" "%WEBUI_USER_PATH%.bak"
        
        REM Add --api flag to COMMANDLINE_ARGS
        powershell -Command "(Get-Content '%WEBUI_USER_PATH%') -replace 'set COMMANDLINE_ARGS=', 'set COMMANDLINE_ARGS=--api --autolaunch ' | Set-Content '%WEBUI_USER_PATH%'"
        
        echo API flag and autolaunch added to webui-user.bat.
    ) else (
        REM Check if autolaunch is enabled
        findstr /i "--autolaunch" "%WEBUI_USER_PATH%" > nul
        if %errorlevel% neq 0 (
            echo Adding autolaunch flag to webui-user.bat...
            
            REM Backup original file if not already backed up
            if not exist "%WEBUI_USER_PATH%.bak" (
                copy "%WEBUI_USER_PATH%" "%WEBUI_USER_PATH%.bak"
            )
            
            REM Add --autolaunch flag to COMMANDLINE_ARGS
            powershell -Command "(Get-Content '%WEBUI_USER_PATH%') -replace '--api', '--api --autolaunch' | Set-Content '%WEBUI_USER_PATH%'"
            
            echo Autolaunch flag added to webui-user.bat.
        ) else (
            echo API and autolaunch are already enabled in webui-user.bat.
        )
    )
    
    REM Start Automatic1111 in a new window
    echo Starting Automatic1111 with browser auto-launch...
    start cmd /c "cd /d %SD_PATH% && call webui.bat"
    
    echo Waiting for Automatic1111 to start...
    echo This may take a minute or two...
    
    REM Wait for the API to become available
    set MAX_ATTEMPTS=60
    set ATTEMPT=0
    set API_READY=0
    
    :check_api
    set /a ATTEMPT+=1
    echo Checking API (attempt %ATTEMPT% of %MAX_ATTEMPTS%)...
    timeout /t 5 /nobreak > nul
    
    REM Check if API is responding
    curl -s %BROWSER_URL%/sdapi/v1/sd-models > nul 2>&1
    if %errorlevel% equ 0 (
        set API_READY=1
        goto api_ready
    )
    
    if %ATTEMPT% lss %MAX_ATTEMPTS% goto check_api
    
    :api_ready
    if %API_READY% equ 1 (
        echo.
        echo Automatic1111 API is ready!
        
        REM Open the browser to the new instance (in case autolaunch didn't work)
        echo Opening browser to Automatic1111...
        start "" %BROWSER_URL%
        
        REM Wait a moment for the browser to open
        timeout /t 3 /nobreak > nul
    ) else (
        echo.
        echo WARNING: Automatic1111 API did not respond within the expected time.
        echo The process will continue, but you may need to check if Automatic1111 is running correctly.
        echo Try opening %BROWSER_URL% in your browser manually.
    )
)

echo.
echo Step 2: Installing dependencies and setting up directories...
echo.

REM Create necessary directories
python create_directory_structure.py

REM Setup style templates
python setup_style_templates.py

REM Setup tarot reference database
python setup_tarot_reference_db.py

echo.
echo Step 3: Starting Guided Workflow...
echo.

echo ========================================================
echo                GUIDED TAROT CREATION WORKFLOW
echo ========================================================
echo.
echo This guided mode will walk you through the recommended
echo workflow for creating tarot cards step by step.
echo.
echo Please refer to the Tarot Creation Guide that has been
echo opened for detailed instructions at each step.
echo.
echo ========================================================
echo.

REM Ask if user wants to place reference images
echo STEP 1: REFERENCE IMAGES
echo -----------------------
echo.
echo Before proceeding, you should place 5-10 reference images
echo in the "reference/images" folder. These images should represent
echo the artistic style you want for your tarot deck.
echo.
set /p images_ready="Have you placed reference images in the folder? (Y/N): "

if /i "%images_ready%"=="N" (
    echo.
    echo Please add reference images to the "reference/images" folder now.
    echo The folder will be opened for you.
    echo.
    echo Press any key when you're ready to continue...
    mkdir "reference\images" 2>nul
    start explorer "reference\images"
    pause > nul
)

echo.
echo STEP 2: SCAN REFERENCE IMAGES
echo ---------------------------
echo.
echo Now we'll scan your reference images to generate text prompts.
echo This will extract visual elements, colors, and styles from your images.
echo.
set /p scan_images="Ready to scan reference images? (Y/N): "

if /i "%scan_images%"=="Y" (
    echo.
    echo Scanning reference images...
    call improved_scan_images.bat
)

echo.
echo STEP 3: ANALYZE DECK STYLE
echo ------------------------
echo.
echo Next, we'll analyze the generated prompts to find common patterns.
echo This will identify recurring elements, colors, and artistic styles.
echo.
set /p analyze_style="Ready to analyze deck style? (Y/N): "

if /i "%analyze_style%"=="Y" (
    echo.
    echo Analyzing deck style...
    call analyze_deck_style.bat
)

echo.
echo STEP 4: ENHANCE DECK STYLE
echo ------------------------
echo.
echo Now we'll clean up and organize the suggested style.
echo This will remove redundancies and categorize elements.
echo.
set /p enhance_style="Ready to enhance deck style? (Y/N): "

if /i "%enhance_style%"=="Y" (
    echo.
    echo Enhancing deck style...
    call enhance_deck_prompt.bat
)

echo.
echo STEP 5: REFINE PROMPTS
echo --------------------
echo.
echo This is the heart of the creative process. You'll use the Prompt Refiner
echo to create detailed prompts for each tarot card.
echo.
echo Follow these steps in the Prompt Refiner:
echo 1. Select a card from the dropdown menu
echo 2. Choose a style template that matches your vision
echo 3. Add elements from different categories
echo 4. Add artist influences
echo 5. Review the negative prompt
echo 6. Save the prompt
echo 7. Repeat for each card (start with 3 cards for testing)
echo.
set /p refine_prompts="Ready to refine prompts? (Y/N): "

if /i "%refine_prompts%"=="Y" (
    echo.
    echo Opening Prompt Refiner...
    call prompt_refiner.bat
)

echo.
echo STEP 6: GENERATE INITIAL SAMPLES
echo -----------------------------
echo.
echo Now we'll generate 3 cards with 2 variations each.
echo The system will use your refined prompts.
echo.
set /p generate_samples="Ready to generate initial samples? (Y/N): "

if /i "%generate_samples%"=="Y" (
    echo.
    echo Generating initial samples...
    python advanced_tarot_generator.py --generate --cards 3 --variations 2 --start 0
)

echo.
echo STEP 7: REVIEW AND PROVIDE FEEDBACK
echo --------------------------------
echo.
echo Now you'll review the generated cards and provide feedback.
echo You can rate different aspects, add comments, and edit prompts.
echo.
set /p review_cards="Ready to review generated cards? (Y/N): "

if /i "%review_cards%"=="Y" (
    echo.
    echo Opening Feedback Interface...
    call user_feedback_interface.bat
)

echo.
echo STEP 8: GENERATE FULL DECK
echo -----------------------
echo.
echo Now you can generate the full deck or just the Major Arcana.
echo.
echo 1. Generate Major Arcana only (22 cards)
echo 2. Generate full deck (78 cards)
echo 3. Skip this step
echo.
set /p generate_deck="Choose an option (1-3): "

if "%generate_deck%"=="1" (
    echo.
    echo Generating Major Arcana...
    python batch_generate_deck.py --major-only
) else if "%generate_deck%"=="2" (
    echo.
    echo Generating full deck...
    python batch_generate_deck.py
)

echo.
echo STEP 9: ADD BORDERS AND ELEMENTS
echo -----------------------------
echo.
echo Finally, you can add borders, nameplates, and numerals to your cards.
echo.
set /p add_borders="Ready to add borders and elements? (Y/N): "

if /i "%add_borders%"=="Y" (
    echo.
    echo Adding borders and elements...
    python add_card_elements.py --all
)

echo.
echo ========================================================
echo                WORKFLOW COMPLETE!
echo ========================================================
echo.
echo Congratulations! You've completed the guided workflow.
echo.
echo Your tarot cards are now available in the "images/final" folder.
echo.
echo Would you like to view your completed cards?
set /p view_cards="Open the final images folder? (Y/N): "

if /i "%view_cards%"=="Y" (
    if exist "images\final" (
        start explorer "images\final"
    ) else (
        echo No final images found. Please check if the cards were generated correctly.
    )
)

echo.
echo Thank you for using the Guided Tarot Creation System!
echo.
echo This window will stay open. Press any key when you're ready to close it...
pause > nul
