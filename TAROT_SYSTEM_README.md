# Tarot Deck Creation System

A comprehensive system for creating custom tarot card decks using Stable Diffusion Automatic1111.

## Overview

This system provides a complete workflow for creating custom tarot card decks, from analyzing reference images to generating the final cards with borders and text. It's designed to be flexible, user-friendly, and produce high-quality results.

## Features

- **Reference Image Analysis**: Scan and analyze reference images to extract style information
- **Style Guide Generation**: Create comprehensive style guides for consistent deck creation
- **Batch Processing**: Generate entire decks in manageable batches
- **Custom Elements**: Add borders, nameplates, and numerals to cards
- **Multiple Style Templates**: Choose from pre-defined style templates or create your own
- **Client Questionnaire**: Gather style preferences systematically
- **Standard Sizing**: All cards use the standard size for virtual tarot cards (900x1500 pixels)

## Getting Started

### Prerequisites

- Stable Diffusion Automatic1111 with API enabled
- Python 3.8+
- Required Python packages (requests, Pillow)

### Installation

1. Clone or download this repository
2. Run `install_dependencies.bat` to install required Python packages
3. Make sure Automatic1111 is running with the API enabled

### Quick Start

1. Run `tarot_master.bat` to open the Master Control Panel
2. Follow the numbered steps in order:
   - Step 1: Analyze reference images and generate a style
   - Step 2: Create a style guide and configure settings
   - Step 3: Generate the cards
   - Step 4: Add borders and finalize the deck

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

### Step 4: Finalization

10. **Add Elements**: Add borders, nameplates, and numerals to the generated cards
11. **Review**: Review the final cards and make any necessary adjustments

## Directory Structure

```
.
├── advanced_tarot_generator.py    # Main generator script
├── analyze_deck_style.py          # Style analyzer script
├── enhance_deck_prompt.py         # Prompt enhancer script
├── batch_generate_deck.py         # Batch processing script
├── add_card_elements.py           # Element adder script
├── generate_style_guide.py        # Style guide generator script
├── tarot_master.bat               # Master control panel
├── config/                        # Configuration files
├── elements/                      # Custom elements
│   ├── borders/                   # Border images
│   ├── nameplates/                # Nameplate images
│   └── numerals/                  # Numeral plate images
├── images/                        # Generated images
│   ├── cards/                     # Raw card images
│   └── final/                     # Finalized cards with elements
├── reference/                     # Reference materials
│   ├── images/                    # Reference images
│   └── prompts/                   # Generated prompts
└── style_templates/               # Pre-defined style templates
```

## Customization

- **Style Templates**: Add your own style templates to the `style_templates` directory
- **Custom Elements**: Add your own borders, nameplates, and numerals to the `elements` directory
- **Configuration**: Modify the configuration files in the `config` directory

## Troubleshooting

If you encounter issues:

1. **API Connection Errors**: Make sure Automatic1111 is running with the API enabled
2. **Image Generation Errors**: Check the Automatic1111 console for error messages
3. **Missing Dependencies**: Run `install_dependencies.bat` to install required packages

## License

[MIT License](LICENSE)
