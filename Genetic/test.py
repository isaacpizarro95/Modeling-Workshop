import numpy as np
import random

m = 4
n = 4
passadis = np.zeros((m, n))

obstacles = True
obs = []
if obstacles == True:
    possibles_obstacles = [np.argwhere(passadis == 0)]
    for i in range(random.randint(2,6)):
        o = tuple(random.choice(possibles_obstacles[0]))
        passadis[o] = 4
        obs.append(o)

print(obs, "\n")
print(passadis)

