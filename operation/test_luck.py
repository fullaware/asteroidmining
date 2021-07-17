#!/usr/bin/env python3
"""Various functions to produce random luck results;

Standard dice 'test' is to roll each die 5x number of sides.

diceroll(sides)
polarity(max_count) # boolean;
coinflip(max_count)
runofluck # Count/MaxLimit moves this should effect

"""
import random
from console_colors import ConColor


DEBUG = True


def diceroll(sides=6):
    max_count = int(sides * 5)

    for _ in range(0, max_count, 1):
        random.seed()
        roll = random.randint(1, sides)

    return roll


def coin_flip():
    """
    coin flip
    0 = heads/positive
    1 = tails/negative

    TODO:
    -----
        * 
    """
    return random.randint(0,1)


def random_window(luck=0, coin=0):
    # coin 0 bad 1 good
    # luck 0 bad 13 good
    range_width = 0
    range_start = 0
    range_end = 0

    while range_end == 0:
        # print(f"end {range_end}")
        while range_width < 1 or range_width > 15:
            range_width = diceroll(10)
            # print(f"width {range_width}")
        while range_start < 1:
            range_start = diceroll(10)
            # print(f"start {range_start}")
        range_end = range_start + range_width

        if range_end > 21:
            range_end = 21

    return range_start, range_end


def alert_msg(msg):
    if DEBUG:
        print(msg)


def test_luck(max_tries=1):
    for _ in range(0, max_tries):
        shield = 100
        luck = 7
        turns = 0
        range_width = 0
        range_start = 0
        range_end = 0
        while shield > 0:
            random.seed()
            turns += 1
            fate = diceroll(20)
            coin = coin_flip() # 0 bad 1 good
            # 0 bad 13 good
            if coin == 0 and luck <= 0:
                alert_msg(f"{ConColor.RED}\tImpact imminent{ConColor.RESET}")
                luck = 0
                range_start = 1
                range_end = 20
            elif coin == 1 and luck >= 13:
                alert_msg(
                    f"{ConColor.GREEN}\tLucky Duck - Dodged{ConColor.RESET}")
                luck = 13
                range_start = 0
                range_end = 0
            elif coin == 0 and luck >= 1:
                alert_msg(f"{ConColor.RED}\tBrace for impact!{ConColor.RESET}")
                range_width = random_window(luck, coin)
                range_start = range_width[0]
                range_end = range_width[1]
                luck -= 1
            elif coin == 1 and luck < 13:
                alert_msg(
                    f"{ConColor.YELLOW}\tEvasive maneuver!{ConColor.RESET}")
                luck += 1
                range_width = random_window(luck, coin)
                range_start = range_width[0]
                range_end = range_width[1]

            if range_start == 0 and range_end == 0:
                damage = 0
                alert_msg(
                    f"turn {turns}, fate {fate}, luck {luck}, coin {coin}, shield {shield}")
            elif fate in range(range_start, range_end):
                if coin == 0:
                    damage = diceroll(6)
                else:
                    damage = 1
                    if luck >= 1:
                        luck -= 1
                alert_msg(
                    f"{ConColor.RED}\tHIT! Shield reduced by {damage}")
                shield -= damage
                alert_msg(
                    f"turn {turns}, fate {fate}, luck {luck}, coin {coin}, range_width {range_width}, damage {damage}, shield {shield}{ConColor.RESET}")
                range_width = 0
                range_start = 0
                range_end = 0

            elif fate not in range(range_start, range_end):
                damage = 0
                alert_msg(f"{ConColor.BLUE}\tDODGED!")
                alert_msg(
                    f"turn {turns}, fate {fate}, luck {luck}, coin {coin}, range_width {range_width}, damage {damage}, shield {shield}{ConColor.RESET}")

        print(f"\nWell crew, it was a good run...\n"
              f"We survived {turns} days on autopilot and my great looks.  Even walked away with {luck} luck.\n")


test_luck()
