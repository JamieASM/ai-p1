# This file is holding everything that I can't fit into the other files in a way that works with my brain.

#*************** States ***************#

NOT_TERMINATED = -200
NOT_IMPLEMENTED = -100
NOT_FOUND = 0


#*************** Heuristic Functions ***************#

def h_AH1(node):
    """
    Heuristic functions for the AH1 mode.

    Parameters:
         node (Node)

    Returns:
        int: The total number of colours remaining in the grid.
    """

    return len(set().union(*node.state) - {'-'})


def h_AH2(node):
    """
    Heuristic functions for the AH1 mode.

    Parameters:
         node (Node)

    Returns:
        int: The total number of connected groups remaining, whose size is greater than 1.
    """

    return len(node.getSuccStates())


# *************** Printers *************** #

def toString(grid, c, end_with_new_line):
    """
    Converts a grid into a string, where each row ends with a specified character, 'c'.

    Parameters:
        grid (list): The grid.
        c (str): The character(s) that each row should end with. This does not include the final row.
        end_with_new_line (bool): If made true, the string will end with a newline character.

    Returns:
        str
    """

    n = len(grid)
    p = ""

    for i in range(n):
        for j in range(n):
            st = grid[i][j]  # add row characters
            p += st + ""

        if i < (n - 1):  # prevent a newline at the end
            p += c

    if end_with_new_line:
        p += "\n"

    return p


def printGrid(grid, end_with_new_line):
    """
    Prints the grid in the format:\n
    RGR\n
    RRR\n
    BGB

    Parameters:
        grid (list): The grid.
        end_with_new_line (bool): If made true, the printed string will end with a newline character.
    """

    print(toString(grid, "\n", end_with_new_line))
