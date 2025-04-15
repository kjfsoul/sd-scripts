import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import glob

def add_border_to_image(
    image_path, 
    border_path, 
    output_path, 
    card_name=None, 
    card_number=None, 
    text_color=(255, 215, 0),  # Gold color
    font_path=None,
    resize_method="fit"  # "fit" or "fill"
):
    """
    Add a decorative border to a tarot card image.
    
    Args:
        image_path: Path to the input image
        border_path: Path to the border image
        output_path: Path to save the output image
        card_name: Text to display at the bottom of the card (optional)
        card_number: Text to display at the top of the card (optional)
        text_color: Color for the text (RGB tuple)
        font_path: Path to a TTF font file (optional, uses default if None)
        resize_method: How to resize the image to fit the border ("fit" or "fill")
    """
    # Load the images
    card_image = Image.open(image_path).convert("RGBA")
    border = Image.open(border_path).convert("RGBA")
    
    # Get dimensions
    border_width, border_height = border.size
    
    # Determine the inner area of the border where the card image will go
    # This is an approximation based on the provided border image
    inner_margin_top = int(border_height * 0.12)  # Top text area
    inner_margin_bottom = int(border_height * 0.12)  # Bottom text area
    inner_margin_left = int(border_width * 0.08)
    inner_margin_right = int(border_width * 0.08)
    
    inner_width = border_width - inner_margin_left - inner_margin_right
    inner_height = border_height - inner_margin_top - inner_margin_bottom
    
    # Resize the card image to fit within the inner area
    card_width, card_height = card_image.size
    
    if resize_method == "fit":
        # Resize while maintaining aspect ratio (may leave empty space)
        ratio = min(inner_width / card_width, inner_height / card_height)
        new_width = int(card_width * ratio)
        new_height = int(card_height * ratio)
        resized_card = card_image.resize((new_width, new_height), Image.LANCZOS)
        
        # Create a blank image with the inner dimensions
        inner_image = Image.new("RGBA", (inner_width, inner_height), (0, 0, 0, 0))
        
        # Calculate position to center the resized card
        x_offset = (inner_width - new_width) // 2
        y_offset = (inner_height - new_height) // 2
        
        # Paste the resized card onto the blank image
        inner_image.paste(resized_card, (x_offset, y_offset), resized_card)
    else:  # "fill"
        # Resize to fill the inner area (may crop the image)
        ratio = max(inner_width / card_width, inner_height / card_height)
        new_width = int(card_width * ratio)
        new_height = int(card_height * ratio)
        resized_card = card_image.resize((new_width, new_height), Image.LANCZOS)
        
        # Crop to fit the inner dimensions
        x_offset = (new_width - inner_width) // 2
        y_offset = (new_height - inner_height) // 2
        inner_image = resized_card.crop((x_offset, y_offset, x_offset + inner_width, y_offset + inner_height))
    
    # Create a new image with the border dimensions
    final_image = Image.new("RGBA", (border_width, border_height), (0, 0, 0, 0))
    
    # Paste the inner image onto the final image
    final_image.paste(inner_image, (inner_margin_left, inner_margin_top), inner_image)
    
    # Paste the border on top
    final_image = Image.alpha_composite(final_image, border)
    
    # Add text if provided
    if card_name or card_number:
        draw = ImageDraw.Draw(final_image)
        
        # Try to use the provided font or fall back to default
        try:
            name_font_size = int(border_height * 0.05)  # 5% of border height
            number_font_size = int(border_height * 0.04)  # 4% of border height
            
            if font_path and os.path.exists(font_path):
                name_font = ImageFont.truetype(font_path, name_font_size)
                number_font = ImageFont.truetype(font_path, number_font_size)
            else:
                # Use default font
                name_font = ImageFont.load_default()
                number_font = ImageFont.load_default()
                
            # Add card name at the bottom
            if card_name:
                # Calculate text position to center it
                text_width = draw.textlength(card_name, font=name_font)
                text_x = (border_width - text_width) // 2
                text_y = border_height - inner_margin_bottom // 2 - name_font_size // 2
                draw.text((text_x, text_y), card_name, fill=text_color, font=name_font)
            
            # Add card number at the top
            if card_number:
                # Calculate text position to center it
                text_width = draw.textlength(card_number, font=number_font)
                text_x = (border_width - text_width) // 2
                text_y = inner_margin_top // 2 - number_font_size // 2
                draw.text((text_x, text_y), card_number, fill=text_color, font=number_font)
                
        except Exception as e:
            print(f"Error adding text: {e}")
    
    # Convert to RGB for saving as JPEG/PNG
    final_image = final_image.convert("RGB")
    
    # Save the final image
    final_image.save(output_path)
    print(f"Saved bordered image to {output_path}")

def process_directory(
    input_dir, 
    border_path, 
    output_dir, 
    name_mapping=None, 
    font_path=None,
    resize_method="fit"
):
    """
    Process all images in a directory, adding the border to each.
    
    Args:
        input_dir: Directory containing input images
        border_path: Path to the border image
        output_dir: Directory to save output images
        name_mapping: Dictionary mapping filenames to card names and numbers
        font_path: Path to a TTF font file
        resize_method: How to resize the image to fit the border
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all image files in the input directory
    image_files = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.webp']:
        image_files.extend(glob.glob(os.path.join(input_dir, ext)))
    
    print(f"Found {len(image_files)} images to process")
    
    # Process each image
    for image_path in image_files:
        filename = os.path.basename(image_path)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}_bordered.png")
        
        # Get card name and number if mapping is provided
        card_name = None
        card_number = None
        if name_mapping and base_name in name_mapping:
            card_name = name_mapping[base_name].get('name')
            card_number = name_mapping[base_name].get('number')
        
        # Add border to the image
        add_border_to_image(
            image_path, 
            border_path, 
            output_path, 
            card_name, 
            card_number, 
            font_path=font_path,
            resize_method=resize_method
        )

def main():
    parser = argparse.ArgumentParser(description="Add decorative borders to tarot card images")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing input images")
    parser.add_argument("--border_path", type=str, required=True, help="Path to the border image")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save output images")
    parser.add_argument("--mapping_file", type=str, help="JSON file mapping filenames to card names and numbers")
    parser.add_argument("--font_path", type=str, help="Path to a TTF font file")
    parser.add_argument("--resize_method", type=str, choices=["fit", "fill"], default="fit", 
                        help="How to resize the image to fit the border")
    
    args = parser.parse_args()
    
    # Load name mapping if provided
    name_mapping = None
    if args.mapping_file and os.path.exists(args.mapping_file):
        import json
        with open(args.mapping_file, 'r') as f:
            name_mapping = json.load(f)
    
    # Process the directory
    process_directory(
        args.input_dir, 
        args.border_path, 
        args.output_dir, 
        name_mapping, 
        args.font_path,
        args.resize_method
    )

if __name__ == "__main__":
    main()
