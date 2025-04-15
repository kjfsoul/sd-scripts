import requests
import sys
import time

def check_api(url="http://127.0.0.1:7860", max_retries=5, retry_delay=2):
    """Check if the Automatic1111 API is accessible"""
    print(f"Checking if Automatic1111 API is running at {url}...")

    for i in range(max_retries):
        try:
            response = requests.get(f"{url}/sdapi/v1/sd-models", timeout=5)
            if response.status_code == 200:
                print("✓ Automatic1111 API is running and accessible!")
                return True
            else:
                print(f"✗ API responded with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Attempt {i+1}/{max_retries}: Could not connect to API: {e}")

        if i < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    print("\nThe Automatic1111 API is not accessible. Please make sure:")
    print("1. Automatic1111 is running")
    print("2. It was started with the --api flag")
    print("3. It's running on the default port (7860)")
    print("\nTo start Automatic1111 with the API enabled, run:")
    print("python webui.py --api")
    print("\nIf it's running on a different port, you can specify it with:")
    print("python check_a1111_api.py http://127.0.0.1:YOUR_PORT")

    return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:7860"
    success = check_api(url)
    sys.exit(0 if success else 1)
