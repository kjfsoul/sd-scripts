import requests
import time
import sys

def test_api(url="http://127.0.0.1:7860", endpoints=None, max_retries=5, retry_delay=2):
    """Test if the Automatic1111 API is accessible"""
    if endpoints is None:
        endpoints = [
            "/sdapi/v1/sd-models",
            "/sdapi/v1/samplers",
            "/sdapi/v1/upscalers",
            "/sdapi/v1/loras"
        ]
    
    print(f"Testing Automatic1111 API at {url}...")
    print(f"Will try {len(endpoints)} endpoints with {max_retries} retries each.")
    print()
    
    all_success = True
    
    for endpoint in endpoints:
        endpoint_url = f"{url}{endpoint}"
        print(f"Testing endpoint: {endpoint_url}")
        
        success = False
        for i in range(max_retries):
            try:
                print(f"  Attempt {i+1}/{max_retries}... ", end="", flush=True)
                response = requests.get(endpoint_url, timeout=10)
                if response.status_code == 200:
                    print(f"SUCCESS (Status: {response.status_code})")
                    print(f"  Response contains {len(response.json())} items")
                    success = True
                    break
                else:
                    print(f"FAILED (Status: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"ERROR: {str(e)}")
            
            if i < max_retries - 1:
                print(f"  Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        
        if not success:
            all_success = False
            print(f"  Failed to access {endpoint_url} after {max_retries} attempts")
        
        print()
    
    if all_success:
        print("All API endpoints are accessible!")
        return True
    else:
        print("Some API endpoints are not accessible.")
        print("\nPossible issues:")
        print("1. Automatic1111 is not running with the API enabled")
        print("2. The API is running on a different port")
        print("3. There's a network issue preventing access to the API")
        print("\nSuggestions:")
        print("1. Make sure Automatic1111 is running with the --api flag")
        print("2. Check if there are any error messages in the Automatic1111 console")
        print("3. Try accessing http://127.0.0.1:7860/docs in your browser")
        return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:7860"
    success = test_api(url)
    sys.exit(0 if success else 1)
