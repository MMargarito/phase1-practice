from pathlib import Path
import json
import copy

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

    for device_id, device_properties in loaded_devices.items():

        key = device_properties.get('zone')
        zone_group.setdefault(key, []).append(device_id)
    
    return zone_group

def add_device(loaded_devices, device_id, device):
    new_dict = copy.deepcopy(loaded_devices)
    
    if device_id in loaded_devices:
        return f'Dictionary unchanged - {loaded_devices} \nDevice id {device_id} is already assigned. Please choose an unassigned id'
    else:
        new_dict[str(device_id)] = device

    return new_dict




def main():
    loaded_devices = load_devices(d_path)
    counted_types = count_by_type(loaded_devices)
    grouped_zones = group_by_zone(loaded_devices)
    new_device_dict = add_device(loaded_devices, "11", {'name': {'Elevator Smoke Detector'}, 'type': {'Alarm'}, 'zone':{3}, 'floor':{2}})

    #sharing test
    new_device_dict['1']['zone'] = 9
    print('Original Dict')
    print(loaded_devices)
    print('-')
    print('Changed new Dict')
    print(new_device_dict)
    print('-')
    print('Orgininal Dict')
    print(loaded_devices)
    
    #grouped_zones test
    print(grouped_zones)
    value_count = 0
    for values in grouped_zones.values():
        value_count += len(values)
    print(value_count == len(loaded_devices))

    
    #length of loaded_devices test
    print(len(loaded_devices))
    print(counted_types)
    print(sum(counted_types.values()) == len(loaded_devices))


if __name__ == "__main__":
    main()
