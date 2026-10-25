"""
Definition: N refers to the number of colours in the grid.

Evaluating:
    - Path Cost against D.
    - Time complexity (number of moves) against D.

Using randomised grids, so results may differ between runs.

Running this file will produce a csv file "D_results.csv" and two graphs "cost_vs_d" and "time_vs_d".
"""

# TODO: Change for D

import csv
import random
import subprocess
import sys

# *************** Constants *************** #

SIZES = [3, 4, 5, 6, 7, 8, 9]
COLOURS = list("RGB")
GRIDS_PER_SIZE = range(10)
ALGORITHMS = ["AH1", "AH2"]
TIMEOUT = 60

# *************** Generator *************** #

def makeGrid(size):
    """
    Generates a grid for a given grid size.

    Parameters:
        size (int): The intended size of the grid

    Returns:
        list: The newly created grid
    """

    return "".join(random.choice(COLOURS) for _ in range(size ** 2))

def runP1main(algo, grid):

    try:
        res = subprocess.run(
            [sys.executable, "P1main.py", algo, grid, True], # Running in verbose to get the number of moves
            capture_output=True,
            text=True,
            timeout=TIMEOUT
        )
        moves, cost = res.stdout.strip().splitlines()[-2:]
    except subprocess.TimeoutExpired:
        cost, moves = -200, 0

    return cost, moves

def startD():
    # set up csv file.
    with open("N_results.csv", "w", newline="") as f:
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