"""
Function to parse JSON file with nested objects into dictionaries
Function to save dictionaries to nested JSON objects into file
"""
import json
from uuid import uuid4
import random as r
from asteroid_builder import asteroid_builder

"""
    Save to data.json
"""
data = {}
data['miner'] = []
data['asteroid'] = []

data['miner'].append({
    'id': str(uuid4()),
    'power': r.randint(75, 100),
    'value': 0
})
for i in range(10):
    data['asteroid'].append(asteroid_builder())

with open('data/data.json', 'w') as json_outfile:
    json.dump(data, json_outfile, indent=4)

"""
    Read from data.json
"""

with open('data/data.json', 'r') as json_file:
    data = json.load(json_file)
    for miner in data['miner']:
        print(f"miner id : {miner['id']}")
        print(f"\tpower : {miner['power']}")
        print(f"\tvalue : {miner['value']}")

    for asteroid in data['asteroid']:
        print(f"asteroid id : {asteroid['id']}\n"
              f"\tclass : {asteroid['class']}\n"
              f"\tmass kg : {asteroid['mass']}\n"
              f"\tice kg : {asteroid['ice']}\n"
              f"\tsilicate kg : {asteroid['silicate']}\n"
              f"\tiron kg : {asteroid['iron']}\n"
              f"\tslag kg : {asteroid['slag']}\n"
              )
