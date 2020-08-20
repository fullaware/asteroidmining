#!/usr/bin/env python3
from uuid import uuid4


class Entity(object):
    '''
    Container for an ID
    Entities have a relationship to their components

    >>> e = Entity('player', 0)
    >>> e
    <Entity player:0>
    >>> print(e)
    {}
    >>> e.health = 1
    >>> print(e.health)
    1
    >>> e['health'] = 10
    >>> e.health
    10
    '''

    def __init__(self, name=None, uid=None):
        self.uid = uuid4() if uid is None else uid
        self.name = name or ''
        self.components = dict()

    def __repr__(self):
        '''<Entity player:0>'''
        cname = self.__class__.__name__
        name = self.name or self.uid
        if name != self.uid:
            name = f'{name}:{self.uid}'
        return f'<{cname} {name}>'

    def __str__(self):
        '''{collection of the components}'''
        # TODO:   Make this better
        return str(self.components)

    def __getitem__(self, key):
        '''Returns the component value using the key'''

    def __setitem__(self, key, value):
        '''Sets the component using the key and value'''

    def __getattr__(self, key):
        '''Allows access to the properties/components as an attribute'''

    def __setattr__(self, key, value):
        '''Allows access to the properties/components as an attribute'''
    

if __name__ == '__main__':
    from doctest import testmod

    testmod()