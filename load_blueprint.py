#!/usr/bin/env python3
import json
from console_colors import ConColor

"""
    Read from asteroid_blueprint.json
    spectral_pop
    elements
        spectral_class : {C:{min:int,max:int}}
        uses : str
        tech : [str,str]
"""

json_element = {
    "iron": {
        "spectral_class": {
            "M": {
                "min": 40,
                "max": 80
            },
            "S": {
                "min": 0,
                "max": 20
            },
            "C": {
                "min": 25,
                "max": 30
            }
        }}}


class LoadBlueprint:

    with open('data/asteroid_blueprint.json', 'r') as json_file:
        data = json.load(json_file)
        # print(data)
        for key, value in data['spectral_pop'].items():
            print(key, ":", value)
        # for key, value in data['elements']['spectral_class']:
        #     # print(key,":",value['spectral_class'])
        #     print(
        #         f"{ConColor.PURPLE}element {ConColor.BOLD}: {ConColor.GREEN}{key}{ConColor.RESET}")
        #     for key, value in value['spectral_class'].items():
        #         print(
        #             f"\t{ConColor.PURPLE}{key} : {ConColor.CYAN}{value}{ConColor.RESET}")
        for elements, values in data['elements'].items():
            # print(f"elements, values)
            for spectral_class, x in values['spectral_class'].items():
                #print(spectral_class, x)
                if spectral_class == 'S':
                    print(spectral_class)
                    for minmax, vals in x.items():
                        print(minmax, vals)


if __name__ == "__main__":
    LoadBlueprint()
