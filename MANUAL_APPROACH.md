# Manual Approach for Tarot Card Generation

If you're having trouble with the automated scripts, try this manual approach.

## Step 1: Diagnose Your Automatic1111 Installation

1. Run `diagnose_a1111.bat`
2. This will check your Automatic1111 installation and provide diagnostic information
3. Review the output to identify any issues

## Step 2: Manually Start Automatic1111

1. Run `manual_start_a1111.bat`
2. This will start Automatic1111 with the API enabled in the current window
3. **Important**: Keep this window open while generating images
4. Wait for Automatic1111 to fully load (you should see "Running on local URL: http://127.0.0.1:7860" in the console)

## Step 3: Manually Generate Tarot Cards

1. Open a new command prompt window
2. Navigate to your sd-scripts directory
3. Run `manual_generate_tarot.bat`
4. This will check if the API is accessible and then generate the tarot card images

## Troubleshooting

If you encounter errors when starting Automatic1111:

1. **Missing Dependencies**: Note the specific error message and install the missing dependency:
   ```
   pip install [missing_dependency]
   ```

2. **Path Issues**: Make sure the path to your Automatic1111 installation is correct:
   ```
   C:\Users\kjfsw\stable-diffusion-webui
   ```

3. **Python Issues**: Make sure Python is installed and in your PATH

4. **API Connection Issues**: Make sure Automatic1111 is fully loaded before trying to generate images

## Complete Manual Approach (if all else fails)

If the scripts above don't work, try these manual commands:

1. Open a command prompt
2. Navigate to your Automatic1111 installation:
   ```
   cd C:\Users\kjfsw\stable-diffusion-webui
   ```
3. Start Automatic1111 with API enabled:
   ```
   python webui.py --api --listen
   ```
4. Wait for Automatic1111 to fully load
5. Open another command prompt
6. Navigate to your sd-scripts directory:
   ```
   cd C:\Users\kjfsw\sd-scripts
   ```
7. Run the tarot card generation script:
   ```
   python generate_tarot_api.py --lora "fool_hypernetwork"
   ```
