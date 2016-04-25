"""
Monte-Carlo simulation:
eclipse probability for test-before-evict.
"""

import itertools
import random

def triedprob(rho, omega):
    """Probability an IP is seeded from the tried table.

    :param rho: (float) proportional size of tried table to new table.
    :param omega: (float) number of connected outgoing peers
    """
    rho_freq = math.sqrt(rho) * (9 - omega)
    return rho_freq / (1 + omega + rho_freq)

random.seed(420)

N = 100	# num of sims
P = (.2, .4, .6, .8)  # churn rate
A = [x for x in range(0,30001)]	# attack IP
H = [x for x in range(0,2501)]	# honest IP

graph = [[None for x in range(A)] for y in range(P)]

honest = 0
attacker = 0

for n in range (N):
	winCount = 0
	for p, h, a in itertools.product(P, H, A):
		# table of outgoing connections from the victim
  		outgoing = []

    	# Matrix of all IP adresses in tried table initialized to index in table
    	triedTable = [[None for x in range(64)] for y in range(64)]
    	triedCount = 0

    	# insert honest in random posions of tried table
    	for _ in range(h):
    		# 0 represents honest IP
    		bucket = randint(0,64)
    		slot = randint(0,64)
    		if triedTable[bucket][slot] is not None: 
    			triedCount += 1
    		triedTable[bucket][slot] = honest 

    	# insert attacker IPs into tried Table
    	for _ in range(a):
    		# 1 represents attack IP
    		bucket = randint(0,64)
    		slot = randint(0,64)
    		if triedTable[bucket][slot] is not None: 
    			triedCount += 1
    		triedTable[bucket][slot] = attacker

    	# fill outgoing connections table
    	while len(outgoing) < 8:
    		omega = len(outgoing)
    		rho = triedCount/256
    		# if tried is selected
    		if triedprob(rho, omega) <= random.random():
    			# append random IP from tried table
    			bucket = randint(0,64)
    			slot = randint(0,64)
    			tempIP = triedTable[bucket][slot]
    			if tempIP == honest:
    				if random.random() <= p:
    					outgoing.append(honest)
    			else:
    				outgoing.append(attacker)

    		else:
    			# append from new table (attacker IP)
    			outgoing.append(attacker)

    	if sum(outgoing) == 8*attacker:
    		winCount += 1
    		graph[p][a] += 1





