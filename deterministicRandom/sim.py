from random import randint

def main():
	# number of buckets in Tried table
	numBuckets = 64
	# number of IP addresses that fit into a bucket
	numIP = 64

	# total num of IPs in existance in simulation
	totalIP=100000
	#Percentage of attacker IPs
	att=0.5
	#Percentage of honest IPs
	hon=1.0-att
	# IPs less than this are honest, greater than this are attacker
	boundary = hon*totalIP
	# number of attacker attempts to insert in tried table
	numAttacks = 20
	# number of successful attacker inserts into tried table
	attackerWins = 0

	# Matrix of all IP adresses in tried table initialized to index in table
	triedTable = [[x+(y*numIP) for x in range(numIP)] for y in range(numBuckets)]

	# insert attacker IP, hash to a bucket first, then hash to an index in the bucket
	for i in range(numAttacks):
		tempIP = randint(0,totalIP)
		triedTable[tempIP%numBuckets][tempIP%numIP] = tempIP

	# count number of inserted attacker IPs
	for i in range(numBuckets):
		for j in range (numIP):
			if (triedTable[i][j] > boundary):
				attackerWins += 1

	print triedTable
	print attackerWins

if __name__ == "__main__":
    main()