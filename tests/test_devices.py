from main import count_by_type, devices_to_rows, add_device, write_devices_csv, read_devices_csv, devices_on_floor
import copy
import os
import csv
import pathlib

fieldnames = ["id", "name", "type", "zone", "floor"]
devices_dict = {"1": {"name": "Manual Pull Station", "type": "Alarm", "zone": 2, "floor": 1}, "2": {"name": "Smoke Detector", "type": "Alarm", "zone": 1, "floor": 2}, "3": {"name": "Waterflow Switch", "type": "" , "zone": 3, "floor": 1}, "4":{"name": "Tamper Switch", "type": None, "zone": 1, "floor": 1}, "5": {"name": "CO detector", "zone": 4, "floor": 1}}
devices_dict_2 = {"1": {"name": "Manual Pull Station", "type": "Alarm", "zone": 2, "floor": 1}, "2": {"name": "Smoke Detector", "type": "Alarm", "zone": 1, "floor": 2}, "4":{"name": "Tamper Switch", "type": "Supervisory", "zone": None, "floor": 1}, "10": {"name": "CO detector", "zone": 4, "floor": 1}, "3": {"name": "Waterflow Switch", "type": "Alarm" , "zone": 4, "floor": 1}}
devices_dict_3 = {"1": {"name": "Manual Pull Station", "type": "Alarm", "zone": 2, "floor": 1}, "2": {"name": "Smoke Detector", "type": "Alarm", "zone": 1, "floor": 2}, "4":{"name": "Tamper Switch", "type": "Supervisory", "zone": 3, "floor": 1}, "10": {"name": "CO detector", "type": "Alarm", "zone": 4, "floor": 1}, "3": {"name": "Waterflow Switch", "type": "Alarm" , "zone": 4, "floor": 1}}
devices_dict_floors = {"1": {"name": "Manual Pull Station", "type": "Alarm", "zone": 2, "floor": 1}, "2": {"name": "Smoke Detector", "type": "Alarm", "zone": 1, "floor": 2}, "4":{"name": "Tamper Switch", "type": "Supervisory", "zone": 3, "floor": 1}, "10": {"name": "CO detector", "type": "Alarm", "zone": 4, "floor": 1}, "3": {"name": "Waterflow Switch", "type": "Alarm" , "zone": 4}}
csv_txt = """id,name,type,zone,floor
1,Smoke Detector,Alarm,2,1
2,CO Detector,Supervisory,x,1
3,Manual Pull Station,Alarm,2,1"""


def test_answer_count_by_type():
    assert count_by_type(devices_dict) == {"Alarm": 2, None: 2, "": 1}

# Prediction devices_to_rows returns [{"id": 2 "name": "Smoke Detector", "type": "Alarm", "zone": 1, "floor": 2}, {"id": "1", "name": "Manual Pull Station", "type": "Alarm", "zone": 2, "floor": 1}, , {"id": 10, "name": "CO detector", "zone": 4, "floor": 1}, {"id": 3, "name": "Waterflow Switch", "type": "Alarm" , "zone": 4, "floor": 1}, {"id": 4, "name": "Tamper Switch", "type": "Supervisory", "zone": None, "floor": 1}]
#The above prediction was wrong.

def test_answer_devices_to_rows_order():
    assert devices_to_rows(devices_dict_2) == [{"id": "2", "name": "Smoke Detector", "type": "Alarm", "zone": 1, "floor": 2}, {"id": "1", "name": "Manual Pull Station", "type": "Alarm", "zone": 2, "floor": 1}, {"id": "3", "name": "Waterflow Switch", "type": "Alarm" , "zone": 4, "floor": 1}, {"id": "10", "name": "CO detector", "type": None, "zone": 4, "floor": 1}, {"id": "4", "name": "Tamper Switch", "type": "Supervisory", "zone": None, "floor": 1}]

#Prediction -> I predict this will pass because we previously checked for this in main.py main(). In order to break this function we need it to modify an input dict. To do this we change a value in device_properties in the devices_to_rows function
devices_dict_2_copy = copy.deepcopy(devices_dict_2)
def test_answer_devices_to_rows_input_unchanged():
    devices_to_rows(devices_dict_2)
    assert devices_dict_2 == devices_dict_2_copy

#Prediction -> I predict this will pass because our logic in add_device() will return the new dict with the added device.
def test_answer_add_device_in_result():
    add_d_result = add_device(devices_dict, "11", {'name': 'Elevator Smoke Detector', 'type': 'Alarm', 'zone':3, 'floor':2})
    assert len(add_d_result) == len(devices_dict) + 1
    add_d_result['1']['zone'] = 3
    assert add_d_result["11"] == {'name': 'Elevator Smoke Detector', 'type': 'Alarm', 'zone':3, 'floor':2}
    assert devices_dict['1']['zone'] == 2
    
devices_dict_copy = copy.deepcopy(devices_dict)
#Prediction -> I predict this will pass because we use copy.deepcopy() within the add device function.
def test_answer_add_device_dict_unchanged():
    dd_copy = copy.deepcopy(devices_dict)
    add_device(dd_copy, "11", {'name': 'Elevator Smoke Detector', 'type': 'Alarm', 'zone':3, 'floor':2})
    assert dd_copy == devices_dict_copy

#Prediction -> I predict this will pass because we use .copy() for the new_device in add_device()
def test_answer_add_device_result_unchanged():
    new_device = {'name': 'Elevator Smoke Detector', 'type': 'Alarm', 'zone':3, 'floor':2}
    new_dict_device = add_device(devices_dict, "11", new_device)
    new_device['zone'] = 9
    assert new_dict_device['11']['zone'] == 3

#Prediction -> I believe the assert will pass because we are taking the data transforming it into a list of dictionaries with id: field. Then, we are writing those to a csv file, then reading those back while converting them to the original data shape 
def test_answer_csv_round_trip(tmp_path):
    d = tmp_path / "csv"
    d.mkdir()
    p = d / "tmp.csv"
    loaded_devices = devices_to_rows(devices_dict_3)
    write_devices_csv(loaded_devices, p)          
    assert read_devices_csv(p) == devices_dict_3

#Predicton -> This will pass. read_devices_csv() will skip the bad zone in csv_txt.    
def test_answer_csv_read_bad_row(tmp_path):
    d = tmp_path/"txt"
    d.mkdir()
    p = d / "tmp.csv"
    p.write_text(csv_txt)
    assert read_devices_csv(p) == {"1":{"name":"Smoke Detector", "type":"Alarm", "zone":2, "floor":1}, "3":{"name":"Manual Pull Station", "type":"Alarm", "zone":2, "floor":1}}

#Prediction -> I write_devices_csv() will attempt to write to a folder in a path but because the folder does not exist it will return False
def test_answer_csv_failed_write(tmp_path):
    d = tmp_path
    loaded_devices = devices_to_rows(devices_dict_3)
    assert write_devices_csv(loaded_devices, d/"Folder"/"file.csv") == False

#Expected value from devices_dict_floors should be [1,4,10] when sorted by integers.
def test_answer_devices_on_floor():
    assert devices_on_floor(devices_dict_floors, 1) == [1,4,10]



    
    

