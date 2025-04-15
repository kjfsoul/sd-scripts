#!/usr/bin/env python3
"""
Basic Tarot Card Generator - A simplified version with minimal dependencies
"""

import os
import requests
import base64
import io
from PIL import Image
import time

# Configuration
API_URL = "http://127.0.0.1:7860"
OUTPUT_DIR = "images/cards"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Basic card definitions
INITIAL_CARDS = [
    {"name": "The Fool", "numeral": "0"},
    {"name": "The Magician", "numeral": "I"},
    {"name": "The High Priestess", "numeral": "II"}
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

def generate_image(prompt, filename):
    """Generate an image using the Automatic1111 API and save it"""
    # Default settings - minimal for testing
    payload = {
        "prompt": prompt,
        "negative_prompt": "deformed, ugly, disfigured, low quality, blurry",
        "steps": 20,
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "sampler_name": "Euler a",
        "batch_size": 1
    }
    
    try:
        print(f"Generating image for: {filename}")
        print(f"Using prompt: {prompt}")
        
        # Send request to API
        print("Sending request to API...")
        response = requests.post(url=f"{API_URL}/sdapi/v1/txt2img", json=payload, timeout=60)
        
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

def main():
    """Main function"""
    print("Basic Tarot Card Generator")
    print("=========================")
    
    if not check_api():
        print("API not accessible. Exiting.")
        return 1
    
    # Get style information
    print("\nLet's define the style for your tarot deck:")
    style = input("Describe the artistic style you want: ")
    
    if not style:
        style = "digital art, fantasy style"
        print(f"Using default style: {style}")
    
    # Get number of variations
    print("\nHow many variations would you like for each card? (1-3)")
    try:
        num_variations = int(input("Enter number: "))
        num_variations = max(1, min(3, num_variations))
    except ValueError:
        print("Invalid input. Using default of 2 variations.")
        num_variations = 2
    
    # Process each card
    for card in INITIAL_CARDS:
        card_name = card["name"]
        
        print(f"\nGenerating {card_name}...")
        
        # Generate variations
        for v in range(1, num_variations + 1):
            # Create the prompt
            prompt = f"{card_name} tarot card, {style}"
            
            # Add variation indicator for prompts after the first
            if v > 1:
                prompt += f", variation {v}"
            
            # Generate the image
            filename = f"{card_name.lower().replace(' ', '')}_v{v}.png"
            success = generate_image(prompt, filename)
            
            if not success:
                print(f"Failed to generate {card_name} variation {v}. Skipping.")
                continue
            
            # Wait a bit between requests to avoid overloading the API
            if v < num_variations or card != INITIAL_CARDS[-1]:
                print("Waiting before next generation...")
                time.sleep(2)
    
    print("\nDone generating initial cards!")
    print(f"Check the {OUTPUT_DIR} directory for the generated images.")
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
