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


def polarity(max_count=5):
    """
    max_count is the upper range limit of the number of times the
    coins will be flipped before returning the results.
    This helps prime the random seed generator and produce more randomized results.

    TODO:
    -----
        * Convert to dict?
    """

    for _ in range(0, max_count, 1):
        pol = []
        random.seed()
        roll = random.randint(1, max_count)
        if roll % 2:
            pol.append(1)
            pol.append('bad')
            pol.append('negative')
            pol.append('tails')
        else:
            pol.append(0)
            pol.append('good')
            pol.append('positive')
            pol.append('heads')
    return pol


# print(f"Dice 1 : {diceroll(20)}\n"
#       f"Dice 2 : {diceroll(20)}")
# # print(f"Polarity : {polarity()[0]+48^4}")
# print(f"Polarity : {polarity()[2]}")
# print(f"Coinflip : {polarity()[3]}")


"""
SIMULATE GAME LOGIC FATE/LUCK system
How many turns can the player survive without mediation
"""


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
            coin = polarity()[0]  # 0 bad 1 good
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
              f"We survived {turns} days on autopilot, my great looks and walked away with {luck} luck.\n")


test_luck()
