from pathlib import Path
import json

fp = Path(__file__).resolve().parent

def load_devices(path):
    try:
        with open(f"{path}/devices.json") as devices: 
            d_load = json.load(devices)      
    except(FileNotFoundError):
        print(f"Could not find devices file: {path}")
        return []
    else:
        print(len(d_load))
        return d_load
        




def main():  
    print(load_devices(fp))
    


if __name__ == "__main__":
    main()
