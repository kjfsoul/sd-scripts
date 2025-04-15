#!/usr/bin/env python3
"""
Advanced Tarot Card Generator - A comprehensive tool for creating tarot cards
with support for user-uploaded images, prompt analysis, and more.
"""

import os
import sys
import requests
import base64
import io
import json
import time
from PIL import Image
import argparse
from pathlib import Path

# Configuration
API_URL = "http://127.0.0.1:7860"
OUTPUT_DIR = "images/cards"
REFERENCE_DIR = "reference/images"
PROMPT_DIR = "reference/prompts"

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REFERENCE_DIR, exist_ok=True)
os.makedirs(PROMPT_DIR, exist_ok=True)

# Basic card definitions
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

def check_api():
    """Check if the Automatic1111 API is accessible"""
    print("Checking API connection...")
    try:
        response = requests.get(f"{API_URL}/sdapi/v1/sd-models", timeout=5)
        if response.status_code == 200:
            print("✓ Automatic1111 API is running and accessible!")
            return True
        else:
            print(f"✗ API responded with status code {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Could not connect to API: {e}")
        print("\nPlease make sure Automatic1111 is running with the API enabled.")
        return False

def check_xformers():
    """Check if xformers is available in the API"""
    print("Checking for xformers support...")
    try:
        response = requests.get(f"{API_URL}/sdapi/v1/options", timeout=5)
        if response.status_code == 200:
            options = response.json()
            if "xformers" in str(options).lower():
                print("✓ xformers appears to be supported!")
                return True
            else:
                print("✗ xformers does not appear to be enabled.")
                print("For better performance, consider adding --xformers to your COMMANDLINE_ARGS.")
                return False
        else:
            print(f"✗ Could not check for xformers. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error checking for xformers: {e}")
        return False

def generate_image(prompt, filename, params=None, no_borders=True):
    """Generate an image using the Automatic1111 API and save it"""
    if params is None:
        params = {}

    # Default settings with standard size for virtual tarot cards (2.75 x 4.75 inches at 300 DPI)
    # Using composition guidance to ensure room for borders and prevent cut-offs
    payload = {
        "prompt": f"{prompt}, centered composition, complete scene, full body shot, nothing cropped out, with margin space around edges, highly detailed",
        "negative_prompt": "deformed, ugly, disfigured, low quality, blurry, border, frame, text, watermark, signature, cut off, cropped, edge of frame, margin too small, bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, missing limbs, floating limbs, disconnected limbs, malformed hands, long neck, mutated, mutation, poorly drawn face, poorly drawn hands, distorted, amateur, out of frame, bad proportions, gross proportions, cloned face, weird colors, bad shadows, grainy, jpeg artifacts, duplicate, error, duplicate artifacts, airbrushed, cartoon, 3d render",
        "steps": 30,
        "cfg_scale": 7.5,  # Slightly higher for better prompt adherence
        "width": 800,  # Slightly smaller than final size to allow for borders
        "height": 1350,  # Slightly smaller than final size to allow for borders
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 1,
        "restore_faces": True,
        "tiling": False,
        "enable_hr": True,  # Enable high-res fix for better details
        "hr_scale": 1.2,  # Scale up to final size
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": 15
    }

    # If no_borders is True, add specific negative prompts to avoid borders
    if no_borders:
        payload["negative_prompt"] += ", border, frame, framing, framed, text, watermark, signature, margins"

    # Update with custom params
    payload.update(params)

    try:
        print(f"Generating image for: {filename}")
        print(f"Using prompt: {prompt}")

        # Send request to API
        print("Sending request to API...")
        response = requests.post(url=f"{API_URL}/sdapi/v1/txt2img", json=payload, timeout=120)

        # Check for errors
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text[:500]}...")
            return False

        # Parse response
        print("Processing response...")
        r = response.json()

        # Decode and save the image
        for img_data in r['images']:
            try:
                image = Image.open(io.BytesIO(base64.b64decode(img_data.split(",", 1)[0])))
                image_path = os.path.join(OUTPUT_DIR, filename)
                image.save(image_path)
                print(f"Image saved to {image_path}")
            except Exception as e:
                print(f"Error saving image: {e}")
                return False

        return True
    except Exception as e:
        print(f"Error generating image: {e}")
        return False

