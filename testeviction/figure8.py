"""
Monte-Carlo simulation:
eclipse probability for test-before-evict.
"""

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
        p_attacker = float(a) / (a + h)
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


random.seed(420)  # seed the random number generator to something... **sigh**.

# N = 1000	 # num of sims
N = 10000
colors = ('green', 'yellow', 'orange', 'red')
a_step = 800
h_step = 100
P = (.2, .4, .6, .8)  # churn rate
A = [x * a_step for x in range(int(30001 / a_step))]	 # attack IP  [0...30000]
H = [x * h_step for x in range(int(4096 / h_step))]	 # honest IP  [0...4096]
graph = {}

honest = 0
attacker = 1

for i, (h, p, a) in enumerate(jointsample(N, H, P, A)):

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
            graph[p][a, h] = 0
        else:
            graph[p][a, h] += 1

# create the plot
series = []
labels = []
plt.title('Eclipses vs. Attacker Resources')
for i, p in enumerate(sorted(graph)):
    x, y = zip(*graph[p])
    series.append(plt.scatter(x, y, color=colors[i], edgecolors=['black'] * len(x), marker='o'))
    labels.append('p=%d%%' % int(100 * p))

plt.legend(series, labels, loc='upper left')
plt.xlabel('Attacker Addresses')
plt.ylabel('Honest Addresses')
plt.xlim(0, 30000)
plt.ylim(0, 4096)
plt.show()
