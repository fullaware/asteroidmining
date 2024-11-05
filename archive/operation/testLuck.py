#!/usr/bin/env python3
"""Various functions to produce random luck results;

Standard dice 'test' is to roll each die 5x number of sides.

diceroll(sides)
coinflip(max_count)
runofluck # Count/MaxLimit moves this should effect

"""
import random
from consoleColors import ConColor


DEBUG = True


def diceroll(sides=6):
    """Return random number from 1 up to X sides.  Default=6
    
    """
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


""" def test_luck(max_tries=1):
    def alert(message, color):
        print(f"{color}{message}{ConColor.RESET}")

    for _ in range(max_tries):
        shield = 100
        luck = 7
        turns = 0
        random.seed()
        
        while shield > 0:
            turns += 1
            fate = diceroll(20)
            coin = coin_flip()  # 0 bad, 1 good
            range_start, range_end = 0, 0

            if coin == 0 and luck <= 0:
                alert("Impact imminent", ConColor.RED)
            elif coin == 1 and luck >= 5:
                alert("Lucky Duck - Dodged", ConColor.GREEN)
                luck += 1
            elif coin == 0 and luck >= 1:
                alert("Brace for impact!", ConColor.RED)
                range_start, range_end = random_window(luck, coin)
                luck -= 1
            elif coin == 1 and luck < 13:
                alert("Evasive maneuver!", ConColor.YELLOW)
                luck += 1
                range_start, range_end = random_window(luck, coin)

            if range_start == 0 and range_end == 0:
                damage = 0
                alert(f"turn {turns}, fate {fate}, luck {luck}, coin {coin}, shield {shield}", ConColor.RESET)
            elif range_start <= fate < range_end:
                damage = diceroll(6) if coin == 0 else 1
                if coin == 1 and luck > 0:
                    luck -= 1
                shield -= damage
                alert(f"HIT! Shield reduced by {damage}", ConColor.RED)
                alert(f"turn {turns}, fate {fate}, luck {luck}, coin {coin}, range ({range_start}-{range_end}), damage {damage}, shield {shield}", ConColor.RESET)
            else:
                alert("DODGED!", ConColor.BLUE)
                alert(f"turn {turns}, fate {fate}, luck {luck}, coin {coin}, shield {shield}", ConColor.RESET)

        print(f"\nWell crew, it was a good run...\n"
              f"We survived {turns} days on autopilot and my great looks. Even walked away with {luck} luck.\n")

 """

def test_luck(max_tries=1):
    def alert(message, color):
        alerts.append({"message": message, "color": color})

    game_data = []
    for _ in range(max_tries):
        shield = 100
        luck = 7
        turns = 0
        random.seed()
        alerts = []  # List to store alerts

        while shield > 0:
            turns += 1
            fate = diceroll(20)
            coin = coin_flip()
            range_start, range_end = 0, 0

            if coin == 0 and luck <= 0:
                alert("Impact imminent", "red")
            elif coin == 1 and luck >= 5:
                alert("Lucky Duck - Dodged", "green")
                luck += 1
            elif coin == 0 and luck >= 1:
                alert("Brace for impact!", "red")
                range_start, range_end = random_window(luck, coin)
                luck -= 1
            elif coin == 1 and luck < 13:
                alert("Evasive maneuver!", "yellow")
                luck += 1
                range_start, range_end = random_window(luck, coin)

            if range_start == 0 and range_end == 0:
                damage = 0
                alert(f"turn {turns}, fate {fate}, luck {luck}, coin {coin}, shield {shield}", "reset")
            elif range_start <= fate < range_end:
                damage = diceroll(6) if coin == 0 else 1
                if coin == 1 and luck > 0:
                    luck -= 1
                shield -= damage
                alert(f"HIT! Shield reduced by {damage}", "red")
                alert(f"turn {turns}, fate {fate}, luck {luck}, coin {coin}, range ({range_start}-{range_end}), damage {damage}, shield {shield}", "reset")
            else:
                alert("DODGED!", "blue")
                alert(f"turn {turns}, fate {fate}, luck {luck}, coin {coin}, shield {shield}", "reset")

        # Append the game data along with alerts to the game data list
        game_data.append({"turns": turns, "shield": shield, "luck": luck, "alerts": alerts})

    return game_data