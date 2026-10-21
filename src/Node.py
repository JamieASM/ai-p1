from copy import deepcopy

class Node:
    def __init__(self, parent, state):
        self.state = state
        self.parent = parent
        self.path_cost =  0 if parent is None else parent.path_cost + 1
        self.h = len(set().union(*self.state) - {'-'})

    # Defines the rules for two nodes to be equal. Here, nodes are considered
    # to be equal if their states are identical
    def __eq__(self, node_2):
        return self.state == node_2.state

    def getF(self):
        return self.h + self.path_cost

    def getH(self):
        return self.h

    def getState(self):
        return self.state

    def isGoal(self):
        grid = self.state

        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] != '-':
                    return False

        return True

    # Finds the successor states from the current node
    def getSuccStates(self):
        grid = self.state
        n = len(grid)

        succ_states = []
        explored = [] # contains the coordinates we have already checked

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
                count = 1 # counter for the connected colours

                for x_offset, y_offset in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                    x, y = (r + x_offset), (c + y_offset)

                    if inBounds(x, y, n) and isColour(colour, grid[x][y]):
                        count = visitNeighbour(count, possibleGrid, explored, x, y, colour)

                if count >= 2:
                    succ_states.append(compress(possibleGrid))

        return succ_states

def visitNeighbour(count, grid, explored, r, c, colour):
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

def inBounds(x, y, n):
    return 0 <= x < n and 0 <= y < n

def isColour(target, possible):
    return target == possible

def compress(grid):
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

    for c in range(n):
        if temp[c] == ['-' for _ in range(n)]:
            temp.append(temp.pop(c))

    grid = transform(temp)

    return grid

def transform(grid):
    n = len(grid)

    return [
        [ grid[r][c] for r in range(n) ]
        for c in range(n)
    ]