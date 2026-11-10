from pathlib import Path
import json
import copy
import csv

d_path = f"{Path(__file__).resolve().parent}/devices.json"
csv_path = f"{Path(__file__).resolve().parent}/devices.csv"


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
    new_device = device.copy()
    
    if str(device_id) in loaded_devices:
        print(f'Dictionary unchanged \nDevice id {device_id} is already assigned. Please choose an unassigned id')
        return new_dict

    else:
        new_dict[str(device_id)] = new_device

    return new_dict

def devices_to_rows(devices):
    prop_list = ["id", "name", "type", "zone", "floor"]
    new_list = []

    for device_id, device_properties in devices.items():
        new_dict = {"id": device_id}
        for prop in prop_list:
            if prop != "id":
                new_dict[prop] = device_properties.get(prop)
        
        new_list.append(new_dict)

    sorted_list = sorted(new_list, key=lambda  x:(x.get('zone') is None, x.get('zone') if x.get('zone') is not None else 0, int(x.get('id'))))
                                               

    return sorted_list

def write_devices_csv(devices, path):

    try:
        with open(path, mode='w', newline='') as csvfile:
            fieldnames = ["id", "name", "type", "zone", "floor"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for device in devices:
                writer.writerow(device)
    except FileNotFoundError:
        print(f"Could not find csv file: {path}")
        return f"Devices not written to file: {path}"

    return "Devices successfully written to file."

 
def main():
    loaded_devices = load_devices(d_path)
    counted_types = count_by_type(loaded_devices)
    grouped_zones = group_by_zone(loaded_devices)
    new_device_dict = add_device(loaded_devices, "11", {'name': 'Elevator Smoke Detector', 'type': 'Alarm', 'zone':3, 'floor':2})
    sorted_devices = devices_to_rows(loaded_devices)

    #sharing test
    new_device_dict['1']['zone'] = 9
    print(f'Are the original and copied dictionaries the same: {loaded_devices == new_device_dict}')
    
    #grouped_zones test
    print(grouped_zones)
    value_count = 0
    for values in grouped_zones.values():
        value_count += len(values)
    print(f'Does grouped_zones group all zones? {value_count == len(loaded_devices)}')

    
    #length of loaded_devices test
    print(len(loaded_devices))
    print(counted_types)
    print(f'Does counted_types count all types: {sum(counted_types.values()) == len(loaded_devices)}')

    #devices_to_rows test
    # print(loaded_devices)
    before = copy.deepcopy(loaded_devices)
    devices_to_rows(loaded_devices)
    after = loaded_devices
    print(f'Is loaded_devices unchanged? {before == after}')
    print(len(devices_to_rows(loaded_devices)))
    #Check to make sure loaded_devices is unchanged when passing through devices_to_rows
    # print(loaded_devices)
    
    #Testing write_devices_csv
    print(write_devices_csv(sorted_devices, csv_path))

if __name__ == "__main__":
    main()
