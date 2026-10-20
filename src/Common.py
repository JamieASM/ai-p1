NOT_TERMINATED = -200
NOT_IMPLEMENTED = -100
NOT_FOUND = 0

# Prints out a formatted version of the grid
def printGrid(grid, newline):
    p = ""

    for i in range(len(grid)):
        for j in range(len(grid)):
            st = grid[i][j]  # add row characters
            p += st + ""

        if i < (len(grid) - 1) or newline:
            p += "\n"  # new row

    print(p)