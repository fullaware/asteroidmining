#!/usr/bin/env python3
from uuid import uuid4


def ship_factory(ship_type='mining', ship_value=9000000, ship_power=1000):
    """Returns single JSON object in the following format:

        {
            '_id': '42be277a-af74-4ff7-9409-eea5dce73b04',
            'type': 'mining',
            'value': 9000000,
            'power': 5000
        }

    Sequences:
    ---------
        randomly generate _id, value, power
        build and return JSON object

    TODO:
    -----
        * Design JSON blueprint
        * Randomly generate all ship elements from JSON blueprint.
        * ISS mass is 419,725 kg
    """

    # if ship_type is mining_factory.__defaults__[0]
    #     pass
    # else:
    #     r.randint(75, 100)

    ship_json = {
        '_id': str(uuid4()),
        'type': ship_type,
        'power': ship_power,
        'value': ship_value
    }
    return ship_json
