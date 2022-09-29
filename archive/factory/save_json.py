#!/usr/bin/env python3
"""Parse JSON file with nested objects into dictionaries
Save dictionaries to nested JSON objects into file

TODO:
-----
    * break out 'ship' creation into 'ship_factory'
"""
import json
from asteroid_factory import asteroid_factory
from ship_factory import ship_factory

"""
    Save to data.json
"""
data = {}
data['ship'] = []
data['asteroid'] = []

data['ship'].append(ship_factory())
for i in range(10):
    data['asteroid'].append(asteroid_factory())

with open('data/data.json', 'w') as json_outfile:
    json.dump(data, json_outfile, indent=4)
