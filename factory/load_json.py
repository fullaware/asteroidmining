#!/usr/bin/env python3
import json
from mine_asteroid import mine_asteroid

"""
    Read from data.json
"""


def load_json(lookup_id=None):

    with open('data/data.json', 'r') as json_file:
        data = json.load(json_file)
        for miner in data['miner']:
            print(f"miner_id : {miner['_id']}")
            print(f"\ttype : {miner['type']}")
            print(f"\tvalue : {miner['value']}")
            print(f"\tpower : {miner['power']}")

        for asteroid in data['asteroid']:
            if asteroid['_id'] == lookup_id:
                print(asteroid)
                mine_asteroid(asteroid, 1000)
                print(asteroid)


if __name__ == "__main__":
    load_json("33d00f32-b6fe-404d-90ef-71f0f1f1af24")
