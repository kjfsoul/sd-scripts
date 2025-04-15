#!/usr/bin/env python3
"""
Batch Tarot Deck Generator - Generates complete tarot decks in batches
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path

# Configuration
OUTPUT_DIR = "images/cards"
PROMPT_DIR = "reference/prompts"
CONFIG_FILE = "config/batch_config.json"

# Tarot card definitions
MAJOR_ARCANA = [
    {"name": "The Fool", "numeral": "0"},
    {"name": "The Magician", "numeral": "I"},
    {"name": "The High Priestess", "numeral": "II"},
    {"name": "The Empress", "numeral": "III"},
    {"name": "The Emperor", "numeral": "IV"},
    {"name": "The Hierophant", "numeral": "V"},
    {"name": "The Lovers", "numeral": "VI"},
    {"name": "The Chariot", "numeral": "VII"},
    {"name": "Strength", "numeral": "VIII"},
    {"name": "The Hermit", "numeral": "IX"},
    {"name": "Wheel of Fortune", "numeral": "X"},
    {"name": "Justice", "numeral": "XI"},
    {"name": "The Hanged Man", "numeral": "XII"},
    {"name": "Death", "numeral": "XIII"},
    {"name": "Temperance", "numeral": "XIV"},
    {"name": "The Devil", "numeral": "XV"},
    {"name": "The Tower", "numeral": "XVI"},
    {"name": "The Star", "numeral": "XVII"},
    {"name": "The Moon", "numeral": "XVIII"},
    {"name": "The Sun", "numeral": "XIX"},
    {"name": "Judgement", "numeral": "XX"},
    {"name": "The World", "numeral": "XXI"}
]

MINOR_ARCANA_SUITS = ["Wands", "Cups", "Swords", "Pentacles"]
MINOR_ARCANA_COURTS = ["Page", "Knight", "Queen", "King"]
MINOR_ARCANA_NUMBERS = list(range(1, 11))  # 1 (Ace) through 10

def load_config():
    """Load batch configuration from file or create default"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return create_default_config()
    else:
        return create_default_config()

def create_default_config():
    """Create default batch configuration"""
    config = {
        "style_prompt": "fantasy art, mystical, art nouveau, storybook illustration, ultrafine detailed",
        "variations": 2,
        "batch_size": 5,
        "wait_time": 10,  # seconds to wait between batches
        "major_arcana_only": False,
        "include_suits": ["Wands", "Cups", "Swords", "Pentacles"],
        "include_courts": True,
        "include_numbers": True,
        "custom_descriptions": {}
    }
    
    # Save default config
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    
    return config

