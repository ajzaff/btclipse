"""
Monte-Carlo simulation:
eclipse probability for test-before-evict.
"""

import collections
import itertools
import random
from random import randrange
import math
import matplotlib.pyplot as plt


def triedprob(rho, omega):
    """Probability an IP is seeded from the tried table.

    :param rho: (float) proportional size of tried table to new table.
    :param omega: (float) number of connected outgoing peers
    """
    rho_freq = math.sqrt(rho) * (9 - omega)
    return rho_freq / (1 + omega + rho_freq)


random.seed(420) # seed the random number generator to something... **sigh**.

N = 1	 # num of sims
colors = ('red', 'orange', 'yellow', 'green')
P = (.8, .6, .4, .2)  # churn rate
A = [round(1.5 ** x) for x in range(26)]	 # attack IP  [0...30000] log_{1.05} scale
H = [round(1.5 ** x) for x in range(20)]	 # honest IP  [0...2500]  log_{1.05} scale
graph = {p: list() for p in P}  # scatter plot

honest = 0
attacker = 0

for n in range(N):
    print("trial %d/%d" % (n+1, N))
    for h, p, a in itertools.product(H, P, A):
        # table of outgoing connections from the victim
        outgoing = []

        # Matrix of all IP adresses in tried table initialized to index in table
        triedTable = dict()

        # insert honest in random posions of tried table
        for _ in range(h):
            # 0 represents honest IP
            bucket = randrange(0,64)
            slot = randrange(0,64)
            triedTable[bucket, slot] = honest

        # insert attacker IPs into tried Table
        for _ in range(a):
            # 1 represents attack IP
            bucket = randrange(0,64)
            slot = randrange(0,64)
            triedTable[bucket, slot] = attacker

        # fill outgoing connections table
        while len(outgoing) < 8:
            omega = len(outgoing)
            rho = len(triedTable) / 256.
            # if tried is selected
            if triedprob(rho, omega) <= random.random():
                # append random IP from tried table
                bucket, slot = random.choice(list(triedTable.keys()))
                tempIP = triedTable[bucket, slot]
                if tempIP == honest:
                    if random.random() <= p:
                        # outgoing.append(honest)
                        break  # attacker did not eclipse the node
                else:
                    outgoing.append(attacker)

            else:
                # append from new table (attacker IP)
                outgoing.append(attacker)

        if sum(outgoing) == 8*attacker:
            # the attacker wins
            graph[p].append((a, h))


# create the plot
for i, p in enumerate(P):
    x, y = zip(*graph[.2])  # unzip
    plt.scatter(x, y, color=colors[1])
plt.show()