@echo off
title Tarot Deck Creation - Simple Guided Mode
color 0A
mode con: cols=80 lines=30

echo Tarot Deck Creation System - Simple Guided Mode
echo ==========================================
echo.
echo This simple guided mode will walk you through the tarot card creation process
echo step by step, without closing unexpectedly.
echo.
echo Press any key to begin...
pause > nul

:menu
cls
echo ========================================================
echo                GUIDED TAROT CREATION WORKFLOW
echo ========================================================
echo.
echo Please select a step to perform:
echo.
echo [1] Place reference images
echo [2] Scan reference images
echo [3] Analyze deck style
echo [4] Enhance deck style
echo [5] Refine prompts
echo [6] Generate initial samples
echo [7] Review and provide feedback
echo [8] Generate full deck
echo [9] Add borders and elements
echo.
echo [0] Exit to main menu
echo.

set /p step="Enter your choice (0-9): "

if "%step%"=="1" (
    cls
    echo STEP 1: PLACE REFERENCE IMAGES
    echo ===========================
    echo.
    echo You should place 5-10 reference images in the "reference/images" folder.
    echo These images should represent the artistic style you want for your tarot deck.
    echo.
    echo Opening the reference images folder...
    
    mkdir "reference\images" 2>nul
    start explorer "reference\images"
    
    echo.
    echo Press any key to return to the menu...
    pause > nul
    goto menu
)

if "%step%"=="2" (
    cls
    echo STEP 2: SCAN REFERENCE IMAGES
    echo ==========================
    echo.
    echo This step will scan your reference images and generate text prompts.
    echo.
    
    REM Check if there are any images in the folder
    dir /b "reference\images\*.jpg" "reference\images\*.png" "reference\images\*.jpeg" "reference\images\*.webp" 2>nul | find /v "" >nul
    if %errorlevel% neq 0 (
        echo No images found in the reference/images folder.
        echo Please add some reference images first (Step 1).
        echo.
        echo Press any key to return to the menu...
        pause > nul
        goto menu
    )
    
    echo Found reference images. Scanning...
    echo.
    
    if exist improved_scan_images.bat (
        call improved_scan_images.bat
    ) else if exist scan_reference_images.py (
        python scan_reference_images.py
    ) else (
        echo ERROR: Scan images script not found.
        echo Please make sure improved_scan_images.bat or scan_reference_images.py exists.
    )
    
    echo.
    echo Press any key to return to the menu...
    pause > nul
    goto menu
)

if "%step%"=="3" (
    cls
    echo STEP 3: ANALYZE DECK STYLE
    echo =======================
    echo.
    echo This step will analyze the generated prompts to find common patterns.
    echo.
    
    REM Check if there are any prompt files
    dir /b "reference\prompts\*.txt" 2>nul | find /v "" >nul
    if %errorlevel% neq 0 (
        echo No prompt files found in the reference/prompts folder.
        echo Please scan your reference images first (Step 2).
        echo.
        echo Press any key to return to the menu...
        pause > nul
        goto menu
    )
    
    echo Found prompt files. Analyzing...
    echo.
    
    if exist analyze_deck_style.bat (
        call analyze_deck_style.bat
    ) else (
        echo ERROR: analyze_deck_style.bat not found.
    )
    
    echo.
    echo Press any key to return to the menu...
    pause > nul
    goto menu
)

if "%step%"=="4" (
    cls
    echo STEP 4: ENHANCE DECK STYLE
    echo =======================
    echo.
    echo This step will clean up and organize the suggested style.
    echo.
    
    REM Check if deck_style.txt exists
    if not exist "deck_style.txt" (
        echo deck_style.txt not found.
        echo Please analyze your deck style first (Step 3).
        echo.
        echo Press any key to return to the menu...
        pause > nul
        goto menu
    )
    
    echo Found deck_style.txt. Enhancing...
    echo.
    
    if exist enhance_deck_prompt.bat (
        call enhance_deck_prompt.bat
    ) else (
        echo ERROR: enhance_deck_prompt.bat not found.
    )
    
    echo.
    echo Press any key to return to the menu...
    pause > nul
    goto menu
)

