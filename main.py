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
        key = value.get('type')

        if key in type_count:
            type_count[key] += 1
        else:
            type_count[key] = 1

    return type_count

def group_by_zone(loaded_devices):
    zone_group = {}

    for i in loaded_devices.items():

        key = i[1].get('zone')
        zone_group.setdefault(key, []).append(i[0])

    return zone_group


def main():
    loaded_devices = load_devices(d_path)
    counted_types = count_by_type(loaded_devices)
    grouped_zones = group_by_zone(loaded_devices)
    print(grouped_zones)
    value_count = 0
    for values in grouped_zones.values():
        value_count += len(values)
    print(value_count)
    # print(loaded_devices)
    # print(len(loaded_devices))
    # print(counted_types)
    # print(sum(counted_types.values()) == len(loaded_devices))


if __name__ == "__main__":
    main()
