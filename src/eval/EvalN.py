"""
Definition: N refers to the size of the grid.

Evaluating:
    - Path Cost against N.
    - Time complexity (number of moves) against N.

Using randomised grids, so results may differ between runs.

Running this file will produce a csv file "N_results.csv".
"""
import csv
import random

from eval.common import runP1main, ALGORITHMS

# *************** Constants *************** #

# For data generation
SIZES = [3, 4, 5, 6, 7, 8, 9]
COLOURS = list("RGB")
GRIDS_PER_SIZE = range(10)
TIMEOUT = 60

# For the csv file
CSV = "../N_results.csv"

# *************** Generators *************** #

def makeGrid(size):
    """
    Generates a grid for a given grid size.

    Parameters:
        size (int): The intended size of the grid

    Returns:
        list: The newly created grid
    """

    return "".join(random.choice(COLOURS) for _ in range(size ** 2))

def startN():
    """
    Runs a wide range of varying sized grids, appends them to a csv file and generates graphs with their key information.
    """

    # set up csv file.
    with open(CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["N", "colours_count", "conf", "algo", "cost", "moves_count"])

        # Create and run every grid
        for n in SIZES:
            for _ in GRIDS_PER_SIZE:
                grid = makeGrid(n)
                for algo in ALGORITHMS:
                    cost, moves = runP1main(algo, grid)
                    w.writerow([n, len(COLOURS), grid, algo, cost, moves])
                    f.flush()