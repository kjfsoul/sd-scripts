# Tarot Card Generation with Automatic1111 API

This is a simplified approach to generate tarot card images using the Automatic1111 API.

## Simplified Workflow

1. Run `generate_tarot_simple.bat`
2. The script will check if Automatic1111 API is running
3. If not, it will offer to start it for you
4. Once the API is available, it will generate the tarot card images
5. Images will be saved to the `tarot_output` folder

## Detailed Steps

### Step 0: Install Dependencies (If Needed)

If you encounter errors about missing modules when starting Automatic1111:

1. Run `install_a1111_dependencies.bat`
2. Enter the full path to your Automatic1111 installation when prompted
3. Wait for the dependencies to install

### Step 1: Start Automatic1111 with API Enabled

1. Run `start_a1111_api.bat`
2. Enter the full path to your Automatic1111 installation when prompted
3. Wait for Automatic1111 to fully load (wait until you see the web UI in your browser)

### Step 2: Check API Availability

1. Run `check_a1111_api.bat`
2. This will verify that the Automatic1111 API is running and accessible

### Step 3: Generate Tarot Card Images

1. Run `generate_tarot_simple.bat`
2. The script will generate 6 tarot card images (3 cards with 2 variations each)
3. Images will be saved to the `tarot_output` folder

## Troubleshooting

If you encounter any issues:

1. **Missing Dependencies**: If you see errors about missing modules (like `pytorch_lightning`), run `install_a1111_dependencies.bat`

2. **API Connection Issues**:
   - Make sure Automatic1111 is running with the API enabled
   - You should see a message in the Automatic1111 console that says "Running on local URL: http://127.0.0.1:7860"
   - Try adding the `--listen` flag when starting Automatic1111 to make it accessible from other processes

3. **LoRA Model Issues**: Check that your LoRA model is properly loaded in Automatic1111

4. **General Errors**: Try restarting Automatic1111 and running the generation script again

## Manual Start (Alternative)

If the automatic start doesn't work, you can manually start Automatic1111 with the API enabled:

1. Navigate to your Automatic1111 installation directory
2. Run one of these commands:
   - `python webui.py --api --listen`
   - `python launch.py --api --listen`
3. Wait for Automatic1111 to fully load
4. Run `generate_tarot_simple.bat` to generate the images
