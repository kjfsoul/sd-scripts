# Tarot Creator 1111

A user-friendly tool for creating custom tarot card decks using Stable Diffusion Automatic1111.

## Overview

Tarot Creator 1111 is a comprehensive tool that guides users through the process of creating custom tarot card decks. It provides a structured workflow for generating card imagery, borders, and text elements, all powered by Stable Diffusion Automatic1111.

## Features

- **Interactive Prompt Generation**: Helps users craft optimal prompts based on their vision
- **Iterative Design Process**: Generate initial samples, gather feedback, and refine
- **Modular Components**: Separate generation of card imagery, borders, and text elements
- **Batch Processing**: Generate cards in manageable batches
- **Export Options**: Prepare decks for virtual use or physical printing

## Getting Started

### Prerequisites

- Stable Diffusion Automatic1111 with API enabled
- Python 3.8+
- Required Python packages (requests, Pillow)

### Installation

1. Clone or download this repository
2. Run `install_dependencies.bat` to install required Python packages

### Enabling the Automatic1111 API

Before using this tool, you need to enable the API in Automatic1111:

1. Open your `webui-user.bat` file in the Automatic1111 directory
2. Add `--api` to the `COMMANDLINE_ARGS` line:
   ```
   set COMMANDLINE_ARGS=--api
   ```
3. Restart Automatic1111

### Usage

1. Start Automatic1111 with the API enabled
2. Run `check_api.bat` to verify the connection
3. Run `generate_initial_cards.bat` to create the first 3 cards
4. Review the generated images in the `images/cards` directory
5. Provide feedback to refine the style
6. Run `run_tarot_creator.bat` for more options

## Workflow

1. **Initial Consultation**: Define the overall style and theme for the deck
2. **Sample Generation**: Create 3 major arcana cards for review and feedback
3. **Style Refinement**: Iterate on the samples until the desired style is achieved
4. **Batch Generation**: Create remaining cards in batches of manageable size
5. **Border Creation**: Generate and select custom borders
6. **Text Elements**: Create and position archetype names and numerals
7. **Final Assembly**: Combine all elements into finished cards
8. **Export**: Prepare the deck for virtual use or physical printing

## Troubleshooting

If you encounter any issues:

1. **API Connection**: Make sure Automatic1111 is running with the API enabled
2. **Missing Dependencies**: Run `install_dependencies.bat`
3. **Image Generation Errors**: Check the error messages and ensure Automatic1111 is working properly
4. **Path Issues**: Make sure you're running the scripts from the project directory

## License

[MIT License](LICENSE)
