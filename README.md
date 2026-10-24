This script loads a json file and counts by type.

###Running the script###
uv run main.py

###Data Shape###

Data shape was updated to be keyed by id numbers. JSON cannot have keys be integers so the number is a string currently. This is okay because we never need to do math with the actual number the id represents.

It does look like we may have a problem in identifying duplicate keys. JSON load will just overwrite the key data with the latest one. So if you have 2 identical keys only the second key data is loaded.