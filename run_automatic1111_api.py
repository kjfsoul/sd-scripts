import os
import sys
import subprocess
import time
import argparse

def find_python_executable():
    """Find a suitable Python executable"""
    # Try the system Python first
    try:
        subprocess.run(["python", "--version"], check=True, capture_output=True)
        return "python"
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    # Try python3
    try:
        subprocess.run(["python3", "--version"], check=True, capture_output=True)
        return "python3"
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    # Check if there's a venv in the current directory
    if os.path.exists("venv"):
        if os.path.exists(os.path.join("venv", "Scripts", "python.exe")):
            return os.path.join("venv", "Scripts", "python.exe")
        elif os.path.exists(os.path.join("venv", "bin", "python")):
            return os.path.join("venv", "bin", "python")
    
    print("Could not find a suitable Python executable.")
    return None

def run_automatic1111(sd_path, api_only=False):
    """Run Automatic1111 with API enabled"""
    python_exe = find_python_executable()
    if not python_exe:
        return False
    
    # Check what files exist in the SD path
    has_launch_py = os.path.exists(os.path.join(sd_path, "launch.py"))
    has_webui_py = os.path.exists(os.path.join(sd_path, "webui.py"))
    
    cmd = []
    
    if has_launch_py:
        cmd = [python_exe, "launch.py", "--api"]
    elif has_webui_py:
        cmd = [python_exe, "webui.py", "--api"]
    else:
        print(f"Could not find launch.py or webui.py in {sd_path}")
        return False
    
    if api_only:
        cmd.append("--nowebui")
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(cmd, cwd=sd_path)
        print(f"Started Automatic1111 with process ID: {process.pid}")
        print("Waiting for the API to become available...")
        
        # Wait for the API to become available
        for _ in range(30):  # Wait up to 30 seconds
            time.sleep(1)
            try:
                import requests
                response = requests.get("http://127.0.0.1:7860/sdapi/v1/sd-models")
                if response.status_code == 200:
                    print("API is now available!")
                    return True
            except:
                pass
        
        print("API did not become available within the timeout period.")
        return False
    
    except Exception as e:
        print(f"Error starting Automatic1111: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run Automatic1111 with API enabled")
    parser.add_argument("--path", type=str, help="Path to Automatic1111 installation")
    parser.add_argument("--api-only", action="store_true", help="Run API only (no web UI)")
    
    args = parser.parse_args()
    
    sd_path = args.path
    if not sd_path:
        sd_path = input("Enter the path to your Automatic1111 installation: ")
    
    if not os.path.exists(sd_path):
        print(f"The path {sd_path} does not exist.")
        return
    
    success = run_automatic1111(sd_path, args.api_only)
    if success:
        print("Automatic1111 is now running with API enabled.")
        print("You can now run generate_tarot_api.py to generate tarot card images.")
    else:
        print("Failed to start Automatic1111.")

if __name__ == "__main__":
    main()
