import json

"""
    Read from data.json
"""

with open('data/data.json', 'r') as json_file:
    data = json.load(json_file)
    for miner in data['miner']:
        print(f"miner_id : {miner['_id']}")
        print(f"\tpower : {miner['power']}")
        print(f"\tvalue : {miner['value']}")

    for asteroid in data['asteroid']:
        print(f"asteroid_id : {asteroid['_id']}\n"
              f"\tclass : {asteroid['class']}\n"
              f"\tmass kg : {asteroid['mass']}\n"
              f"\tice kg : {asteroid['ice']}\n"
              f"\tsilicate kg : {asteroid['silicate']}\n"
              f"\tiron kg : {asteroid['iron']}\n"
              f"\tslag kg : {asteroid['slag']}\n"
              )
