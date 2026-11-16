from main import count_by_type

devices_dict = {"1": {"name": "Manual Pull Station", "type": "Alarm", "zone": 2, "floor": 1}, "2": {"name": "Smoke Detector", "type": "Alarm", "zone": 1, "floor": 2}, "3": {"name": "Waterflow Switch", "type": "" , "zone": 3, "floor": 1}, "4":{"name": "Tamper Switch", "type": None, "zone": 1, "floor": 1}, "5": {"name": "CO detector", "zone": 4, "floor": 1}}

def test_answer_count_by_type():
    assert count_by_type(devices_dict) == {"Alarm": 2, None: 2, "": 1}

