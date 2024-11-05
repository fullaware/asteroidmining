#!/usr/bin/env python3
import json
from mineAsteroid import mine_asteroid

"""
    Read from data.json
"""


def load_json(lookup_id=None):

    with open('data/data.json', 'r') as json_file:
        data = json.load(json_file)
        for ship in data['ship']:
            print(f"ship_id : {ship['_id']}")
            print(f"\ttype : {ship['type']}")
            print(f"\tvalue : {ship['value']}")
            print(f"\tpower : {ship['power']}")

        for asteroid in data['asteroid']:
            if asteroid['_id'] == lookup_id:
                print(asteroid)
                mine_asteroid(asteroid, 1000)
                print(asteroid)


if __name__ == "__main__":
    load_json("33d00f32-b6fe-404d-90ef-71f0f1f1af24")
