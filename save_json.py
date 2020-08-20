"""Parse JSON file with nested objects into dictionaries
Save dictionaries to nested JSON objects into file

TODO:
-----
    * break out 'miner' creation into 'ship_builder'
"""
import json
from uuid import uuid4
import random as r
from asteroid_builder import asteroid_builder
from ship_builder import ship_builder

"""
    Save to data.json
"""
data = {}
data['miner'] = []
data['asteroid'] = []

data['miner'].append(ship_builder())
for i in range(10):
    data['asteroid'].append(asteroid_builder())

with open('data/data.json', 'w') as json_outfile:
    json.dump(data, json_outfile, indent=4)
