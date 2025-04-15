#!/usr/bin/env python3
"""
Diagnostic tool for Automatic1111 API
"""

import requests
import json
import sys
import time

def test_api_endpoint(url, endpoint, method="GET", data=None, description=None):
    """Test a specific API endpoint"""
    full_url = f"{url}{endpoint}"
    if description:
        print(f"Testing {description}...")
    else:
        print(f"Testing endpoint: {full_url}")
    
    try:
        if method == "GET":
            response = requests.get(full_url, timeout=10)
        elif method == "POST":
            headers = {"Content-Type": "application/json"}
            response = requests.post(full_url, json=data, headers=headers, timeout=30)
        else:
            print(f"Unsupported method: {method}")
            return False
        
        if response.status_code == 200:
            print(f"✓ Success! Status code: {response.status_code}")
            return True
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            print(f"Response: {response.text[:500]}...")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_txt2img(url, minimal=False):
    """Test the txt2img endpoint with a minimal payload"""
    endpoint = "/sdapi/v1/txt2img"
    
    if minimal:
        # Minimal payload to test basic functionality
        payload = {
            "prompt": "test",
            "steps": 2,  # Minimum steps for quick test
            "width": 64,  # Small image for quick test
            "height": 64,  # Small image for quick test
            "cfg_scale": 7,
            "sampler_name": "Euler a"
        }
    else:
        # Standard payload
        payload = {
            "prompt": "a simple landscape, test image",
            "negative_prompt": "blurry, bad",
            "steps": 20,
            "width": 512,
            "height": 512,
            "cfg_scale": 7,
            "sampler_name": "Euler a"
        }
    
    print("\nTesting image generation with minimal settings...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    start_time = time.time()
    result = test_api_endpoint(url, endpoint, "POST", payload, "txt2img API")
    end_time = time.time()
    
    if result:
        print(f"Image generation completed in {end_time - start_time:.2f} seconds")
    
    return result

def get_available_models(url):
    """Get list of available models"""
    endpoint = "/sdapi/v1/sd-models"
    print("\nGetting available models...")
    
    try:
        response = requests.get(f"{url}{endpoint}", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"Found {len(models)} models:")
            for i, model in enumerate(models):
                print(f"  {i+1}. {model.get('title', 'Unknown')}")
            return True
        else:
            print(f"Failed to get models. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error getting models: {str(e)}")
        return False

def get_available_samplers(url):
    """Get list of available samplers"""
    endpoint = "/sdapi/v1/samplers"
    print("\nGetting available samplers...")
    
    try:
        response = requests.get(f"{url}{endpoint}", timeout=10)
        if response.status_code == 200:
            samplers = response.json()
            print(f"Found {len(samplers)} samplers:")
            for i, sampler in enumerate(samplers):
                print(f"  {i+1}. {sampler.get('name', 'Unknown')}")
            return True
        else:
            print(f"Failed to get samplers. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error getting samplers: {str(e)}")
        return False

def main():
    """Main function"""
    api_url = "http://127.0.0.1:7860"
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    
    print(f"Diagnosing Automatic1111 API at {api_url}")
    print("=" * 50)
    
    # Test basic connectivity
    print("\nTesting basic API connectivity...")
    if not test_api_endpoint(api_url, "/sdapi/v1/sd-models", description="API connectivity"):
        print("\nCannot connect to the API. Please make sure:")
        print("1. Automatic1111 is running")
        print("2. It was started with the --api flag")
        print("3. It's running on the correct port (default: 7860)")
        return
    
    # Get available models
    get_available_models(api_url)
    
    # Get available samplers
    get_available_samplers(api_url)
    
    # Test txt2img with minimal settings
    test_txt2img(api_url, minimal=True)
    
    # Test txt2img with standard settings
    test_txt2img(api_url, minimal=False)
    
    print("\nDiagnostic complete!")

if __name__ == "__main__":
    main()
