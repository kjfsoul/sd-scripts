#!/usr/bin/env python3
"""
Regenerate Tarot Card - Regenerates a specific tarot card based on feedback
"""

import os
import sys
import json
import argparse
from pathlib import Path

def regenerate_card(filename):
    """Regenerate a specific card"""
    # Check if file exists
    card_path = os.path.join("images/cards", filename)
    if not os.path.exists(card_path):
        print(f"Error: Card file not found: {card_path}")
        return False
    
    # Get prompt file
    prompt_file = os.path.join("prompts/cards", f"{os.path.splitext(filename)[0]}.txt")
    
    # Check if feedback exists
    feedback_file = os.path.join("feedback", f"{os.path.splitext(filename)[0]}_feedback.json")
    
    prompt = None
    
    # Try to get prompt from feedback
    if os.path.exists(feedback_file):
        try:
            with open(feedback_file, 'r') as f:
                feedback = json.load(f)
                if "edited_prompt" in feedback:
                    prompt = feedback["edited_prompt"]
        except Exception as e:
            print(f"Error reading feedback: {e}")
    
    # If no prompt in feedback, try to get from prompt file
    if not prompt and os.path.exists(prompt_file):
        try:
            with open(prompt_file, 'r') as f:
                prompt = f.read().strip()
        except Exception as e:
            print(f"Error reading prompt file: {e}")
    
    if not prompt:
        print("Error: No prompt found for regeneration.")
        return False
    
    # Import the generator module
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        import advanced_tarot_generator
        
        # Extract card info from filename
        card_base = os.path.splitext(filename)[0]
        if "_v" in card_base:
            card_base, variation = card_base.split("_v")
            variation = int(variation)
        else:
            variation = 1
        
        # Create generator instance
        generator = advanced_tarot_generator.TarotCreator()
        
        print(f"Regenerating {filename}...")
        print(f"Using prompt: {prompt}")
        
        # Create custom parameters
        params = {
            "width": 800,  # Slightly smaller than final size to allow for borders
            "height": 1350,  # Slightly smaller than final size to allow for borders
            "sampler_name": "DPM++ 2M Karras",
            "enable_hr": True,
            "hr_scale": 1.2,
            "hr_upscaler": "Latent",
            "hr_second_pass_steps": 15
        }
        
        success = generator.generate_image(prompt, filename, params=params)
        
        if success:
            print(f"Successfully regenerated {filename}")
            return True
        else:
            print(f"Failed to regenerate {filename}")
            return False
    except Exception as e:
        print(f"Error regenerating card: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Regenerate a specific tarot card")
    parser.add_argument("--file", type=str, required=True, help="Card filename to regenerate")
    
    args = parser.parse_args()
    
    print("Tarot Card Regenerator")
    print("=====================")
    
    success = regenerate_card(args.file)
    
    if success:
        print("\nCard regenerated successfully!")
    else:
        print("\nFailed to regenerate card.")
    
    return 0 if success else 1

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
