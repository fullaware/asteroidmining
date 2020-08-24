import json

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
        #print(data)
        for key,value in data['type_pop'].items():
            print(key,":",value)
        for key,value in data['elements'].items():
            print(key,":",value['types'])
            for key,value in value['types'].items():
                print(value)

if __name__ == "__main__":
    Blueprint()