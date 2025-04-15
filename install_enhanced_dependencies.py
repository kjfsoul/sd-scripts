#!/usr/bin/env python3
"""
Install Enhanced Dependencies - Installs additional Python packages for tarot card generation
"""

import os
import sys
import subprocess
import argparse

# List of recommended packages with descriptions
RECOMMENDED_PACKAGES = [
    {
        "name": "pillow",
        "description": "Python Imaging Library for image processing"
    },
    {
        "name": "requests",
        "description": "HTTP library for API requests"
    },
    {
        "name": "numpy",
        "description": "Numerical computing library"
    },
    {
        "name": "pandas",
        "description": "Data analysis library for organizing tarot card metadata"
    },
    {
        "name": "matplotlib",
        "description": "Plotting library for visualizing data"
    },
    {
        "name": "scikit-image",
        "description": "Image processing library for advanced image analysis"
    },
    {
        "name": "opencv-python",
        "description": "Computer vision library for image analysis"
    },
    {
        "name": "beautifulsoup4",
        "description": "Web scraping library for gathering tarot card references"
    },
    {
        "name": "transformers",
        "description": "Hugging Face Transformers for text generation and analysis"
    },
    {
        "name": "diffusers",
        "description": "Hugging Face Diffusers for working with diffusion models"
    },
    {
        "name": "accelerate",
        "description": "Hugging Face Accelerate for faster model inference"
    },
    {
        "name": "safetensors",
        "description": "Safe way to store and distribute tensors"
    },
    {
        "name": "gradio",
        "description": "Create UIs for machine learning models"
    },
    {
        "name": "pyyaml",
        "description": "YAML parser and emitter for configuration files"
    },
    {
        "name": "tqdm",
        "description": "Progress bar library for long-running tasks"
    }
]

def install_package(package_name):
    """Install a Python package using pip"""
    try:
        print(f"Installing {package_name}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"Successfully installed {package_name}.")
            return True
        else:
            print(f"Failed to install {package_name}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error installing {package_name}: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Install enhanced dependencies for tarot card generation")
    parser.add_argument("--all", action="store_true", help="Install all recommended packages without prompting")
    
    args = parser.parse_args()
    
    print("Enhanced Dependencies Installer for Tarot Card Generation")
    print("=====================================================")
    print()
    
    # Update pip
    print("Updating pip...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    
    # Display recommended packages
    if not args.all:
        print("\nRecommended packages for tarot card generation:")
        for i, pkg in enumerate(RECOMMENDED_PACKAGES, 1):
            print(f"{i}. {pkg['name']}: {pkg['description']}")
        
        # Ask user which packages to install
        print("\nWhich packages would you like to install?")
        print("Enter numbers separated by spaces, 'all' for all packages, or 'q' to quit.")
        
        choice = input("> ")
        
        if choice.lower() == 'q':
            print("Exiting without installing packages.")
            return 0
        
        packages_to_install = []
        
        if choice.lower() == 'all':
            packages_to_install = RECOMMENDED_PACKAGES
        else:
            try:
                indices = [int(x) - 1 for x in choice.split()]
                for i in indices:
                    if 0 <= i < len(RECOMMENDED_PACKAGES):
                        packages_to_install.append(RECOMMENDED_PACKAGES[i])
                    else:
                        print(f"Warning: {i+1} is not a valid package number.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")
                return 1
    else:
        packages_to_install = RECOMMENDED_PACKAGES
    
    # Install selected packages
    print("\nInstalling selected packages...")
    
    success_count = 0
    for pkg in packages_to_install:
        if install_package(pkg["name"]):
            success_count += 1
    
    print(f"\nInstalled {success_count} of {len(packages_to_install)} packages.")
    
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
