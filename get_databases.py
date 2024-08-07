import json
import requests
#import requests_mock


# Write a script that retrieves info from the API and prints out all database names, their storage type, their used storage, and percentage of storage used. Sort the output by storage used in descending order by percentage of storage used.

def sort_databases(data):
    databases = data["databases"]


    for database in databases:
        storage_size = database["storage_size"]
        # This is occasionally null - treating as zero - could be ok, might want to throw an error or drop entire entry...
        storage_used = database["storage_used"] if database["storage_used"] is not None else 0
        percentage_used = round(storage_used / storage_size * 100, 2)
        database["percentage_used"] = percentage_used

    sortedDB = list(reversed(sorted(databases, key=lambda d: d['percentage_used'])))
    for database in sortedDB:
        name = database['name']
        storage_size = database["storage_size"]
        storage_type = database["storage_type"]
        storage_used = database["storage_used"]
        # Storage capacity was not requested, however makes it easier to visually compare
        print(f"Database Name: {name}\n  Storage Type: {storage_type}\n  Storage Capacity (GB): {round(storage_size, 2)}  \n  Storage Used (GB): {storage_used}\n  Storage Utilization: {database['percentage_used']}%")




url = "https://6god8pgyzf.execute-api.us-west-2.amazonaws.com/databases"
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"Error Calling endpoint: {url}")
    print(err.args[0])
    exit(1)


data = response.json()

# In reality i would mock this and use a separate testing method - advised to keep simple

#file = open("sample_data.json")
# data = json.load(file)
sort_databases(data)
