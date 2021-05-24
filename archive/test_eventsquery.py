#!/usr/bin/env python3
"""
Test loading blueprint, generating x objects, writing all objects to file
Load LARGER file, test multiple queries for speed.
    
# Must be run multiple times to get a read
    import time

    t0 = time.time()
    code_block
    t1 = time.time()

    total = t1-t0

TODO:
-----

"""
import json
from uuid import uuid4
from pprint import pprint
from random import randint
import time

"""
    
"""
with open('data/events_blueprint.json', 'r') as json_events:
    events = json.load(json_events)


def searchKeysByVal(dict, byVal):
    keysList = []
    itemsList = dict.items()
    for item in itemsList:
        if item[1] == byVal:
            keysList.append(item[0])
    return keysList


def build_events(count=1):

    events_output = {}
    # print(events['Events'][0]['EventID'])

    for event_dict in events['Events']:
        # print(event_dict)
        for item in event_dict.items():
            if item[0] == 'LevelCheck' and item[1] == 3:
                # print(pprint(event_dict))
                new_events = event_dict

    # print(type(new_events))
    for _ in range(count):
        new_events['EventID'] = str(uuid4())
        new_events['LevelCheck'] = randint(1, 10)
        new_events['LuckCheck'] = randint(1, 10)
        events_output.update(new_events)
        # print(new_events['EventID'])
        events['Events'].append(events_output)
        events_output = {}

    with open('data/events.json', 'w') as json_outfile:
        json.dump(events, json_outfile, indent=4)


def query_events(level_minimum=1):
    with open('data/events.json', 'r') as json_events:
        events = json.load(json_events)
    counti = 0
    for event_dict in events['Events']:
        # print(event_dict)
        for item in event_dict.items():
            if item[0] == 'LevelCheck' and item[1] > level_minimum:
                counti += 1
                # print(pprint(event_dict))

    print(counti)


t0 = time.time()
build_events(9)
query_events(9)
t1 = time.time()

print(f"Total {t1-t0}")
