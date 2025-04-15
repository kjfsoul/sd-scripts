# Tarot Card Creation Guide

This guide provides step-by-step instructions for creating your own tarot card deck using the Tarot Deck Creation System.

## Getting Started

1. **Launch the System**:
   - Double-click the "Tarot Creator (Improved)" icon on your desktop
   - This will:
     - Start Automatic1111 in your browser
     - Set up all necessary directories and files
     - Launch the Master Control Panel

2. **Prepare Your Reference Images**:
   - Place 5-10 reference images in the `reference/images` folder
   - These should represent the artistic style you want for your tarot deck
   - Use consistent image sizes for best results

## Step-by-Step Workflow

### Step 1: Analyze Your Style

3. **Scan Reference Images** (Option 1 in Master Control Panel):
   - This analyzes your reference images and generates text prompts
   - The system extracts visual elements, colors, and styles
   - Prompts are saved in the `reference/prompts` folder

4. **Analyze Deck Style** (Option 2):
   - This examines all the generated prompts to find common patterns
   - It identifies recurring elements, colors, and artistic styles
   - The result is saved in `deck_style.txt`

5. **Enhance Deck Style** (Option 3):
   - This cleans up and organizes the suggested style
   - It removes redundancies and categorizes elements
   - The enhanced style is saved in `enhanced_deck_style.txt`

### Step 2: Create a Style Guide

6. **Setup Tarot Reference Database** (Option 4):
   - This creates a database of tarot card symbolism and meanings
   - It includes traditional elements for each card
   - This information helps create more accurate prompts

7. **Generate Style Guide** (Option 5):
   - Creates a comprehensive style guide for your deck
   - Combines your reference style with tarot symbolism
   - Provides a consistent framework for all cards

### Step 3: Refine Your Prompts

8. **Refine Prompts** (Option 6):
   - This is the heart of the creative process
   - The Prompt Refiner interface will open
   - Follow these steps in the Prompt Refiner:

     a. **Select a Card**: Choose from the dropdown menu (start with The Fool)

     b. **Choose a Style Template**: Select a template that matches your vision

     c. **Add Elements**: Click on suggestions from different categories:
        - Art Style (e.g., fantasy art, mystical)
        - Color Palette (e.g., vibrant colors, teal and cyan)
        - Lighting (e.g., moonlight ambiance)
        - Composition (e.g., centered composition)
        - Character Details (e.g., intricate costume details)
        - Environment (e.g., mystical throne, glowing stone arch)
        - Symbolism (e.g., magical symbols)
        - Mood/Atmosphere (e.g., mysterious, ethereal)
        - Technical Details (e.g., highly detailed)

     d. **Add Artist Influence**: Click on an artist name to add their style

     e. **Review the Negative Prompt**: This helps avoid common issues

     f. **Save the Prompt**: This stores the prompt for the selected card

     g. **Repeat for Each Card**: Start with 3 cards for initial testing

### Step 4: Generate Initial Cards

9. **Generate Initial Samples** (Option 9):
   - This will create 3 cards with 2 variations each
   - The system uses your refined prompts
   - Images are saved in the `images/cards` folder

10. **Review and Provide Feedback** (Option 12):
    - The Feedback Interface will open
    - Navigate through the generated cards
    - Rate different aspects of each card
    - Add comments and edit prompts if needed
    - Accept or reject each card

11. **Regenerate Cards** (Option 13):
    - Regenerate any cards that need improvement
    - The system will use your edited prompts

### Step 5: Generate Full Deck

12. **Generate Major Arcana** (Option 10):
    - This will create all 22 Major Arcana cards
    - The system uses your refined prompts and style

13. **Add Borders and Elements** (Option 16):
    - This adds borders, nameplates, and numerals to your cards
    - You can customize the appearance of these elements

14. **View Final Images** (Option 18):
    - This opens the folder with your completed tarot cards

## Prompt Refinement Tips

### Structure of an Effective Prompt

1. **Card Description**: Basic description of the card
   - Example: "The Fool tarot card, young person standing near cliff edge"

2. **Key Symbols**: Important symbolic elements for the card
   - Example: "small white dog, cliff edge, bundle on stick, mountains in background"

3. **Art Style**: Your preferred artistic style
   - Example: "fantasy art, mystical, art nouveau, ethereal"

4. **Color & Lighting**: Color palette and lighting effects
   - Example: "teal and cyan color palette, moonlight ambiance, ethereal glow"

5. **Technical Details**: Level of detail and quality
   - Example: "highly detailed, ultra detailed, realistic digital painting"

6. **Artist Influence**: Artists whose style you want to emulate
   - Example: "in the style of Aaron Jasinski, Edgar Ainsworth"

### Example Prompts

#### The Fool

```
The Fool tarot card, young person in colorful clothes standing near cliff edge, small white dog, bundle on stick, mountains in background, fantasy art, mystical, art nouveau, teal and cyan color palette, moonlight ambiance, ethereal glow, mystical atmosphere, highly detailed, realistic digital painting, in the style of Aaron Jasinski, Edgar Ainsworth
```

#### The Magician

```
The Magician tarot card, robed figure at altar with magical tools, infinity symbol above head, one hand pointing up and one down, fantasy art, mystical, art nouveau, teal and cyan color palette, moonlight ambiance, ethereal glow, mystical atmosphere, highly detailed, realistic digital painting, in the style of Aaron Jasinski, Edgar Ainsworth
```jfui

## Troubleshooting

### Automatic1111 Not Starting
- Make sure you have the correct path in the script
- Try running `webui.bat` directly from your Stable Diffusion folder
- Check if there are any error messages in the command prompt window

### Prompt Refiner Not Working
- Make sure all dependencies are installed
- Check if the necessary directories exist
- Try running `prompt_refiner.bat` directly

### Generated Images Have Issues
- Refine your prompts to be more specific
- Adjust the negative prompt to avoid common problems
- Try different style templates or artist influences

### Need More Help?
- Check the documentation in the `docs` folder
- Look for error messages in the command prompt windows
- Try running individual components separately to isolate issues
