"""
Monte-Carlo simulation:
eclipse probability for test-before-evict.
"""

import addresses
import tables
import node


N = 100
attack_size_values = (0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000)
p_values = (.2, .4, .6, .8)  # churn rate

attack_addrs = [addresses.SimpleAddress.randomaddress()
                for _ in range(8000)]

n = node.Node(
    newtable=tables.NewTable(),
    triedtable=tables.TriedTable(),
    outpeers=8)

for i in range(N):
    for addrs in attack_size_values:
        n.clear()
        a = addrs
        while a > 0:
            a -= 1