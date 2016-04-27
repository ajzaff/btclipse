"""
Monte-Carlo simulation:
eclipse probability for test-before-evict.
"""

import numpy as np
import random
from random import randrange
import math
import matplotlib.pyplot as plt

random.seed(420)  # seed the random number generator to something... **sigh**.

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


def testsampleips(a, h, p, n=None, tablesize=4096):
    """Samples the IP to place in a given table cell.

    :param a: (int) attacker IPs
    :param h: (int) honest IPs
    :param tablesize: (int) the size of the tried table
    :return: yields a stream of (bucket, slot) => IP
    """
    a = round(a * (1 - p))
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


def sizemap(sizes, base=3):
    return tuple(map(lambda s: min(100, max(4, base * s)), sizes))


N = 400000
colors = ('blue', 'purple', 'pink', 'black')
regcolors = ('blue', 'purple', 'pink', 'gray')
P = (.2, .4, .6, .8)  # churn rate

honest = 0
attacker = 1

# Plot figures
fig = plt.figure()
ax1 = fig.add_subplot(212)
ax2 = fig.add_subplot(211)

# start sim 1
a_step = 200
h_step = 20
A = [x * a_step for x in range(round(35001 / a_step))]	 # attack IP  [0...30000]
H = [x * h_step for x in range(round(5000 / h_step))]	 # honest IP  [0...4096]
graph = {}

for (h, p, a) in jointsample(N, H, P, A):

    eclipse = True
    for _, ip in testsampleips(a, h, p, n=8):
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

# figure 1
for i, p in enumerate(sorted(graph)):
    points, size = zip(*graph[p].items())
    x, y = zip(*points)
    ax2.scatter(x, y,
                color=colors[i],
                sizes=sizemap(size),
                marker='o')

    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)
    ax2.plot(x, f(x),
             color=regcolors[i],
             linewidth=4.)

ax2.set_ylabel('Honest Addresses')
ax2.set_xlim(0, 30000)
ax2.set_ylim(0, 2500)

# start sim 2
a_step = 50
h_step = 100
A = [x * a_step for x in range(round(12001 / a_step))]	 # attack IP  [0...8000]
H = [y * h_step for y in range(round(8001 / h_step))]	 # honest IP  [0...4000]
graph = {}

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

# figure 2
series = []
labels = []
ax1.set_title('Eclipses vs. Attacker Resources')
for i, p in enumerate(sorted(graph)):
    points, size = zip(*graph[p].items())
    x, y = zip(*points)
    series.append(
        ax1.scatter(x, y,
                    color=colors[i],
                    sizes=sizemap(size),
                    marker='o'))
    labels.append('p=%d%%' % int(100 * p))
    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)
    ax1.plot(x, f(x),
             color=regcolors[i],
             linewidth=4.)
ax1.legend(series, labels, loc='lower right', prop={'size': 6})
ax1.set_xlabel('Adversarial Addresses')
ax1.set_ylabel('Honest Addresses')
ax1.set_xlim(0, 8000)
ax1.set_ylim(0, 4000)


# save figure
fig.savefig('../figures/figure-8.png')
