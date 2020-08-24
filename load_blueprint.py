#!/usr/bin/env python3
import json
from console_colors import ConColor

"""
    Read from asteroid_blueprint.json
    type_pop
    elements
        types : {[]}
        uses : str
        tech : []
"""


class Blueprint:

    with open('data/asteroid_blueprint.json', 'r') as json_file:
        data = json.load(json_file)
        # print(data)
        for key, value in data['type_pop'].items():
            print(key, ":", value)
        for key, value in data['elements'].items():
            # print(key,":",value['types'])
            print(
                f"{ConColor.PURPLE}element {ConColor.BOLD}: {ConColor.GREEN}{key}{ConColor.RESET}")
            for key, value in value['types'].items():
                print(
                    f"\t{ConColor.PURPLE}{key} : {ConColor.CYAN}{value}{ConColor.RESET}")


if __name__ == "__main__":
    Blueprint()
