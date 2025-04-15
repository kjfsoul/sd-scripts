# Enhanced Tarot Deck Creation System

A comprehensive system for creating custom tarot card decks using Stable Diffusion Automatic1111, with advanced feedback and refinement capabilities.

## Overview

This enhanced system provides a complete workflow for creating custom tarot card decks, from analyzing reference images to generating the final cards with borders and text. It features a robust user feedback interface, improved image composition, and a streamlined workflow.

## Key Features

- **Reference Image Analysis**: Scan and analyze reference images to extract style information
- **Style Guide Generation**: Create comprehensive style guides for consistent deck creation
- **Batch Processing**: Generate entire decks in manageable batches
- **User Feedback Interface**: Review, rate, and provide feedback on generated cards
- **Prompt Refinement**: Edit prompts and regenerate cards based on feedback
- **Improved Image Composition**: Ensures proper spacing for borders and prevents cut-offs
- **Custom Elements**: Add borders, nameplates, and numerals to cards
- **Multiple Style Templates**: Choose from pre-defined style templates or create your own
- **Client Questionnaire**: Gather style preferences systematically

## Getting Started

### Prerequisites

- Stable Diffusion Automatic1111 with API enabled
- Python 3.8+
- Required Python packages (requests, Pillow, tkinter)

### Installation

1. Clone or download this repository
2. Run `install_dependencies.bat` to install required Python packages and create the directory structure
3. Make sure Automatic1111 is running with the API enabled

### Quick Start

1. Run `tarot_master.bat` to open the Master Control Panel
2. Follow the numbered steps in order:
   - Step 1: Analyze reference images and generate a style
   - Step 2: Create a style guide and configure settings
   - Step 3: Generate the initial cards
   - Step 4: Review and provide feedback on the cards
   - Step 5: Add borders and finalize the deck

## Workflow

### Step 1: Reference Images and Style Analysis

1. **Scan Reference Images**: Place reference images in the `reference/images` folder and scan them to generate prompts
2. **Analyze Deck Style**: Analyze the generated prompts to find common patterns and suggest a cohesive style
3. **Enhance Deck Style**: Clean up and organize the suggested style for better results

### Step 2: Style Guide and Configuration

4. **Generate Style Guide**: Create a comprehensive style guide document for the project
5. **Configure Batch Settings**: Set up batch generation parameters (style, variations, batch size)
6. **Configure Element Settings**: Set up border, nameplate, and numeral settings

### Step 3: Card Generation

7. **Generate Initial Samples**: Create 3 sample cards with 2 variations each for review
8. **Generate Major Arcana**: Generate the 22 Major Arcana cards
9. **Generate Full Deck**: Generate the complete deck including Minor Arcana

### Step 4: Feedback and Refinement

10. **Review Cards**: Use the feedback interface to review and rate each card
11. **Edit Prompts**: Modify prompts for cards that need improvement
12. **Regenerate Cards**: Regenerate specific cards based on feedback

### Step 5: Finalization

13. **Add Elements**: Add borders, nameplates, and numerals to the generated cards
14. **Review Final Cards**: Review the final cards with all elements added
15. **Export Deck**: Export the complete deck for use

## User Feedback Interface

The enhanced system includes a dedicated user feedback interface that allows you to:

- View all generated cards in a user-friendly interface
- Rate different aspects of each card (composition, style consistency, etc.)
- Provide detailed comments on each card
- Edit prompts directly in the interface
- Regenerate cards with improved prompts
- Quickly accept or reject cards

### Using the Feedback Interface

1. Run `user_feedback_interface.bat` or select option 10 from the Master Control Panel
2. Navigate between cards using the Previous/Next buttons or arrow keys
3. Rate different aspects of each card using the rating scales
4. Add comments in the Comments field
5. Edit the prompt in the Edit Prompt field if needed
6. Click "Save Feedback" to save your feedback
7. Click "Regenerate" to regenerate the card with the edited prompt
8. Use the Accept/Reject buttons for quick feedback

## Image Composition Improvements

The enhanced system includes several improvements to ensure proper image composition:

- **Centered Composition**: Ensures the main subject is centered in the frame
- **Complete Scene**: Prevents important elements from being cut off
- **Margin Space**: Leaves adequate space around the edges for borders
- **High-Resolution Fix**: Uses Stable Diffusion's high-res fix for better details
- **Negative Prompts**: Includes specific negative prompts to prevent cut-offs and ensure proper margins

## Directory Structure

```
.
├── advanced_tarot_generator.py    # Main generator script
├── analyze_deck_style.py          # Style analyzer script
├── enhance_deck_prompt.py         # Prompt enhancer script
├── batch_generate_deck.py         # Batch processing script
├── add_card_elements.py           # Element adder script
├── generate_style_guide.py        # Style guide generator script
├── user_feedback_interface.py     # User feedback interface
├── regenerate_card.py             # Card regeneration script
├── tarot_master.bat               # Master control panel
├── config/                        # Configuration files
├── elements/                      # Custom elements
│   ├── borders/                   # Border images
│   ├── nameplates/                # Nameplate images
│   └── numerals/                  # Numeral plate images
├── feedback/                      # User feedback data
├── images/                        # Generated images
│   ├── cards/                     # Raw card images
│   └── final/                     # Finalized cards with elements
├── prompts/                       # Prompt files
│   └── cards/                     # Card-specific prompts
├── reference/                     # Reference materials
│   ├── images/                    # Reference images
│   └── prompts/                   # Generated prompts
└── style_templates/               # Pre-defined style templates
```

## Customization

- **Style Templates**: Add your own style templates to the `style_templates` directory
- **Custom Elements**: Add your own borders, nameplates, and numerals to the `elements` directory
- **Feedback Categories**: Modify the feedback categories in the `config/feedback_config.json` file
- **Image Parameters**: Adjust image generation parameters in the `advanced_tarot_generator.py` file

## Troubleshooting

If you encounter issues:

1. **API Connection Errors**: Make sure Automatic1111 is running with the API enabled
2. **Image Generation Errors**: Check the Automatic1111 console for error messages
3. **Missing Dependencies**: Run `install_dependencies.bat` to install required packages
4. **Directory Structure Issues**: Run `create_directory_structure.py` to ensure all directories exist

## License

[MIT License](LICENSE)