def save_config(config):
    """Save configuration to file"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {CONFIG_FILE}")

def load_style_prompt():
    """Load style prompt from file if available"""
    # Try to load from finalized_deck_style.txt first
    if os.path.exists("finalized_deck_style.txt"):
        try:
            with open("finalized_deck_style.txt", 'r') as f:
                content = f.read()
                # Look for the simple version
                match = content.find("## Simple Version")
                if match != -1:
                    lines = content[match:].split('\n')
                    if len(lines) > 1:
                        return lines[1].strip()
        except Exception:
            pass
    
    # Try enhanced_deck_style.txt next
    if os.path.exists("enhanced_deck_style.txt"):
        try:
            with open("enhanced_deck_style.txt", 'r') as f:
                content = f.read()
                # Look for the enhanced prompt
                match = content.find("## Enhanced Prompt")
                if match != -1:
                    lines = content[match:].split('\n')
                    if len(lines) > 1:
                        return lines[1].strip()
        except Exception:
            pass
    
    # Finally try deck_style.txt
    if os.path.exists("deck_style.txt"):
        try:
            with open("deck_style.txt", 'r') as f:
                content = f.read()
                # Look for the suggested prompt
                match = content.find("## Suggested Deck Style Prompt")
                if match != -1:
                    lines = content[match:].split('\n')
                    if len(lines) > 1:
                        return lines[1].strip()
        except Exception:
            pass
    
    return None

def get_all_cards(config):
    """Get a list of all cards to generate based on configuration"""
    cards = []
    
    # Add Major Arcana
    cards.extend(MAJOR_ARCANA)
    
    # Add Minor Arcana if needed
    if not config["major_arcana_only"]:
        # Add number cards
        if config["include_numbers"]:
            for suit in config["include_suits"]:
                for num in MINOR_ARCANA_NUMBERS:
                    if num == 1:
                        name = f"Ace of {suit}"
                    else:
                        name = f"{num} of {suit}"
                    cards.append({"name": name, "numeral": str(num)})
        
        # Add court cards
        if config["include_courts"]:
            for suit in config["include_suits"]:
                for court in MINOR_ARCANA_COURTS:
                    name = f"{court} of {suit}"
                    cards.append({"name": name, "numeral": court[0]})
    
    return cards

def generate_batch(start_idx, batch_size, cards, config):
    """Generate a batch of cards"""
    end_idx = min(start_idx + batch_size, len(cards))
    batch_cards = cards[start_idx:end_idx]
    
    print(f"\nGenerating batch of {len(batch_cards)} cards...")
    
    # Prepare command
    cmd = [
        "python", "advanced_tarot_generator.py",
        "--generate",
        "--style", config["style_prompt"],
        "--variations", str(config["variations"]),
        "--cards", str(len(batch_cards)),
        "--start", str(start_idx)
    ]
    
    # Run the command
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating batch: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Batch Tarot Deck Generator")
    parser.add_argument("--configure", action="store_true", help="Configure batch settings")
    parser.add_argument("--style", type=str, help="Style prompt to use")
    parser.add_argument("--variations", type=int, help="Number of variations per card")
    parser.add_argument("--batch-size", type=int, help="Number of cards per batch")
    parser.add_argument("--major-only", action="store_true", help="Generate only Major Arcana")
    parser.add_argument("--start", type=int, default=0, help="Starting index")
    parser.add_argument("--end", type=int, help="Ending index (inclusive)")
    
    args = parser.parse_args()
    
    print("Batch Tarot Deck Generator")
    print("=========================")
    
    # Load configuration
    config = load_config()
    
    # Update config with command line arguments
    if args.style:
        config["style_prompt"] = args.style
    elif not config["style_prompt"]:
        # Try to load from style files
        style_prompt = load_style_prompt()
        if style_prompt:
            config["style_prompt"] = style_prompt
    
    if args.variations:
        config["variations"] = args.variations
    
    if args.batch_size:
        config["batch_size"] = args.batch_size
    
    if args.major_only:
        config["major_arcana_only"] = True
    
    # Configure mode
    if args.configure:
        print("\nConfigure Batch Settings")
        print("======================")
        
        # Style prompt
        print(f"\nCurrent style prompt: {config['style_prompt']}")
        new_prompt = input("Enter new style prompt (or press Enter to keep current): ")
        if new_prompt:
            config["style_prompt"] = new_prompt
        
        # Variations
        print(f"\nCurrent variations per card: {config['variations']}")
        try:
            new_variations = input("Enter number of variations (1-5, or press Enter to keep current): ")
            if new_variations:
                config["variations"] = max(1, min(5, int(new_variations)))
        except ValueError:
            print("Invalid input. Keeping current value.")
        
        # Batch size
        print(f"\nCurrent batch size: {config['batch_size']}")
        try:
            new_batch_size = input("Enter batch size (1-10, or press Enter to keep current): ")
            if new_batch_size:
                config["batch_size"] = max(1, min(10, int(new_batch_size)))
        except ValueError:
            print("Invalid input. Keeping current value.")
        
        # Major Arcana only
        print(f"\nCurrent setting: {'Major Arcana only' if config['major_arcana_only'] else 'Full deck'}")
        major_only = input("Generate Major Arcana only? (Y/N, or press Enter to keep current): ").strip().lower()
        if major_only == 'y':
            config["major_arcana_only"] = True
        elif major_only == 'n':
            config["major_arcana_only"] = False
        
        # If generating full deck, configure suits
        if not config["major_arcana_only"]:
            print("\nInclude which suits? (Enter comma-separated list)")
            print(f"Current suits: {', '.join(config['include_suits'])}")
            suits_input = input("Enter suits (Wands,Cups,Swords,Pentacles, or press Enter to keep current): ")
            if suits_input:
                suits = [s.strip() for s in suits_input.split(',')]
                valid_suits = [s for s in suits if s in MINOR_ARCANA_SUITS]
                if valid_suits:
                    config["include_suits"] = valid_suits
            
            # Court cards
            print(f"\nInclude court cards? (Currently: {'Yes' if config['include_courts'] else 'No'})")
            courts = input("Include court cards? (Y/N, or press Enter to keep current): ").strip().lower()
            if courts == 'y':
                config["include_courts"] = True
            elif courts == 'n':
                config["include_courts"] = False
            
            # Number cards
            print(f"\nInclude number cards? (Currently: {'Yes' if config['include_numbers'] else 'No'})")
            numbers = input("Include number cards? (Y/N, or press Enter to keep current): ").strip().lower()
            if numbers == 'y':
                config["include_numbers"] = True
            elif numbers == 'n':
                config["include_numbers"] = False
        
        # Save configuration
        save_config(config)
        print("\nConfiguration updated.")
        
        # Ask if user wants to start generation
        start_gen = input("\nStart generating cards now? (Y/N): ").strip().lower()
        if start_gen != 'y':
            return 0
    
    # Check if style prompt is set
    if not config["style_prompt"]:
        print("Error: No style prompt specified.")
        print("Please run with --configure to set a style prompt or specify with --style.")
        return 1
    
    # Get all cards to generate
    all_cards = get_all_cards(config)
    
    # Determine start and end indices
    start_idx = args.start
    end_idx = args.end if args.end is not None else len(all_cards) - 1
    
    # Validate indices
    if start_idx < 0 or start_idx >= len(all_cards):
        print(f"Error: Start index {start_idx} is out of range (0-{len(all_cards)-1}).")
        return 1
    
    if end_idx < start_idx or end_idx >= len(all_cards):
        print(f"Error: End index {end_idx} is out of range ({start_idx}-{len(all_cards)-1}).")
        return 1
    
    # Calculate number of cards to generate
    num_cards = end_idx - start_idx + 1
    
    # Calculate number of batches
    batch_size = config["batch_size"]
    num_batches = (num_cards + batch_size - 1) // batch_size
    
    print(f"\nGenerating {num_cards} cards in {num_batches} batches")
    print(f"Starting with: {all_cards[start_idx]['name']}")
    print(f"Ending with: {all_cards[end_idx]['name']}")
    print(f"Using style: {config['style_prompt']}")
    print(f"Variations per card: {config['variations']}")
    
    # Confirm
    confirm = input("\nProceed with generation? (Y/N): ").strip().lower()
    if confirm != 'y':
        print("Generation cancelled.")
        return 0
    
    # Generate batches
    current_idx = start_idx
    for batch_num in range(num_batches):
        print(f"\nBatch {batch_num + 1} of {num_batches}")
        
        # Generate batch
        success = generate_batch(current_idx, batch_size, all_cards, config)
        
        # Update current index
        current_idx += batch_size
        
        # If more batches to go, wait a bit
        if batch_num < num_batches - 1 and success:
            wait_time = config["wait_time"]
            print(f"\nWaiting {wait_time} seconds before next batch...")
            time.sleep(wait_time)
    
    print("\nBatch generation complete!")
    print(f"Check the {OUTPUT_DIR} directory for the generated images.")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        exit(1)
