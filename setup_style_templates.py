#!/usr/bin/env python3
"""
Setup Style Templates - Creates default style templates for the prompt refiner
"""

import os
import sys
from pathlib import Path

# Configuration
STYLE_TEMPLATES_DIR = "style_templates"

def create_fantasy_template():
    """Create fantasy style template"""
    content = """# Fantasy Tarot Style Template

## Art Style Foundation
fantasy art, mystical, magical realism, ethereal, dreamlike

## Color Palette
vibrant colors, magical glow, dramatic lighting, rich shadows

## Key Elements
mystical creatures, magical symbols, enchanted objects, fantasy landscapes

## Detail Level
highly detailed, intricate, ornate, meticulous

## Artist Influence
in the style of Michael Whelan, Julie Bell, Boris Vallejo

## Complete Prompt
fantasy art, mystical, magical realism, ethereal, dreamlike, vibrant colors, magical glow, dramatic lighting, rich shadows, mystical creatures, magical symbols, enchanted objects, fantasy landscapes, highly detailed, intricate, ornate, meticulous, in the style of Michael Whelan, Julie Bell, Boris Vallejo"""
    
    file_path = os.path.join(STYLE_TEMPLATES_DIR, "fantasy.txt")
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created fantasy style template: {file_path}")

def create_vintage_template():
    """Create vintage style template"""
    content = """# Vintage Tarot Style Template

## Art Style Foundation
vintage illustration, art deco, retro, antique aesthetic, classic tarot

## Color Palette
muted colors, sepia tones, aged paper texture, soft lighting

## Key Elements
classical symbolism, traditional iconography, ornate frames, vintage patterns

## Detail Level
elegant linework, woodcut style, stippled shading, hand-drawn quality

## Artist Influence
in the style of Pamela Colman Smith, Arthur Rackham, Alphonse Mucha

## Complete Prompt
vintage illustration, art deco, retro, antique aesthetic, classic tarot, muted colors, sepia tones, aged paper texture, soft lighting, classical symbolism, traditional iconography, ornate frames, vintage patterns, elegant linework, woodcut style, stippled shading, hand-drawn quality, in the style of Pamela Colman Smith, Arthur Rackham, Alphonse Mucha"""
    
    file_path = os.path.join(STYLE_TEMPLATES_DIR, "vintage.txt")
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created vintage style template: {file_path}")

def create_minimalist_template():
    """Create minimalist style template"""
    content = """# Minimalist Tarot Style Template

## Art Style Foundation
minimalist, clean lines, geometric, abstract, modern

## Color Palette
limited color palette, high contrast, bold colors, flat lighting

## Key Elements
simple symbols, geometric shapes, negative space, essential elements only

## Detail Level
clean, precise, uncluttered, elegant simplicity

## Artist Influence
in the style of Piet Mondrian, Saul Bass, Malika Favre

## Complete Prompt
minimalist, clean lines, geometric, abstract, modern, limited color palette, high contrast, bold colors, flat lighting, simple symbols, geometric shapes, negative space, essential elements only, clean, precise, uncluttered, elegant simplicity, in the style of Piet Mondrian, Saul Bass, Malika Favre"""
    
    file_path = os.path.join(STYLE_TEMPLATES_DIR, "minimalist.txt")
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created minimalist style template: {file_path}")

def create_watercolor_template():
    """Create watercolor style template"""
    content = """# Watercolor Tarot Style Template

## Art Style Foundation
watercolor painting, fluid, organic, painterly, impressionistic

## Color Palette
soft colors, color bleeding, translucent layers, natural lighting

## Key Elements
flowing forms, organic shapes, natural elements, gentle transitions

## Detail Level
soft edges, textured, loose brushwork, delicate details

## Artist Influence
in the style of J.M.W. Turner, Yoshitaka Amano, Agnes Cecile

## Complete Prompt
watercolor painting, fluid, organic, painterly, impressionistic, soft colors, color bleeding, translucent layers, natural lighting, flowing forms, organic shapes, natural elements, gentle transitions, soft edges, textured, loose brushwork, delicate details, in the style of J.M.W. Turner, Yoshitaka Amano, Agnes Cecile"""
    
    file_path = os.path.join(STYLE_TEMPLATES_DIR, "watercolor.txt")
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created watercolor style template: {file_path}")

def create_cyberpunk_template():
    """Create cyberpunk style template"""
    content = """# Cyberpunk Tarot Style Template

## Art Style Foundation
cyberpunk, futuristic, digital, neon, high-tech

## Color Palette
neon colors, electric blue, magenta, high contrast, digital glow

## Key Elements
cybernetic enhancements, holographic displays, urban dystopia, digital interfaces

## Detail Level
hyper-detailed, complex, intricate circuitry, technical precision

## Artist Influence
in the style of Syd Mead, Simon Stålenhag, Josan Gonzalez

## Complete Prompt
cyberpunk, futuristic, digital, neon, high-tech, neon colors, electric blue, magenta, high contrast, digital glow, cybernetic enhancements, holographic displays, urban dystopia, digital interfaces, hyper-detailed, complex, intricate circuitry, technical precision, in the style of Syd Mead, Simon Stålenhag, Josan Gonzalez"""
    
    file_path = os.path.join(STYLE_TEMPLATES_DIR, "cyberpunk.txt")
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created cyberpunk style template: {file_path}")

def create_dark_fantasy_template():
    """Create dark fantasy style template"""
    content = """# Dark Fantasy Tarot Style Template

## Art Style Foundation
dark fantasy art, mystical, gothic, ethereal, occult

## Color Palette
teal and cyan color palette, moonlight ambiance, dark tones, ethereal glow

## Key Elements
mystical throne, glowing stone arch, magical symbols, intricate costume details

## Detail Level
highly detailed, ultra detailed, intricate details, realistic digital painting

## Artist Influence
in the style of Aaron Jasinski, Edgar Ainsworth, Cedric Seaut

## Complete Prompt
dark fantasy art, mystical, gothic, ethereal, occult, teal and cyan color palette, moonlight ambiance, dark tones, ethereal glow, mystical throne, glowing stone arch, magical symbols, intricate costume details, highly detailed, ultra detailed, intricate details, realistic digital painting, fantasy RPG aesthetic, in the style of Aaron Jasinski, Edgar Ainsworth, Cedric Seaut"""
    
    file_path = os.path.join(STYLE_TEMPLATES_DIR, "dark_fantasy.txt")
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created dark fantasy style template: {file_path}")

def main():
    """Main function"""
    print("Setting up style templates...")
    
    # Create style templates directory
    os.makedirs(STYLE_TEMPLATES_DIR, exist_ok=True)
    
    # Create templates
    create_fantasy_template()
    create_vintage_template()
    create_minimalist_template()
    create_watercolor_template()
    create_cyberpunk_template()
    create_dark_fantasy_template()
    
    print("\nStyle templates setup complete!")
    
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
