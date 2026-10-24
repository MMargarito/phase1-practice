This script loads a json file and counts by type.

###Running the script###
uv run main.py

###Data Shape###
I am aware that the current shape of the data can make finding id errors more difficult. I also understand that this implies their is a unique name for each device. If we had multiple smoke detectors the data's shape would need to change. I may change it so the keys are the ids. This makes more sense because the ids should be unique and devices on a full project will share names. 