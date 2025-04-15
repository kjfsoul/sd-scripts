#!/usr/bin/env python3
"""
Tarot Card Prompt Refiner - Helps create and refine prompts for tarot cards
"""

import os
import sys
import json
import argparse
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path

# Configuration
PROMPT_DIR = "prompts/cards"
STYLE_DIR = "style_templates"
CONFIG_FILE = "config/prompt_refiner_config.json"

class PromptRefinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tarot Card Prompt Refiner")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Load configuration
        self.config = self.load_config()
        
        # Ensure directories exist
        os.makedirs(PROMPT_DIR, exist_ok=True)
        os.makedirs(STYLE_DIR, exist_ok=True)
        
        # Load style templates
        self.style_templates = self.load_style_templates()
        
        # Load tarot card definitions
        self.tarot_cards = self.load_tarot_cards()
        
        # Create UI
        self.create_ui()
    
    def load_config(self):
        """Load configuration from file or create default"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.create_default_config()
        else:
            return self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        config = {
            "prompt_categories": [
                "Art Style",
                "Color Palette",
                "Lighting",
                "Composition",
                "Character Details",
                "Environment",
                "Symbolism",
                "Mood/Atmosphere",
                "Technical Details"
            ],
            "prompt_suggestions": {
                "Art Style": [
                    "fantasy art", "mystical", "art nouveau", "dark fantasy", "realistic digital painting",
                    "watercolor", "oil painting", "storybook illustration", "vintage tarot", "surrealism"
                ],
                "Color Palette": [
                    "vibrant colors", "muted colors", "teal and cyan color palette", "golden hues", 
                    "rich jewel tones", "pastel colors", "monochromatic", "high contrast"
                ],
                "Lighting": [
                    "dramatic lighting", "soft lighting", "moonlight ambiance", "ethereal glow",
                    "golden hour", "backlit", "rim lighting", "volumetric light"
                ],
                "Composition": [
                    "centered composition", "rule of thirds", "symmetrical", "dynamic pose",
                    "full body shot", "portrait framing", "wide angle", "looking at viewer"
                ],
                "Character Details": [
                    "intricate costume details", "flowing robes", "ornate headdress", "mystical jewelry",
                    "detailed facial features", "expressive pose", "holding symbolic items"
                ],
                "Environment": [
                    "mystical throne", "glowing stone arch", "magical forest", "cosmic background",
                    "ancient temple", "misty landscape", "starry sky", "sacred geometry patterns"
                ],
                "Symbolism": [
                    "magical symbols", "alchemical symbols", "zodiac elements", "elemental magic",
                    "spiritual imagery", "mythological references", "sacred geometry"
                ],
                "Mood/Atmosphere": [
                    "mysterious", "serene", "foreboding", "hopeful", "transcendent",
                    "magical atmosphere", "dreamlike", "otherworldly", "fantasy RPG aesthetic"
                ],
                "Technical Details": [
                    "highly detailed", "ultra detailed", "intricate details", "8k resolution",
                    "photorealistic", "hyperrealistic", "masterpiece", "best quality"
                ]
            },
            "artist_suggestions": [
                "Aaron Jasinski", "Edgar Ainsworth", "Cedric Seaut", "Alphonse Mucha", 
                "Arthur Rackham", "John William Waterhouse", "Stephanie Law", "James Jean"
            ],
            "default_negative_prompt": "deformed, ugly, disfigured, low quality, blurry, border, frame, text, watermark, signature, cut off, cropped, edge of frame, margin too small, bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, missing limbs, floating limbs, disconnected limbs, malformed hands, long neck, mutated, mutation, poorly drawn face, poorly drawn hands, distorted, amateur, out of frame, bad proportions, gross proportions, cloned face, weird colors, bad shadows, grainy, jpeg artifacts, duplicate, error, duplicate artifacts, airbrushed, cartoon, 3d render"
        }
        
        # Save default config
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        
        return config
    
    def save_config(self):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def load_style_templates(self):
        """Load style templates from files"""
        templates = {}
        
        # Check for style template files
        template_files = list(Path(STYLE_DIR).glob("*.txt"))
        
        for file in template_files:
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    
                    # Extract the complete prompt
                    for line in content.split('\n'):
                        if line.startswith("## Complete Prompt"):
                            # Get the next non-empty line
                            for prompt_line in content.split('\n')[content.split('\n').index(line) + 1:]:
                                if prompt_line.strip():
                                    templates[file.stem] = prompt_line.strip()
                                    break
                            break
                    
                    # If no complete prompt found, use the file name as a placeholder
                    if file.stem not in templates:
                        templates[file.stem] = f"Style template: {file.stem}"
            except Exception as e:
                print(f"Error loading style template {file}: {e}")
        
        return templates
    
    def load_tarot_cards(self):
        """Load tarot card definitions"""
        # Major Arcana
        major_arcana = [
            {"name": "The Fool", "numeral": "0", "keywords": "beginnings, innocence, spontaneity, free spirit"},
            {"name": "The Magician", "numeral": "I", "keywords": "manifestation, resourcefulness, power, inspired action"},
            {"name": "The High Priestess", "numeral": "II", "keywords": "intuition, sacred knowledge, divine feminine, subconscious mind"},
            {"name": "The Empress", "numeral": "III", "keywords": "femininity, beauty, nature, nurturing, abundance"},
            {"name": "The Emperor", "numeral": "IV", "keywords": "authority, structure, control, fatherhood, leadership"},
            {"name": "The Hierophant", "numeral": "V", "keywords": "spiritual wisdom, religious beliefs, conformity, tradition"},
            {"name": "The Lovers", "numeral": "VI", "keywords": "love, harmony, relationships, values alignment, choices"},
            {"name": "The Chariot", "numeral": "VII", "keywords": "control, willpower, success, action, determination"},
            {"name": "Strength", "numeral": "VIII", "keywords": "strength, courage, patience, control, compassion"},
            {"name": "The Hermit", "numeral": "IX", "keywords": "soul-searching, introspection, being alone, inner guidance"},
            {"name": "Wheel of Fortune", "numeral": "X", "keywords": "good luck, karma, life cycles, destiny, turning point"},
            {"name": "Justice", "numeral": "XI", "keywords": "justice, fairness, truth, cause and effect, law"},
            {"name": "The Hanged Man", "numeral": "XII", "keywords": "surrender, letting go, new perspective, sacrifice"},
            {"name": "Death", "numeral": "XIII", "keywords": "endings, change, transformation, transition"},
            {"name": "Temperance", "numeral": "XIV", "keywords": "balance, moderation, patience, purpose, meaning"},
            {"name": "The Devil", "numeral": "XV", "keywords": "shadow self, attachment, addiction, restriction, sexuality"},
            {"name": "The Tower", "numeral": "XVI", "keywords": "sudden change, upheaval, chaos, revelation, awakening"},
            {"name": "The Star", "numeral": "XVII", "keywords": "hope, faith, purpose, renewal, spirituality"},
            {"name": "The Moon", "numeral": "XVIII", "keywords": "illusion, fear, anxiety, subconscious, intuition"},
            {"name": "The Sun", "numeral": "XIX", "keywords": "positivity, fun, warmth, success, vitality"},
            {"name": "Judgement", "numeral": "XX", "keywords": "rebirth, inner calling, absolution, self-evaluation"},
            {"name": "The World", "numeral": "XXI", "keywords": "completion, accomplishment, travel, harmony, wholeness"}
        ]
        
        return major_arcana
    
    def create_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for card selection
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Card selection
        ttk.Label(top_frame, text="Select Tarot Card:").pack(side=tk.LEFT)
        
        self.card_var = tk.StringVar()
        card_combo = ttk.Combobox(top_frame, textvariable=self.card_var, width=30)
        card_combo['values'] = [card["name"] for card in self.tarot_cards]
        card_combo.pack(side=tk.LEFT, padx=5)
        card_combo.bind('<<ComboboxSelected>>', self.on_card_selected)
        
        # Card info
        self.card_info_label = ttk.Label(top_frame, text="", font=("Arial", 10, "italic"))
        self.card_info_label.pack(side=tk.LEFT, padx=20)
        
        # Style template selection
        ttk.Label(top_frame, text="Style Template:").pack(side=tk.LEFT, padx=(20, 0))
        
        self.style_var = tk.StringVar()
        style_combo = ttk.Combobox(top_frame, textvariable=self.style_var, width=20)
        style_combo['values'] = ["None"] + list(self.style_templates.keys())
        style_combo.current(0)
        style_combo.pack(side=tk.LEFT, padx=5)
        style_combo.bind('<<ComboboxSelected>>', self.on_style_selected)
        
        # Content frame (left and right panels)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for categories and suggestions
        left_frame = ttk.Frame(content_frame, width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Categories notebook
        self.categories_notebook = ttk.Notebook(left_frame)
        self.categories_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create a tab for each category
        self.category_frames = {}
        for category in self.config["prompt_categories"]:
            frame = ttk.Frame(self.categories_notebook, padding=10)
            self.categories_notebook.add(frame, text=category)
            self.category_frames[category] = frame
            
            # Add suggestions as buttons
            if category in self.config["prompt_suggestions"]:
                for suggestion in self.config["prompt_suggestions"][category]:
                    btn = ttk.Button(frame, text=suggestion, 
                                     command=lambda s=suggestion: self.add_to_prompt(s))
                    btn.pack(fill=tk.X, pady=2)
        
        # Add artist tab
        artist_frame = ttk.Frame(self.categories_notebook, padding=10)
        self.categories_notebook.add(artist_frame, text="Artists")
        
        for artist in self.config["artist_suggestions"]:
            btn = ttk.Button(artist_frame, text=artist, 
                             command=lambda a=artist: self.add_artist_to_prompt(a))
            btn.pack(fill=tk.X, pady=2)
        
        # Right frame for prompt editing
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Prompt editing
        ttk.Label(right_frame, text="Tarot Card Prompt:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.prompt_text = scrolledtext.ScrolledText(right_frame, height=10, wrap=tk.WORD)
        self.prompt_text.pack(fill=tk.X, pady=(0, 10))
        
        # Negative prompt
        ttk.Label(right_frame, text="Negative Prompt:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        self.negative_prompt_text = scrolledtext.ScrolledText(right_frame, height=5, wrap=tk.WORD)
        self.negative_prompt_text.pack(fill=tk.X, pady=(0, 10))
        self.negative_prompt_text.insert(tk.END, self.config["default_negative_prompt"])
        
        # Final prompt preview
        ttk.Label(right_frame, text="Final Prompt Preview:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        self.final_prompt_text = scrolledtext.ScrolledText(right_frame, height=8, wrap=tk.WORD)
        self.final_prompt_text.pack(fill=tk.X, pady=(0, 10))
        self.final_prompt_text.config(state=tk.DISABLED)
        
        # Buttons frame
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Update Preview", command=self.update_preview).pack(side=tk.LEFT)
        ttk.Button(buttons_frame, text="Save Prompt", command=self.save_prompt).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Clear Prompt", command=self.clear_prompt).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Reset Negative Prompt", command=self.reset_negative_prompt).pack(side=tk.LEFT, padx=5)
        
        # Bottom frame for status
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(bottom_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Initialize with first card if available
        if self.tarot_cards:
            card_combo.current(0)
            self.on_card_selected(None)
    
    def on_card_selected(self, event):
        """Handle card selection"""
        card_name = self.card_var.get()
        
        # Find the selected card
        selected_card = None
        for card in self.tarot_cards:
            if card["name"] == card_name:
                selected_card = card
                break
        
        if selected_card:
            # Update card info label
            self.card_info_label.config(text=f"{selected_card['numeral']} - {selected_card['keywords']}")
            
            # Check if a prompt file exists for this card
            card_filename = card_name.lower().replace(" ", "")
            prompt_file = os.path.join(PROMPT_DIR, f"{card_filename}.txt")
            
            if os.path.exists(prompt_file):
                # Load existing prompt
                try:
                    with open(prompt_file, 'r') as f:
                        prompt = f.read().strip()
                    
                    self.prompt_text.delete(1.0, tk.END)
                    self.prompt_text.insert(tk.END, prompt)
                    self.status_label.config(text=f"Loaded existing prompt for {card_name}")
                except Exception as e:
                    self.status_label.config(text=f"Error loading prompt: {e}")
            else:
                # Start with card name as base prompt
                self.prompt_text.delete(1.0, tk.END)
                self.prompt_text.insert(tk.END, f"{card_name} tarot card, ")
                self.status_label.config(text=f"Started new prompt for {card_name}")
            
            # Update preview
            self.update_preview()
    
    def on_style_selected(self, event):
        """Handle style template selection"""
        style_name = self.style_var.get()
        
        if style_name != "None" and style_name in self.style_templates:
            # Get current prompt
            current_prompt = self.prompt_text.get(1.0, tk.END).strip()
            
            # Extract card name part
            card_part = ""
            if "tarot card" in current_prompt:
                card_part = current_prompt.split("tarot card")[0] + "tarot card"
            else:
                card_name = self.card_var.get()
                card_part = f"{card_name} tarot card"
            
            # Apply style template
            new_prompt = f"{card_part}, {self.style_templates[style_name]}"
            
            # Update prompt
            self.prompt_text.delete(1.0, tk.END)
            self.prompt_text.insert(tk.END, new_prompt)
            
            self.status_label.config(text=f"Applied {style_name} style template")
            
            # Update preview
            self.update_preview()
    
    def add_to_prompt(self, suggestion):
        """Add a suggestion to the prompt"""
        current_prompt = self.prompt_text.get(1.0, tk.END).strip()
        
        # Add comma if needed
        if current_prompt and not current_prompt.endswith(","):
            current_prompt += ", "
        elif not current_prompt:
            # If empty, start with card name
            card_name = self.card_var.get()
            current_prompt = f"{card_name} tarot card, "
        
        # Add suggestion
        new_prompt = current_prompt + suggestion
        
        # Update prompt
        self.prompt_text.delete(1.0, tk.END)
        self.prompt_text.insert(tk.END, new_prompt)
        
        self.status_label.config(text=f"Added '{suggestion}' to prompt")
        
        # Update preview
        self.update_preview()
    
    def add_artist_to_prompt(self, artist):
        """Add an artist to the prompt"""
        current_prompt = self.prompt_text.get(1.0, tk.END).strip()
        
        # Check if already has artist
        if "in the style of" in current_prompt.lower():
            messagebox.showinfo("Artist Already Added", 
                               "The prompt already contains an artist reference. Please remove it first.")
            return
        
        # Add comma if needed
        if current_prompt and not current_prompt.endswith(","):
            current_prompt += ", "
        elif not current_prompt:
            # If empty, start with card name
            card_name = self.card_var.get()
            current_prompt = f"{card_name} tarot card, "
        
        # Add artist
        new_prompt = current_prompt + f"in the style of {artist}"
        
        # Update prompt
        self.prompt_text.delete(1.0, tk.END)
        self.prompt_text.insert(tk.END, new_prompt)
        
        self.status_label.config(text=f"Added artist '{artist}' to prompt")
        
        # Update preview
        self.update_preview()
    
    def update_preview(self):
        """Update the final prompt preview"""
        # Get current prompt
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        
        # Add composition guidance
        final_prompt = f"{prompt}, centered composition, complete scene, full body shot, nothing cropped out, with margin space around edges, highly detailed"
        
        # Update preview
        self.final_prompt_text.config(state=tk.NORMAL)
        self.final_prompt_text.delete(1.0, tk.END)
        self.final_prompt_text.insert(tk.END, final_prompt)
        self.final_prompt_text.config(state=tk.DISABLED)
        
        self.status_label.config(text="Preview updated")
    
    def save_prompt(self):
        """Save the prompt to a file"""
        card_name = self.card_var.get()
        if not card_name:
            messagebox.showerror("Error", "Please select a tarot card first.")
            return
        
        # Get prompts
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        negative_prompt = self.negative_prompt_text.get(1.0, tk.END).strip()
        
        if not prompt:
            messagebox.showerror("Error", "Prompt cannot be empty.")
            return
        
        # Create filename
        card_filename = card_name.lower().replace(" ", "")
        prompt_file = os.path.join(PROMPT_DIR, f"{card_filename}.txt")
        
        # Save prompt
        try:
            os.makedirs(PROMPT_DIR, exist_ok=True)
            with open(prompt_file, 'w') as f:
                f.write(prompt)
            
            # Also save negative prompt to a separate file
            negative_file = os.path.join(PROMPT_DIR, f"{card_filename}_negative.txt")
            with open(negative_file, 'w') as f:
                f.write(negative_prompt)
            
            self.status_label.config(text=f"Saved prompt for {card_name}")
            messagebox.showinfo("Success", f"Prompt for {card_name} saved successfully.")
        except Exception as e:
            self.status_label.config(text=f"Error saving prompt: {e}")
            messagebox.showerror("Error", f"Could not save prompt: {e}")
    
    def clear_prompt(self):
        """Clear the current prompt"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the current prompt?"):
            card_name = self.card_var.get()
            self.prompt_text.delete(1.0, tk.END)
            self.prompt_text.insert(tk.END, f"{card_name} tarot card, ")
            self.status_label.config(text="Prompt cleared")
            self.update_preview()
    
    def reset_negative_prompt(self):
        """Reset the negative prompt to default"""
        if messagebox.askyesno("Confirm", "Are you sure you want to reset the negative prompt to default?"):
            self.negative_prompt_text.delete(1.0, tk.END)
            self.negative_prompt_text.insert(tk.END, self.config["default_negative_prompt"])
            self.status_label.config(text="Negative prompt reset to default")

def main():
    """Main function"""
    root = tk.Tk()
    app = PromptRefinerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
