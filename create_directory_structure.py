#!/usr/bin/env python3
"""
Create Directory Structure - Ensures all required directories exist for the tarot card system
"""

import os
import sys

# Define all required directories
DIRECTORIES = [
    "config",
    "elements/borders",
    "elements/nameplates",
    "elements/numerals",
    "feedback",
    "images/cards",
    "images/final",
    "prompts/cards",
    "reference/images",
    "reference/prompts",
    "style_guides",
    "style_templates"
]

def create_directories():
    """Create all required directories"""
    print("Creating directory structure...")
    
    for directory in DIRECTORIES:
        path = os.path.normpath(directory)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print(f"Created: {path}")
            except Exception as e:
                print(f"Error creating {path}: {e}")
        else:
            print(f"Already exists: {path}")
    
    print("\nDirectory structure created successfully.")

def main():
    """Main function"""
    print("Tarot Card System - Directory Structure Creator")
    print("===========================================")
    
    create_directories()
    
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
