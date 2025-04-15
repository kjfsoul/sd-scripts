# setup_lora_dataset.py

import os

dataset_name = "fooldeck-lora"
image_input_folder = "raw_images"  # Put your training images here
train_folder = f"training/{dataset_name}/train"
reg_folder = f"training/{dataset_name}/reg"

os.makedirs(train_folder, exist_ok=True)
os.makedirs(reg_folder, exist_ok=True)

default_caption = "fooldeck style, pastel art nouveau tarot card, ethereal, fantasy soft lighting"

for file in os.listdir(image_input_folder):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        src = os.path.join(image_input_folder, file)
        dst = os.path.join(train_folder, file)
        os.system(f'copy "{src}" "{dst}"')  # Windows uses 'copy' instead of 'cp'

        base = os.path.splitext(file)[0]
        caption_path = os.path.join(train_folder, f"{base}.txt")
        with open(caption_path, "w") as f:
            f.write(default_caption)

print(f"✅ Dataset structure created in: training/{dataset_name}/")
print(f"📄 Each image has a matching caption file.")
