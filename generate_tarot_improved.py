import os
import json
import argparse
from pathlib import Path

# Configuration
OUTPUT_DIR = "tarot_output"
CARDS_JSON = "tarot_cards.json"

def load_tarot_cards():
    """Load tarot card definitions from JSON file"""
    with open(CARDS_JSON, 'r') as f:
        data = json.load(f)
    return data['cards']

def save_prompts_to_file(cards, output_file="tarot_prompts.txt"):
    """Save all prompts to a text file for reference"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(os.path.join(OUTPUT_DIR, output_file), "w") as f:
        for card in cards:
            f.write(f"# {card['name']} ({card['numeral']})\n\n")
            for i, variation in enumerate(card["variations"], 1):
                f.write(f"## Variation {i}\n")
                f.write(f"{variation}\n\n")
            f.write("\n---\n\n")
    
    print(f"Prompts saved to {os.path.join(OUTPUT_DIR, output_file)}")

def display_generation_instructions(cards):
    """Display instructions for generating images"""
    print("\nTo generate images, use these prompts in Automatic1111:")
    print("\nRecommended settings:")
    print("- Steps: 40")
    print("- Sampler: DPM++ 2M Karras or Euler a")
    print("- CFG Scale: 7.5")
    print("- Size: 512x768 (portrait orientation for tarot cards)")
    print("- Use your trained LoRA: fool_hypernetwork.safetensors with weight 0.8")
    
    for card in cards:
        print(f"\n\n{'='*50}")
        print(f"# {card['name']} ({card['numeral']})")
        print(f"{'='*50}")
        
        for i, prompt in enumerate(card["variations"], 1):
            print(f"\n## Variation {i}")
            print(f"\nPrompt:\n{prompt}")
            
    print("\nAfter generating, save the images to the 'tarot_output' folder with names like:")
    print("- fool_v1.png, fool_v2.png")
    print("- highpriestess_v1.png, highpriestess_v2.png")
    print("- star_v1.png, star_v2.png")

def update_card_prompt(cards, card_name, variation_num, new_prompt):
    """Update a specific card's prompt"""
    for card in cards:
        if card['name'].lower() == card_name.lower():
            if 1 <= variation_num <= len(card['variations']):
                card['variations'][variation_num-1] = new_prompt
                return True
    return False

def save_cards_to_json(cards):
    """Save updated cards back to JSON file"""
    with open(CARDS_JSON, 'w') as f:
        json.dump({"cards": cards}, f, indent=2)
    print(f"Updated card definitions saved to {CARDS_JSON}")

def main():
    parser = argparse.ArgumentParser(description='Tarot Card Generation Helper')
    parser.add_argument('--display', action='store_true', help='Display generation instructions')
    parser.add_argument('--save-prompts', action='store_true', help='Save prompts to text file')
    parser.add_argument('--update-card', nargs=3, metavar=('CARD_NAME', 'VARIATION_NUM', 'NEW_PROMPT_FILE'), 
                        help='Update a card prompt (reads prompt from file)')
    
    args = parser.parse_args()
    
    # Load card definitions
    cards = load_tarot_cards()
    
    if args.update_card:
        card_name, variation_num, prompt_file = args.update_card
        try:
            with open(prompt_file, 'r') as f:
                new_prompt = f.read().strip()
            
            if update_card_prompt(cards, card_name, int(variation_num), new_prompt):
                save_cards_to_json(cards)
                print(f"Updated {card_name} variation {variation_num}")
            else:
                print(f"Card {card_name} or variation {variation_num} not found")
        except FileNotFoundError:
            print(f"Prompt file {prompt_file} not found")
    
    if args.save_prompts:
        save_prompts_to_file(cards)
    
    if args.display or (not args.save_prompts and not args.update_card):
        display_generation_instructions(cards)

if __name__ == "__main__":
    main()
