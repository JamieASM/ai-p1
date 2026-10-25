import csv
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt

SIZES = [3, 4, 5, 6, 7, 8, 9]
ALGORITHMS = ["AH1", "AH2"]


def makeGraphN():
    # Read CSV and gather data
    with open("N_results.csv", 'r') as f:
        data = csv.DictReader(f)

        costs = defaultdict(list)  # key = (Algo, size), value = list of costs != -200, 0
        moves = defaultdict(list)  # key = (Algo, size), value = list of moves
        total = defaultdict(int)  # key = (Algo, size), value = number of runs
        not_founds = defaultdict(int)  # key = (Algo, size), value = num cost == 0
        timeouts = defaultdict(int)  # key = (Algo, size), value = num cost == -200

        for r in data:
            key = (r["algo"], int(r["N"]))
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
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11, 4))

        # Want a plot of mean path cost vs grid size (AH1 / AH2 separate lines)
        # costs per N != -200 or 0 averaged mapped to grid size
        for a in ALGORITHMS:
            x = [n for n in SIZES if costs[(a, n)]]
            yc = [sum(costs[(a, n)]) / len(costs[(a, n)]) for n in x]
            ym = [sum(moves[(a, n)]) / len(moves[(a, n)]) for n in x]
            ax1.plot(x, yc, marker="o", label=a)
            ax2.plot(x, ym, marker="o", label=a)

        ax1.set_xlabel("Grid size N")
        ax1.set_ylabel("Mean path cost")
        ax1.set_title("Path cost vs grid size (solved grids only)")
        ax1.set_xticks(SIZES)
        ax1.legend()
        ax1.grid(alpha=0.3)

        # Want a plot of mean moves vs grid size (AH1 / AH2 separate lines)
        ax2.set_xlabel("Grid size N")
        ax2.set_ylabel("Mean number of moves")
        ax2.set_title("Moves vs grid size (solved grids only)")
        ax2.set_xticks(SIZES)
        ax2.legend()
        ax2.grid(alpha=0.3)

        # Want a box plot to show how many of each grid size had successful results (FYI)
        a = ALGORITHMS[0]
        solved = [len(costs[(a, n)]) for n in SIZES]
        unsolved = [not_founds[(a, n)] for n in SIZES]
        to = [timeouts[(a, n)] for n in SIZES]
        ax3.bar(SIZES, solved, label="solved")
        ax3.bar(SIZES, unsolved, bottom=solved, label="unsolvable (0)")
        ax3.bar(SIZES, to, bottom=[s + u for s, u in zip(solved, unsolved)], label="timeout (-200)")
        ax3.set_xlabel("Grid size N")
        ax3.set_ylabel("Number of grids")
        ax3.set_title(f"Outcomes per size ({a})")
        ax3.set_xticks(SIZES)
        ax3.legend()

        a = ALGORITHMS[1]
        solved = [len(costs[(a, n)]) for n in SIZES]
        unsolved = [not_founds[(a, n)] for n in SIZES]
        to = [timeouts[(a, n)] for n in SIZES]
        ax4.bar(SIZES, solved, label="solved")
        ax4.bar(SIZES, unsolved, bottom=solved, label="unsolvable (0)")
        ax4.bar(SIZES, to, bottom=[s + u for s, u in zip(solved, unsolved)], label="timeout (-200)")
        ax4.set_xlabel("Grid size N")
        ax4.set_ylabel("Number of grids")
        ax4.set_title(f"Outcomes per size ({a})")
        ax4.set_xticks(SIZES)
        ax4.legend()

        plt.tight_layout()
        plt.savefig("n.png", dpi=200)


makeGraphN()