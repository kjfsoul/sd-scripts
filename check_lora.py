import requests
import sys
import json

def check_lora(url="http://127.0.0.1:7860", lora_name="fool_hypernetwork"):
    """Check if a specific LoRA model is available in Automatic1111"""
    print(f"Checking if LoRA model '{lora_name}' is available...")
    
    try:
        # Get list of available LoRA models
        response = requests.get(f"{url}/sdapi/v1/loras", timeout=10)
        response.raise_for_status()
        
        loras = response.json()
        
        print(f"Found {len(loras)} LoRA models:")
        for lora in loras:
            print(f"  - {lora.get('name', 'Unknown')} ({lora.get('alias', 'No alias')})")
        
        # Check if our LoRA model is in the list
        found = False
        for lora in loras:
            if lora.get('name') == lora_name or lora.get('alias') == lora_name:
                print(f"\nFound LoRA model '{lora_name}'!")
                print(f"Details: {json.dumps(lora, indent=2)}")
                found = True
                break
        
        if not found:
            print(f"\nLoRA model '{lora_name}' not found!")
            print("Please make sure the LoRA model is properly loaded in Automatic1111.")
            print("You might need to:")
            print("1. Check if the LoRA file exists in the correct directory")
            print("2. Refresh the LoRA models in Automatic1111")
            print("3. Use a different name for the LoRA model in your generation script")
        
        return found
    
    except Exception as e:
        print(f"Error checking LoRA models: {e}")
        return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:7860"
    lora_name = sys.argv[2] if len(sys.argv) > 2 else "fool_hypernetwork"
    success = check_lora(url, lora_name)
    sys.exit(0 if success else 1)
