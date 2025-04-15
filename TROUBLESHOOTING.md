# Troubleshooting Guide for Tarot Creator 1111

If you're experiencing issues with the Tarot Creator 1111 tool, this guide will help you diagnose and fix common problems.

## 500 Server Errors

If you're seeing 500 server errors when trying to generate images, this typically indicates a problem with the Automatic1111 API. Here are some possible causes and solutions:

### 1. API Not Enabled

**Symptoms**: Cannot connect to the API at all.

**Solution**:
- Make sure Automatic1111 is running
- Ensure the API is enabled by adding `--api` to the `COMMANDLINE_ARGS` in your `webui-user.bat` file
- Restart Automatic1111

### 2. Model Loading Issues

**Symptoms**: API connects but image generation fails with 500 errors.

**Solution**:
- Wait a few minutes after starting Automatic1111 to ensure the model is fully loaded
- Check the Automatic1111 console for any error messages
- Try using a different model if available

### 3. Resource Limitations

**Symptoms**: Image generation starts but fails with out-of-memory errors.

**Solution**:
- Reduce the image size (width and height)
- Reduce the number of steps
- Use a more efficient sampler like "Euler a"
- Close other applications to free up memory

### 4. Prompt Issues

**Symptoms**: Only certain prompts fail with 500 errors.

**Solution**:
- Simplify your prompts
- Avoid using too many style keywords
- Remove any potentially problematic terms

## Diagnostic Tools

We've provided several diagnostic tools to help you troubleshoot issues:

### 1. Check API Connection

Run `check_api.bat` to verify that the Automatic1111 API is accessible.

### 2. Detailed API Diagnosis

Run `diagnose_api.bat` for a more comprehensive check of the API, including:
- Testing basic connectivity
- Listing available models and samplers
- Testing image generation with minimal settings

### 3. Simplified Generator

If the main generator is failing, try `simple_generator.bat` which uses:
- Reduced image size
- Fewer generation steps
- Simpler prompts
- More error handling

## Common Error Messages

### "Could not connect to API"

This means the script cannot reach the Automatic1111 API. Make sure:
- Automatic1111 is running
- The API is enabled
- The correct port is being used (default is 7860)

### "Error generating image"

This could be due to:
- Insufficient resources (VRAM/RAM)
- Issues with the prompt
- Problems with the model

### "ModuleNotFoundError"

This means a required Python package is missing. Run:
```
pip install requests Pillow
```

## Still Having Issues?

If you're still experiencing problems after trying these solutions:

1. Check the Automatic1111 logs for any error messages
2. Try restarting your computer
3. Reinstall Automatic1111
4. Try a different model or sampler

For more help, please refer to the Automatic1111 documentation or community forums.
