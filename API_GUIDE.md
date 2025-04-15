# Using the Automatic1111 API for Tarot Card Generation

This guide explains how to use the API script to automatically generate tarot card images.

## Step 1: Start Automatic1111 with API Enabled

You need to start Automatic1111 with the API enabled. There are two ways to do this:

### Option 1: Modify your existing webui-user.bat file
Add the `--api` flag to your COMMANDLINE_ARGS in the webui-user.bat file:

```batch
set COMMANDLINE_ARGS=--xformers --api
```

### Option 2: Create a new batch file to start with API
Create a file named `start_with_api.bat` with the following content:

```batch
@echo off
call webui-user.bat --api
```

## Step 2: Run the API Script

Once Automatic1111 is running with the API enabled, you can run the script to generate the tarot cards:

1. Double-click on `generate_tarot_api.bat`
2. The script will connect to Automatic1111 and generate all the tarot card variations
3. Images will be saved to the `tarot_output` folder

## Troubleshooting

- If you get connection errors, make sure Automatic1111 is running and the API is enabled
- The default API URL is `http://127.0.0.1:7860/sdapi/v1/txt2img`. If your Automatic1111 is running on a different port, you can specify it with the `--api-url` parameter
- If you want to generate only specific cards, you can use the `--cards` parameter, e.g., `python generate_tarot_api.py --cards "Fool" "Star"`

## Customizing

You can customize the generation settings by editing the `generate_tarot_api.py` file. Look for the `payload` dictionary in the `generate_image` function to change parameters like steps, CFG scale, etc.
