from pathlib import Path
import json

fp = Path(__file__).resolve().parent

def load_devices(path):
    full_path = f"{path}/devices.json"
    try:
        with open(full_path, newline='') as devices: 
            d_load = json.load(devices)      
    except(FileNotFoundError):
        print(f"Could not find devices file: {path}")
        
    else:
        return d_load
        




def main():  
    print(load_devices(fp))


if __name__ == "__main__":
    main()
