#!/usr/bin/env python3
"""
Tarot Deck Prompt Enhancer - Refines and improves deck style prompts
"""

import os
import re
import sys
import argparse
from collections import OrderedDict

def remove_redundancies(prompt):
    """Remove redundant terms from a prompt"""
    # Split the prompt into terms
    terms = [term.strip() for term in prompt.split(',')]
    
    # Remove empty terms
    terms = [term for term in terms if term]
    
    # Remove duplicates while preserving order
    unique_terms = list(OrderedDict.fromkeys(terms))
    
    # Remove terms that are substrings of other terms
    filtered_terms = []
    for i, term in enumerate(unique_terms):
        is_substring = False
        term_lower = term.lower()
        for j, other_term in enumerate(unique_terms):
            if i != j and term_lower in other_term.lower() and len(term_lower) < len(other_term.lower()):
                is_substring = True
                break
        if not is_substring:
            filtered_terms.append(term)
    
    return filtered_terms

def categorize_terms(terms):
    """Categorize terms into different groups"""
    art_styles = []
    artists = []
    descriptors = []
    subjects = []
    
    # Art style keywords
    art_style_keywords = ['art', 'style', 'illustration', 'painting', 'digital', 'fantasy', 'nouveau', 'deco', 'realistic', 'surreal', 'impressionist', 'expressionist', 'minimalist', 'abstract', 'storybook']
    
    # Subject keywords
    subject_keywords = ['man', 'woman', 'figure', 'character', 'person', 'rabbit', 'animal', 'chair', 'background', 'scene', 'landscape', 'portrait', 'sitting', 'standing']
    
    # Descriptor keywords
    descriptor_keywords = ['detailed', 'fine', 'ultra', 'high', 'quality', 'beautiful', 'elegant', 'ornate', 'intricate', 'vibrant', 'colorful', 'mystical', 'magical', 'ethereal']
    
    # Check for capitalized words (potential artist names)
    artist_pattern = re.compile(r'\b[A-Z][a-z]+\b')
    
    for term in terms:
        term_lower = term.lower()
        
        # Check if it's an artist name (starts with "by" or contains capitalized words)
        if term.startswith('by ') or term.startswith('in the style of '):
            artists.append(term)
        elif any(word for word in artist_pattern.findall(term) if len(word) > 2):
            artists.append(term)
        # Check if it's an art style
        elif any(keyword in term_lower for keyword in art_style_keywords):
            art_styles.append(term)
        # Check if it's a subject
        elif any(keyword in term_lower for keyword in subject_keywords):
            subjects.append(term)
        # Check if it's a descriptor
        elif any(keyword in term_lower for keyword in descriptor_keywords):
            descriptors.append(term)
        else:
            # If we can't categorize, put in descriptors as default
            descriptors.append(term)
    
    return {
        'art_styles': art_styles,
        'artists': artists,
        'descriptors': descriptors,
        'subjects': subjects
    }

def enhance_prompt(prompt):
    """Enhance a deck style prompt by removing redundancies and organizing terms"""
    # Remove redundancies
    terms = remove_redundancies(prompt)
    
    # Categorize terms
    categories = categorize_terms(terms)
    
    # Build enhanced prompt
    enhanced_parts = []
    
    # Add art styles first
    if categories['art_styles']:
        enhanced_parts.append(', '.join(categories['art_styles']))
    
    # Add descriptors
    if categories['descriptors']:
        enhanced_parts.append(', '.join(categories['descriptors']))
    
    # Add subjects if any
    if categories['subjects']:
        enhanced_parts.append(', '.join(categories['subjects']))
    
    # Add artists last
    if categories['artists']:
        enhanced_parts.append('in the style of ' + ', '.join(categories['artists']))
    
    # Join all parts
    enhanced_prompt = ', '.join(enhanced_parts)
    
    return enhanced_prompt

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Enhance and refine tarot deck style prompts")
    parser.add_argument("--input", type=str, default="deck_style.txt", help="Input file containing the deck style prompt")
    parser.add_argument("--output", type=str, default="enhanced_deck_style.txt", help="Output file for the enhanced prompt")
    parser.add_argument("--prompt", type=str, help="Direct prompt to enhance instead of reading from file")
    
    args = parser.parse_args()
    
    print("Tarot Deck Prompt Enhancer")
    print("=========================")
    
    prompt = args.prompt
    
    # If no direct prompt provided, read from file
    if not prompt:
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            return 1
        
        try:
            with open(args.input, 'r') as f:
                content = f.read()
                
                # Extract the suggested style prompt
                match = re.search(r'Suggested Deck Style Prompt:.*?\n(.*?)(?:\n\n|\n#|\Z)', content, re.DOTALL)
                if match:
                    prompt = match.group(1).strip()
                else:
                    # Try to find any line that looks like a prompt
                    lines = content.strip().split('\n')
                    for line in lines:
                        if ',' in line and not line.startswith('#') and not line.startswith('='):
                            prompt = line.strip()
                            break
                    
                    if not prompt:
                        print("Error: Could not find a prompt in the input file.")
                        return 1
        except Exception as e:
            print(f"Error reading input file: {e}")
            return 1
    
    print("\nOriginal Prompt:")
    print(prompt)
    
    # Enhance the prompt
    enhanced_prompt = enhance_prompt(prompt)
    
    print("\nEnhanced Prompt:")
    print(enhanced_prompt)
    
    # Save to file
    try:
        with open(args.output, 'w') as f:
            f.write("# Enhanced Tarot Deck Style Prompt\n\n")
            f.write("## Original Prompt\n")
            f.write(prompt + "\n\n")
            f.write("## Enhanced Prompt\n")
            f.write(enhanced_prompt + "\n\n")
            f.write("## Categories\n")
            
            # Add categorized terms
            terms = remove_redundancies(prompt)
            categories = categorize_terms(terms)
            
            f.write("\n### Art Styles\n")
            for style in categories['art_styles']:
                f.write(f"- {style}\n")
            
            f.write("\n### Descriptors\n")
            for desc in categories['descriptors']:
                f.write(f"- {desc}\n")
            
            f.write("\n### Subjects\n")
            for subj in categories['subjects']:
                f.write(f"- {subj}\n")
            
            f.write("\n### Artists\n")
            for artist in categories['artists']:
                f.write(f"- {artist}\n")
        
        print(f"\nEnhanced prompt saved to {args.output}")
    except Exception as e:
        print(f"Error saving enhanced prompt: {e}")
    
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
