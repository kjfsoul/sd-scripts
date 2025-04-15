#!/usr/bin/env python3
"""
Scan Reference Images - Analyzes reference images and generates text prompts
"""

import os
import sys
import json
import argparse
from pathlib import Path
import requests
import base64
import time

# Configuration
REFERENCE_DIR = "reference"
IMAGES_DIR = os.path.join(REFERENCE_DIR, "images")
PROMPTS_DIR = os.path.join(REFERENCE_DIR, "prompts")
API_URL = "http://127.0.0.1:7860/sdapi/v1/interrogate"

def ensure_directories():
    """Ensure all required directories exist"""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(PROMPTS_DIR, exist_ok=True)

def get_image_files():
    """Get all image files in the reference directory"""
    image_files = []
    for ext in ['.png', '.jpg', '.jpeg', '.webp']:
        image_files.extend(list(Path(IMAGES_DIR).glob(f"*{ext}")))
    return sorted(image_files)

def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def interrogate_image(image_path):
    """Interrogate image using CLIP interrogator"""
    try:
        print(f"Analyzing {os.path.basename(image_path)}...")
        
        # Encode image
        encoded_image = encode_image(image_path)
        
        # Prepare payload
        payload = {
            "image": f"data:image/png;base64,{encoded_image}",
            "model": "clip"
        }
        
        # Send request
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("caption", "")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return ""
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return ""

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Scan reference images and generate prompts")
    
    args = parser.parse_args()
    
    print("Reference Image Scanner")
    print("======================")
    print()
    
    # Ensure directories exist
    ensure_directories()
    
    # Get image files
    image_files = get_image_files()
    
    if not image_files:
        print("No image files found in the reference directory.")
        return 1
    
    print(f"Found {len(image_files)} image files.")
    print()
    
    # Check if API is available
    try:
        response = requests.get("http://127.0.0.1:7860/sdapi/v1/sd-models")
        if response.status_code != 200:
            print("Error: Automatic1111 API is not available.")
            print("Please make sure Automatic1111 is running with the API enabled.")
            return 1
    except Exception:
        print("Error: Could not connect to Automatic1111 API.")
        print("Please make sure Automatic1111 is running with the API enabled.")
        return 1
    
    # Process each image
    for i, image_path in enumerate(image_files):
        print(f"Processing image {i+1} of {len(image_files)}: {image_path.name}")
        
        # Generate prompt
        prompt = interrogate_image(image_path)
        
        if prompt:
            # Save prompt to file
            prompt_file = os.path.join(PROMPTS_DIR, f"{image_path.stem}.txt")
            with open(prompt_file, 'w') as f:
                f.write(prompt)
            
            print(f"Saved prompt to {prompt_file}")
            print(f"Prompt: {prompt}")
        else:
            print(f"Failed to generate prompt for {image_path.name}")
        
        print()
        
        # Wait a bit between requests to avoid overloading the API
        if i < len(image_files) - 1:
            time.sleep(1)
    
    print("All images processed successfully!")
    
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
