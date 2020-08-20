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
    '_id': str(uuid4()),
    'power': r.randint(75, 100),
    'value': 0
})
for i in range(10):
    data['asteroid'].append(asteroid_builder())

with open('data/data.json', 'w') as json_outfile:
    json.dump(data, json_outfile, indent=4)
