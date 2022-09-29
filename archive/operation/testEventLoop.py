#!/usr/bin/env python3
"""Feeding events into a game loop

    while game != finished:
        for player in players:
            player.doTurn(Events(turnNumber))

"""

from consoleColors import ConColor

DEBUG = True

def alertMsg(msg):
    if DEBUG:
        print(msg)

def gameLoop(maxTries=1):
    for _ in range(0, maxTries):
        shield = 100
        turns = 0

        while shield > 0:
            turns += 1
            alertMsg(f"{ConColor.RED}\tTesting {turns}{ConColor.RESET}")
            shield -= 1


gameLoop()