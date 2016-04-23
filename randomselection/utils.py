"""
Implements random selection algorithm utils
"""

import math


def triedprob(rho, omega):
    """Probability an IP is seeded from the tried table.

    :param rho: (float) proportional size of tried table to new table.
    :param omega: (float) number of connected outgoing peers
    """
    rho_freq = math.sqrt(rho) * (9 - omega)
    return rho_freq / (1 + omega + rho_freq)


def acceptprob(i, tau):
    """Probability of accepting entry ``e''

    :param e: (tables.PeerEntry) the candidate entry
    :param i: (int) number of rejected entries
    :param tau: (duration) the elapsed time
    """
    return min(1, 1.2 ** i / (1 + tau))