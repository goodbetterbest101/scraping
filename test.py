import json
from pprint import pprint

with open('Attraction-1-thai.json') as data_file:
    data = json.load(data_file)

for i in data['attraction']:
    print(i)
