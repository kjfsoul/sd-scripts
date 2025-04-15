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
API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"  # Default URL for Automatic1111 API

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

def main():
    # Simple test prompt
    prompt = "fooldeck style, The Fool tarot card, pastel art nouveau, ethereal, fantasy soft lighting, a youthful figure in flowing garments standing at the edge of a cliff, white dog companion, dreamy landscape, decorative border, \"0\" at top, \"THE FOOL\" at bottom, elegant sans serif font"
    filename = "test_fool.png"
    
    # Try to generate the image
    success = generate_image(prompt, filename)
    
    if success:
        print("\nSuccessfully generated test image!")
        print(f"Check {os.path.join(OUTPUT_DIR, filename)} to see the result.")
    else:
        print("\nFailed to generate test image.")
        print("Please make sure Automatic1111 is running with the API enabled.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
