from Frontier import Frontier
from Node import Node
from Common import NOT_FOUND, printGrid

# n = number of rows / columns
# grid = The initial grid configuration
# verbose = will every step be printed out
def searchAH1(grid, verbose):
    initial_node = Node(None, grid)
    frontier = Frontier(initial_node)
    explored = []
    nodes_explored = 0

    while not frontier.isEmpty():
        if verbose:
            for n in frontier.getNodes():
                printFrontierNode(n, n.getH(), n.getF())

        nd = frontier.remove()
        explored.append(nd.getState())
        nodes_explored += 1

        if verbose:
            printGrid(nd.getState(), False)
            print("%")

        if nd.isGoal():
            if verbose:
                print(nodes_explored)

            return nd.getF()
        else:
            succ_states = nd.getSuccStates()
            succ_nodes = []

            for s in succ_states:
                if s not in explored:
                    succ_nodes.append(Node(nd, s))

        frontier.insertPriority(succ_nodes)

    if verbose:
        print(nodes_explored)
    return NOT_FOUND

def printFrontierNode(node, h, f):
    grid = node.state
    p = ""

    for i in range(len(grid)):
        for j in range(len(grid)):
            p += grid[i][j] + ""

    print(f'[{p}:{h}:{f}]')