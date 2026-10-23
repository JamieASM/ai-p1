# This file is holding everything that I can't fit into the other files in a way that works with my brain.

#*************** States ***************#

NOT_TERMINATED = -200
NOT_IMPLEMENTED = -100
NOT_FOUND = 0

#*************** Heuristic Functions ***************#

def h_AH1(node):
    return len(set().union(*node.state) - {'-'})

def h_AH2(node):
    return len(node.getSuccStates())

# *************** Printers *************** #

def toString(grid, c, end_with_new_line):
    n = len(grid)
    p = ""

    for i in range(n):
        for j in range(n):
            st = grid[i][j]  # add row characters
            p += st + ""

        if i < (n - 1): # prevent a newline at the end
            p += c

    if end_with_new_line:
        p += "\n"

    return p

def printGrid(grid, end_with_new_line):
    print(toString(grid,"\n", end_with_new_line))