def analyze_image(image_path, max_retries=3, timeout=180):
    """Analyze an image using the Automatic1111 API to generate a prompt"""
    print(f"Analyzing image: {image_path}")

    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return None

    # Try to resize the image if it's too large (to reduce memory usage)
    try:
        img = Image.open(image_path)
        img_size = os.path.getsize(image_path) / (1024 * 1024)  # Size in MB

        # If image is larger than 4MB, resize it to reduce memory usage
        if img_size > 4:
            print(f"Image is large ({img_size:.1f}MB), resizing for analysis...")
            max_size = (1024, 1024)  # Max dimensions
            img.thumbnail(max_size, Image.LANCZOS)

            # Save to a temporary file
            temp_path = os.path.join(os.path.dirname(image_path), f"temp_{os.path.basename(image_path)}")
            img.save(temp_path)
            image_path = temp_path
            print(f"Resized image saved to {temp_path}")
    except Exception as e:
        print(f"Warning: Could not process image size: {e}")

    # Retry loop
    for attempt in range(max_retries):
        try:
            # Read the image file
            with open(image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')

            # Prepare the payload
            payload = {
                "image": f"data:image/png;base64,{img_data}",
                "model": "clip"
            }

            # Send request to API with increased timeout
            print(f"Sending image analysis request (attempt {attempt+1}/{max_retries})...")
            response = requests.post(url=f"{API_URL}/sdapi/v1/interrogate", json=payload, timeout=timeout)

            # Check for errors
            if response.status_code != 200:
                print(f"Error: API returned status code {response.status_code}")
                print(f"Response: {response.text[:500]}...")
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)  # Exponential backoff
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                return None

            # Parse response
            result = response.json()
            if "caption" in result:
                print(f"Analysis result: {result['caption']}")

                # Clean up temporary file if it was created
                if image_path.startswith(os.path.join(os.path.dirname(image_path), "temp_")):
                    try:
                        os.remove(image_path)
                        print("Temporary file removed.")
                    except:
                        pass

                return result['caption']
            else:
                print("Error: No caption found in the response")
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                return None

        except requests.exceptions.Timeout:
            print(f"Error: Request timed out after {timeout} seconds")
            if attempt < max_retries - 1:
                wait_time = 10 * (attempt + 1)  # Longer wait for timeouts
                print(f"Retrying with longer timeout in {wait_time} seconds...")
                time.sleep(wait_time)
                timeout += 60  # Increase timeout for next attempt
                continue
            return None

        except requests.exceptions.ConnectionError as e:
            print(f"Error: Connection error: {e}")
            if attempt < max_retries - 1:
                wait_time = 10 * (attempt + 1)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            return None

        except Exception as e:
            print(f"Error analyzing image: {e}")
            if attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            return None

    return None  # If all retries failed

def scan_reference_images(batch_size=5):
    """Scan all images in the reference directory and generate prompts"""
    print("\nScanning reference images...")

    # Get all image files in the reference directory
    image_files = []
    for ext in ['.png', '.jpg', '.jpeg', '.webp']:
        image_files.extend(list(Path(REFERENCE_DIR).glob(f"*{ext}")))

    if not image_files:
        print("No image files found in the reference directory.")
        return {}

    total_images = len(image_files)
    print(f"Found {total_images} image files.")

    # Ask if user wants to process all images or a subset
    if total_images > 10:
        print(f"\nYou have {total_images} images. Processing all of them might take a while.")
        process_all = input("Process all images? (Y/N, default: Y): ").strip().lower() != 'n'

        if not process_all:
            try:
                num_to_process = int(input(f"How many images to process (1-{total_images}): "))
                num_to_process = max(1, min(num_to_process, total_images))
                image_files = image_files[:num_to_process]
                print(f"Will process {len(image_files)} images.")
            except ValueError:
                print("Invalid input. Processing all images.")

    # Check if API is still accessible
    if not check_api():
        print("API not accessible. Cannot scan images.")
        return {}

    # Process images in batches to avoid overloading the API
    results = {}
    total_batches = (len(image_files) + batch_size - 1) // batch_size

    for batch_idx in range(total_batches):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, len(image_files))
        batch = image_files[start_idx:end_idx]

        print(f"\nProcessing batch {batch_idx + 1}/{total_batches} ({len(batch)} images)...")

        # Process each image in the batch
        for i, img_path in enumerate(batch):
            print(f"\nAnalyzing image {start_idx + i + 1}/{len(image_files)}: {img_path.name}...")

            # Check if a prompt already exists for this image
            existing_prompt_path = os.path.join(PROMPT_DIR, f"{img_path.stem}.txt")
            if os.path.exists(existing_prompt_path):
                print(f"Prompt already exists for {img_path.name}. Skipping analysis.")
                try:
                    with open(existing_prompt_path, 'r') as f:
                        prompt = f.read().strip()
                    results[img_path.name] = prompt
                    print(f"Loaded existing prompt: {prompt[:100]}..." if len(prompt) > 100 else f"Loaded existing prompt: {prompt}")
                    continue
                except Exception as e:
                    print(f"Error reading existing prompt: {e}. Will analyze image.")

            # Analyze the image
            prompt = analyze_image(str(img_path))
            if prompt:
                results[img_path.name] = prompt

                # Save the prompt to a file
                prompt_path = os.path.join(PROMPT_DIR, f"{img_path.stem}.txt")
                with open(prompt_path, 'w') as f:
                    f.write(prompt)
                print(f"Saved prompt to {prompt_path}")
            else:
                print(f"Failed to analyze {img_path.name}. Skipping.")

            # Wait a bit between requests to avoid overloading the API
            if i < len(batch) - 1 or batch_idx < total_batches - 1:
                wait_time = 2
                print(f"Waiting {wait_time} seconds before next image...")
                time.sleep(wait_time)

        # If there are more batches, check API again and wait between batches
        if batch_idx < total_batches - 1:
            print("\nChecking API before processing next batch...")
            if not check_api():
                print("API not accessible. Stopping scan.")
                break

            wait_time = 5
            print(f"Waiting {wait_time} seconds before next batch...")
            time.sleep(wait_time)

    # Summary
    print(f"\nAnalysis complete. Successfully analyzed {len(results)}/{len(image_files)} images.")
    return results

