#!/usr/bin/env python3
import json
import pprint
from collections import ChainMap

"""
    Read from asteroid_blueprint.json
    spectral_population - is the population of spectral types (C,S,M) by % of total population
    elements - (ice,iron,silicate,etc) 
        spectral_class : {C:{min:int,max:int}} - expected range of occurance of element for each spectral class
        uses : str
        tech : [str] - # TODO: Tech tree ideas need to be developed

    Return:
        blueprint_class_choices = ['C', 'S', 'M'] 
        blueprint_class_weights = (75, 17, 10) 
        blueprint_asteriods
"""


class LoadBlueprint:

    def __init__(self):
        self.blueprint_class_choices = []
        self.blueprint_class_weights = []
        blueprint_construct = {}

        with open('data/asteroid_blueprint.json', 'r') as json_file:
            blueprint = json.load(json_file)

            for class_type, percent_of_pop in blueprint['spectral_population'].items():

                self.blueprint_class_choices.append(class_type)
                self.blueprint_class_weights.append(percent_of_pop)
                elements_list = []
                for element in blueprint['elements'].keys():
                    for spectral_class, minmax in blueprint['elements'][element]['spectral_class'].items():
                        if spectral_class == class_type:
                            elements_list.append(
                                {element: [minmax['min'], minmax['max']]})
                    # Converting list to dict
                    new_dict = dict(ChainMap(*elements_list))
                    blueprint_construct[class_type] = new_dict

        self.blueprint_asteriods = json.dumps(blueprint_construct)


if __name__ == "__main__":
    LoadBlueprint()
