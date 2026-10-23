import math
import signal
import sys

from helpers.Search import search
from helpers.utils import NOT_IMPLEMENTED, NOT_TERMINATED, h_AH1, h_AH2, printGrid


def runSearch(algo, grid, time_limit, verbose):
	"""
	    Entry point to the search algorithm. Selects the heuristic to use, according 'algo'.

	    Args:
	        algo (str): The heuristic algorithm.
	        grid (list): The initial grid.
	        time_limit (int): The number of seconds the algorithm can run before timing out.
	        verbose (bool): When enabled, extra debugging information is printed to standard output.

	    Returns:
	        int: Path cost
	"""

	# set up the timer
	signal.signal(signal.SIGALRM, handle_timeout)
	signal.alarm(time_limit)

	try:
		# implement your search
		match algo:
			case "AH1":
				return search(grid, verbose, h_AH1)
			case "AH2":
				return search(grid, verbose, h_AH2)
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
pathCost = runSearch(algo, grid, time_limit, verbose)

#print the path cost 
print(pathCost)

