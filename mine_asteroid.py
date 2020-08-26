#!/usr/bin/env python3
import json
import random as r


def mine_asteroid(asteroid=None, power=1):
    """Take single asteroid JSON object, remove int(power) from random elements, return object with reduced weights.

    1 power = 1 kg of mass && material removed

    MAX int(power) = 10000

    Sequences:
    ----------
        randomly choose ice, silicate, iron, slag
        deduct 1 (kg) from material
        deduct 1 (kg) from mass
        repeat x times

    TODO:
    -----
        * Design JSON blueprint
        * Randomly mine all asteroid elements from JSON blueprint.
    """
    if asteroid is None:
        asteroid = {'_id': '6a5f6bec-63b5-48f6-9156-0ad57022a00c',
                    'class': 'C',
                    'mass': 1674592559127,
                    'elements': [{'rabbits': 142659290493},
                                 {'hats': 113557337390},
                                 {'ninnys': 95014553453},
                                 {'cabbage': 94892834241},
                                 {'slag': 152402428236},
                                 {'gungans': 98200055989},
                                 {'sandwich': 482811749307},
                                 {'olive': 133053279763},
                                 {'smurfs': 213684113388},
                                 {'silence': 148316916864}]}

    if power > 10000:
        power = 10000
    element_choices = []

    for element_dict in asteroid['elements']:
        for elements in element_dict.keys():
            element_choices.append(elements)
    # print(element_choices)
    for _ in range(power):
        def remove_mass():
            asteroid['elements'][idx][elements] -= 1
            asteroid['mass'] -= 1
        r.seed()
        mine_extract = ''.join(r.choices(element_choices, weights=None, k=1))

        for idx, element_dict in enumerate(asteroid['elements']):
            #print(idx,element_dict)
            for elements, mass in element_dict.items():
                #print(elements, mass)
                if elements == mine_extract:
                    if mass > 0:
                        remove_mass()
                    else:
                        r.seed()
                        element_choices.remove(mine_extract)
                        mine_extract = ''.join(r.choices(element_choices, weights=None, k=1))
                        remove_mass()

        json_composition = asteroid

    return json_composition
    # for asteroid in data['asteroid']:
    #     if asteroid['ice'] or asteroid['iron'] == 0:
    #         print(f"asteroid_id : {asteroid['_id']}\n"
    #               f"\tclass : {asteroid['class']}\n"
    #               f"\tmass \t: {asteroid['mass']}\n"
    #               f"\tice \t: {asteroid['ice']}\n"
    #               f"\tsil \t: {asteroid['silicate']}\n"
    #               f"\tiron \t: {asteroid['iron']}\n"
    #               f"\tslag \t: {asteroid['slag']}\n"
    #               )

    # with open('data/data.json', 'w') as json_outfile:
    #     json.dump(data, json_outfile, indent=4)


if __name__ == "__main__":
    print(mine_asteroid(power=50))
