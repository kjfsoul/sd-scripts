# Advanced Tarot Card Generator

A comprehensive tool for creating custom tarot card decks using Stable Diffusion Automatic1111, with support for reference image analysis, custom prompts, and proper aspect ratios.

## Features

- **Standard Tarot Card Size**: Uses 900x1500 pixels (2.75 x 4.75 inches at 300 DPI) - the standard size for virtual tarot cards
- **No Borders or Cut-offs**: Specifically designed to avoid borders and ensure complete images
- **Reference Image Analysis**: Scan your existing images to generate prompts based on their style and content
- **Custom Prompt Creation**: Create and save custom prompts for each card
- **Multiple Variations**: Generate multiple variations of each card
- **xformers Support**: Detects and utilizes xformers for better performance if available
- **Command Line Interface**: Run with specific options or use the interactive mode

## Getting Started

### Prerequisites

- Stable Diffusion Automatic1111 with API enabled
- Python 3.8+
- Required Python packages (requests, Pillow)

### Enabling the Automatic1111 API

Before using this tool, you need to enable the API in Automatic1111:

1. Open your `webui-user.bat` file in the Automatic1111 directory
2. Add `--api` to the `COMMANDLINE_ARGS` line:
   ```
   set COMMANDLINE_ARGS=--xformers --api
   ```
3. Restart Automatic1111

### Using Reference Images

To use your own reference images:

1. Place your reference images in the `reference/images` folder
2. Run `scan_reference_images.bat` to analyze them
3. The generated prompts will be saved in the `reference/prompts` folder
4. These prompts can be used as a starting point for your tarot card generation

## Usage

### Interactive Mode

1. Run `run_advanced_generator.bat`
2. Follow the on-screen prompts to:
   - Choose whether to scan reference images or generate cards
   - Define your artistic style
   - Specify the number of variations
   - Provide custom descriptions for each card

### Command Line Options

You can also run the script directly with command line options:

```
python advanced_tarot_generator.py [options]
```

Options:
- `--scan`: Scan reference images and generate prompts
- `--generate`: Generate tarot cards
- `--style TEXT`: Style to use for generation
- `--variations N`: Number of variations per card (default: 2)
- `--cards N`: Number of cards to generate (default: 3)
- `--start N`: Starting index for cards (default: 0)

Examples:
```
# Scan reference images
python advanced_tarot_generator.py --scan

# Generate 3 cards with 2 variations each
python advanced_tarot_generator.py --generate --style "fantasy art, vibrant colors" --variations 2 --cards 3

# Generate cards 5-10 with 3 variations each
python advanced_tarot_generator.py --generate --style "art nouveau, ethereal" --variations 3 --cards 6 --start 5
```

## Troubleshooting

If you encounter issues:

1. **API Connection Errors**: Make sure Automatic1111 is running with the API enabled
2. **Image Generation Errors**: Check the Automatic1111 console for error messages
3. **Cut-off Images**: The script is designed to avoid this, but if it happens, try adjusting the aspect ratio
4. **Border Issues**: The script includes negative prompts to avoid borders, but you may need to adjust them

## Directory Structure

```
.
├── advanced_tarot_generator.py    # Main Python script
├── run_advanced_generator.bat     # Batch file to run the generator
├── scan_reference_images.bat      # Batch file to scan reference images
├── images/                        # Generated images
│   └── cards/                     # Generated tarot cards
├── reference/                     # Reference materials
│   ├── images/                    # Your reference images
│   └── prompts/                   # Generated/saved prompts
└── README_ADVANCED.md             # This file
```

## License

[MIT License](LICENSE)
