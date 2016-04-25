from random import randint

def main(numBuckets=64, numIP=64, totalIP=100000, att=0.5, numAttacks=20):
    """
    numBuckets: (int) number of buckets in Tried table
    numIP: (int) number of IP addresses that fit into a bucket (aka "slots")
    totalIP: (int) total num of IPs in existance in simulation
    att: (float) Percentage of attacker IPs
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

    # insert attacker IP, hash to a bucket first, then hash to an index in the bucket
    for i in range(numAttacks):
        tempIP = randint(0,totalIP)
        triedTable[tempIP%numBuckets][tempIP%numIP] = tempIP

    # count number of inserted dattacker IPs
    for i in range(numBuckets):
        for j in range (numIP):
            if (triedTable[i][j] > boundary):
                attackerWins += 1

    return attackerWins, triedTable

if __name__ == "__main__":
    wins, _ = main()