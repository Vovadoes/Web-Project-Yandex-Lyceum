import json


with open('numbers.json') as json_file:
    data = json.load(json_file)
    print(data[0]['title'])