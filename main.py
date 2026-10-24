from pathlib import Path
import json

d_path = f"{Path(__file__).resolve().parent}/devices.json"

def load_devices(path):
    try:
        with open(path) as devices: 
            d_load = json.load(devices)      
    except(FileNotFoundError):
        print(f"Could not find devices file: {path}")
        return {}
    else:
        return d_load
        

def count_by_type(json_file):
    type_count = {}
    for value in json_file.values():

        if value.get('type', None) in type_count:
            type_count[value.get('type', None)] += 1
        else:
            type_count[value.get('type', None)] = 1

    return type_count


def main():
    loaded_devices = load_devices(d_path)
    counted_types = count_by_type(loaded_devices)
    print(loaded_devices)
    print(len(loaded_devices))
    print(counted_types)
    print(sum(counted_types.values()) == len(loaded_devices))


if __name__ == "__main__":
    main()
