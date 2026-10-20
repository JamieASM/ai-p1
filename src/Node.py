class Node:
    def __init__(self, parent, state):
        self.state = state
        self.parent = parent
        self.path_cost =  0 if parent is None else parent.path_cost + 1

    # Defines the rules for two nodes to be equal. Here, nodes are considered
    # to be equal if their states are identical
    def __eq__(self, node_2):
        return self.state == node_2.state

    def getPathCost(self):
        return self.path_cost

    def getState(self):
        return self.state

    def setCost(self, amount):
        if amount > 0:
            self.path_cost = amount

    def isGoal(self):
        grid = self.state

        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] != '-':
                    return False

        return True

    # Finds the successor states from the current node
    def getSuccStates(self):
        def isValid(x, y, colour, explored):
            return 0 <= x < len(grid) and 0 <= y < len(grid) and (x, y) not in explored and grid[x][y] == colour

        grid = self.state
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

                    for x_dir, y_dir in [-1, 0], [1, 0], [0, -1], [0, 1]:
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
