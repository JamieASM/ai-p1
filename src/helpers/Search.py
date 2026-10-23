from helpers.Frontier import Frontier
from helpers.Node import Node
from helpers.utils import NOT_FOUND, printGrid


def search(grid, verbose, hFunc):
    """
    Performs the A* Algorithm.

    Args:
        grid(list): The initial grid.
        verbose(bool): When enabled, extra debugging information is printed to standard output.
        hFunc: A heuristic function.

    Returns:
        int: Path cost
    """

    initial_node = Node(None, grid, hFunc)
    frontier = Frontier(initial_node)
    explored = []

    while not frontier.isEmpty():
        if verbose:
            for n in frontier.getNodes():
                n.printFrontierNode()

        nd = frontier.remove()
        explored.append(nd.getState())

        if verbose:
            printGrid(nd.getState(), False)
            print("%")

        if nd.isGoal():
            if verbose:
                print(len(explored))
            return nd.getPathCost()

        else:
            succ_states = nd.getSuccStates()
            succ_nodes = []

            for s in succ_states:
                if s not in explored:
                    succ_nodes.append(Node(nd, s, hFunc))

            frontier.insertPriority(succ_nodes)

    if verbose:
        print(len(explored))

    return NOT_FOUND
