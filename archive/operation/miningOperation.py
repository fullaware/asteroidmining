#!/usr/bin/env python3
"""
Take 2 objects; ship & Asteroid
Assign attributes:
    ship has power
    Asteroid has value
Create function to use the ships power to collect the value of the Asteroid
"""

import random
import json

ship = {"power": 100, "value": 0, "production": 0}
asteroid = {"value": 101}


def mine_value():
    ship['production'] = random.randint(0, ship['power'])
    if asteroid['value'] > 0 and asteroid['value'] >= ship['production']:
        asteroid['value'] -= ship['production']
        ship['value'] += ship['production']
    elif asteroid['value'] < ship['production'] and asteroid['value'] != 0:
        ship['value'] += asteroid['value']
        ship['production'] = asteroid['value']
        asteroid['value'] = 0
    else:
        ship['production'] = 0
        print("\nThis asteroid is tapped out.  Locate another one.")

    print_attributes()


def find_asteroid():
    random.seed()  # helps with better random number generation
    asteroid['value'] = random.randint(100, 999)


def print_attributes():
    """
    returns
    power  :  100
    value  :  0
    value  :  101
    """

    print("\nship")
    for attribute in ship.keys():
        print(f"\t{attribute} : {ship[attribute]}")

    print("\nasteroid")
    for attribute in asteroid.keys():
        print(f"\t{attribute} : {asteroid[attribute]}")

# def save_attributes():
#     with open('data.json', 'w') as outfile:
#         json.dump(workload, outfile,indent=4)


def load_attributes():
    with open('data/ship.json') as json_file:
        workload = json.load(json_file)
        for ship in workload['ships']:
            print(f"ship name : {ship['name']}")
            print(f"ship power : {ship['power']}")
            print(f"ship value : {ship['value']}")
            print(f"ship all {ship}")


def impact_countdown(initial, impact):
    # Take initial number and decrease by impact %
    # initial : 100
    # impact : 50
    # 50
    # 25
    # 12.5
    # 0
    pass


running = True

while running:
    choice_message = f"\n1. Mine asteroid ({asteroid['value']} resources left)" \
        f"\n2. Show all attributes" \
        f"\n3. Find new asteroid" \
        f"\n0. Exit\n"

    choice = int(input(choice_message))

    if choice == 1:
        mine_value()
    elif choice == 2:
        print_attributes()
    elif choice == 3:
        find_asteroid()
    elif choice == 4:
        load_attributes()
    elif choice == 0:
        running = False
    else:
        pass