#!/usr/bin/env python3
"""
Simplified Tarot Card Generator
"""

import os
import json
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

# Simplified card definitions
INITIAL_CARDS = [
    {"name": "The Fool", "numeral": "0", "description": "youthful figure with dog at cliff edge"},
    {"name": "The Magician", "numeral": "I", "description": "figure with one hand raised, ritual objects on table"},
    {"name": "The High Priestess", "numeral": "II", "description": "seated woman between pillars with scroll"}
]

def check_api():
    """Check if the Automatic1111 API is accessible"""
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

def generate_image(prompt, filename, params=None):
    """Generate an image using the Automatic1111 API and save it"""
    if params is None:
        params = {}
    
    # Default settings - minimal for testing
    payload = {
        "prompt": prompt,
        "negative_prompt": "deformed, ugly, disfigured, low quality, blurry",
        "steps": 20,  # Reduced steps
        "cfg_scale": 7,
        "width": 512,
        "height": 512,  # Square format for testing
        "sampler_name": "Euler a",  # Fast sampler
        "batch_size": 1
    }
    
    # Update with custom params
    payload.update(params)
    
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
        for i, img_data in enumerate(r['images']):
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
    print("Simple Tarot Card Generator")
    print("=========================")
    
    if not check_api():
        print("API not accessible. Exiting.")
        return
    
    print("\nLet's define the style for your tarot deck:")
    style = input("Describe the artistic style you want (or press Enter for default): ")
    
    if not style:
        style = "digital art, fantasy style"
    
    # Save the style for future use
    os.makedirs("config", exist_ok=True)
    with open("config/style.txt", 'w') as f:
        f.write(style)
    
    print(f"\nUsing style: {style}")
    print("\nGenerating initial cards...")
    
    for card in INITIAL_CARDS:
        card_name = card["name"]
        card_description = card["description"]
        
        print(f"\nGenerating {card_name}...")
        
        # Create a simple prompt
        prompt = f"{card_name} tarot card, {style}, {card_description}"
        
        # Generate the image
        filename = f"{card_name.lower().replace(' ', '')}.png"
        success = generate_image(prompt, filename)
        
        if not success:
            print(f"Failed to generate {card_name}. Trying with simpler settings...")
            
            # Try with even simpler settings
            simpler_params = {
                "steps": 10,
                "width": 384,
                "height": 384,
                "sampler_name": "Euler"
            }
            
            simpler_prompt = f"{card_name}, {style}"
            success = generate_image(simpler_prompt, filename, simpler_params)
            
            if not success:
                print(f"Still failed to generate {card_name}. Skipping.")
        
        # Save the prompt
        os.makedirs("prompts/cards", exist_ok=True)
        with open(f"prompts/cards/{card_name.lower().replace(' ', '')}.txt", 'w') as f:
            f.write(prompt)
        
        # Wait a bit between requests to avoid overloading the API
        time.sleep(2)
    
    print("\nDone generating initial cards!")
    print(f"Check the {OUTPUT_DIR} directory for the generated images.")

if __name__ == "__main__":
    main()
