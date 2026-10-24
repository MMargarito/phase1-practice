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
        return d_load
        

def count_by_type(json_file):
    type_count = {}
    for value in json_file.values():
        
        if value['type'] in type_count:
            type_count[value['type']] += 1
        else:
            type_count[value['type']] = 1

    return type_count


        
loaded_devices = load_devices(d_path)

def main():
    print(loaded_devices)
    print(len(loaded_devices))
    print(count_by_type(loaded_devices))


if __name__ == "__main__":
    main()