if "%step%"=="5" (
    cls
    echo STEP 5: REFINE PROMPTS
    echo ===================
    echo.
    echo This is the heart of the creative process. You'll use the Prompt Refiner
    echo to create detailed prompts for each tarot card.
    echo.
    
    if exist prompt_refiner.bat (
        call prompt_refiner.bat
    ) else (
        echo ERROR: prompt_refiner.bat not found.
    )
    
    echo.
    echo Press any key to return to the menu...
    pause > nul
    goto menu
)

if "%step%"=="6" (
    cls
    echo STEP 6: GENERATE INITIAL SAMPLES
    echo ============================
    echo.
    echo This step will generate 3 cards with 2 variations each.
    echo.
    
    if exist advanced_tarot_generator.py (
        python advanced_tarot_generator.py --generate --cards 3 --variations 2 --start 0
    ) else (
        echo ERROR: advanced_tarot_generator.py not found.
    )
    
    echo.
    echo Press any key to return to the menu...
    pause > nul
    goto menu
)

if "%step%"=="7" (
    cls
    echo STEP 7: REVIEW AND PROVIDE FEEDBACK
    echo ===============================
    echo.
    echo This step allows you to review the generated cards and provide feedback.
    echo.
    
    REM Check if there are any card images
    dir /b "images\cards\*.jpg" "images\cards\*.png" "images\cards\*.jpeg" "images\cards\*.webp" 2>nul | find /v "" >nul
    if %errorlevel% neq 0 (
        echo No card images found in the images/cards folder.
        echo Please generate some cards first (Step 6).
        echo.
        echo Press any key to return to the menu...
        pause > nul
        goto menu
    )
    
    echo Found card images. Opening feedback interface...
    echo.
    
    if exist user_feedback_interface.bat (
        call user_feedback_interface.bat
    ) else (
        echo ERROR: user_feedback_interface.bat not found.
    )
    
    echo.
    echo Press any key to return to the menu...
    pause > nul
    goto menu
)

if "%step%"=="8" (
    cls
    echo STEP 8: GENERATE FULL DECK
    echo ======================
    echo.
    echo This step will generate the full deck or just the Major Arcana.
    echo.
    echo 1. Generate Major Arcana only (22 cards)
    echo 2. Generate full deck (78 cards)
    echo 3. Return to main menu
    echo.
    
    set /p deck_choice="Enter your choice (1-3): "
    
    if "%deck_choice%"=="1" (
        echo.
        echo Generating Major Arcana...
        echo.
        
        if exist batch_generate_deck.py (
            python batch_generate_deck.py --major-only
        ) else (
            echo ERROR: batch_generate_deck.py not found.
        )
    ) else if "%deck_choice%"=="2" (
        echo.
        echo Generating full deck...
        echo.
        
        if exist batch_generate_deck.py (
            python batch_generate_deck.py
        ) else (
            echo ERROR: batch_generate_deck.py not found.
        )
    )
    
    echo.
    echo Press any key to return to the menu...
    pause > nul
    goto menu
)

if "%step%"=="9" (
    cls
    echo STEP 9: ADD BORDERS AND ELEMENTS
    echo ============================
    echo.
    echo This step will add borders, nameplates, and numerals to your cards.
    echo.
    
    REM Check if there are any card images
    dir /b "images\cards\*.jpg" "images\cards\*.png" "images\cards\*.jpeg" "images\cards\*.webp" 2>nul | find /v "" >nul
    if %errorlevel% neq 0 (
        echo No card images found in the images/cards folder.
        echo Please generate some cards first (Steps 6 or 8).
        echo.
        echo Press any key to return to the menu...
        pause > nul
        goto menu
    )
    
    echo Found card images. Adding borders and elements...
    echo.
    
    if exist add_card_elements.py (
        python add_card_elements.py --all
    ) else (
        echo ERROR: add_card_elements.py not found.
    )
    
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
    echo Press any key to return to the menu...
    pause > nul
    goto menu
)

if "%step%"=="0" (
    cls
    echo Returning to main menu...
    exit /b
) else (
    echo Invalid choice. Please try again.
    timeout /t 2 /nobreak > nul
    goto menu
)
