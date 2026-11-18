from main import count_by_type, devices_to_rows
import copy

devices_dict = {"1": {"name": "Manual Pull Station", "type": "Alarm", "zone": 2, "floor": 1}, "2": {"name": "Smoke Detector", "type": "Alarm", "zone": 1, "floor": 2}, "3": {"name": "Waterflow Switch", "type": "" , "zone": 3, "floor": 1}, "4":{"name": "Tamper Switch", "type": None, "zone": 1, "floor": 1}, "5": {"name": "CO detector", "zone": 4, "floor": 1}}
devices_dict_2 = {"1": {"name": "Manual Pull Station", "type": "Alarm", "zone": 2, "floor": 1}, "2": {"name": "Smoke Detector", "type": "Alarm", "zone": 1, "floor": 2}, "4":{"name": "Tamper Switch", "type": "Supervisory", "zone": None, "floor": 1}, "10": {"name": "CO detector", "zone": 4, "floor": 1}, "3": {"name": "Waterflow Switch", "type": "Alarm" , "zone": 4, "floor": 1}}

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
