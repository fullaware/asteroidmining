import json
import random as r

def mine_asteroid(asteroid, kgs):
    """Take single asteroid JSON object, remove int(kgs) from random elements, return object with reduced weights.

    sequences
    ---------
        randomly choose ice, silicate, iron, slag
        deduct 1 (kg) from material
        deduct 1 (kg) from mass
        repeat x times
    """
    mining_list = ['ice', 'silicate', 'iron', 'slag']

    for _ in range(kgs):
        def mine_asteroid():
            asteroid[f'{mine_extract}'] -= 1
            #print(f"mined_material {mine_extract} : {asteroid[f'{mine_extract}']}")

            asteroid['mass'] -= 1
            #print(f"mined_mass : {asteroid['mass']}")
        r.seed()
        mine_extract = ''.join(r.choices(mining_list, weights=None, k=1))
        if asteroid[f'{mine_extract}'] > 0:
            mine_asteroid()
        else:
            r.seed()
            mining_list.remove(f'{mine_extract}')
            mine_extract = ''.join(r.choices(mining_list, weights=None, k=1))
            mine_asteroid()

    # for asteroid in data['asteroid']:
    #     if asteroid['ice'] or asteroid['iron'] == 0:
    #         print(f"asteroid id : {asteroid['id']}\n"
    #               f"\tclass : {asteroid['class']}\n"
    #               f"\tmass \t: {asteroid['mass']}\n"
    #               f"\tice \t: {asteroid['ice']}\n"
    #               f"\tsil \t: {asteroid['silicate']}\n"
    #               f"\tiron \t: {asteroid['iron']}\n"
    #               f"\tslag \t: {asteroid['slag']}\n"
    #               )

    # with open('data/data.json', 'w') as json_outfile:
    #     json.dump(data, json_outfile, indent=4)