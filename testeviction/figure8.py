"""
Monte-Carlo simulation:
eclipse probability for test-before-evict.
"""

import numpy as np
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


def sampleips(a, h, n=None, tablesize=4096):
    """Samples the IP to place in a given table cell.

    :param a: (int) attacker IPs
    :param h: (int) honest IPs
    :param tablesize: (int) the size of the tried table
    :return: yields a stream of (bucket, slot) => IP
    """
    if a + h == 0:
        return
    if n is None:
        n = max(a, h)
    for _ in range(n):
        p_attacker = float(a + tablesize) / (a + h + tablesize)
        r = random.random()
        if r <= p_attacker:
            bucket = randrange(64)
            slot = randrange(64)
            yield (bucket, slot), attacker
            a = max(0, a - 1)
        else:
            bucket = randrange(64)
            slot = randrange(64)
            yield (bucket,slot), honest
            h = max(0, h - 1)


def jointsample(n, *params):
    for _ in range(n):
        yield tuple(map(lambda e: random.choice(e), params))


def sizemap(sizes):
    return tuple(map(lambda s: max(4, 1.1 ** s), sizes))


random.seed(420)  # seed the random number generator to something... **sigh**.

# N = 1000	 # num of sims
N = 100000
colors = ('green', 'yellow', 'orange', 'red')
a_step = 1200
h_step = 200
P = (.2, .4, .6, .8)  # churn rate
A = [x * a_step for x in range(round(30001 / a_step))]	 # attack IP  [0...30000]
H = [x * h_step for x in range(round(4096 / h_step))]	 # honest IP  [0...4096]
graph = {}

honest = 0
attacker = 1

for (h, p, a) in jointsample(N, H, P, A):

    eclipse = True
    for _, ip in sampleips(a, h, n=8):
        if ip == honest:
            eclipse = False
            break

    if eclipse:
        # the attacker wins
        if p not in graph:
            graph[p] = {}
        if (a, h) not in graph[p]:
            graph[p][a, h] = 1
        else:
            graph[p][a, h] += 1

# create the plot
series = []
labels = []
plt.title('Eclipses vs. Attacker Resources')
for i, p in enumerate(sorted(graph)):
    points, size = zip(*graph[p].items())
    x, y = zip(*points)
    series.append(plt.scatter(x, y, color=colors[i], sizes=sizemap(size), edgecolors=['black'] * len(x), marker='o'))
    labels.append('p=%d%%' % int(100 * p))

    # z = np.polyfit(x, y, 1)
    # f = np.poly1d(z)
    # plt.plot(x, f(x), color=colors[i])

plt.legend(series, labels, loc='upper left')
plt.xlabel('Attacker Addresses')
plt.ylabel('Honest Addresses')
plt.xlim(0, 30000)
plt.ylim(0, 4096)
plt.show()
