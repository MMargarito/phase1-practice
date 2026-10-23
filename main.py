from pathlib import Path
import json

fp = Path(__file__).resolve().parent

def load_devices(path):
    path = f"{fp}/devices.json"
    try:
        with open(path, newline='') as devices: 
            d_load = json.load(devices)      
    except(FileNotFoundError):
        print(f"Could not find devices file: {path}")
        
    else:
        return d_load
        




def main():  
    print(load_devices(fp))


if __name__ == "__main__":
    main()
