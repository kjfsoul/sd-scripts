#!/usr/bin/env python3
"""
Install Recommended Plugins for Automatic1111 - Enhances functionality for tarot card generation
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Configuration
DEFAULT_SD_PATH = "C:/Users/kjfsw/sd-scripts"
EXTENSIONS_DIR = "extensions"

# List of recommended extensions with their GitHub URLs
RECOMMENDED_EXTENSIONS = [
    {
        "name": "Stable Diffusion WebUI Images Browser",
        "url": "https://github.com/AlUlkesh/stable-diffusion-webui-images-browser",
        "description": "Enhanced image browser with advanced tagging and organization features"
    },
    {
        "name": "Tag Complete",
        "url": "https://github.com/DominikDoom/a1111-sd-webui-tagcomplete",
        "description": "Provides autocompletion for tags and improves prompt engineering"
    },
    {
        "name": "ControlNet",
        "url": "https://github.com/Mikubill/sd-webui-controlnet",
        "description": "Adds ControlNet support for better control over image composition"
    },
    {
        "name": "Prompt Styles",
        "url": "https://github.com/Klace/stable-diffusion-webui-prompt-styles",
        "description": "Allows saving and reusing prompt styles for consistent tarot card aesthetics"
    },
    {
        "name": "Dynamic Prompts",
        "url": "https://github.com/adieyal/sd-dynamic-prompts",
        "description": "Create dynamic prompts with wildcards for tarot symbolism and themes"
    },
    {
        "name": "Dataset Tag Editor",
        "url": "https://github.com/toshiaki1729/stable-diffusion-webui-dataset-tag-editor",
        "description": "Edit tags for your dataset, useful for organizing tarot card collections"
    },
    {
        "name": "Booru Tag Autocomplete",
        "url": "https://github.com/DominikDoom/a1111-sd-webui-tagcomplete",
        "description": "Autocomplete for tags from various image booru sites"
    },
    {
        "name": "Civitai Helper",
        "url": "https://github.com/butaixianran/Stable-Diffusion-Webui-Civitai-Helper",
        "description": "Helps manage and use models, LoRAs, and embeddings from Civitai"
    },
    {
        "name": "LoRA Block Weight",
        "url": "https://github.com/hako-mikan/sd-webui-lora-block-weight",
        "description": "Adjust LoRA weights for different parts of the model, useful for fine-tuning tarot card styles"
    },
    {
        "name": "Image Browser",
        "url": "https://github.com/yfszzx/stable-diffusion-webui-images-browser",
        "description": "Enhanced image browser with filtering and organization features"
    },
    {
        "name": "Stable Diffusion WebUI Aesthetic Gradients",
        "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui-aesthetic-gradients",
        "description": "Create aesthetic gradients for more visually appealing tarot cards"
    },
    {
        "name": "Stable Diffusion WebUI Wildcards",
        "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui-wildcards",
        "description": "Use wildcards in your prompts for more variety in tarot card generation"
    },
    {
        "name": "Latent Couple",
        "url": "https://github.com/opparco/stable-diffusion-webui-two-shot",
        "description": "Generate pairs of related images, useful for creating matching tarot cards"
    },
    {
        "name": "Stable Diffusion WebUI Smart Process",
        "url": "https://github.com/d8ahazard/sd_smartprocess",
        "description": "Automate image processing workflows for tarot card production"
    },
    {
        "name": "Stable Diffusion WebUI Model Converter",
        "url": "https://github.com/Akegarasu/sd-webui-model-converter",
        "description": "Convert models between different formats for compatibility"
    }
]

def get_sd_path(provided_path=None):
    """Get the Stable Diffusion WebUI path"""
    if provided_path and os.path.exists(provided_path):
        return provided_path
    
    if os.path.exists(DEFAULT_SD_PATH):
        return DEFAULT_SD_PATH
    
    # Ask user for path
    print("Stable Diffusion WebUI path not found.")
    user_path = input("Please enter the path to your Stable Diffusion WebUI installation: ")
    
    if os.path.exists(user_path):
        return user_path
    else:
        print(f"Error: Path {user_path} does not exist.")
        sys.exit(1)

def install_extension(sd_path, extension_url, extension_name):
    """Install an extension from GitHub"""
    extensions_path = os.path.join(sd_path, EXTENSIONS_DIR)
    
    # Create extensions directory if it doesn't exist
    os.makedirs(extensions_path, exist_ok=True)
    
    # Extract repository name from URL
    repo_name = extension_url.split('/')[-1]
    
    # Check if extension is already installed
    if os.path.exists(os.path.join(extensions_path, repo_name)):
        print(f"Extension {extension_name} is already installed.")
        return True
    
    # Clone the repository
    try:
        print(f"Installing {extension_name}...")
        result = subprocess.run(
            ["git", "clone", extension_url],
            cwd=extensions_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"Successfully installed {extension_name}.")
            return True
        else:
            print(f"Failed to install {extension_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error installing {extension_name}: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Install recommended plugins for Automatic1111")
    parser.add_argument("--sd-path", type=str, help="Path to Stable Diffusion WebUI installation")
    
    args = parser.parse_args()
    
    print("Automatic1111 Plugin Installer for Tarot Card Generation")
    print("=====================================================")
    print()
    
    # Get Stable Diffusion WebUI path
    sd_path = get_sd_path(args.sd_path)
    print(f"Using Stable Diffusion WebUI path: {sd_path}")
    
    # Check if git is installed
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: Git is not installed or not in PATH. Please install Git and try again.")
        return 1
    
    # Display recommended extensions
    print("\nRecommended extensions for tarot card generation:")
    for i, ext in enumerate(RECOMMENDED_EXTENSIONS, 1):
        print(f"{i}. {ext['name']}: {ext['description']}")
    
    # Ask user which extensions to install
    print("\nWhich extensions would you like to install?")
    print("Enter numbers separated by spaces, 'all' for all extensions, or 'q' to quit.")
    
    choice = input("> ")
    
    if choice.lower() == 'q':
        print("Exiting without installing extensions.")
        return 0
    
    extensions_to_install = []
    
    if choice.lower() == 'all':
        extensions_to_install = RECOMMENDED_EXTENSIONS
    else:
        try:
            indices = [int(x) - 1 for x in choice.split()]
            for i in indices:
                if 0 <= i < len(RECOMMENDED_EXTENSIONS):
                    extensions_to_install.append(RECOMMENDED_EXTENSIONS[i])
                else:
                    print(f"Warning: {i+1} is not a valid extension number.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")
            return 1
    
    # Install selected extensions
    print("\nInstalling selected extensions...")
    
    success_count = 0
    for ext in extensions_to_install:
        if install_extension(sd_path, ext["url"], ext["name"]):
            success_count += 1
    
    print(f"\nInstalled {success_count} of {len(extensions_to_install)} extensions.")
    
    if success_count > 0:
        print("\nTo activate the new extensions:")
        print("1. Restart your Automatic1111 WebUI")
        print("2. Go to the 'Extensions' tab")
        print("3. Click 'Apply and restart UI'")
    
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
