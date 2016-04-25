from random import randint

def main(att=0.5, totalIP=100000, numBuckets=256, numIP=64, numAttacks=20):
    """
    att: (float) Percentage of attacker IPs
    totalIP: (int) total num of IPs in existance in simulation
    numBuckets: (int) number of buckets in Tried table (4x more in this sim)
    numIP: (int) number of IP addresses that fit into a bucket (aka "slots")
    numAttacks: (int) number of attacker attempts to insert in tried table
    """
    #Percentage of honest IPs
    hon=1.0-att
    # IPs less than this are honest, greater than this are attacker
    boundary = hon*totalIP
    # number of successful attacker inserts into tried table
    attackerWins = 0

    # Matrix of all IP adresses in tried table initialized to index in table
    triedTable = [[-1 for x in range(numIP)] for y in range(numBuckets)]

    # insert attacker IP, hash to a bucket first, then randomly evict a previous IP in the bucket
    for i in range(numAttacks):
        tempIP = randint(0,totalIP)
        triedTable[tempIP%numBuckets][randint(0,numIP)-1] = tempIP

    # count number of inserted attacker IPs
    for i in range(numBuckets):
        for j in range (numIP):
            if (triedTable[i][j] > boundary):
                attackerWins += 1

    return attackerWins, triedTable

if __name__ == "__main__":
    wins, table = main()
    print wins