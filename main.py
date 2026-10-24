from pathlib import Path
import json

d_path = f"{Path(__file__).resolve().parent}/devices.json"

def load_devices(path):
    try:
        with open(path) as devices: 
            d_load = json.load(devices)      
    except(FileNotFoundError):
        print(f"Could not find devices file: {path}")
        return []
    else:
        print(len(d_load))
        return d_load
        




def main():  
    print(load_devices(d_path))
    


if __name__ == "__main__":
    main()
