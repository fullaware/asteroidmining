#!/usr/bin/env python3
"""
Each time a 'turn' is taken the qualifying events should be weighed to see which one activates.

Some events should occur every n turns
Some events should occur only after other events make it possible:
    
Some events should occur as a result of triggering a series: 
    Discovering organic life causes govt seize miner and lose any accumulated materials
    Govt promise compensation in x turns
    Compensation arrives; enough money to buy a new miner and market price of materials + interest
"""

game_in_play = True

while game_in_play:

    event_list = {}
