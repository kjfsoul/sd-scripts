#!/usr/bin/env python3
"""
Tarot Deck Style Guide Generator - Creates comprehensive style guides from analyzed prompts
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from PIL import Image

# Configuration
STYLE_TEMPLATES_DIR = "style_templates"
OUTPUT_DIR = "style_guides"
REFERENCE_DIR = "reference/images"
PROMPT_DIR = "reference/prompts"

def load_style_template(template_name):
    """Load a style template from the templates directory"""
    template_path = os.path.join(STYLE_TEMPLATES_DIR, f"{template_name}.txt")
    
    if not os.path.exists(template_path):
        print(f"Error: Template '{template_name}' not found.")
        return None
    
    try:
        with open(template_path, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error loading template: {e}")
        return None

def load_deck_style():
    """Load the deck style from the deck_style.txt file if it exists"""
    style_file = "enhanced_deck_style.txt"
    if not os.path.exists(style_file):
        style_file = "deck_style.txt"
        if not os.path.exists(style_file):
            return None
    
    try:
        with open(style_file, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error loading deck style: {e}")
        return None

def get_reference_images():
    """Get a list of reference images"""
    image_files = []
    for ext in ['.png', '.jpg', '.jpeg', '.webp']:
        image_files.extend(list(Path(REFERENCE_DIR).glob(f"*{ext}")))
    return image_files

def create_style_guide(project_name, template_name=None, client_name=None):
    """Create a comprehensive style guide"""
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load deck style
    deck_style = load_deck_style()
    
    # Load template if specified
    template_content = None
    if template_name:
        template_content = load_style_template(template_name)
    
    # Get reference images
    reference_images = get_reference_images()
    
    # Create style guide filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project_name.replace(' ', '_').lower()}_style_guide_{timestamp}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Write style guide
    try:
        with open(filepath, 'w') as f:
            # Header
            f.write(f"# {project_name} - Tarot Deck Style Guide\n\n")
            f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            
            if client_name:
                f.write(f"**Client:** {client_name}\n\n")
            
            # Introduction
            f.write("## Introduction\n\n")
            f.write("This style guide defines the visual aesthetic for the tarot deck. It should be used as a reference for all card generation to ensure consistency across the entire deck.\n\n")
            
            # Reference Images
            f.write("## Reference Images\n\n")
            if reference_images:
                f.write(f"The style is based on {len(reference_images)} reference images located in `{REFERENCE_DIR}`:\n\n")
                for img in reference_images[:5]:  # List up to 5 images
                    f.write(f"- `{img.name}`\n")
                if len(reference_images) > 5:
                    f.write(f"- *(and {len(reference_images) - 5} more)*\n")
            else:
                f.write("No reference images found. Please add reference images to the `reference/images` directory.\n")
            f.write("\n")
            
            # Style Template
            if template_content:
                f.write("## Style Template\n\n")
                f.write("This deck uses the following style template as a foundation:\n\n")
                f.write("```\n")
                f.write(template_content)
                f.write("\n```\n\n")
            
            # Analyzed Style
            if deck_style:
                f.write("## Analyzed Style\n\n")
                f.write("Based on the reference images, the following style has been identified:\n\n")
                f.write("```\n")
                f.write(deck_style)
                f.write("\n```\n\n")
            
            # Style Categories
            f.write("## Style Categories\n\n")
            
            # Art Style Foundation
            f.write("### Art Style Foundation\n\n")
            if template_name:
                if template_name == "fantasy":
                    f.write("- Fantasy art with mystical and ethereal qualities\n")
                    f.write("- Magical realism approach with dreamlike elements\n")
                elif template_name == "vintage":
                    f.write("- Vintage illustration with art deco influences\n")
                    f.write("- Classic tarot aesthetic with retro styling\n")
                elif template_name == "minimalist":
                    f.write("- Clean, geometric designs with modern sensibility\n")
                    f.write("- Abstract representation of tarot concepts\n")
                elif template_name == "watercolor":
                    f.write("- Fluid, painterly style with organic qualities\n")
                    f.write("- Impressionistic approach with soft transitions\n")
                elif template_name == "cyberpunk":
                    f.write("- Futuristic digital aesthetic with high-tech elements\n")
                    f.write("- Neon-infused visuals with urban dystopian themes\n")
            else:
                f.write("- *(To be defined based on reference images and client preferences)*\n")
            f.write("\n")
            
            # Color & Lighting
            f.write("### Color & Lighting\n\n")
            if template_name:
                if template_name == "fantasy":
                    f.write("- Vibrant colors with magical glow effects\n")
                    f.write("- Dramatic lighting with rich shadows\n")
                elif template_name == "vintage":
                    f.write("- Muted colors and sepia tones\n")
                    f.write("- Soft lighting with aged paper texture\n")
                elif template_name == "minimalist":
                    f.write("- Limited color palette with high contrast\n")
                    f.write("- Flat lighting with bold color blocks\n")
                elif template_name == "watercolor":
                    f.write("- Soft colors with bleeding effects\n")
                    f.write("- Natural lighting with translucent layers\n")
                elif template_name == "cyberpunk":
                    f.write("- Neon colors with electric blue and magenta highlights\n")
                    f.write("- High contrast with digital glow effects\n")
            else:
                f.write("- *(To be defined based on reference images and client preferences)*\n")
            f.write("\n")
            
            # Key Elements
            f.write("### Key Elements\n\n")
            if template_name:
                if template_name == "fantasy":
                    f.write("- Mystical creatures and magical symbols\n")
                    f.write("- Enchanted objects and fantasy landscapes\n")
                elif template_name == "vintage":
                    f.write("- Classical symbolism and traditional iconography\n")
                    f.write("- Ornate frames and vintage patterns\n")
                elif template_name == "minimalist":
                    f.write("- Simple symbols and geometric shapes\n")
                    f.write("- Negative space and essential elements only\n")
                elif template_name == "watercolor":
                    f.write("- Flowing forms and organic shapes\n")
                    f.write("- Natural elements and gentle transitions\n")
                elif template_name == "cyberpunk":
                    f.write("- Cybernetic enhancements and holographic displays\n")
                    f.write("- Urban dystopia and digital interfaces\n")
            else:
                f.write("- *(To be defined based on reference images and client preferences)*\n")
            f.write("\n")
            
            # Detail Level
            f.write("### Detail Level\n\n")
            if template_name:
                if template_name == "fantasy":
                    f.write("- Highly detailed with intricate elements\n")
                    f.write("- Ornate and meticulous rendering\n")
                elif template_name == "vintage":
                    f.write("- Elegant linework with woodcut style\n")
                    f.write("- Stippled shading with hand-drawn quality\n")
                elif template_name == "minimalist":
                    f.write("- Clean and precise with uncluttered composition\n")
                    f.write("- Elegant simplicity with essential details only\n")
                elif template_name == "watercolor":
                    f.write("- Soft edges with textured appearance\n")
                    f.write("- Loose brushwork with delicate details\n")
                elif template_name == "cyberpunk":
                    f.write("- Hyper-detailed with complex elements\n")
                    f.write("- Intricate circuitry with technical precision\n")
            else:
                f.write("- *(To be defined based on reference images and client preferences)*\n")
            f.write("\n")
            
            # Production Guidelines
            f.write("## Production Guidelines\n\n")
            
            # Image Specifications
            f.write("### Image Specifications\n\n")
            f.write("- **Dimensions:** 900 x 1500 pixels (2.75 x 4.75 inches at 300 DPI)\n")
            f.write("- **Format:** PNG with transparency\n")
            f.write("- **Color Space:** sRGB\n\n")
            
            # Generation Parameters
            f.write("### Generation Parameters\n\n")
            f.write("- **Steps:** 30-40\n")
            f.write("- **CFG Scale:** 7-8\n")
            f.write("- **Sampler:** DPM++ 2M Karras\n")
            f.write("- **Negative Prompt:** deformed, ugly, disfigured, low quality, blurry, border, frame, text, watermark, signature, cut off, cropped\n\n")
            
            # Workflow
            f.write("## Workflow\n\n")
            f.write("1. Generate initial samples (3 cards, 2 variations each)\n")
            f.write("2. Review and refine style based on feedback\n")
            f.write("3. Generate remaining cards in batches of 10\n")
            f.write("4. Add borders, nameplates, and numerals separately\n")
            f.write("5. Final review and adjustments\n\n")
            
            # Final Prompt
            f.write("## Final Generation Prompt\n\n")
            if deck_style:
                # Extract the enhanced prompt if available
                match = re.search(r'## Enhanced Prompt\n(.*?)(?:\n\n|\n##|\Z)', deck_style, re.DOTALL)
                if match:
                    final_prompt = match.group(1).strip()
                    f.write("```\n")
                    f.write(final_prompt)
                    f.write("\n```\n\n")
                else:
                    # Try to find any line that looks like a prompt
                    lines = deck_style.strip().split('\n')
                    for line in lines:
                        if ',' in line and not line.startswith('#') and not line.startswith('='):
                            f.write("```\n")
                            f.write(line.strip())
                            f.write("\n```\n\n")
                            break
            else:
                f.write("*(Final prompt to be determined after style analysis)*\n\n")
            
        print(f"Style guide created: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error creating style guide: {e}")
        return None

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Generate a comprehensive tarot deck style guide")
    parser.add_argument("--project", type=str, required=True, help="Project name")
    parser.add_argument("--client", type=str, help="Client name")
    parser.add_argument("--template", type=str, choices=["fantasy", "vintage", "minimalist", "watercolor", "cyberpunk"], help="Style template to use")
    
    args = parser.parse_args()
    
    print("Tarot Deck Style Guide Generator")
    print("===============================")
    
    # Check if style templates directory exists
    if not os.path.exists(STYLE_TEMPLATES_DIR):
        print(f"Creating style templates directory: {STYLE_TEMPLATES_DIR}")
        os.makedirs(STYLE_TEMPLATES_DIR)
    
    # Create style guide
    filepath = create_style_guide(args.project, args.template, args.client)
    
    if filepath:
        print(f"\nStyle guide created successfully: {filepath}")
        
        # Open the style guide
        try:
            os.startfile(filepath)
        except:
            try:
                import subprocess
                subprocess.call(["open", filepath])
            except:
                print(f"Please open the style guide manually: {filepath}")
    else:
        print("\nFailed to create style guide.")
    
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
