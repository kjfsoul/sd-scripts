#!/usr/bin/env python3
"""
Tarot Card Element Adder - Adds borders, nameplates, and numerals to tarot card images
"""

import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

# Configuration
CARDS_DIR = "images/cards"
BORDERS_DIR = "elements/borders"
NAMEPLATES_DIR = "elements/nameplates"
NUMERALS_DIR = "elements/numerals"
OUTPUT_DIR = "images/final"
CONFIG_FILE = "config/elements_config.json"

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

def load_config():
    """Load element configuration from file or create default"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return create_default_config()
    else:
        return create_default_config()

def create_default_config():
    """Create default element configuration"""
    config = {
        "border": {
            "file": "default_border.png",
            "opacity": 0.9
        },
        "nameplate": {
            "file": "default_nameplate.png",
            "position": "bottom",
            "offset_y": -50,
            "opacity": 0.9
        },
        "numeral": {
            "file": "default_numeral.png",
            "position": "top",
            "offset_y": 50,
            "opacity": 0.9
        },
        "text": {
            "font": "Arial",
            "size": 60,
            "color": "#FFFFFF",
            "stroke_width": 2,
            "stroke_color": "#000000",
            "position": "bottom",
            "offset_y": -50
        },
        "use_custom_elements": {
            "border": True,
            "nameplate": True,
            "numeral": True,
            "text": True
        }
    }
    
    # Save default config
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    
    return config

def save_config(config):
    """Save configuration to file"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {CONFIG_FILE}")

