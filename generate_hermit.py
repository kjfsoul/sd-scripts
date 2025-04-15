import os
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

# Create output directory if it doesn't exist
output_dir = "output/tarot_cards"
os.makedirs(output_dir, exist_ok=True)

# Load the model
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cuda")

# Enable attention slicing for lower memory usage
pipe.enable_attention_slicing()

# Define style prompts
style_prompts = [
    "The Hermit tarot card, detailed illustration, ornate golden border, mystical symbols, clear text, high quality, fantasy art style",
    "The Hermit tarot card, intricate artwork, decorative frame, esoteric symbols, vibrant colors, professional illustration, clear typography"
]

# Generate images
for i in range(2):
    # Use different style for each variation
    prompt = style_prompts[i]
    
    # Generate the image
    image = pipe(
        prompt=prompt,
        negative_prompt="blurry, low quality, distorted text, poorly drawn, bad anatomy",
        num_inference_steps=30,
        guidance_scale=7.5
    ).images[0]
    
    # Save the image
    filename = f"the_hermit_{i+1}.png"
    image.save(os.path.join(output_dir, filename))
    print(f"Saved {filename}")

print("The Hermit card generated successfully!")
