import random


"""
Various functions to produce random luck results;

max_count = 45

#   max_count is the upper range limit of the number of times the 
#       dice will be rolled before returning the results.  
#       This helps produce more randomized results.

diceroll(sides, max_count) 
polarity(max_count) # boolean; 
coinflip(max_count)
runofluck # Count/MaxLimit moves this should effect

"""


def diceroll(sides=6, max_count=90):
    roll = {}
    
    for _ in range(0, max_count, 1):
        random.seed()
        dice1 = random.randint(1,sides)
        random.seed()
        dice2 = random.randint(1,sides)
    
    roll['dice1'] = dice1
    roll['dice2'] = dice2
    # print(dice1, dice2)
    return roll


def polarity(max_count=90):

    for _ in range(0, max_count, 1):
        pol = []
        random.seed()
        roll = random.randint(1, max_count)
        if roll % 2:
            pol.append(1)
            pol.append('bad')
            pol.append('negative')
        else:
            pol.append(0)
            pol.append('good')
            pol.append('positive')

    return pol



def coinflip():
    pass

print(f"Dice 1 : {diceroll()['dice1']}\nDice 2 : {diceroll()['dice2']}" )
# print(f"Polarity : {polarity()[0]+48^4}")
print(f"Polarity : {polarity()[2]}")

"""
Roll Dice
If > x Bad Luck
If < x Good Luck
Roll Dice
Power of luck
Duration of Luck

If Luck roll is the same 3 X in a row, use Duration modifier
"""