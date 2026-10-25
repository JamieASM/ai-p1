"""
Definition: N refers to the number of colours in the grid.

Evaluating:
    - Path Cost against D.
    - Time complexity (number of moves) against D.

Using randomised grids, so results may differ between runs.

Running this file will produce a csv file "D_results.csv" and two graphs "cost_vs_d" and "time_vs_d".
"""
from eval.common import runP1main, ALGORITHMS

import csv
import random

# *************** Constants *************** #

# For data generation
SIZE = 6
COLOURS = list("ABCDEFGHI") # 9 colours
GRIDS_PER_COLOUR = range(10)
TIMEOUT = 60

# For the csv file
CSV = "../D_results.csv"

# *************** Generators *************** #

def makeGrid(c):
    """
    Generates a grid for a given grid size.

    Parameters:
        c (list): The intended colours of the grid

    Returns:
        list: The newly created grid
    """

    return "".join(random.choice(c) for _ in range(SIZE ** 2))

def startD():
    """
    Runs a wide range of varying sized grids, appends them to a csv file and generates graphs with their key information.
    """

    # set up csv file.
    with open(CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["N", "colours_count", "conf", "algo", "cost", "moves_count"])

        # Create and run every grid
        for c in range(1, len(COLOURS)):
            for _ in GRIDS_PER_COLOUR:
                grid = makeGrid(COLOURS[:c])
                for algo in ALGORITHMS:
                    cost, moves = runP1main(algo, grid)
                    w.writerow([SIZE, len(set(grid)), grid, algo, cost, moves])
                    f.flush()