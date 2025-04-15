@echo off
echo Tarot Deck Creation System - Master Control Panel
echo =============================================
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

:menu
cls
echo Tarot Deck Creation System - Master Control Panel
echo =============================================
echo.
echo STEP 1: REFERENCE IMAGES AND STYLE ANALYSIS
echo ------------------------------------------
echo 1. Scan reference images
echo 2. Analyze deck style
echo 3. Enhance deck style prompt
echo 4. Setup tarot reference database
echo.
echo STEP 2: STYLE GUIDE AND PROMPT REFINEMENT
echo ------------------------------------
echo 5. Generate comprehensive style guide
echo 6. Refine prompts for tarot cards
echo 7. Configure batch generation settings
echo 8. Configure card element settings
echo.
echo STEP 3: CARD GENERATION
echo --------------------
echo 9. Generate initial samples (3 cards)
echo 10. Generate Major Arcana
echo 11. Generate full deck
echo.
echo STEP 4: FEEDBACK AND REFINEMENT
echo ---------------------------
echo 12. Review and provide feedback on cards
echo 13. Regenerate cards based on feedback
echo.
echo STEP 5: PLUGINS AND ENHANCEMENTS
echo ----------------------------
echo 14. Install Automatic1111 plugins
echo 15. Install enhanced dependencies
echo.
echo STEP 6: FINALIZATION
echo -----------------
echo 16. Add borders, nameplates, and numerals
echo 17. View generated images
echo 18. View final images
echo.
echo 19. Exit
echo.

set /p choice="Enter your choice (1-19): "

if "%choice%"=="1" (
    call improved_scan_images.bat
    goto menu
) else if "%choice%"=="2" (
    call analyze_deck_style.bat
    goto menu
) else if "%choice%"=="3" (
    call enhance_deck_prompt.bat
    goto menu
) else if "%choice%"=="4" (
    call setup_tarot_reference_db.bat
    goto menu
) else if "%choice%"=="5" (
    call generate_style_guide.bat
    goto menu
) else if "%choice%"=="6" (
    call prompt_refiner.bat
    goto menu
) else if "%choice%"=="7" (
    python batch_generate_deck.py --configure
    goto menu
) else if "%choice%"=="8" (
    python add_card_elements.py --configure
    goto menu
) else if "%choice%"=="9" (
    python advanced_tarot_generator.py --generate --cards 3 --variations 2 --start 0
    goto menu
) else if "%choice%"=="10" (
    python batch_generate_deck.py --major-only
    goto menu
) else if "%choice%"=="11" (
    python batch_generate_deck.py
    goto menu
) else if "%choice%"=="12" (
    call user_feedback_interface.bat
    goto menu
) else if "%choice%"=="13" (
    echo This will regenerate cards based on feedback.
    echo Please make sure you have provided feedback first.
    echo.
    set /p card_name="Enter card filename to regenerate (or press Enter to cancel): "
    if not "%card_name%"=="" (
        python regenerate_card.py --file "%card_name%"
    )
    goto menu
) else if "%choice%"=="14" (
    call install_a1111_plugins.bat
    goto menu
) else if "%choice%"=="15" (
    call install_enhanced_dependencies.bat
    goto menu
) else if "%choice%"=="16" (
    python add_card_elements.py --all
    goto menu
) else if "%choice%"=="17" (
    if exist "images\cards" (
        start explorer "images\cards"
    ) else (
        echo No generated images found.
        pause
    )
    goto menu
) else if "%choice%"=="18" (
    if exist "images\final" (
        start explorer "images\final"
    ) else (
        echo No final images found.
        pause
    )
    goto menu
) else if "%choice%"=="19" (
    echo Exiting.
    exit /b
) else (
    echo Invalid choice.
    pause
    goto menu
)
