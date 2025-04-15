#!/usr/bin/env python3
"""
Tarot Creator 1111 - A tool for creating custom tarot card decks using Stable Diffusion Automatic1111
"""

import os
import json
import argparse
import requests
from pathlib import Path
import time
import base64
import io
from PIL import Image

# Configuration
CONFIG_FILE = Path("config/config.json")
DEFAULT_API_URL = "http://127.0.0.1:7860"
DEFAULT_OUTPUT_DIR = Path("images/cards")
DEFAULT_PROMPTS_DIR = Path("prompts/cards")

# Ensure directories exist
os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
os.makedirs(DEFAULT_PROMPTS_DIR, exist_ok=True)

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

class TarotCreator:
    """Main class for the Tarot Creator application"""
    
    def __init__(self, api_url=DEFAULT_API_URL):
        """Initialize the TarotCreator"""
        self.api_url = api_url
        self.txt2img_url = f"{api_url}/sdapi/v1/txt2img"
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file or create default"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            config = {
                "api_url": DEFAULT_API_URL,
                "default_params": {
                    "steps": 40,
                    "cfg_scale": 7.5,
                    "width": 512,
                    "height": 768,
                    "sampler_name": "DPM++ 2M Karras",
                    "batch_size": 1,
                    "n_iter": 1
                },
                "default_negative_prompt": "deformed, ugly, disfigured, low quality, blurry, nsfw"
            }
            
            # Save default config
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
                
            return config
    
    def check_api(self):
        """Check if the Automatic1111 API is accessible"""
        try:
            response = requests.get(f"{self.api_url}/sdapi/v1/sd-models", timeout=5)
            if response.status_code == 200:
                print("✓ Automatic1111 API is running and accessible!")
                return True
            else:
                print(f"✗ API responded with status code {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Could not connect to API: {e}")
            print("\nPlease make sure Automatic1111 is running with the API enabled.")
            print("You can enable the API by adding --api to the COMMANDLINE_ARGS in webui-user.bat")
            return False
    
    def generate_image(self, prompt, filename, output_dir=None, params=None):
        """Generate an image using the Automatic1111 API and save it"""
        if output_dir is None:
            output_dir = DEFAULT_OUTPUT_DIR
            
        if params is None:
            params = {}
        
        # Default settings from config
        payload = self.config["default_params"].copy()
        payload["prompt"] = prompt
        payload["negative_prompt"] = self.config["default_negative_prompt"]
        
        # Update with custom params
        payload.update(params)
        
        try:
            print(f"Generating image for: {filename}")
            print(f"Using prompt: {prompt[:100]}...")
            
            response = requests.post(url=self.txt2img_url, json=payload)
            response.raise_for_status()
            
            r = response.json()
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Decode and save the image
            for img_data in r['images']:
                image = Image.open(io.BytesIO(base64.b64decode(img_data.split(",", 1)[0])))
                image_path = os.path.join(output_dir, filename)
                image.save(image_path)
                print(f"Image saved to {image_path}")
            
            return True
        except Exception as e:
            print(f"Error generating image: {e}")
            return False
    
    def save_prompt(self, card_name, prompt, prompt_dir=None):
        """Save a prompt to a file"""
        if prompt_dir is None:
            prompt_dir = DEFAULT_PROMPTS_DIR
            
        os.makedirs(prompt_dir, exist_ok=True)
        filename = f"{card_name.lower().replace(' ', '_')}.txt"
        filepath = os.path.join(prompt_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(prompt)
        
        print(f"Prompt saved to {filepath}")
    
    def generate_initial_cards(self):
        """Generate the initial 3 major arcana cards for review"""
        if not self.check_api():
            return False
        
        # Select the first 3 cards
        initial_cards = MAJOR_ARCANA[:3]
        
        print(f"Generating initial {len(initial_cards)} cards for review...")
        
        # Get user input for style
        print("\nLet's define the style for your tarot deck:")
        style = input("Describe the artistic style you want for your deck: ")
        
        # Save the style for future use
        os.makedirs("config", exist_ok=True)
        with open("config/style.txt", 'w') as f:
            f.write(style)
        
        # Generate 2 variations for each card
        for card in initial_cards:
            card_name = card["name"]
            card_numeral = card["numeral"]
            
            print(f"\nGenerating {card_name} ({card_numeral})...")
            
            # Variation 1
            prompt1 = self.create_card_prompt(card_name, style)
            filename1 = f"{card_name.lower().replace(' ', '')}_v1.png"
            self.generate_image(prompt1, filename1)
            self.save_prompt(f"{card_name}_v1", prompt1)
            
            # Variation 2
            prompt2 = self.create_card_prompt(card_name, style, variation=2)
            filename2 = f"{card_name.lower().replace(' ', '')}_v2.png"
            self.generate_image(prompt2, filename2)
            self.save_prompt(f"{card_name}_v2", prompt2)
        
        return True
    
    def create_card_prompt(self, card_name, style, variation=1):
        """Create a prompt for a card based on its name and the desired style"""
        # Base descriptions for major arcana cards
        card_descriptions = {
            "The Fool": [
                "a youthful figure in flowing garments standing at the edge of a cliff, white dog companion, dreamy landscape",
                "androgynous figure with flower crown carrying a white rose and knapsack, playful white dog, mountain background"
            ],
            "The Magician": [
                "figure with one hand raised to the sky and one pointing to the ground, table with ritual objects, lemniscate symbol above head",
                "mystical figure performing magic, surrounded by the four elements, infinity symbol, garden setting"
            ],
            "The High Priestess": [
                "serene woman seated between two pillars, crescent moon at her feet, veil behind her, scroll in hand",
                "mysterious feminine figure with lunar crown, blue robes, pomegranates and dates, cosmic background"
            ],
            "The Empress": [
                "regal woman on throne in lush garden, pregnant or maternal figure, venus symbol, flowing robes",
                "abundant feminine figure surrounded by nature, wheat crown, heart symbol, flowing water"
            ],
            "The Emperor": [
                "stern ruler on stone throne, holding ankh and orb, ram decorations, mountains in background",
                "powerful masculine figure with crown and scepter, red robes, eagle symbol, stone architecture"
            ],
            "The Hierophant": [
                "religious figure with triple crown, hand raised in blessing, two acolytes, crossed keys",
                "spiritual teacher between two pillars, religious symbols, followers kneeling, ancient wisdom"
            ],
            "The Lovers": [
                "naked man and woman under angel's blessing, tree of knowledge, tree of life, serpent",
                "two figures joining hands under divine light, garden setting, choice between paths, heart symbolism"
            ],
            "The Chariot": [
                "armored figure in chariot drawn by sphinxes or horses, crown of stars, walled city",
                "triumphant warrior controlling opposing forces, moving forward, celestial symbols, victory"
            ],
            "Strength": [
                "woman gently closing lion's mouth, flower garland, lemniscate symbol, serene expression",
                "feminine figure taming wild beast with gentle touch, inner power, courage symbol, natural setting"
            ],
            "The Hermit": [
                "robed elder holding lantern on snowy peak, staff, star light, solitary journey",
                "wise figure with light of wisdom, seeking truth alone, mountain path, inner guidance"
            ],
            "Wheel of Fortune": [
                "great wheel with mystical creatures at corners, sphinx on top, serpent and anubis, celestial symbols",
                "cosmic wheel of fate with zodiac symbols, four elements, divine hand turning wheel, cyclical nature"
            ],
            "Justice": [
                "figure with scales and sword, balanced throne, pillars, crown or halo",
                "blindfolded figure weighing actions, perfect balance, sword of truth, mathematical precision"
            ],
            "The Hanged Man": [
                "man suspended upside-down from tree or tau cross, peaceful expression, halo, crossed leg",
                "figure in suspended animation, new perspective, sacrifice, mystical illumination, tree of life"
            ],
            "Death": [
                "skeleton with scythe, sunset, dying king, rising sun, transformation symbol",
                "dark rider on white horse, fallen figures, phoenix rising, river of rebirth, transformation"
            ],
            "Temperance": [
                "angel with one foot in water, pouring liquid between cups, path to mountains, flowing robes",
                "divine figure blending elements, healing energy, balance of opposites, alchemical transformation"
            ],
            "The Devil": [
                "horned figure on pedestal, chained nude figures below, inverted pentagram, bat wings",
                "imposing satyr with chains, enslaved figures, material temptation, dark cave setting"
            ],
            "The Tower": [
                "lightning-struck tower, people falling, crown tumbling, flames, rocky foundation",
                "crumbling structure in storm, divine fire, sudden revelation, chaos and liberation"
            ],
            "The Star": [
                "nude figure kneeling by water pouring from two vessels, one foot on land, one in water, seven stars above",
                "graceful figure under starry night sky, pouring water onto earth and into pond, celestial glow, hope"
            ],
            "The Moon": [
                "full moon with face, howling wolf and dog, crayfish emerging from pool, twin towers, path",
                "mysterious night scene, lunar reflection in water, creatures of instinct, hidden path, psychic vision"
            ],
            "The Sun": [
                "child on white horse under radiant sun, sunflowers, red banner, garden wall",
                "joyful youth in sunlit garden, solar radiance, achievement, vitality, golden light"
            ],
            "Judgement": [
                "angel blowing trumpet, people rising from graves, mountains, divine light",
                "cosmic awakening, figures answering divine call, resurrection, final reckoning, transformation"
            ],
            "The World": [
                "dancing figure in wreath, four living creatures at corners, wands or sashes",
                "accomplished figure at center of universe, cosmic completion, four elements, divine harmony"
            ]
        }
        
        # Get description for this card and variation
        description = ""
        if card_name in card_descriptions:
            var_idx = (variation - 1) % len(card_descriptions[card_name])
            description = card_descriptions[card_name][var_idx]
        
        # Create the prompt - remove border references
        prompt = f"{card_name} tarot card, {style}, {description}"
        
        return prompt
    
    def get_feedback(self):
        """Get user feedback on generated images"""
        print("\nPlease review the generated images and provide feedback.")
        print("What aspects do you like? What would you like to change?")
        feedback = input("Your feedback: ")
        return feedback
    
    def refine_style(self, feedback):
        """Refine the style based on user feedback"""
        print("\nBased on your feedback, let's refine the style.")
        print("Current feedback:", feedback)
        
        # Ask for specific refinements
        refinements = input("What specific changes would you like to make to the style? ")
        
        return refinements
    
    def generate_batch(self, start_idx, batch_size):
        """Generate a batch of cards"""
        if not self.check_api():
            return False
        
        end_idx = min(start_idx + batch_size, len(MAJOR_ARCANA))
        batch_cards = MAJOR_ARCANA[start_idx:end_idx]
        
        print(f"\nGenerating batch of {len(batch_cards)} cards...")
        
        # Get current style
        if os.path.exists("config/style.txt"):
            with open("config/style.txt", 'r') as f:
                style = f.read().strip()
        else:
            print("\nNo style defined. Let's define one now:")
            style = input("Describe the artistic style you want for your deck: ")
            with open("config/style.txt", 'w') as f:
                f.write(style)
        
        # Generate each card
        for card in batch_cards:
            card_name = card["name"]
            card_numeral = card["numeral"]
            
            print(f"\nGenerating {card_name} ({card_numeral})...")
            
            # Create prompt for this card
            prompt = self.create_card_prompt(card_name, style)
            filename = f"{card_name.lower().replace(' ', '')}.png"
            self.generate_image(prompt, filename)
            self.save_prompt(card_name, prompt)
        
        return True
    
    def generate_borders(self, num_variations=5):
        """Generate border variations"""
        if not self.check_api():
            return False
        
        print(f"\nGenerating {num_variations} border variations...")
        
        # Get user input for border style
        print("\nLet's define the style for your card borders:")
        border_style = input("Describe the border style you want (e.g., ornate golden floral, minimalist geometric): ")
        
        # Generate variations
        for i in range(1, num_variations + 1):
            # Create prompt for this border
            prompt = f"tarot card border, {border_style}, decorative frame, isolated on transparent background, high detail"
            
            if i > 1:
                prompt += f", variation {i}"
                
            filename = f"border_v{i}.png"
            output_dir = "images/borders"
            self.generate_image(prompt, filename, output_dir)
            self.save_prompt(f"border_v{i}", prompt, "prompts/borders")
        
        return True
    
    def generate_nameplates(self, num_variations=5):
        """Generate nameplate variations"""
        if not self.check_api():
            return False
        
        print(f"\nGenerating {num_variations} nameplate variations...")
        
        # Get user input for nameplate style
        print("\nLet's define the style for your card nameplates:")
        nameplate_style = input("Describe the nameplate style you want (e.g., elegant serif, mystical runes): ")
        
        # Generate variations
        for i in range(1, num_variations + 1):
            # Create prompt for this nameplate
            prompt = f"tarot card nameplate, {nameplate_style}, text placeholder, isolated on transparent background"
            
            if i > 1:
                prompt += f", variation {i}"
                
            filename = f"nameplate_v{i}.png"
            output_dir = "images/nameplates"
            self.generate_image(prompt, filename, output_dir)
            self.save_prompt(f"nameplate_v{i}", prompt, "prompts/nameplates")
        
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Tarot Creator 1111")
    parser.add_argument("--api-url", type=str, default=DEFAULT_API_URL,
                        help="URL for the Automatic1111 API")
    parser.add_argument("--check-api", action="store_true",
                        help="Check if the API is accessible")
    parser.add_argument("--initial", action="store_true",
                        help="Generate initial 3 cards for review")
    parser.add_argument("--batch", type=int, nargs=2, metavar=("START", "SIZE"),
                        help="Generate a batch of cards starting at index START with size SIZE")
    parser.add_argument("--borders", type=int, nargs="?", const=5, metavar="NUM",
                        help="Generate NUM border variations (default: 5)")
    parser.add_argument("--nameplates", type=int, nargs="?", const=5, metavar="NUM",
                        help="Generate NUM nameplate variations (default: 5)")
    
    args = parser.parse_args()
    
    creator = TarotCreator(api_url=args.api_url)
    
    if args.check_api:
        creator.check_api()
    elif args.initial:
        creator.generate_initial_cards()
    elif args.batch:
        creator.generate_batch(args.batch[0], args.batch[1])
    elif args.borders:
        creator.generate_borders(args.borders)
    elif args.nameplates:
        creator.generate_nameplates(args.nameplates)
    else:
        # Interactive mode
        print("Welcome to Tarot Creator 1111!")
        print("This tool will help you create a custom tarot card deck.")
        
        if not creator.check_api():
            return
        
        print("\nWhat would you like to do?")
        print("1. Generate initial 3 cards for review")
        print("2. Generate a batch of cards")
        print("3. Generate border variations")
        print("4. Generate nameplate variations")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            creator.generate_initial_cards()
        elif choice == "2":
            start = int(input("Start index (0-21): "))
            size = int(input("Batch size: "))
            creator.generate_batch(start, size)
        elif choice == "3":
            num = int(input("Number of variations: "))
            creator.generate_borders(num)
        elif choice == "4":
            num = int(input("Number of variations: "))
            creator.generate_nameplates(num)
        elif choice == "5":
            print("Goodbye!")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
