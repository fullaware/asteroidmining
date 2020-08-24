#!/usr/bin/env python3
import json

"""
    Read from data.json
"""


def print_asteroid(asteroid):
    print(f"asteroid_id : {asteroid['_id']}\n"
          f"\tclass : {asteroid['class']}\n"
          f"\tmass kg : {asteroid['mass']}\n"
          f"\tice kg : {asteroid['ice']}\n"
          f"\tsilicate kg : {asteroid['silicate']}\n"
          f"\tiron kg : {asteroid['iron']}\n"
          f"\tslag kg : {asteroid['slag']}\n"
          )


def load_json(lookup_id=None):

    with open('data/data.json', 'r') as json_file:
        data = json.load(json_file)
        for miner in data['miner']:
            print(f"miner_id : {miner['_id']}")
            print(f"\ttype : {miner['type']}")
            print(f"\tvalue : {miner['value']}")
            print(f"\tpower : {miner['power']}")

        for asteroid in data['asteroid']:
            if lookup_id is None:
                print_asteroid(asteroid)
            else:
                if asteroid['_id'] == lookup_id:
                    print_asteroid(asteroid)


if __name__ == "__main__":
    # load_json("f8f1c72d-9e51-476e-8632-d5f8ee0a3c9c")
    load_json()
