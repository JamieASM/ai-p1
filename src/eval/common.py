import subprocess
import sys


def runP1main(algo, grid):
    """
    Runs P1main for a given algorithm and grid configuration.

    Parameters:
         algo (str): The algorithm to run.
         grid (list): The grid configuration.

    Returns:
        list: Cost, Moves
    """

    try:
        res = subprocess.run(
            [sys.executable, "P1main.py", algo, grid, "verbose"], # Running in verbose to get the number of moves
            capture_output=True,
            text=True,
            timeout=60
        )
        moves, cost = res.stdout.strip().splitlines()[-2:]
    except subprocess.TimeoutExpired:
        cost, moves = -200, 0

    return cost, moves