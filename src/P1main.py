import math
import sys

from src.Frontier import Frontier
from src.Node import AH1_Node

NOT_TERMINATED = -200
NOT_IMPLEMENTED = -100
NOT_FOUND = 0

# Prints out a formatted version of the grid 
def printGrid(grid):
	p = ""
    
	for i in range(len(grid)):
		for j in range(len(grid)):
			st = grid[i][j] #add row characters
			p += st + ""

		p += "\n" #new row 

	print(p)

# Entry point to the search algorithm
# n = number of rows / columns
# grid = The initial grid configuration
# time_limit = the max amount of time we can wait for a response
# verbose = will every step be printed out
def runSearch(algo, n, colours, grid, time_limit, verbose):
	#implement your search
	match algo:
		case "AH1":
			return searchAHI(n, colours, grid, time_limit, verbose)
		case "AH2":
			return NOT_IMPLEMENTED
		case "AH3":
			return NOT_IMPLEMENTED
	return NOT_IMPLEMENTED

def searchAHI(n, colours, grid, time_limit, verbose):
	initial_node = AH1_Node(None, grid)
	frontier = Frontier(initial_node)
	explored = set()
	
	while not frontier.isEmpty():
		if verbose:
			print()

		nd = frontier.remove()
		explored.add(nd)

		if nd.isGoal():
			return nd
		else:
			succ_states = nd.getSuccStates()
			succ_nodes = []
			
			for s in succ_states:
				if not s in explored:
					succ_nodes.append(AH1_Node(nd, s))

		frontier.insertPriority(succ_nodes)

	return NOT_FOUND


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
printGrid(grid)

#*************** Run and Output ***************#

#run the search 
pathCost=runSearch(algo, n, colours, grid, time_limit, verbose)

if(verbose): # TODO
    #remember to include required printing for verbose mode
	pass

#print the path cost 
print(pathCost)

