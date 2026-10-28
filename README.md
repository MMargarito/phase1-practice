This script loads a json file and counts by type.

###Running the script###
uv run main.py

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
I've decided to convert id entries into strings rather than rejecting them outright because this allows none strings like None to be treated as place holders and changed later. 