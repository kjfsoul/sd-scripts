#!/usr/bin/env python3
"""
Tarot Deck Style Analyzer - Analyzes prompt files to suggest a cohesive style for the entire deck
"""

import os
import re
import sys
import glob
from pathlib import Path
from collections import Counter
import argparse

# Configuration
PROMPT_DIR = "reference/prompts"
OUTPUT_FILE = "deck_style.txt"

def extract_keywords(text):
    """Extract meaningful keywords from text"""
    # Remove common words and keep style-related terms
    text = text.lower()
    
    # Remove tarot card specific terms
    text = re.sub(r'tarot card|the fool|the magician|the high priestess|the empress|the emperor|the hierophant|the lovers|the chariot|strength|the hermit|wheel of fortune|justice|the hanged man|death|temperance|the devil|the tower|the star|the moon|the sun|judgement|the world', '', text)
    
    # Remove common articles, prepositions, etc.
    stop_words = ['a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of', 'from', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could']
    
    for word in stop_words:
        text = re.sub(r'\b' + word + r'\b', '', text)
    
    # Extract words and phrases
    words = re.findall(r'\b\w+\b', text)
    phrases = re.findall(r'\b\w+\s+\w+\b', text)
    art_styles = re.findall(r'art\s+\w+|art\s+nouveau|art\s+deco|\w+\s+art', text)
    
    return words, phrases, art_styles

def analyze_prompts(prompt_dir):
    """Analyze all prompt files to find common patterns"""
    if not os.path.exists(prompt_dir):
        print(f"Error: Prompt directory '{prompt_dir}' not found.")
        return None
    
    # Get all text files in the prompt directory
    prompt_files = glob.glob(os.path.join(prompt_dir, "*.txt"))
    
    if not prompt_files:
        print("No prompt files found.")
        return None
    
    print(f"Found {len(prompt_files)} prompt files.")
    
    # Analyze each file
    all_words = []
    all_phrases = []
    all_art_styles = []
    
    for file_path in prompt_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read().strip()
                
                # Extract keywords
                words, phrases, art_styles = extract_keywords(content)
                all_words.extend(words)
                all_phrases.extend(phrases)
                all_art_styles.extend(art_styles)
                
                print(f"Analyzed {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Count occurrences
    word_counter = Counter(all_words)
    phrase_counter = Counter(all_phrases)
    style_counter = Counter(all_art_styles)
    
    # Filter out less common terms
    common_words = [word for word, count in word_counter.most_common(20) if count > 1 and len(word) > 3]
    common_phrases = [phrase for phrase, count in phrase_counter.most_common(10) if count > 1]
    common_styles = [style for style, count in style_counter.most_common(5) if count > 1]
    
    # Look for artist names (capitalized words)
    artist_pattern = re.compile(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b|\b[A-Z][a-z]+\b')
    artists = set()
    
    for file_path in prompt_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                found_artists = artist_pattern.findall(content)
                artists.update(found_artists)
        except Exception:
            pass
    
    # Generate style suggestion
    style_elements = []
    
    # Add art styles
    if common_styles:
        style_elements.extend(common_styles)
    
    # Add common descriptive phrases
    if common_phrases:
        style_elements.extend(common_phrases[:5])
    
    # Add common descriptive words
    if common_words:
        style_elements.extend(common_words[:10])
    
    # Add artists if found
    if artists:
        style_elements.append("in the style of " + ", ".join(list(artists)[:3]))
    
    # Create the final style suggestion
    style_suggestion = ", ".join(style_elements)
    
    # Create a more structured suggestion
    structured_suggestion = {
        "art_styles": common_styles,
        "descriptive_phrases": common_phrases[:5],
        "descriptive_words": common_words[:10],
        "artists": list(artists)[:3],
        "combined_suggestion": style_suggestion
    }
    
    return structured_suggestion

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Analyze tarot card prompts to suggest a cohesive deck style")
    parser.add_argument("--prompt-dir", type=str, default=PROMPT_DIR, help="Directory containing prompt files")
    parser.add_argument("--output", type=str, default=OUTPUT_FILE, help="Output file for the style suggestion")
    
    args = parser.parse_args()
    
    print("Tarot Deck Style Analyzer")
    print("========================")
    
    # Analyze prompts
    result = analyze_prompts(args.prompt_dir)
    
    if not result:
        print("Analysis failed. No style suggestion generated.")
        return 1
    
    # Print results
    print("\nStyle Analysis Results:")
    print("=====================")
    
    print("\nCommon Art Styles:")
    for style in result["art_styles"]:
        print(f"- {style}")
    
    print("\nCommon Descriptive Phrases:")
    for phrase in result["descriptive_phrases"]:
        print(f"- {phrase}")
    
    print("\nCommon Descriptive Words:")
    for word in result["descriptive_words"]:
        print(f"- {word}")
    
    print("\nDetected Artists:")
    for artist in result["artists"]:
        print(f"- {artist}")
    
    print("\nSuggested Deck Style Prompt:")
    print("==========================")
    print(result["combined_suggestion"])
    
    # Save to file
    try:
        with open(args.output, 'w') as f:
            f.write("# Tarot Deck Style Analysis\n\n")
            f.write("## Common Art Styles\n")
            for style in result["art_styles"]:
                f.write(f"- {style}\n")
            
            f.write("\n## Common Descriptive Phrases\n")
            for phrase in result["descriptive_phrases"]:
                f.write(f"- {phrase}\n")
            
            f.write("\n## Common Descriptive Words\n")
            for word in result["descriptive_words"]:
                f.write(f"- {word}\n")
            
            f.write("\n## Detected Artists\n")
            for artist in result["artists"]:
                f.write(f"- {artist}\n")
            
            f.write("\n## Suggested Deck Style Prompt\n")
            f.write(result["combined_suggestion"])
        
        print(f"\nStyle suggestion saved to {args.output}")
    except Exception as e:
        print(f"Error saving style suggestion: {e}")
    
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
