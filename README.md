# Project README

This repo holds two programs: `main.py` (contains devices) and `weather.py` (contains API call and weather-related material).

## Setup with `uv`

**Requirements:**
- Python 3.14 or newer
- `uv`
- `httpx` and `pytest`

If you already have a `pyproject.toml` in the repo, sync the environment:
```bash
uv sync
```

If you are setting up the environment from scratch:
```bash
uv init --python 3.14
uv add httpx
uv add --dev pytest
```

---

# `main.py`

This script loads a JSON file and counts devices by type.

### Running the script
```bash
uv run main.py
```

### Example Output
```text
Are the original and copied dictionaries the same: False
{4: ['1', '3'], 3: ['2', '4', '6'], 2: ['5', '7', '9'], 1: ['8'], None: ['10']}
True
10
{'Alarm': 3, 'Supervisory': 3, None: 2, 'Trouble': 2}
True
```

### Data Shape
Data shape was updated to be keyed by ID numbers. JSON cannot have keys be integers, so the number is a string currently. This is okay because we never need to do math with the actual number the ID represents.

It does look like we may have a problem in identifying duplicate keys. `json.load` will just overwrite the key data with the latest one. So if you have 2 identical keys, only the second key's data is loaded.

### Missing Types
Missing types are included when using the `count_by_type()` function. This is to provide clarity on the data that is being processed by the function.
- **Output:** `{'Alarm': 3, 'Supervisory': 3, None: 2, 'Trouble': 2}` — The `None` key represents missing types in the data as well as types that are explicitly `null`.

### Grouping by zones
Use the `group_by_zone` function to group devices by assigned zones. If a zone is `null` or a zone is missing, the group's key will be `None`.

### Duplicate-ID error handling
I chose to simply return a string saying that the dictionary is unchanged and return the unchanged dictionary. I didn't choose to raise an error here because no error is raised organically by Python if the ID is a duplicate—Python just overwrites the dictionary entry. I understand that there is the ability to raise an error anyway, though currently the user has no way of knowing if the dictionary changed successfully unless they read the screen.

### Converting ID entries into strings
I've decided to convert ID entries into strings rather than rejecting them outright because this allows non-strings like `None` to be treated as placeholders and changed later.

### Add Device
`add_device()` uses `.copy()` and `copy.deepcopy` to make copies of `device` (which is a dictionary) and the list of nested dictionaries to add a device to a new list without altering the inputs.

### Device to Rows
This function creates a new list of devices where their device ID is now a key-value pair in their respective dictionary. It also sorts the list by zone assignment in ascending order, where zones that have no value are placed at the end of the list.

### Write Device CSV
This takes a list of dictionaries and writes them to a CSV file. We are returning `True` or `False` for success or failure of writing to CSV. This is so a future function that relies on `write_device_csv()` will be able to pivot correctly based on its returned value.

### Read Device CSV
`read_devices_csv()` reads the device CSV file from the path. It converts all rows into `key: value` pairs where the keys are the IDs and the values are a dictionary of each device's properties. We convert all empty cells into `None` and `zone` and `floor` into `int`s. We catch `ValueError`s, and we are choosing to handle the exception by printing the row and the error. This allows for the rest of the file to be read, excluding the row with the error. Printing the row with the error allows the user to understand why the row was not read.

### Why `null` is used in `devices.json`
CSV can't tell a missing key from a `null`, so the data in `devices.json` uses `null` for "unknown".

---

### Pytest (`main.py`)

**How to run:**
```bash
uv run pytest
```

- **`test_answer_count_by_type()`**: This test takes in `devices_dict` and counts the amount of devices with the same type. A type with `None` or a type that is missing are treated separately.
- **`test_answer_devices_to_rows_order()`**: This test tests the `devices_to_rows()` function in `main.py`. It confirms that the function is returning the rows in ascending order, sorted by zone. Zones with `None` appear at the end of the list.
- **`test_answer_devices_to_rows_input_unchanged()`**: This test checks whether or not the original input is changed when passed through the `devices_to_rows()` function.
- **`test_answer_add_device_in_result()`**: This test checks if the device is included in the result returned by the function `add_device()` in `main.py`. It also checks to make sure the device was added completely, and that the function doesn't erase the data it's adding to.
- **`test_answer_add_device_dict_unchanged()`**: Checks that the `add_device()` function does not alter the original dict passed to it.
- **`test_answer_add_device_result_unchanged()`**: Checks to make sure changing the original device does not change the device stored in the dictionary.
- **`test_answer_csv_round_trip()`**: Checks to make sure `devices_dict` correctly goes through `devices_to_rows()` -> `write_devices_csv()` -> `read_devices_csv()`. The `devices_dict` should be the same as it was when it originally entered `devices_to_rows()`. This test also uses `tmp_path` to create a temporary directory that is specific to the test.
- **`test_answer_csv_failed_write()`**: This checks if `write_devices_csv()` correctly returns `False` when faced with a `FileNotFoundError`.
- **`test_answer_devices_on_floor()`**: This checks the `devices_on_floor()` function in `main.py`. It checks if the function is sorting the strings as integers, returning a blank list for floors with no devices, and ensuring the original data passed through the function remains unchanged.

---

# `weather.py`

This program uses `httpx` to fetch weather information for specific locations (sites) from a weather API called `open-meteo.com`. It then organizes the information into a CSV file called `site_weather.csv`.

In order to run the program, an internet connection is required (not required for tests).

### Running the script
```bash
uv run weather.py
```

### Running tests
```bash
uv run pytest tests/test_weather.py
```

### Example Output
```text
Bad request for site: London: Client error '400 Bad Request' for url 'https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=999&current=temperature_2m&current=wind_speed_10m'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400
3 succeeded, 1 failed
```
> **Note:** The London site is intended to fail. `3 succeeded, 1 failed` is the intended correct output.

### Example `sites.json`
```json
{
  "1": {"name": "New York", "latitude": 40.7128, "longitude": -74.006},
  "2": {"name": "Paris", "latitude": 48.8566, "longitude": 2.3522},
  "3": {"name": "London", "latitude": 51.5074, "longitude": 999},
  "4": {"name": "Tokyo", "latitude": 35.6762, "longitude": 139.6503}
}
```

### Testing

- **`test_weather_transform_normal()`**: This test the transform function with a normal complete data set called `parsed_data`.
- **`test_weather_transform_missing_current()`**: This test the transform function with a data set that is missing the `current` field from the data set `parsed_data`.
- **`test_weather_transform_missing_o_key()`**: This test the transform function with a data set that is missing the `temperature_2m` value from the `current` field from the data set `parsed_data`.


> **Note:** Please note that the tests do not make live network calls. Weather can change within the hour, so making live calls would be unpredictable and have a negative effect on automated testing. Instead, the tests check the transform function using a sample fetch response.
