This script loads a json file and counts by type.

###Running the script###
uv run main.py

###Data Shape###

Data shape was updated to be keyed by id numbers. JSON cannot have keys be integers so the number is a string currently. This is okay because we never need to do math with the actual number the id represents.

It does look like we may have a problem in identifying duplicate keys. JSON load will just overwrite the key data with the latest one. So if you have 2 identical keys only the second key data is loaded.

###Missing Types###

Missing types are included when using the count_by_type() function. This is to provide clarity on the data that is being processed by the function. 
Output: {'Alarm': 3, 'Supervisory': 3, None: 2, 'Trouble': 2}  -The None key represents missing types in the data.