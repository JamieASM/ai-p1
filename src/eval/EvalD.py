"""
Definition: N refers to the number of colours in the grid.

Evaluating:
    - Path Cost against D.
    - Time complexity (number of moves) against D.

Using randomised grids, so results may differ between runs.

Running this file will produce a csv file "D_results.csv" and two graphs "cost_vs_d" and "time_vs_d".
"""
from common import runP1main, ALGORITHMS

import csv
import random
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt

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

def makeGraph():
    colour_sizes = range(1, len(COLOURS))

    # Read CSV and gather data
    with open(CSV, 'r') as f:
        data = csv.DictReader(f)

        costs = defaultdict(list)  # key = (Algo, colours_count), value = list of costs != -200, 0
        moves = defaultdict(list)  # key = (Algo, colours_count), value = list of moves
        total = defaultdict(int)  # key = (Algo, colours_count), value = number of runs
        not_founds = defaultdict(int)  # key = (Algo, colours_count), value = num cost == 0
        timeouts = defaultdict(int)  # key = (Algo, colours_count), value = num cost == -200

        for r in data:
            key = (r["algo"], int(r["colours_count"]))
            c = int(r["cost"])
            total[key] += 1

            if c == 0:
                not_founds[key] += 1
            elif c == -200:
                timeouts[key] += 1
            else:
                costs[key].append(c)
                moves[key].append(int(r["moves_count"]))

        # set up our plots (4)
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))

        # Want a plot of mean path cost vs grid size (AH1 / AH2 separate lines)
        # costs per N != -200 or 0 averaged mapped to grid size
        for a in ALGORITHMS:
            x = [n for n in colour_sizes if costs[(a, n)]]
            yc = [sum(costs[(a, n)]) / len(costs[(a, n)]) for n in x]
            ym = [sum(moves[(a, n)]) / len(moves[(a, n)]) for n in x]
            ax1.plot(x, yc, marker="o", label=a)
            ax2.plot(x, ym, marker="o", label=a)

        ax1.set_xlabel("Number of colours D")
        ax1.set_ylabel("Mean path cost")
        ax1.set_title("Path cost vs number of colours (solved grids only)")
        ax1.set_xticks(colour_sizes)
        ax1.legend()
        ax1.grid(alpha=0.3)

        # Want a plot of mean moves vs grid size (AH1 / AH2 separate lines)
        ax2.set_xlabel("Number of colours D")
        ax2.set_ylabel("Mean number of moves")
        ax2.set_title("Moves vs number of colours (solved grids only)")
        ax2.set_xticks(colour_sizes)
        ax2.legend()
        ax2.grid(alpha=0.3)

        # Want a box plot to show how many of each grid size had successful results (FYI)
        a = ALGORITHMS[0]
        solved = [len(costs[(a, n)]) for n in colour_sizes]
        unsolved = [not_founds[(a, n)] for n in colour_sizes]
        to = [timeouts[(a, n)] for n in colour_sizes]
        ax3.bar(colour_sizes, solved, label="solved")
        ax3.bar(colour_sizes, unsolved, bottom=solved, label="unsolvable (0)")
        ax3.bar(colour_sizes, to, bottom=[s + u for s, u in zip(solved, unsolved)], label="timeout (-200)")
        ax3.set_xlabel("Number of colours D")
        ax3.set_ylabel("Number of grids")
        ax3.set_title(f"Outcomes per size ({a})")
        ax3.set_xticks(colour_sizes)
        ax3.legend()

        a = ALGORITHMS[1]
        solved = [len(costs[(a, n)]) for n in colour_sizes]
        unsolved = [not_founds[(a, n)] for n in colour_sizes]
        to = [timeouts[(a, n)] for n in colour_sizes]
        ax4.bar(colour_sizes, solved, label="solved")
        ax4.bar(colour_sizes, unsolved, bottom=solved, label="unsolvable (0)")
        ax4.bar(colour_sizes, to, bottom=[s + u for s, u in zip(solved, unsolved)], label="timeout (-200)")
        ax4.set_xlabel("Number of colours D")
        ax4.set_ylabel("Number of grids")
        ax4.set_title(f"Outcomes per size ({a})")
        ax4.set_xticks(colour_sizes)
        ax4.legend()

        plt.tight_layout()
        plt.savefig("d.png", dpi=200)

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

    # finally, make graph
    makeGraph()