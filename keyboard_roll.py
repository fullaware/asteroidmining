import random

while True:
    try:
        roll = random.randint(1, 6)
        print(roll, end='\x1b[1K\r')
    except KeyboardInterrupt:
        print(roll)
        break
    except:
        break
