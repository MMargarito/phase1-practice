from pathlib import Path
import json
import copy
import csv

d_path = f"{Path(__file__).resolve().parent}/devices.json"
csv_path = f"{Path(__file__).resolve().parent}/devices.csv"
#Names of headers for CSV file and names of keys in device dictionaries
fieldnames = ["id", "name", "type", "zone", "floor"]


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
    new_list = []

    for device_id, device_properties in devices.items():
        new_dict = {"id": device_id}
        for field in fieldnames:
            if field != "id":
                new_dict[field] = device_properties.get(field)
        
        new_list.append(new_dict)

    sorted_list = sorted(new_list, key=lambda  x:(x.get('zone') is None, x.get('zone') if x.get('zone') is not None else 0, int(x.get('id'))))
                                               

    return sorted_list

def write_devices_csv(devices, path):

    try:
        with open(path, mode='w', newline='') as csvfile:
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            written_row_count = 0
            for device in devices:
                writer.writerow(device)
                written_row_count += 1
            print(f"{written_row_count} rows written successfully")
            return True
    
    except FileNotFoundError:
        print(f"Error: The directory path for '{path}' is invalid or could not be found.")
        
    except (ValueError, TypeError) as e:
        print(f"Data structure error (check dictionary keys and row types): {e}")

    except OSError as e:
        print(f"Operating System Error: {e}")
        
    return False
    

 
def main():
    loaded_devices = load_devices(d_path)
    counted_types = count_by_type(loaded_devices)
    grouped_zones = group_by_zone(loaded_devices)
    new_device_dict = add_device(loaded_devices, "11", {'name': 'Elevator Smoke Detector', 'type': 'Alarm', 'zone':3, 'floor':2})
    

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

    #Check to make sure loaded_devices is unchanged when passing through devices_to_rows
    before = copy.deepcopy(loaded_devices)
    sorted_devices = devices_to_rows(loaded_devices)
    after = loaded_devices
    print(f'Is loaded_devices unchanged? {before == after}')
    # len(devices_to_rows(loaded_devices))
    
    #Testing write_devices_csv
    write_devices_csv(sorted_devices, csv_path)

if __name__ == "__main__":
    main()
