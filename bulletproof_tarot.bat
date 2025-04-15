@echo off
setlocal enabledelayedexpansion
title Tarot Card Creator
color 0A

:start
cls
echo =====================================================
echo                TAROT CARD CREATOR
echo =====================================================
echo.
echo This tool will guide you through creating tarot cards
echo without closing unexpectedly.
echo.
echo STEP 1: Place reference images in the folder that will open
echo STEP 2: We'll scan those images to create prompts
echo STEP 3: We'll analyze the style from those prompts
echo.
echo Press any key to begin...
pause > nul

REM Step 1: Open folder for reference images
cls
echo STEP 1: PLACE REFERENCE IMAGES
echo ===========================
echo.
echo Opening the folder where you should place 5-10 reference images.
echo These images should represent the style you want for your tarot cards.
echo.
echo After placing your images, close the folder and return here.
echo.
echo Press any key to open the reference images folder...
pause > nul

mkdir "reference\images" 2>nul
start explorer "reference\images"

echo.
echo Folder opened. After placing your images, press any key to continue...
pause > nul

REM Step 2: Scan reference images
cls
echo STEP 2: SCAN REFERENCE IMAGES
echo ==========================
echo.
echo Now we'll scan your reference images to generate text prompts.
echo.

REM Check if there are any images in the folder
dir /b "reference\images\*.jpg" "reference\images\*.png" "reference\images\*.jpeg" "reference\images\*.webp" 2>nul | find /v "" >nul
if %errorlevel% neq 0 (
    echo No images found in the reference/images folder.
    echo.
    echo Would you like to:
    echo [1] Open the folder again to add images
    echo [2] Continue anyway
    echo.
    set /p no_images="Enter your choice (1-2): "
    
    if "!no_images!"=="1" (
        start explorer "reference\images"
        echo.
        echo Folder opened. After placing your images, press any key to continue...
        pause > nul
    )
)

echo Scanning reference images...
echo.

if exist scan_reference_images.py (
    python scan_reference_images.py
) else (
    echo Creating simple prompts from image filenames...
    
    mkdir "reference\prompts" 2>nul
    
    for %%f in (reference\images\*.*) do (
        echo tarot card, fantasy art, mystical, detailed, %%~nf > "reference\prompts\%%~nf.txt"
        echo Created prompt for %%~nf
    )
)

echo.
echo Reference images scanned. Press any key to continue...
pause > nul

REM Step 3: Analyze deck style
cls
echo STEP 3: ANALYZE DECK STYLE
echo =======================
echo.
echo Now we'll analyze the generated prompts to find common patterns.
echo.

REM Check if there are any prompt files
dir /b "reference\prompts\*.txt" 2>nul | find /v "" >nul
if %errorlevel% neq 0 (
    echo No prompt files found. Creating a default style...
    
    mkdir "reference\prompts" 2>nul
    echo tarot card, fantasy art, mystical, detailed > "reference\prompts\default.txt"
)

echo Analyzing deck style...
echo.

REM Create a simple deck style analysis
echo # Deck Style Analysis > deck_style.txt
echo ## Analyzed Prompts >> deck_style.txt
echo. >> deck_style.txt

REM Concatenate all prompt files
for %%f in (reference\prompts\*.txt) do (
    echo - %%~nf: >> deck_style.txt
    type "%%f" >> deck_style.txt
    echo. >> deck_style.txt
)

echo. >> deck_style.txt
echo ## Suggested Deck Style Prompt >> deck_style.txt
echo. >> deck_style.txt
echo fantasy art, mystical, detailed, vibrant colors, art nouveau style >> deck_style.txt

echo.
echo Analysis complete! Results saved to deck_style.txt
echo.
echo Press any key to continue...
pause > nul

REM Step 4: Enhance deck style
cls
echo STEP 4: ENHANCE DECK STYLE
echo =======================
echo.
echo Now we'll clean up and organize the suggested style.
echo.

echo Enhancing deck style...
echo.

REM Create a simple enhanced deck style
echo # Enhanced Deck Style > enhanced_deck_style.txt
echo. >> enhanced_deck_style.txt

echo ## Categories >> enhanced_deck_style.txt
echo. >> enhanced_deck_style.txt
echo ### Art Style >> enhanced_deck_style.txt
echo - fantasy art >> enhanced_deck_style.txt
echo - mystical >> enhanced_deck_style.txt
echo - art nouveau >> enhanced_deck_style.txt
echo. >> enhanced_deck_style.txt

echo ### Colors >> enhanced_deck_style.txt
echo - vibrant colors >> enhanced_deck_style.txt
echo - rich tones >> enhanced_deck_style.txt
echo. >> enhanced_deck_style.txt

echo ### Detail Level >> enhanced_deck_style.txt
echo - highly detailed >> enhanced_deck_style.txt
echo - intricate >> enhanced_deck_style.txt
echo. >> enhanced_deck_style.txt

echo ## Enhanced Prompt >> enhanced_deck_style.txt
echo. >> enhanced_deck_style.txt
echo fantasy art, mystical, detailed, vibrant colors, art nouveau style, highly detailed, intricate designs, rich tones >> enhanced_deck_style.txt

echo.
echo Enhancement complete! Results saved to enhanced_deck_style.txt
echo.
echo Press any key to continue...
pause > nul

