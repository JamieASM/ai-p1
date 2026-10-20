import math
import signal
import sys

from Search import searchAH1
from Common import NOT_IMPLEMENTED, NOT_TERMINATED, printGrid

# Entry point to the search algorithm
def runSearch(algo, n, colours, grid, time_limit, verbose):
	# set up the timer
	signal.signal(signal.SIGALRM, handle_timeout)
	signal.alarm(time_limit)

	try:
		#implement your search
		match algo:
			case "AH1":
				return searchAH1(grid, verbose)
			case "AH2":
				return NOT_IMPLEMENTED
			case "AH3":
				return NOT_IMPLEMENTED
		return NOT_IMPLEMENTED
	except TimeoutError:
		return NOT_TERMINATED

def handle_timeout(signum, frame):
	raise TimeoutError()

# START OF PROGRAM
if len(sys.argv) < 2:
	print("usage: python3 P1main.py <AH1|AH2|AH3> <conf> [<verbose>]")
	sys.exit()

#*************** Process Input ***************#

#assume problem is correctly specified, set the problem components

algo = sys.argv[1] # algorithm chosen
conf = sys.argv[2] # configuration

time_limit = 60 #run at most for 60s
verbose = True if 'verbose' in sys.argv else False 

n = int(math.sqrt(len(conf))) # number or rows/columns (assumed to be a square)

grid = [[None] * n for _ in range(n)]

colours = set()

for x in range(n):
	for y in range(n):
		grid[x][y] = conf[n * x + y]
		colours.add(grid[x][y])

#*************** Print settings ***************#

print("Algorithm: "+algo)
print("Grid Size: "+str(n))
print("Colours: "+str(len(colours)))
print("Conf:\n")
printGrid(grid, True)

#*************** Run and Output ***************#

#run the search 
pathCost = runSearch(algo, n, colours, grid, time_limit, verbose)

#print the path cost 
print(pathCost)