def load_existing_prompts():
    """Load existing prompts from the prompts directory"""
    print("\nLoading existing prompts...")

    prompts = {}
    prompt_files = list(Path(PROMPT_DIR).glob("*.txt"))

    if not prompt_files:
        print("No prompt files found.")
        return prompts

    print(f"Found {len(prompt_files)} prompt files.")

    for p_file in prompt_files:
        try:
            with open(p_file, 'r') as f:
                content = f.read().strip()
                prompts[p_file.stem] = content
                print(f"Loaded prompt for {p_file.stem}")
        except Exception as e:
            print(f"Error loading prompt from {p_file}: {e}")

    return prompts

def save_prompt(name, prompt):
    """Save a prompt to a file"""
    prompt_path = os.path.join(PROMPT_DIR, f"{name}.txt")
    with open(prompt_path, 'w') as f:
        f.write(prompt)
    print(f"Saved prompt to {prompt_path}")

def generate_cards_from_style(style, cards=None, variations=2, custom_descriptions=None):
    """Generate tarot cards based on a specified style"""
    if cards is None:
        cards = MAJOR_ARCANA[:3]  # Default to first 3 cards

    if custom_descriptions is None:
        custom_descriptions = {}

    print(f"\nGenerating {len(cards)} cards with {variations} variations each...")
    print(f"Style: {style}")

    for card in cards:
        card_name = card["name"]
        card_numeral = card["numeral"]

        print(f"\nGenerating {card_name} ({card_numeral})...")

        # Get custom description if available
        description = custom_descriptions.get(card_name, "")

        # Generate variations
        for v in range(1, variations + 1):
            # Create the prompt
            if description:
                prompt = f"{card_name} tarot card, {style}, {description}"
            else:
                prompt = f"{card_name} tarot card, {style}"

            # Add variation indicator for prompts after the first
            if v > 1:
                prompt += f", variation {v}"

            # Generate the image
            filename = f"{card_name.lower().replace(' ', '')}_v{v}.png"

            # Set parameters for standard virtual tarot card size
            params = {
                "width": 900,  # 2.75 inches at 300 DPI
                "height": 1500,  # 4.75 inches at 300 DPI
                "sampler_name": "DPM++ 2M Karras"
            }

            success = generate_image(prompt, filename, params, no_borders=True)

            if not success:
                print(f"Failed to generate {card_name} variation {v}. Skipping.")
                continue

            # Save the prompt
            save_prompt(f"{card_name.lower().replace(' ', '')}_v{v}", prompt)

            # Wait a bit between requests to avoid overloading the API
            if v < variations or card != cards[-1]:
                print("Waiting before next generation...")
                time.sleep(2)

    print("\nDone generating cards!")
    print(f"Check the {OUTPUT_DIR} directory for the generated images.")

