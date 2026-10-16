NOT_IMPLEMENTED = -100

class Node:
    def __init__(self, parent, state):
        self.state = state
        self.parent = parent
        self.path_cost =  0 if parent is None else parent.path_cost + self.getCost(parent.state)

    # Defines the rules for two nodes to be equal. Here, nodes are considered
    # to be equal if their states are identical
    def __eq__(self, node_2):
        return self.state == node_2.state

    def getPathCost(self):
        return self.path_cost

    def getCost(self, parent_state):
        return 1

    def isGoal(self):
        grid = self.state

        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] != '-':
                    return False

        return True

# The AH1 node, whose path cost is just 1
class AH1_Node(Node):
    def __init__(self, parent, state):
        super().__init__(parent, state)

# The AH2 node, whose path cost is {}
class AH2_Node(Node):
    def __init__(self, parent, state):
        super().__init__(parent, state)

    def getCost(self, parent_state):
        return NOT_IMPLEMENTED

# The AH3 node, whose path cost is {}
class AH3_Node(Node):
    def __init__(self, parent, state):
        super().__init__(parent, state)

    def getCost(self, parent_state):
        return NOT_IMPLEMENTED

# Finds the successor states from the current node
def getSuccStates(grid):
    def isValid(x, y, colour, explored):
        return 0 <= x < len(grid) and 0 <= y < len(grid) and (x, y) not in explored and grid[x][y] == colour

    n = len(grid)
    explored = set()
    succ_states = []

    for x in range(n):
        for y in range(n):
            colour = grid[x][y]

            if colour == '-' or (x, y) in explored:
                continue

            block_group = []
            possible_nodes = [(x, y)]
            explored.add((x, y))

            while possible_nodes:
                x_pos, y_pos = possible_nodes.pop()
                block_group.append((x_pos, y_pos))

                directions = [-1, 1, 0, 0]

                for x_dir in directions:
                    for y_dir in reversed(directions):
                        new_x, new_y = (x_pos + x_dir), (y_pos + y_dir)

                        if isValid(new_x, new_y, colour, explored):
                            explored.add((new_x, new_y))
                            possible_nodes.append((new_x, new_y))

            if len(block_group) > 0:
                possible_state = [row[:] for row in grid]

                for a, b in block_group:
                    possible_state[a][b] = '-'

                succ_states.append(compress(possible_state))

    return succ_states

def compress(grid):
    n = len(grid)

    # sink each non-empty block
    for col in range(n):
        # create a list of the non-empty elements within the column
        non_empty = [grid[row][col] for row in range(n) if grid[row][col] != '-']

        # skip if there are no non-empty elements
        if len(non_empty) == 0:
            continue

        # move down blocks
        for row in range(n):
            diff = n - len(non_empty)
            grid[row][col] = ['-' if row < diff else non_empty[row - diff]]

    # move each block right to left
    for row in range(n):
        non_empty = [grid[row][col] for col in range(n) if grid[row][col] != '-']

        # skip if there are no non-empty elements
        if len(non_empty) == 0:
            continue

        # move blocks right to left
        for col in range(n, -1):
            diff = n - len(non_empty)
            grid[row][col] = ['-' if col > diff else non_empty.pop()] # replace with last element of list (if applicable)

    return grid