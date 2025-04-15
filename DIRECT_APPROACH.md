# Direct Approach for Tarot Card Generation

If you're having trouble with the standard approach, try these direct scripts that use hardcoded paths and simplified steps.

## One-Step Solution

1. Run `direct_generate_tarot.bat`
2. This will:
   - Start Automatic1111 with API enabled
   - Wait for it to load
   - Generate the tarot card images
   - Save them to the `tarot_output` folder

## Individual Steps (if the one-step solution fails)

### Step 1: Install Dependencies (if needed)

1. Run `direct_install_dependencies.bat`
2. This will install pytorch_lightning and other required dependencies

### Step 2: Start Automatic1111

1. Run `direct_start_a1111.bat`
2. This will start Automatic1111 with the API enabled
3. Wait for it to fully load (wait until you see the web UI in your browser)

### Step 3: Generate Tarot Cards

1. Run `generate_tarot_simple.bat`
2. This will generate the tarot card images and save them to the `tarot_output` folder

## Manual Approach (if all else fails)

If the scripts above don't work, try this manual approach:

1. Open a command prompt
2. Navigate to your Automatic1111 installation:
   ```
   cd C:\Users\kjfsw\stable-diffusion-webui
   ```
3. Activate the virtual environment (if it exists):
   ```
   call venv\Scripts\activate.bat
   ```
4. Start Automatic1111 with API enabled:
   ```
   python webui.py --api --listen
   ```
5. Wait for Automatic1111 to fully load
6. Open another command prompt
7. Navigate to your sd-scripts directory:
   ```
   cd C:\Users\kjfsw\sd-scripts
   ```
8. Run the tarot card generation script:
   ```
   python generate_tarot_api.py --lora "fool_hypernetwork"
   ```

## Troubleshooting

If you still encounter issues:

1. **Missing Dependencies**: Run `direct_install_dependencies.bat`

2. **API Connection Issues**: Make sure Automatic1111 is fully loaded before trying to generate images

3. **LoRA Model Issues**: Make sure your LoRA model is properly loaded in Automatic1111

4. **Port Issues**: If Automatic1111 is running on a different port, you can specify it:
   ```
   python generate_tarot_api.py --api-base "http://127.0.0.1:YOUR_PORT" --api-url "http://127.0.0.1:YOUR_PORT/sdapi/v1/txt2img"
   ```
