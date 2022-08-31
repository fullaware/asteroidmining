#!/usr/bin/env python3
"""Parse JSON file with nested objects into dictionaries
Save dictionaries to nested JSON objects into file

TODO:
-----
    * break out 'miner' creation into 'miner_factory'
"""
import json
from uuid import uuid4
import random as r
from asteroid_factory import asteroid_factory
from miner_factory import miner_factory

"""
    Save to data.json
"""
data = {}
data['miner'] = []
data['asteroid'] = []

data['miner'].append(miner_factory())
for i in range(10):
    data['asteroid'].append(asteroid_factory())

with open('data/data.json', 'w') as json_outfile:
    json.dump(data, json_outfile, indent=4)
