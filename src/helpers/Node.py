from copy import deepcopy

from helpers.utils import toString


class Node:
    """
    A class representing a Node.

    Attributes:
        state (list): The node's grid configuration.
        parent (Node): The node's parent.
        path_cost (int): The number of moves it has taken to get to the node.
        h (int): The heuristic value of the node.
    """

    def __init__(self, parent, state, hFunc):
        """
        Initialises a Node object.

        Parameters:
            parent (Node | None): The node's parent. If it is the initial node, None should be passed in.
            state (list): The node's grid configuration.
            hFunc: A function which calculates the heuristic.
        """

        self.state = state
        self.parent = parent
        self.path_cost = 0 if parent is None else parent.getPathCost() + 1
        self.h = hFunc(self)

    # *************** Getters for Attributes ***************#

    def getState(self):
        """
        Returns:
            list: The Node object's grid configuration.
        """

        return self.state

    def getPathCost(self):
        """
        Returns:
            int: The Node object's path cost.
        """

        return self.path_cost

    def getF(self):
        """
        Returns:
            int: The Node object's f value. This the sum of the heuristic and the path cost.
        """

        return self.h + self.path_cost

    def isGoal(self):
        """
        Returns:
            bool: True if the grid is empty, false otherwise.
        """

        n = len(self.state)
        return self.state == [["-" for _ in range(n)] for _ in range(n)]

    def getSuccStates(self):
        """
        Searches the current grid configuration to find any possible block groups that can be removed

        Returns:
            list: All possible next moves from the current grid configuration.
        """

        grid = self.state
        n = len(grid)

        succ_states = []
        explored = []  # contains the coordinates we have already checked

        for r in range(n):
            for c in range(n):
                colour = grid[r][c]

                # skip if we have already explored this node, or it is empty
                if [r, c] in explored or colour == '-':
                    continue

                # Otherwise, set up the environment to find the next possible path
                explored.append([r, c])
                possibleGrid = deepcopy(grid)
                possibleGrid[r][c] = '-'
                count = 1  # counter for the connected colours

                for x_offset, y_offset in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                    x, y = (r + x_offset), (c + y_offset)

                    if inBounds(x, y, n) and isColour(colour, grid[x][y]):
                        count = visitNeighbour(count, possibleGrid, explored, x, y, colour)

                if count >= 2:
                    succ_states.append(compress(possibleGrid))

        return succ_states

    # *************** Rules ***************#

    def __eq__(self, node_2):
        """
        Compares two Node objects. Nodes are considered equal when their states are the same

        Parameters:
            node_2 (Node): the Node object to compare.

        Returns:
            bool
        """

        return self.state == node_2.state

    # *************** Printer *************** #

    def printFrontierNode(self):
        """
        Prints the Node object in the format outlined for frontier nodes in the spec.
        """

        p = toString(self.state, "", False)

        print(f'[{p}:{self.h}:{self.getF()}]')


#*************** Helper functions for getSuccStates() ***************#

def inBounds(x, y, n):
    """
    Checks if the x and y coordinates are the in the bounds of a grid.

    Parameters:
        x (int): X coordinate
        y (int): Y coordinate
        n (int): Length of the grid. Assumes the grid has an equal number of rows and columns.

    Returns:
        bool
    """

    return 0 <= x < n and 0 <= y < n


def isColour(c1, c2):
    """
    Checks if the colours match.

    Parameters:
        c1 (str): The first colour.
        c2 (str): The second colour.

    Returns:
        bool
    """

    return c1 == c2


def visitNeighbour(count, grid, explored, r, c, colour):
    """
    Recursive function. Checks a neighbouring node to see if there are any more nodes of a particular colour surrounding it.

    Parameters:
         count (int): The current size of the chain of same-colour grid squares.
         grid (list): The current grid configuration.
         explored (list): All coordinates that have already been seen across all searches. Avoids redundant checks.
         r (int): The current row being checked.
         c (int): The current column being checked.
         colour (str): The target colour for the neighbours to also have.

    Returns:
        count
    """

    # there is a chance that we have already seen this (due to backtracking)
    if [r, c] in explored:
        return count

    explored.append([r, c])
    grid[r][c] = '-'
    count += 1

    for x_offset, y_offset in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        x, y = (r + x_offset), (c + y_offset)

        if inBounds(x, y, len(grid)) and isColour(colour, grid[x][y]):
            count = visitNeighbour(count, grid, explored, x, y, colour)

    return count


def compress(grid):
    """
    Reorders the grid. Empty rows are moved upwards whilst empty columns are moved to the right.

    Parameters:
        grid (list): The current grid configuration

    Returns:
        list: The newly compressed grid
    """

    n = len(grid)

    # sink each non-empty block
    for col in range(n):
        # create a list of the non-empty elements within the column
        non_empty = [grid[row][col] for row in range(n) if grid[row][col] != '-']
        diff = n - len(non_empty)

        # move down blocks
        for row in range(n):
            grid[row][col] = '-' if row < diff else non_empty[row - diff]

    # move each block right to left
    temp = transform(grid)

    i = 0
    target = ["-" for _ in range(n)]
    empties = temp.count(target)

    while i < n and empties > 0:
        if temp[i] == target:
            temp.append(temp.pop(i))
            empties -= 1 # found an instance
        else:
            i += 1

    grid = transform(temp)

    return grid


def transform(grid):
    """
    Swaps a particular grid's rows and columns.

    Parameters:
        grid (list): The grid to be transformed

    Returns:
        list: The newly transformed grid
    """

    n = len(grid)

    return [
        [grid[r][c] for r in range(n)]
        for c in range(n)
    ]
