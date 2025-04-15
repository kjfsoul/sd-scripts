import os
import json
import requests
import io
import base64
import time
import sys
from PIL import Image

# Configuration
OUTPUT_DIR = "tarot_output"
CARDS_JSON = "tarot_cards.json"
API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"  # Default URL for Automatic1111 API
API_BASE = "http://127.0.0.1:7860"  # Base URL for API checks

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def check_api(base_url=API_BASE, max_retries=3, retry_delay=2):
    """Check if the Automatic1111 API is accessible"""
    print(f"Checking if Automatic1111 API is running at {base_url}...")
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{base_url}/sdapi/v1/sd-models", timeout=5)
            if response.status_code == 200:
                print("✓ Automatic1111 API is running and accessible!")
                return True
            else:
                print(f"✗ API responded with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Attempt {i+1}/{max_retries}: Could not connect to API: {e}")
        
        if i < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    print("\nThe Automatic1111 API is not accessible. Please make sure:")
    print("1. Automatic1111 is running")
    print("2. It was started with the --api flag")
    print("3. It's running on the default port (7860)")
    print("\nTo start Automatic1111 with the API enabled, run:")
    print("python webui.py --api")
    
    return False

def load_tarot_cards():
    """Load tarot card definitions from JSON file"""
    with open(CARDS_JSON, 'r') as f:
        data = json.load(f)
    return data['cards']

def generate_image(prompt, filename, settings=None):
    """Generate an image using the Automatic1111 API and save it"""
    if settings is None:
        settings = {}
    
    # Default settings
    payload = {
        "prompt": prompt,
        "negative_prompt": "deformed, ugly, disfigured, low quality, blurry, nsfw",
        "steps": 40,
        "cfg_scale": 7.5,
        "width": 512,
        "height": 768,
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 1,
        "n_iter": 1,
        "seed": -1,  # Random seed
    }
    
    # Update with custom settings
    payload.update(settings)
    
    try:
        print(f"Generating image for: {filename}")
        print(f"Using prompt: {prompt[:100]}...")
        
        response = requests.post(url=API_URL, json=payload)
        response.raise_for_status()
        
        r = response.json()
        
        # Decode and save the image
        for img_data in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(img_data.split(",", 1)[0])))
            image_path = os.path.join(OUTPUT_DIR, filename)
            image.save(image_path)
            print(f"Image saved to {image_path}")
        
        return True
    except Exception as e:
        print(f"Error generating image: {e}")
        return False

def generate_all_cards(cards=None):
    """Generate images for all cards"""
    if cards is None:
        cards = load_tarot_cards()
    
    for card in cards:
        card_name = card['name'].lower().replace(' ', '')
        for i, prompt in enumerate(card['variations'], 1):
            filename = f"{card_name}_v{i}.png"
            generate_image(prompt, filename)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate tarot card images using Automatic1111 API')
    parser.add_argument('--api-url', type=str, default="http://127.0.0.1:7860/sdapi/v1/txt2img",
                        help='URL for the Automatic1111 API')
    parser.add_argument('--api-base', type=str, default="http://127.0.0.1:7860",
                        help='Base URL for the Automatic1111 API')
    parser.add_argument('--cards', type=str, nargs='+', default=None,
                        help='Specific cards to generate (by name)')
    parser.add_argument('--skip-check', action='store_true',
                        help='Skip API availability check')
    
    args = parser.parse_args()
    
    global API_URL, API_BASE
    API_URL = args.api_url
    API_BASE = args.api_base
    
    # Check if the API is accessible
    if not args.skip_check:
        if not check_api(API_BASE):
            print("\nAPI is not accessible. Please start Automatic1111 with the API enabled.")
            print("You can run start_a1111_api.bat to do this.")
            return
    
    # Load all cards
    all_cards = load_tarot_cards()
    
    # Filter cards if specified
    if args.cards:
        filtered_cards = []
        for name in args.cards:
            for card in all_cards:
                if name.lower() in card['name'].lower():
                    filtered_cards.append(card)
        cards_to_generate = filtered_cards
    else:
        cards_to_generate = all_cards
    
    if not cards_to_generate:
        print("No cards found to generate!")
        return
    
    print(f"Generating {len(cards_to_generate)} cards with {sum(len(card['variations']) for card in cards_to_generate)} variations...")
    generate_all_cards(cards_to_generate)
    print("Done!")

if __name__ == "__main__":
    main()