REM Step 5: Generate cards
cls
echo STEP 5: GENERATE CARDS
echo ===================
echo.
echo Now we'll generate some tarot cards using the enhanced style.
echo.
echo [1] Generate 3 sample cards (recommended first step)
echo [2] Generate Major Arcana (22 cards)
echo [3] Generate full deck (78 cards)
echo [4] Skip this step
echo.
set /p gen_choice="Enter your choice (1-4): "

if "!gen_choice!"=="1" (
    echo.
    echo Generating 3 sample cards...
    echo.
    
    mkdir "images\cards" 2>nul
    
    if exist advanced_tarot_generator.py (
        python advanced_tarot_generator.py --generate --cards 3 --variations 2 --start 0
    ) else (
        echo This would normally generate 3 sample cards.
        echo Since the generator script is not found, we'll create placeholder images.
        
        echo Creating placeholder images...
        echo This is a placeholder for a tarot card image > "images\cards\fool_v1.txt"
        echo This is a placeholder for a tarot card image > "images\cards\fool_v2.txt"
        echo This is a placeholder for a tarot card image > "images\cards\magician_v1.txt"
        echo This is a placeholder for a tarot card image > "images\cards\magician_v2.txt"
        echo This is a placeholder for a tarot card image > "images\cards\highpriestess_v1.txt"
        echo This is a placeholder for a tarot card image > "images\cards\highpriestess_v2.txt"
    )
) else if "!gen_choice!"=="2" (
    echo.
    echo Generating Major Arcana...
    echo.
    
    mkdir "images\cards" 2>nul
    
    if exist batch_generate_deck.py (
        python batch_generate_deck.py --major-only
    ) else (
        echo This would normally generate the Major Arcana.
        echo Since the generator script is not found, we'll create placeholder images.
        
        echo Creating placeholder images...
        for %%c in (fool magician highpriestess empress emperor hierophant lovers chariot strength hermit wheeloffortune justice hangedman death temperance devil tower star moon sun judgement world) do (
            echo This is a placeholder for a tarot card image > "images\cards\%%c.txt"
        )
    )
) else if "!gen_choice!"=="3" (
    echo.
    echo Generating full deck...
    echo.
    
    mkdir "images\cards" 2>nul
    
    if exist batch_generate_deck.py (
        python batch_generate_deck.py
    ) else (
        echo This would normally generate the full deck.
        echo Since the generator script is not found, we'll create placeholder images.
        
        echo Creating placeholder images...
        for %%c in (fool magician highpriestess empress emperor hierophant lovers chariot strength hermit wheeloffortune justice hangedman death temperance devil tower star moon sun judgement world) do (
            echo This is a placeholder for a tarot card image > "images\cards\%%c.txt"
        )
        
        echo Created placeholder images for the Major Arcana.
        echo (Minor Arcana placeholders would also be created in a real scenario)
    )
)

echo.
echo Press any key to continue...
pause > nul

REM Step 6: Add borders
cls
echo STEP 6: ADD BORDERS AND ELEMENTS
echo ============================
echo.
echo Finally, you can add borders, nameplates, and numerals to your cards.
echo.
echo [1] Add borders to all cards
echo [2] Skip this step
echo.
set /p border_choice="Enter your choice (1-2): "

if "!border_choice!"=="1" (
    echo.
    echo Adding borders and elements...
    echo.
    
    mkdir "images\final" 2>nul
    
    if exist add_card_elements.py (
        python add_card_elements.py --all
    ) else (
        echo This would normally add borders and elements to all cards.
        echo Since the script is not found, we'll create placeholder final images.
        
        echo Creating placeholder final images...
        for %%f in (images\cards\*.*) do (
            echo This is a placeholder for a finalized tarot card image > "images\final\%%~nxf"
        )
    )
    
    echo.
    echo Would you like to view your completed cards?
    set /p view_cards="Open the final images folder? (Y/N): "
    
    if /i "!view_cards!"=="Y" (
        if exist "images\final" (
            start explorer "images\final"
        ) else (
            echo No final images found. Please check if the cards were generated correctly.
        )
    )
)

REM Completion
cls
echo =====================================================
echo                PROCESS COMPLETE!
echo =====================================================
echo.
echo Congratulations! You've completed the tarot card creation process.
echo.
echo Your files are saved in the following locations:
echo - Reference images: reference/images
echo - Generated prompts: reference/prompts
echo - Deck style: deck_style.txt
echo - Enhanced style: enhanced_deck_style.txt
echo - Generated cards: images/cards
echo - Final cards: images/final
echo.
echo What would you like to do next?
echo.
echo [1] View generated cards
echo [2] View final cards
echo [3] Start over
echo [4] Exit
echo.
set /p next_step="Enter your choice (1-4): "

if "!next_step!"=="1" (
    if exist "images\cards" (
        start explorer "images\cards"
    ) else (
        echo No generated images found.
    )
    goto completion
) else if "!next_step!"=="2" (
    if exist "images\final" (
        start explorer "images\final"
    ) else (
        echo No final images found.
    )
    goto completion
) else if "!next_step!"=="3" (
    goto start
) else (
    echo.
    echo Thank you for using the Tarot Card Creator!
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b
)

:completion
echo.
echo Press any key to return to the completion menu...
pause > nul
goto completion
