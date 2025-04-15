import os
import argparse
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

# Define the major arcana cards to generate
MAJOR_ARCANA = [
    "The Fool",
    "The Magician",
    "The High Priestess",
    "The Empress",
    "The Emperor",
    "The Hierophant",
    "The Lovers",
    "The Chariot",
    "Strength",
    "The Hermit"
]

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate tarot card images")
parser.add_argument("--model_path", type=str, default="runwayml/stable-diffusion-v1-5", help="Path to the model")
parser.add_argument("--output_dir", type=str, default="output/tarot_cards", help="Output directory")
parser.add_argument("--num_variations", type=int, default=2, help="Number of variations per card")
parser.add_argument("--seed", type=int, default=None, help="Random seed for generation")
args = parser.parse_args()

# Create output directory if it doesn't exist
os.makedirs(args.output_dir, exist_ok=True)

# Load the model
pipe = StableDiffusionPipeline.from_pretrained(args.model_path, torch_dtype=torch.float16)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cuda")

# Enable attention slicing for lower memory usage
pipe.enable_attention_slicing()

# Generate images
for card in MAJOR_ARCANA:
    print(f"Generating {args.num_variations} variations of {card}...")
    
    # Define two different style prompts
    style_prompts = [
        f"{card} tarot card, detailed illustration, ornate golden border, mystical symbols, clear text, high quality, fantasy art style",
        f"{card} tarot card, intricate artwork, decorative frame, esoteric symbols, vibrant colors, professional illustration, clear typography"
    ]
    
    for i in range(args.num_variations):
        # Use different style for each variation
        prompt = style_prompts[i % len(style_prompts)]
        
        # Set seed for reproducibility if provided
        generator = None
        if args.seed is not None:
            generator = torch.Generator(device="cuda").manual_seed(args.seed + i)
        
        # Generate the image
        image = pipe(
            prompt=prompt,
            negative_prompt="blurry, low quality, distorted text, poorly drawn, bad anatomy",
            num_inference_steps=30,
            guidance_scale=7.5,
            generator=generator
        ).images[0]
        
        # Save the image
        filename = f"{card.lower().replace(' ', '_')}_{i+1}.png"
        image.save(os.path.join(args.output_dir, filename))
        print(f"Saved {filename}")

print("All tarot cards generated successfully!")
