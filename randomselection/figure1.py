# -*- coding: utf-8 -*-

"""
Plot of Outgoing Connections v. Pr[Selecting from Tried]
"""

from randomselection import utils
import numpy as np
from matplotlib import pyplot as plt

np.random.seed(0)
rho_sample = (.001, .01, .1, .5, 1, 2, 10, 100, 1000)
omega_sample = (0, 1, 2, 3, 4, 5, 6, 7)
lines = [[0 for j in range(len(omega_sample))]
         for i in range(len(rho_sample))]

for i, rho in enumerate(rho_sample):
    for j, omega in enumerate(omega_sample):
        tried = utils.triedprob(rho=rho, omega=omega)
        lines[i][j] = tried

plt.title('Probability of Selecting from Tried')
plt.xlabel('Number of outgoing connections')
plt.ylabel('Pr[Selecting from Tried Table]')
for i, line in enumerate(lines):
    plt.plot(omega_sample, line, linewidth=2., label=u'p=%s' % (u'%.3f' % rho_sample[i]).rstrip(u'0').rstrip(u'.'))
plt.legend(loc='upper right')
plt.savefig('../figures/figure-1.png')