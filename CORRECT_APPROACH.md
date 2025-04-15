# Correct Approach for Tarot Card Generation

Based on your feedback, here's the correct approach to generate tarot card images using Automatic1111's API.

## Step 1: Modify webui-user.bat to Enable API

1. Run `modify_webui_user.bat`
2. This will modify your webui-user.bat file to include the `--api` flag in the COMMANDLINE_ARGS
3. It will create a backup of your original file in case you need to restore it

## Step 2: Start Automatic1111

1. Start Automatic1111 by running the modified webui-user.bat
2. Wait for it to fully load
3. You can verify the API is enabled by checking if http://127.0.0.1:7860/docs is accessible

## Step 3: Generate Tarot Card Images

1. Run `manual_generate_tarot.bat`
2. This will check if the API is accessible and then generate the tarot card images
3. Images will be saved to the `tarot_output` folder

## Troubleshooting

If you encounter any issues:

1. **API Not Accessible**: Make sure Automatic1111 is fully loaded and the API is enabled
   - Check if http://127.0.0.1:7860/docs is accessible in your browser
   - If not, make sure the `--api` flag is included in your webui-user.bat

2. **LoRA Model Issues**: Make sure your LoRA model is properly loaded in Automatic1111
   - You can check available models at http://127.0.0.1:7860/sdapi/v1/loras

3. **Generation Errors**: If you encounter errors during image generation, check:
   - That your LoRA model name is correct in the generation script
   - That Automatic1111 has all required dependencies installed

## Manual Commands (if needed)

If you prefer to use manual commands:

1. Modify webui-user.bat to include `--api` in COMMANDLINE_ARGS
2. Start Automatic1111 using webui-user.bat
3. Run the following command to generate tarot cards:
   ```
   python generate_tarot_api.py --lora "fool_hypernetwork"
   ```
