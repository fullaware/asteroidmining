#!/usr/bin/env python3
import json
from uuid import uuid4
import random as r
from collections import ChainMap
from load_blueprint import LoadBlueprint
from pprint import pprint

bp = LoadBlueprint()


def asteroid_builder():
    """Returns single JSON object

    Sequences:
    ---------
        randomly generate mass
        randomly assign materials to random range of overall mass by priority of asteroid type
        build and return JSON object

    TODO:
    -----
        * Randomly generate all asteroid elements from JSON blueprint.
    """

    def percent_of(percent, whole):
        """
        >>> percent_of(50, 60)
        30.0
        >>> percent_of(50, 10)
        5.0
        """
        percent_of_whole = round((percent * whole) / 100.0)
        if percent_of_whole == 0:
            percent_of_whole = 1
        return (percent * whole) / 100.0

    """
        Given the weights of known asteroids we will randomize up to 6 digits, then 
            expand by multiplying to 10**10.  We aren't looking for simulation
            but I would like to show the massive sizes we are dealing with.
            We will not target anything smaller than 10 x 10**10
            which will be 100,000,000,000 kg.  
            
            Plan for ships to mine between 0 and 5000kg per cycle

                Ceres 938350 × 10^15 kg
                Vesta 259076 x 10^15
                Psyche 241000 x 10^15 M
                Europa 227000 x 10^15
                Ganymed 167 x 10^15
                Eros 6.6 x 10^15
                Phobos 10.6 x 10^15 - Moon of Mars
                Ryugu 450 x 10^9 kg
                Bennu 78 x 10^9
    """
    def mass_expand(mass):
        # converts small to 10^15
        return mass*(10**10)

    """
        Generate max MASS in kg given number of asteroids by that size
        Given that there are only 10 or so Ceres sized asteroids, that's the weight it's assigned

        TODO : create AdminUI for tweaking weights
    """

    r.seed()
    mass_min = 10
    mass_max = int(''.join(r.choices(
        ['99', '999', '9999', '99999'], weights=(25, 25, 15, 2), k=1)))

    r.seed()
    asteroid_mass = r.randint(mass_min, mass_max)

    """
        Generate class by the likely number of asteroids by that class
        This will then be used to increase the percentage of a certain elements

        C = highest ice content
            C-type (carbonaceous) asteroids are the most common variety, forming around 75% of known asteroids
        S = highest silicate content
            S-type asteroids consist mainly of iron- and magnesium-silicates Approximately 17% of asteroids
        M = highest metal content (iron and platinum group)
            M-type Some, but not all, are made of nickel–iron, either pure or mixed with small amounts of stone 10% of asteroids
    """

    asteroid_comp = {}
    r.seed()
    asteroid_class = ''.join(
        r.choices(bp.blueprint_class_choices, weights=bp.blueprint_class_weights, k=1))

    r.seed()

    """
        Breaking down the mass by composit
        Making sure primary material has first priority of assigned mass
        slag should always be last and is "leftover" from the initial mass assignment priority
        make sure MAX of randint = < 100 to always allow for slag

        TODO: Add unique provisional designation names https://en.wikipedia.org/wiki/Provisional_designation_in_astronomy

    """
    bp_asteriods_json = json.loads(bp.blueprint_asteriods)
    elements_list = []

    mass_total = 0
    for element, element_ranges in bp_asteriods_json[asteroid_class].items():

        asteroid_comp[element] = percent_of(
            r.uniform(element_ranges[0], element_ranges[1]), asteroid_mass)
        asteroid_element_expand = int(mass_expand(asteroid_comp[element]))
        elements_list.append({element: asteroid_element_expand})
        mass_total += asteroid_element_expand

    json_composition = {
        "_id": str(uuid4()),
        "class": asteroid_class,
        "mass": mass_total,
        "elements": elements_list
    }

    return json_composition


if __name__ == "__main__":
    pprint(asteroid_builder())