def ensure_directories():
    """Ensure all required directories exist"""
    os.makedirs(CARDS_DIR, exist_ok=True)
    os.makedirs(BORDERS_DIR, exist_ok=True)
    os.makedirs(NAMEPLATES_DIR, exist_ok=True)
    os.makedirs(NUMERALS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_card_info(filename):
    """Get card name and numeral from filename"""
    # Remove extension and variation suffix
    base_name = os.path.splitext(filename)[0]
    if "_v" in base_name:
        base_name = base_name.split("_v")[0]
    
    # Convert to title case and replace underscores with spaces
    card_name = base_name.replace("_", " ").title()
    
    # Find matching card in MAJOR_ARCANA
    for card in MAJOR_ARCANA:
        if card["name"].lower().replace(" ", "") == base_name.lower():
            return card["name"], card["numeral"]
    
    # If not found in major arcana, try to parse it
    if "of" in card_name:
        parts = card_name.split("Of")
        if len(parts) == 2:
            rank, suit = parts
            return f"{rank.strip()} of {suit.strip()}", ""
    
    # Default to filename and empty numeral
    return card_name, ""

def add_border(image, config):
    """Add border to image"""
    if not config["use_custom_elements"]["border"]:
        return image
    
    border_path = os.path.join(BORDERS_DIR, config["border"]["file"])
    if not os.path.exists(border_path):
        print(f"Warning: Border file not found: {border_path}")
        return image
    
    try:
        border = Image.open(border_path).convert("RGBA")
        border = border.resize(image.size, Image.LANCZOS)
        
        # Apply opacity
        opacity = config["border"]["opacity"]
        if opacity < 1.0:
            r, g, b, a = border.split()
            a = ImageEnhance.Brightness(a).enhance(opacity)
            border = Image.merge("RGBA", (r, g, b, a))
        
        # Composite border onto image
        composite = Image.alpha_composite(image, border)
        return composite
    except Exception as e:
        print(f"Error adding border: {e}")
        return image

def add_nameplate(image, card_name, config):
    """Add nameplate to image"""
    if not config["use_custom_elements"]["nameplate"]:
        return image
    
    nameplate_path = os.path.join(NAMEPLATES_DIR, config["nameplate"]["file"])
    if not os.path.exists(nameplate_path):
        print(f"Warning: Nameplate file not found: {nameplate_path}")
        return image
    
    try:
        nameplate = Image.open(nameplate_path).convert("RGBA")
        
        # Resize nameplate to appropriate width (70% of image width)
        width_ratio = 0.7
        new_width = int(image.width * width_ratio)
        ratio = new_width / nameplate.width
        new_height = int(nameplate.height * ratio)
        nameplate = nameplate.resize((new_width, new_height), Image.LANCZOS)
        
        # Calculate position
        position = config["nameplate"]["position"]
        offset_y = config["nameplate"]["offset_y"]
        
        x = (image.width - nameplate.width) // 2
        if position == "top":
            y = offset_y
        elif position == "bottom":
            y = image.height - nameplate.height + offset_y
        else:  # center
            y = (image.height - nameplate.height) // 2 + offset_y
        
        # Apply opacity
        opacity = config["nameplate"]["opacity"]
        if opacity < 1.0:
            r, g, b, a = nameplate.split()
            a = ImageEnhance.Brightness(a).enhance(opacity)
            nameplate = Image.merge("RGBA", (r, g, b, a))
        
        # Create a temporary image for the nameplate
        temp = Image.new("RGBA", image.size, (0, 0, 0, 0))
        temp.paste(nameplate, (x, y), nameplate)
        
        # Composite nameplate onto image
        composite = Image.alpha_composite(image, temp)
        return composite
    except Exception as e:
        print(f"Error adding nameplate: {e}")
        return image

def add_numeral(image, numeral, config):
    """Add numeral to image"""
    if not numeral or not config["use_custom_elements"]["numeral"]:
        return image
    
    numeral_path = os.path.join(NUMERALS_DIR, config["numeral"]["file"])
    if not os.path.exists(numeral_path):
        print(f"Warning: Numeral file not found: {numeral_path}")
        return image
    
    try:
        numeral_img = Image.open(numeral_path).convert("RGBA")
        
        # Resize numeral to appropriate width (20% of image width)
        width_ratio = 0.2
        new_width = int(image.width * width_ratio)
        ratio = new_width / numeral_img.width
        new_height = int(numeral_img.height * ratio)
        numeral_img = numeral_img.resize((new_width, new_height), Image.LANCZOS)
        
        # Calculate position
        position = config["numeral"]["position"]
        offset_y = config["numeral"]["offset_y"]
        
        x = (image.width - numeral_img.width) // 2
        if position == "top":
            y = offset_y
        elif position == "bottom":
            y = image.height - numeral_img.height + offset_y
        else:  # center
            y = (image.height - numeral_img.height) // 2 + offset_y
        
        # Apply opacity
        opacity = config["numeral"]["opacity"]
        if opacity < 1.0:
            r, g, b, a = numeral_img.split()
            a = ImageEnhance.Brightness(a).enhance(opacity)
            numeral_img = Image.merge("RGBA", (r, g, b, a))
        
        # Create a temporary image for the numeral
        temp = Image.new("RGBA", image.size, (0, 0, 0, 0))
        temp.paste(numeral_img, (x, y), numeral_img)
        
        # Composite numeral onto image
        composite = Image.alpha_composite(image, temp)
        return composite
    except Exception as e:
        print(f"Error adding numeral: {e}")
        return image

def add_text(image, card_name, numeral, config):
    """Add text to image"""
    if not config["use_custom_elements"]["text"]:
        return image
    
    try:
        # Create a drawing context
        draw = ImageDraw.Draw(image)
        
        # Get font
        font_name = config["text"]["font"]
        font_size = config["text"]["size"]
        
        try:
            font = ImageFont.truetype(font_name, font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
            font_size = 40
        
        # Calculate position for card name
        text_width, text_height = draw.textsize(card_name, font=font)
        position = config["text"]["position"]
        offset_y = config["text"]["offset_y"]
        
        x = (image.width - text_width) // 2
        if position == "top":
            y = offset_y
        elif position == "bottom":
            y = image.height - text_height + offset_y
        else:  # center
            y = (image.height - text_height) // 2 + offset_y
        
        # Draw text with stroke
        stroke_width = config["text"]["stroke_width"]
        stroke_color = config["text"]["stroke_color"]
        text_color = config["text"]["color"]
        
        # Draw stroke
        if stroke_width > 0:
            for dx in range(-stroke_width, stroke_width + 1):
                for dy in range(-stroke_width, stroke_width + 1):
                    if dx*dx + dy*dy <= stroke_width*stroke_width:
                        draw.text((x + dx, y + dy), card_name, font=font, fill=stroke_color)
        
        # Draw text
        draw.text((x, y), card_name, font=font, fill=text_color)
        
        # Add numeral if available
        if numeral:
            numeral_width, numeral_height = draw.textsize(numeral, font=font)
            numeral_x = (image.width - numeral_width) // 2
            numeral_y = y - numeral_height - 20  # Above the card name
            
            # Draw stroke for numeral
            if stroke_width > 0:
                for dx in range(-stroke_width, stroke_width + 1):
                    for dy in range(-stroke_width, stroke_width + 1):
                        if dx*dx + dy*dy <= stroke_width*stroke_width:
                            draw.text((numeral_x + dx, numeral_y + dy), numeral, font=font, fill=stroke_color)
            
            # Draw numeral
            draw.text((numeral_x, numeral_y), numeral, font=font, fill=text_color)
        
        return image
    except Exception as e:
        print(f"Error adding text: {e}")
        return image

def process_card(filename, config):
    """Process a single card image"""
    input_path = os.path.join(CARDS_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    try:
        # Open image
        image = Image.open(input_path).convert("RGBA")
        
        # Get card info
        card_name, numeral = get_card_info(filename)
        
        # Add elements
        image = add_border(image, config)
        image = add_nameplate(image, card_name, config)
        image = add_numeral(image, numeral, config)
        image = add_text(image, card_name, numeral, config)
        
        # Save final image
        image.save(output_path)
        print(f"Processed: {filename}")
        return True
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Add borders, nameplates, and numerals to tarot card images")
    parser.add_argument("--configure", action="store_true", help="Configure element settings")
    parser.add_argument("--file", type=str, help="Process a specific file")
    parser.add_argument("--all", action="store_true", help="Process all files in the cards directory")
    
    args = parser.parse_args()
    
    print("Tarot Card Element Adder")
    print("=======================")
    
    # Ensure directories exist
    ensure_directories()
    
    # Load configuration
    config = load_config()
    
    # Configure mode
    if args.configure:
        print("\nConfigure Element Settings")
        print("========================")
        
        # Border settings
        print("\nBorder Settings:")
        use_border = input(f"Use custom border? (Y/N, current: {'Y' if config['use_custom_elements']['border'] else 'N'}): ").strip().lower()
        if use_border == 'y':
            config["use_custom_elements"]["border"] = True
            
            # List available borders
            borders = [f for f in os.listdir(BORDERS_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if borders:
                print("\nAvailable borders:")
                for i, border in enumerate(borders):
                    print(f"{i+1}. {border}")
                
                try:
                    choice = int(input(f"Select border (1-{len(borders)}, current: {config['border']['file']}): "))
                    if 1 <= choice <= len(borders):
                        config["border"]["file"] = borders[choice-1]
                except ValueError:
                    print("Invalid choice. Keeping current border.")
            else:
                print("No border files found. Please add border images to the elements/borders directory.")
            
            # Border opacity
            try:
                opacity = float(input(f"Border opacity (0.0-1.0, current: {config['border']['opacity']}): "))
                if 0.0 <= opacity <= 1.0:
                    config["border"]["opacity"] = opacity
            except ValueError:
                print("Invalid opacity. Keeping current value.")
        elif use_border == 'n':
            config["use_custom_elements"]["border"] = False
        
        # Nameplate settings
        print("\nNameplate Settings:")
        use_nameplate = input(f"Use custom nameplate? (Y/N, current: {'Y' if config['use_custom_elements']['nameplate'] else 'N'}): ").strip().lower()
        if use_nameplate == 'y':
            config["use_custom_elements"]["nameplate"] = True
            
            # List available nameplates
            nameplates = [f for f in os.listdir(NAMEPLATES_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if nameplates:
                print("\nAvailable nameplates:")
                for i, nameplate in enumerate(nameplates):
                    print(f"{i+1}. {nameplate}")
                
                try:
                    choice = int(input(f"Select nameplate (1-{len(nameplates)}, current: {config['nameplate']['file']}): "))
                    if 1 <= choice <= len(nameplates):
                        config["nameplate"]["file"] = nameplates[choice-1]
                except ValueError:
                    print("Invalid choice. Keeping current nameplate.")
            else:
                print("No nameplate files found. Please add nameplate images to the elements/nameplates directory.")
            
            # Nameplate position
            position = input(f"Nameplate position (top/center/bottom, current: {config['nameplate']['position']}): ").strip().lower()
            if position in ['top', 'center', 'bottom']:
                config["nameplate"]["position"] = position
            
            # Nameplate offset
            try:
                offset = int(input(f"Nameplate Y offset (current: {config['nameplate']['offset_y']}): "))
                config["nameplate"]["offset_y"] = offset
            except ValueError:
                print("Invalid offset. Keeping current value.")
            
            # Nameplate opacity
            try:
                opacity = float(input(f"Nameplate opacity (0.0-1.0, current: {config['nameplate']['opacity']}): "))
                if 0.0 <= opacity <= 1.0:
                    config["nameplate"]["opacity"] = opacity
            except ValueError:
                print("Invalid opacity. Keeping current value.")
        elif use_nameplate == 'n':
            config["use_custom_elements"]["nameplate"] = False
        
        # Numeral settings
        print("\nNumeral Settings:")
        use_numeral = input(f"Use custom numeral plate? (Y/N, current: {'Y' if config['use_custom_elements']['numeral'] else 'N'}): ").strip().lower()
        if use_numeral == 'y':
            config["use_custom_elements"]["numeral"] = True
            
            # List available numerals
            numerals = [f for f in os.listdir(NUMERALS_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if numerals:
                print("\nAvailable numeral plates:")
                for i, numeral in enumerate(numerals):
                    print(f"{i+1}. {numeral}")
                
                try:
                    choice = int(input(f"Select numeral plate (1-{len(numerals)}, current: {config['numeral']['file']}): "))
                    if 1 <= choice <= len(numerals):
                        config["numeral"]["file"] = numerals[choice-1]
                except ValueError:
                    print("Invalid choice. Keeping current numeral plate.")
            else:
                print("No numeral files found. Please add numeral images to the elements/numerals directory.")
            
            # Numeral position
            position = input(f"Numeral position (top/center/bottom, current: {config['numeral']['position']}): ").strip().lower()
            if position in ['top', 'center', 'bottom']:
                config["numeral"]["position"] = position
            
            # Numeral offset
            try:
                offset = int(input(f"Numeral Y offset (current: {config['numeral']['offset_y']}): "))
                config["numeral"]["offset_y"] = offset
            except ValueError:
                print("Invalid offset. Keeping current value.")
            
            # Numeral opacity
            try:
                opacity = float(input(f"Numeral opacity (0.0-1.0, current: {config['numeral']['opacity']}): "))
                if 0.0 <= opacity <= 1.0:
                    config["numeral"]["opacity"] = opacity
            except ValueError:
                print("Invalid opacity. Keeping current value.")
        elif use_numeral == 'n':
            config["use_custom_elements"]["numeral"] = False
        
        # Text settings
        print("\nText Settings:")
        use_text = input(f"Add text directly to cards? (Y/N, current: {'Y' if config['use_custom_elements']['text'] else 'N'}): ").strip().lower()
        if use_text == 'y':
            config["use_custom_elements"]["text"] = True
            
            # Font
            font = input(f"Font name (current: {config['text']['font']}): ")
            if font:
                config["text"]["font"] = font
            
            # Font size
            try:
                size = int(input(f"Font size (current: {config['text']['size']}): "))
                if size > 0:
                    config["text"]["size"] = size
            except ValueError:
                print("Invalid size. Keeping current value.")
            
            # Text color
            color = input(f"Text color (hex code, current: {config['text']['color']}): ")
            if color:
                config["text"]["color"] = color
            
            # Stroke width
            try:
                width = int(input(f"Stroke width (0 for none, current: {config['text']['stroke_width']}): "))
                if width >= 0:
                    config["text"]["stroke_width"] = width
            except ValueError:
                print("Invalid width. Keeping current value.")
            
            # Stroke color
            if config["text"]["stroke_width"] > 0:
                color = input(f"Stroke color (hex code, current: {config['text']['stroke_color']}): ")
                if color:
                    config["text"]["stroke_color"] = color
            
            # Text position
            position = input(f"Text position (top/center/bottom, current: {config['text']['position']}): ").strip().lower()
            if position in ['top', 'center', 'bottom']:
                config["text"]["position"] = position
            
            # Text offset
            try:
                offset = int(input(f"Text Y offset (current: {config['text']['offset_y']}): "))
                config["text"]["offset_y"] = offset
            except ValueError:
                print("Invalid offset. Keeping current value.")
        elif use_text == 'n':
            config["use_custom_elements"]["text"] = False
        
        # Save configuration
        save_config(config)
        print("\nConfiguration updated.")
        
        # Ask if user wants to process cards
        process_cards = input("\nProcess cards now? (Y/N): ").strip().lower()
        if process_cards != 'y':
            return 0
    
    # Process specific file
    if args.file:
        if os.path.exists(os.path.join(CARDS_DIR, args.file)):
            process_card(args.file, config)
        else:
            print(f"Error: File not found: {args.file}")
            return 1
    
    # Process all files
    elif args.all or (not args.configure and not args.file):
        card_files = [f for f in os.listdir(CARDS_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if not card_files:
            print("No card images found in the cards directory.")
            return 1
        
        print(f"\nProcessing {len(card_files)} card images...")
        
        success_count = 0
        for filename in card_files:
            if process_card(filename, config):
                success_count += 1
        
        print(f"\nProcessed {success_count} of {len(card_files)} cards successfully.")
        print(f"Check the {OUTPUT_DIR} directory for the processed images.")
    
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
