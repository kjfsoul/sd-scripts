#!/usr/bin/env python3
"""
Tarot Card User Feedback Interface - Collects and manages user feedback on generated cards
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import glob
from pathlib import Path

# Configuration
CARDS_DIR = "images/cards"
FEEDBACK_DIR = "feedback"
CONFIG_FILE = "config/feedback_config.json"

class FeedbackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tarot Card Feedback Interface")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Load configuration
        self.config = self.load_config()
        
        # Ensure directories exist
        os.makedirs(CARDS_DIR, exist_ok=True)
        os.makedirs(FEEDBACK_DIR, exist_ok=True)
        
        # Get card images
        self.card_files = self.get_card_files()
        self.current_index = 0
        
        # Create UI
        self.create_ui()
        
        # Load first card if available
        if self.card_files:
            self.load_card(self.current_index)
        else:
            messagebox.showinfo("No Cards", "No card images found in the cards directory.")
    
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
            "feedback_categories": [
                "Overall Impression",
                "Style Consistency",
                "Composition",
                "Color Palette",
                "Details",
                "Symbolism",
                "Other"
            ],
            "rating_scale": 5,
            "auto_save": True
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
    
    def get_card_files(self):
        """Get all card image files"""
        card_files = []
        for ext in ['.png', '.jpg', '.jpeg', '.webp']:
            card_files.extend(glob.glob(os.path.join(CARDS_DIR, f"*{ext}")))
        return sorted(card_files)
    
    def create_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for navigation
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Navigation buttons
        ttk.Button(top_frame, text="Previous", command=self.prev_card).pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Next", command=self.next_card).pack(side=tk.LEFT, padx=5)
        
        # Card counter
        self.counter_label = ttk.Label(top_frame, text="Card 0/0")
        self.counter_label.pack(side=tk.LEFT, padx=10)
        
        # Card name
        self.name_label = ttk.Label(top_frame, text="", font=("Arial", 14, "bold"))
        self.name_label.pack(side=tk.LEFT, padx=20)
        
        # Accept/Reject buttons
        ttk.Button(top_frame, text="Accept", command=lambda: self.quick_feedback("accept")).pack(side=tk.RIGHT)
        ttk.Button(top_frame, text="Reject", command=lambda: self.quick_feedback("reject")).pack(side=tk.RIGHT, padx=5)
        
        # Content frame (image and feedback)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Image frame (left)
        image_frame = ttk.Frame(content_frame, borderwidth=2, relief="groove")
        image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Image canvas with scrollbars
        self.canvas = tk.Canvas(image_frame, bg="black")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars for canvas
        v_scrollbar = ttk.Scrollbar(image_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = ttk.Scrollbar(content_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Feedback frame (right)
        feedback_frame = ttk.Frame(content_frame, padding=10, width=400)
        feedback_frame.pack(side=tk.RIGHT, fill=tk.Y)
        feedback_frame.pack_propagate(False)  # Prevent shrinking
        
        # Feedback form
        ttk.Label(feedback_frame, text="Feedback", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Ratings
        ratings_frame = ttk.LabelFrame(feedback_frame, text="Ratings")
        ratings_frame.pack(fill=tk.X, pady=5)
        
        self.ratings = {}
        for category in self.config["feedback_categories"]:
            category_frame = ttk.Frame(ratings_frame)
            category_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(category_frame, text=category, width=20).pack(side=tk.LEFT)
            
            rating_var = tk.IntVar(value=3)  # Default rating
            self.ratings[category] = rating_var
            
            rating_frame = ttk.Frame(category_frame)
            rating_frame.pack(side=tk.LEFT)
            
            for i in range(1, self.config["rating_scale"] + 1):
                ttk.Radiobutton(rating_frame, text=str(i), variable=rating_var, value=i).pack(side=tk.LEFT)
        
        # Comments
        ttk.Label(feedback_frame, text="Comments", anchor=tk.W).pack(fill=tk.X, pady=(10, 5))
        self.comments = scrolledtext.ScrolledText(feedback_frame, height=10)
        self.comments.pack(fill=tk.X)
        
        # Edit prompt
        ttk.Label(feedback_frame, text="Edit Prompt", anchor=tk.W).pack(fill=tk.X, pady=(10, 5))
        self.prompt_text = scrolledtext.ScrolledText(feedback_frame, height=6)
        self.prompt_text.pack(fill=tk.X)
        
        # Action buttons
        buttons_frame = ttk.Frame(feedback_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Save Feedback", command=self.save_feedback).pack(side=tk.LEFT)
        ttk.Button(buttons_frame, text="Regenerate", command=self.regenerate_card).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="View Prompt", command=self.view_prompt).pack(side=tk.LEFT, padx=5)
        
        # Bottom frame for status
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(bottom_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Bind keyboard shortcuts
        self.root.bind('<Left>', lambda e: self.prev_card())
        self.root.bind('<Right>', lambda e: self.next_card())
        self.root.bind('<a>', lambda e: self.quick_feedback("accept"))
        self.root.bind('<r>', lambda e: self.quick_feedback("reject"))
        self.root.bind('<s>', lambda e: self.save_feedback())
    
    def on_canvas_configure(self, event):
        """Handle canvas resize"""
        if hasattr(self, 'image_on_canvas'):
            self.canvas.itemconfig(self.image_on_canvas, anchor="center")
            self.canvas.coords(self.image_on_canvas, event.width/2, event.height/2)
    
    def load_card(self, index):
        """Load a card image"""
        if not self.card_files:
            return
        
        # Update counter
        self.current_index = index
        self.counter_label.config(text=f"Card {index + 1}/{len(self.card_files)}")
        
        # Get card file
        card_file = self.card_files[index]
        card_name = os.path.basename(card_file)
        self.name_label.config(text=card_name)
        
        # Load image
        try:
            image = Image.open(card_file)
            
            # Calculate scaling factor to fit in canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Ensure canvas has been drawn
                scale_width = canvas_width / image.width
                scale_height = canvas_height / image.height
                scale = min(scale_width, scale_height, 1.0)  # Don't scale up
                
                new_width = int(image.width * scale)
                new_height = int(image.height * scale)
                
                if scale < 1.0:
                    image = image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage
            self.tk_image = ImageTk.PhotoImage(image)
            
            # Display image
            self.canvas.delete("all")
            self.image_on_canvas = self.canvas.create_image(
                self.canvas.winfo_width()/2, 
                self.canvas.winfo_height()/2, 
                anchor=tk.CENTER, 
                image=self.tk_image
            )
            
            # Configure scrollregion
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Load existing feedback if available
            self.load_feedback(card_name)
            
            # Load prompt if available
            self.load_prompt(card_name)
            
            self.status_label.config(text=f"Loaded {card_name}")
        except Exception as e:
            self.status_label.config(text=f"Error loading image: {e}")
    
    def load_feedback(self, card_name):
        """Load existing feedback for a card"""
        feedback_file = os.path.join(FEEDBACK_DIR, f"{os.path.splitext(card_name)[0]}_feedback.json")
        
        # Clear current feedback
        for category in self.ratings:
            self.ratings[category].set(3)  # Reset to middle value
        self.comments.delete(1.0, tk.END)
        
        # Load feedback if exists
        if os.path.exists(feedback_file):
            try:
                with open(feedback_file, 'r') as f:
                    feedback = json.load(f)
                
                # Set ratings
                for category, rating in feedback.get("ratings", {}).items():
                    if category in self.ratings:
                        self.ratings[category].set(rating)
                
                # Set comments
                if "comments" in feedback:
                    self.comments.insert(tk.END, feedback["comments"])
                
                self.status_label.config(text=f"Loaded feedback for {card_name}")
            except Exception as e:
                self.status_label.config(text=f"Error loading feedback: {e}")
    
    def load_prompt(self, card_name):
        """Load prompt for a card"""
        prompt_file = os.path.join("prompts/cards", f"{os.path.splitext(card_name)[0]}.txt")
        
        # Clear current prompt
        self.prompt_text.delete(1.0, tk.END)
        
        # Load prompt if exists
        if os.path.exists(prompt_file):
            try:
                with open(prompt_file, 'r') as f:
                    prompt = f.read()
                
                self.prompt_text.insert(tk.END, prompt)
            except Exception as e:
                self.status_label.config(text=f"Error loading prompt: {e}")
    
    def save_feedback(self):
        """Save feedback for the current card"""
        if not self.card_files:
            return
        
        card_file = self.card_files[self.current_index]
        card_name = os.path.basename(card_file)
        
        # Collect feedback
        feedback = {
            "card_name": card_name,
            "ratings": {category: var.get() for category, var in self.ratings.items()},
            "comments": self.comments.get(1.0, tk.END).strip()
        }
        
        # Save feedback
        feedback_file = os.path.join(FEEDBACK_DIR, f"{os.path.splitext(card_name)[0]}_feedback.json")
        
        try:
            os.makedirs(FEEDBACK_DIR, exist_ok=True)
            with open(feedback_file, 'w') as f:
                json.dump(feedback, f, indent=4)
            
            self.status_label.config(text=f"Feedback saved for {card_name}")
        except Exception as e:
            self.status_label.config(text=f"Error saving feedback: {e}")
            messagebox.showerror("Error", f"Could not save feedback: {e}")
        
        # Save prompt if edited
        prompt_file = os.path.join("prompts/cards", f"{os.path.splitext(card_name)[0]}.txt")
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        
        if prompt:
            try:
                os.makedirs(os.path.dirname(prompt_file), exist_ok=True)
                with open(prompt_file, 'w') as f:
                    f.write(prompt)
                
                self.status_label.config(text=f"Prompt saved for {card_name}")
            except Exception as e:
                self.status_label.config(text=f"Error saving prompt: {e}")
    
    def quick_feedback(self, status):
        """Quickly mark a card as accepted or rejected"""
        if not self.card_files:
            return
        
        card_file = self.card_files[self.current_index]
        card_name = os.path.basename(card_file)
        
        # Create feedback with just status
        feedback = {
            "card_name": card_name,
            "status": status,
            "ratings": {category: var.get() for category, var in self.ratings.items()},
            "comments": self.comments.get(1.0, tk.END).strip()
        }
        
        # Save feedback
        feedback_file = os.path.join(FEEDBACK_DIR, f"{os.path.splitext(card_name)[0]}_feedback.json")
        
        try:
            os.makedirs(FEEDBACK_DIR, exist_ok=True)
            with open(feedback_file, 'w') as f:
                json.dump(feedback, f, indent=4)
            
            self.status_label.config(text=f"Card {card_name} marked as {status}")
            
            # Move to next card
            self.next_card()
        except Exception as e:
            self.status_label.config(text=f"Error saving status: {e}")
    
    def view_prompt(self):
        """View the prompt for the current card in a popup"""
        if not self.card_files:
            return
        
        card_file = self.card_files[self.current_index]
        card_name = os.path.basename(card_file)
        prompt_file = os.path.join("prompts/cards", f"{os.path.splitext(card_name)[0]}.txt")
        
        if os.path.exists(prompt_file):
            try:
                with open(prompt_file, 'r') as f:
                    prompt = f.read()
                
                # Create popup
                popup = tk.Toplevel(self.root)
                popup.title(f"Prompt for {card_name}")
                popup.geometry("600x400")
                
                # Add text area
                text = scrolledtext.ScrolledText(popup)
                text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                text.insert(tk.END, prompt)
                text.config(state=tk.DISABLED)  # Read-only
            except Exception as e:
                messagebox.showerror("Error", f"Could not load prompt: {e}")
        else:
            messagebox.showinfo("No Prompt", f"No prompt file found for {card_name}")
    
    def regenerate_card(self):
        """Regenerate the current card with the edited prompt"""
        if not self.card_files:
            return
        
        card_file = self.card_files[self.current_index]
        card_name = os.path.basename(card_file)
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        
        if not prompt:
            messagebox.showwarning("No Prompt", "Please enter a prompt to regenerate the card.")
            return
        
        # Save the prompt
        prompt_file = os.path.join("prompts/cards", f"{os.path.splitext(card_name)[0]}.txt")
        
        try:
            os.makedirs(os.path.dirname(prompt_file), exist_ok=True)
            with open(prompt_file, 'w') as f:
                f.write(prompt)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save prompt: {e}")
            return
        
        # Ask for confirmation
        if not messagebox.askyesno("Regenerate Card", f"Are you sure you want to regenerate {card_name}?"):
            return
        
        # Import the generator module
        try:
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            import advanced_tarot_generator
            
            # Extract card info from filename
            card_base = os.path.splitext(card_name)[0]
            if "_v" in card_base:
                card_base, variation = card_base.split("_v")
                variation = int(variation)
            else:
                variation = 1
            
            # Find the card in the major arcana list
            card_info = None
            for card in advanced_tarot_generator.MAJOR_ARCANA:
                if card["name"].lower().replace(" ", "") == card_base.lower():
                    card_info = card
                    break
            
            if not card_info:
                messagebox.showerror("Error", f"Could not identify card from filename: {card_name}")
                return
            
            # Create generator instance
            generator = advanced_tarot_generator.TarotCreator()
            
            # Generate the card
            self.status_label.config(text=f"Regenerating {card_name}...")
            
            # Create custom parameters
            params = {
                "width": 900,  # Standard tarot card width
                "height": 1500,  # Standard tarot card height
                "sampler_name": "DPM++ 2M Karras"
            }
            
            success = generator.generate_image(prompt, card_name, params=params)
            
            if success:
                self.status_label.config(text=f"Successfully regenerated {card_name}")
                
                # Reload the card
                self.card_files = self.get_card_files()  # Refresh file list
                self.load_card(self.current_index)
            else:
                self.status_label.config(text=f"Failed to regenerate {card_name}")
                messagebox.showerror("Error", f"Failed to regenerate {card_name}")
        except Exception as e:
            self.status_label.config(text=f"Error regenerating card: {e}")
            messagebox.showerror("Error", f"Could not regenerate card: {e}")
    
    def next_card(self):
        """Go to the next card"""
        if not self.card_files:
            return
        
        # Auto-save feedback if enabled
        if self.config["auto_save"]:
            self.save_feedback()
        
        # Go to next card
        next_index = (self.current_index + 1) % len(self.card_files)
        self.load_card(next_index)
    
    def prev_card(self):
        """Go to the previous card"""
        if not self.card_files:
            return
        
        # Auto-save feedback if enabled
        if self.config["auto_save"]:
            self.save_feedback()
        
        # Go to previous card
        prev_index = (self.current_index - 1) % len(self.card_files)
        self.load_card(prev_index)

def main():
    """Main function"""
    root = tk.Tk()
    app = FeedbackApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
