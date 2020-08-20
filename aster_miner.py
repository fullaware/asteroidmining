"""
Take 2 objects; Miner & Asteroid
Assign attributes:
    Miner has power
    Asteroid has value
Create function to use the Miners power to collect the value of the Asteroid
"""

import random
import json
from itertools import count

miner = {"power": 100, "value": 0, "production": 0}
asteroid = {"value": 101}
rocks = {}


class Asteroid:
    _counter = count(4)

    def __init__(self):
        self.id = next(self._counter)
        random.seed()  # helps with better random number generation
        self.value = random.randint(100, 999)


def mine_value():
    miner['production'] = random.randint(0, miner['power'])
    if asteroid['value'] > 0 and asteroid['value'] >= miner['production']:
        asteroid['value'] -= miner['production']
        miner['value'] += miner['production']
    elif asteroid['value'] < miner['production'] and asteroid['value'] != 0:
        miner['value'] += asteroid['value']
        miner['production'] = asteroid['value']
        asteroid['value'] = 0
    else:
        miner['production'] = 0
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

    print("\nminer")
    for attribute in miner.keys():
        print(f"\t{attribute} : {miner[attribute]}")

    print("\nasteroid")
    for attribute in asteroid.keys():
        print(f"\t{attribute} : {asteroid[attribute]}")

# def save_attributes():
#     with open('data.json', 'w') as outfile:
#         json.dump(workload, outfile,indent=4)


def load_attributes():
    with open('data.json') as json_file:
        workload = json.load(json_file)
        for miner in workload['miner']:
            print(f"miner power : {miner['power']}")
            print(f"miner value : {miner['value']}")

        for asteroid in workload['asteroid']:
            print(f"asteroid value : {asteroid['value']}")


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
        gem = Asteroid()
        print(gem.id)
        print(gem.value)
        rocks.__setitem__(gem.id, gem.value)
    elif choice == 5:
        print(rocks)
        for key in rocks:
            print(key, ' : ', rocks[key])
    elif choice == 0:
        running = False
    else:
        pass
