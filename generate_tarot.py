import os
import subprocess
import json
from pathlib import Path

# Configuration
OUTPUT_DIR = "tarot_output"
LORA_PATH = "output/fooldeck-lora/fool_hypernetwork.safetensors"
SD_PATH = "C:/Users/kjfsw/sd-models/v1-5-pruned-emaonly.safetensors"
AUTOMATIC1111_PATH = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
WEBUI_PATH = "path/to/your/webui.py"  # Update this with your actual webui.py path

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Tarot card definitions
tarot_cards = [
    {
        "name": "The Fool",
        "numeral": "0",
        "variations": [
            "fooldeck style, The Fool tarot card, pastel art nouveau, ethereal, fantasy soft lighting, a youthful figure in flowing garments standing at the edge of a cliff, white dog companion, dreamy landscape, decorative border, \"0\" at top, \"THE FOOL\" at bottom, elegant sans serif font",
            "fooldeck style, The Fool tarot card, pastel art nouveau, ethereal, fantasy soft lighting, androgynous figure with flower crown carrying a white rose and knapsack, playful white dog, mountain background, decorative art nouveau border, \"0\" at top, \"THE FOOL\" at bottom, elegant sans serif font"
        ]
    },
    {
        "name": "The High Priestess",
        "numeral": "II",
        "variations": [
            "fooldeck style, The High Priestess tarot card, pastel art nouveau, ethereal, fantasy soft lighting, serene woman seated between two pillars, crescent moon at her feet, veil behind her, scroll in hand, water elements, decorative border, \"II\" at top, \"THE HIGH PRIESTESS\" at bottom, elegant sans serif font",
            "fooldeck style, The High Priestess tarot card, pastel art nouveau, ethereal, fantasy soft lighting, mysterious feminine figure with lunar crown, blue robes, pomegranates and dates, sacred geometry, cosmic background, decorative art nouveau border, \"II\" at top, \"THE HIGH PRIESTESS\" at bottom, elegant sans serif font"
        ]
    },
    {
        "name": "The Star",
        "numeral": "XVII",
        "variations": [
            "fooldeck style, The Star tarot card, pastel art nouveau, ethereal, fantasy soft lighting, nude figure kneeling by water pouring from two vessels, one foot on land, one in water, seven stars above, ibis bird, decorative border, \"XVII\" at top, \"THE STAR\" at bottom, elegant sans serif font",
            "fooldeck style, The Star tarot card, pastel art nouveau, ethereal, fantasy soft lighting, graceful figure under starry night sky, pouring water onto earth and into pond, celestial glow, hope and renewal symbolism, decorative art nouveau border, \"XVII\" at top, \"THE STAR\" at bottom, elegant sans serif font"
        ]
    }
]

def save_prompts_to_file():
    """Save all prompts to a text file for reference"""
    with open(os.path.join(OUTPUT_DIR, "tarot_prompts.txt"), "w") as f:
        for card in tarot_cards:
            f.write(f"# {card['name']} ({card['numeral']})\n\n")
            for i, variation in enumerate(card["variations"], 1):
                f.write(f"## Variation {i}\n")
                f.write(f"{variation}\n\n")
            f.write("\n---\n\n")
    
    print(f"Prompts saved to {os.path.join(OUTPUT_DIR, 'tarot_prompts.txt')}")

def generate_images():
    """Generate images using the Automatic1111 API"""
    # This is a placeholder - you'll need to implement the actual API call
    # or command line execution based on your setup
    print("To generate images, please run the following commands in your Automatic1111 interface:")
    
    for card in tarot_cards:
        for i, prompt in enumerate(card["variations"], 1):
            print(f"\n# {card['name']} - Variation {i}")
            print(f"Prompt: {prompt}")
            print("Settings: Steps: 40, Sampler: DPM++ 2M Karras, CFG Scale: 7.5")
            print(f"Use LoRA: {LORA_PATH} with weight 0.8")
            
    print("\nAfter generating, save the images to the 'tarot_output' folder with appropriate names.")

if __name__ == "__main__":
    save_prompts_to_file()
    generate_images()
    print("\nAfter generating all variations, review them and note which ones you prefer.")
    print("You can then modify this script to refine the prompts based on feedback.")