def load_deck_style():
    """Load the deck style from the deck_style.txt file if it exists"""
    style_file = "deck_style.txt"
    if os.path.exists(style_file):
        try:
            with open(style_file, 'r') as f:
                content = f.read()
                # Extract the suggested style prompt (last line of the file)
                lines = content.strip().split('\n')
                for line in reversed(lines):
                    if line and not line.startswith('#') and not line.startswith('-'):
                        return line.strip()
        except Exception as e:
            print(f"Error loading deck style: {e}")
    return None

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Advanced Tarot Card Generator")
    parser.add_argument("--scan", action="store_true", help="Scan reference images and generate prompts")
    parser.add_argument("--generate", action="store_true", help="Generate tarot cards")
    parser.add_argument("--analyze-style", action="store_true", help="Analyze prompts to suggest a deck style")
    parser.add_argument("--style", type=str, help="Style to use for generation")
    parser.add_argument("--variations", type=int, default=2, help="Number of variations per card")
    parser.add_argument("--cards", type=int, default=3, help="Number of cards to generate")
    parser.add_argument("--start", type=int, default=0, help="Starting index for cards")

    args = parser.parse_args()

    print("Advanced Tarot Card Generator")
    print("============================")

    if not check_api():
        print("API not accessible. Exiting.")
        return 1

    # Check for xformers support
    check_xformers()

    # If no arguments provided, run in interactive mode
    if len(sys.argv) == 1:
        print("\nWelcome to the Advanced Tarot Card Generator!")
        print("\nWhat would you like to do?")
        print("1. Scan reference images and generate prompts")
        print("2. Generate tarot cards")
        print("3. Analyze prompts to suggest a deck style")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            args.scan = True
        elif choice == "2":
            args.generate = True
        elif choice == "3":
            args.analyze_style = True
        else:
            print("Exiting.")
            return 0

    # Scan reference images if requested
    if args.scan:
        print("\n=== Scanning Reference Images ===")
        print(f"Looking for images in: {REFERENCE_DIR}")
        print("This will analyze your reference images and generate prompts based on their content.")
        print("You can use these prompts as a starting point for your tarot card generation.")

        input("\nPress Enter to continue or Ctrl+C to cancel...")

        results = scan_reference_images()

        if results:
            print(f"\nSuccessfully analyzed {len(results)} images.")
            print(f"Prompts have been saved to the {PROMPT_DIR} directory.")
        else:
            print("\nNo images were successfully analyzed.")
            print(f"Make sure you have placed reference images in the {REFERENCE_DIR} directory.")

    # Analyze prompts to suggest a deck style if requested
    if args.analyze_style:
        print("\n=== Analyzing Prompts for Deck Style ===")
        print("This will analyze your prompt files to suggest a cohesive style for your entire deck.")

        # Check if prompt directory exists and has files
        prompt_files = list(Path(PROMPT_DIR).glob("*.txt"))
        if not prompt_files:
            print(f"No prompt files found in {PROMPT_DIR} directory.")
            print("Please run the image scanner first to generate prompts.")
            return 1

        print(f"Found {len(prompt_files)} prompt files to analyze.")
        print("Running analysis...")

        # Run the analyzer script
        try:
            # Import the analyzer module
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            import analyze_deck_style

            # Run the analysis
            analyze_deck_style.main()
            print("\nAnalysis complete! Check deck_style.txt for the results.")
        except Exception as e:
            print(f"Error running style analysis: {e}")
            print("Please run analyze_deck_style.bat separately.")

    # Generate tarot cards if requested
    if args.generate:
        print("\n=== Generating Tarot Cards ===")

        # Load existing prompts
        existing_prompts = load_existing_prompts()

        # Check for deck style file
        deck_style = load_deck_style()

        # Get style
        style = args.style
        if not style:
            if deck_style:
                print(f"\nFound suggested deck style from analysis:")
                print(f"{deck_style}")
                use_suggested = input("Use this suggested style? (Y/N, default: Y): ").strip().lower() != 'n'

                if use_suggested:
                    style = deck_style
                    print("Using suggested deck style.")
                else:
                    print("\nLet's define a custom style for your tarot deck:")
                    style = input("Describe the artistic style you want: ")
            else:
                print("\nLet's define the style for your tarot deck:")
                print("(Tip: Run 'Analyze prompts' first to get a suggested style based on your reference images)")
                style = input("Describe the artistic style you want: ")

            if not style:
                style = "digital art, fantasy style"
                print(f"Using default style: {style}")

        # Get number of variations
        variations = args.variations
        if variations < 1 or variations > 5:
            print("\nInvalid number of variations. Using default of 2.")
            variations = 2

        # Get cards to generate
        num_cards = args.cards
        start_idx = args.start

        if start_idx < 0 or start_idx >= len(MAJOR_ARCANA):
            start_idx = 0

        end_idx = min(start_idx + num_cards, len(MAJOR_ARCANA))
        cards_to_generate = MAJOR_ARCANA[start_idx:end_idx]

        print(f"\nGenerating {len(cards_to_generate)} cards starting with {cards_to_generate[0]['name']}")
        print(f"Creating {variations} variations for each card")

        # Ask for custom descriptions
        custom_descriptions = {}
        print("\nWould you like to provide custom descriptions for each card?")
        use_custom = input("Enter Y for custom descriptions or N to skip: ").strip().lower() == 'y'

        if use_custom:
            for card in cards_to_generate:
                card_name = card["name"]
                print(f"\nEnter a description for {card_name} (or press Enter to skip):")
                description = input("> ")
                if description:
                    custom_descriptions[card_name] = description

        # Generate the cards
        generate_cards_from_style(style, cards_to_generate, variations, custom_descriptions)

    print("\nThank you for using the Advanced Tarot Card Generator!")
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
