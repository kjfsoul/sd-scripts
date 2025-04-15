# Tarot Card Generation Project

This project helps you generate tarot card images using Stable Diffusion with your trained LoRA model.

## Getting Started

1. Make sure your Stable Diffusion environment is set up and your LoRA model is trained.
2. Use the provided scripts to manage your tarot card prompts and generation process.

## Files in this Project

- `generate_tarot_improved.py` - Main script for managing tarot card prompts
- `tarot_cards.json` - JSON file containing all card definitions and prompts
- `generate_tarot.bat` - Batch file for easy execution of the script
- `tarot_output/` - Directory where generated images and prompt files are stored

## How to Use

### Generating Initial Cards

1. Run the script to display generation instructions:
   ```
   python generate_tarot_improved.py
   ```
   or simply double-click `generate_tarot.bat`

2. Copy each prompt and use it in the Automatic1111 web UI with these settings:
   - Steps: 40
   - Sampler: DPM++ 2M Karras or Euler a
   - CFG Scale: 7.5
   - Size: 512x768 (portrait orientation for tarot cards)
   - Use your trained LoRA: fool_hypernetwork.safetensors with weight 0.8

3. Save the generated images to the `tarot_output` folder with appropriate names:
   - fool_v1.png, fool_v2.png
   - highpriestess_v1.png, highpriestess_v2.png
   - star_v1.png, star_v2.png

### Refining Prompts Based on Feedback

1. Create a text file with your updated prompt (e.g., `updated_fool_v1.txt`)

2. Update the card prompt using:
   ```
   python generate_tarot_improved.py --update-card "The Fool" 1 updated_fool_v1.txt
   ```

3. Generate new images using the updated prompts

### Adding More Cards

1. Edit the `tarot_cards.json` file to add new card definitions
2. Run the script again to get the new generation instructions

## Workflow

1. Generate the initial 3 cards (The Fool, The High Priestess, The Star) with 2 variations each
2. Review the results and provide feedback
3. Refine the prompts based on feedback and regenerate until satisfied
4. Continue with additional cards in batches of 10 (or your preferred batch size)
5. Repeat the feedback and refinement process

## Tips for Best Results

- Keep the core style elements consistent across all cards
- Pay attention to the composition and ensure the figure is prominently featured
- Make sure the text elements (numeral and card name) are clearly visible
- Use the same border style across all cards for a cohesive deck
