This script loads a json file and counts by type.

###Running the script###
uv run main.py

###Example Output###

Are the original and copied dictionaries the same: False
{4: ['1', '3'], 3: ['2', '4', '6'], 2: ['5', '7', '9'], 1: ['8'], None: ['10']}
True
10
{'Alarm': 3, 'Supervisory': 3, None: 2, 'Trouble': 2}
True


###Data Shape###

Data shape was updated to be keyed by id numbers. JSON cannot have keys be integers so the number is a string currently. This is okay because we never need to do math with the actual number the id represents.

It does look like we may have a problem in identifying duplicate keys. JSON load will just overwrite the key data with the latest one. So if you have 2 identical keys only the second key data is loaded.

###Missing Types###

Missing types are included when using the count_by_type() function. This is to provide clarity on the data that is being processed by the function. 
Output: {'Alarm': 3, 'Supervisory': 3, None: 2, 'Trouble': 2}  -The None key represents missing types in the data as well as types that are explicitly null.

###Grouping by zones###

Use the group_by_zone function to group devices by assigned zones. If a zone is null or a zone is missing the group's key will be None.

###Duplicate-id error handling###
I chose to simply return a string saying that the dictionary is unchanged and returning the unchanged dictionary. I didn't choose to raise an error here because no error is raised organically by python if the id is duplicate. Python just overwrites the dictionary entry. I understand that there is the ability to raise an error anyway, currently the user has no way of knowing if the dictionary changed successfully unless they read the screen. 

###Converting id entries into strings###
I've decided to convert id entries into strings rather than rejecting them outright because this allows non-strings like None to be treated as place holders and changed later. 

###Add Device###
add_device() uses .copy() and copy.deepcopy to make copies of device which is a dictionary and the list of nested dictionaires to add a device to a new list without altering the inputs.

###Device to Rows###
This function creates a new list of devices where their device id is now a key, value pair in their respective dictionary. It also sorts the list by zone assignment in ascending order where zones that have no value are placed at the end of the list.

###Write Device CSV### 
This takes the a list of dictionaries and writes them to a csv file. We are returning True or False for success of failure of writing to CSV. This is so a future function that relies on the write_device_csv() will be able to pivot correctly based on its returned value.

###Read Device CSV###
The read_devices_csv() reads the device csv file from the path. It converts all rows into key:value pairs where the keys are the id's and the values are a dictionary of each devices properties. We convert all empty cells into None and zone and floor into ints. We except ValueErrors, we are choosing to handle the exception by printing the row and the error. This allows for the rest of the file to be read excluding the row with the error. Printing the row with the error allows the user to understand why the row was not read.

###Why null is used in the devices.json###
CSV can't tell a misisng key from a null, so the data uses null for "unknown".