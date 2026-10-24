This script loads a json file and counts by type.

###Running the script###
uv run main.py

###Data Shape###
I am aware that the current shape of the data can make finding id errors more difficult. I also understand that this implies their is a unique name for each device. If we had multiple smoke detectors the data's shape would need to change. I may change it so the keys are the ids. This makes more sense because the ids should be unique and devices on a full project will share names. 

Data shape was updated to be keyed by id numbers. JSON cannot have keys be integers so the number is a string currently. This is okay because we never need to do math with the actual number the id represents.

It does look like we may have a problem in identifying duplicate keys. JSON load will just overwrite the key data with the latest one. So if you have 2 identical keys only the second key data is loaded.