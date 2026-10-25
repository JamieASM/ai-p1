import subprocess
import sys
import unittest

from helpers.utils import h_AH1, h_AH2, NOT_FOUND
from helpers.Search import search
from helpers.Node import Node, compress


#*************** Args to PImain ***************#

class TestP1main(unittest.TestCase):
    """
    Tests P1main.py.
    """

    def run_P1main(self, args):
        return subprocess.run(
            [sys.executable, "P1main.py", *args],
            capture_output=True,
            text=True,
            timeout=60
        )

    def test_P1main_01_no_args(self):
        """
        Checks that P1main throws an error if there are no arguments provided.
        """

        r = self.run_P1main([])
        self.assertIn("usage: python3 P1main.py <AH1|AH2|AH3> <conf> [<verbose>]", r.stdout)

    def test_P1main_02_conf_verbose_only(self):
        """
        Checks that P1main throws an error if only the conf and verbose are provided as arguments.
        """

        r = self.run_P1main(["RGRRRRBGB", "verbose"])
        self.assertIn(
            "Incorrect algorithm argument provided. The algorithm provided must be one of the following: AH1 | AH2 | AH3.",
            r.stdout
        )

    def test_P1main_03_AH1_verbose_only(self):
        """
        Tests that an error is thrown when only 'AH1' and 'verbose' are provided as arguments.
        The error is not because of lack of config. We cannot police if someone wants their grid to be the word
        'verbose' but the word 'verbose' does not create an N x N grid so would error anyway.
        """

        r = self.run_P1main(["AH1", "verbose"])
        self.assertIn(
            "The grid provided must be of size N x N (square).",
            r.stdout
        )

    def test_P1main_04_nonexistent_AH(self):
        """
        Tests that a non-existent AH argument returns an error.
        """

        r = self.run_P1main(["foo", "RGRRRRBGB"])
        self.assertIn(
            "Incorrect algorithm argument provided. The algorithm provided must be one of the following: AH1 | AH2 | AH3.",
            r.stdout
        )

    def test_P1main_05_runs(self):
        """
        Checks that an average input runs as expected.
        """

        r = self.run_P1main(["AH1", "RGRRRRBGB"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("3", r.stdout)


#*************** Search() ***************#
class TestSearch(unittest.TestCase):
    """
    Tests the search algorithm.
    """

    def setUp(self):
        """
        Sets up all the h functions currently implemented.
        """

        self.funcs = [h_AH1, h_AH2]

    def test_search_01_small_grid_solution(self):
        """
        Tests that a small grid with a solution behaves correctly.
        """

        grid = [
            list("RB"),
            list("RB")
        ]

        for algo in self.funcs:
            assert search(grid=grid, verbose=False, hFunc=algo) == 2  # doing it like this to be extremely clear

    def test_search_02_small_grid_no_solution(self):
        """
        Tests that a small grid with no solutions returns NOT_FOUND.
        """

        grid = [
            list("RB"),
            list("RC")
        ]

        for algo in self.funcs:
            assert search(grid=grid, verbose=False, hFunc=algo) == NOT_FOUND

    def test_search_03_large_grid_solution(self):
        """
        Tests that a large grid with a solution behaves correctly.
        """

        grid = [
            ["R" for _ in range(10)],
            ["R" for _ in range(10)],
            ["R" for _ in range(10)],
            ["G" for _ in range(10)],
            ["G" for _ in range(10)],
            ["G" for _ in range(10)],
            ["B" for _ in range(10)],
            ["B" for _ in range(10)],
            ["B" for _ in range(10)],
            ["B" for _ in range(10)],
        ]

        for algo in self.funcs:
            assert search(grid=grid, verbose=False, hFunc=algo) == 3

    def test_search_04_large_grid_no_solution(self):
        """
        Tests that a large grid with no solutions behaves correctly.
        """

        grid = [
            list("ROYGBPIVOP"),
            list("OYGBPIVOPR"),
            list("YGBPIVOPRO"),
            list("GBPIVOPROY"),
            list("BPIVOPROYG"),
            list("PIVOPROYGB"),
            list("IVOPROYGBP"),
            list("VOPROYGBPI"),
            list("OPROYGBPIV"),
            list("PROYGBPIVO")
        ]

        for algo in self.funcs:
            assert search(grid=grid, verbose=False, hFunc=algo) == NOT_FOUND

    def test_search_05_1x1_grid(self):
        """
        Tests that a 1x1 grid does not find a solution.
        """

        grid = [
            list("R")
        ]

        for algo in self.funcs:
            assert search(grid=grid, verbose=False, hFunc=algo) == NOT_FOUND

    def test_search_06_already_solved(self):
        """
        Tests that an empty grid is treat as empty / solved.
        """

        grid = [["-" for _ in range(3)] for _ in range(3)]

        for algo in self.funcs:
            assert search(grid=grid, verbose=False, hFunc=algo) == 0

    def test_search_07_partially_solved(self):
        """
        Tests that a partially solved grid is treat as such.
        """

        grid = [
            ["-" for _ in range(3)],
            list("-G-"),
            list("BGB")
        ]

        for algo in self.funcs:
            assert search(grid=grid, verbose=False, hFunc=algo) == 2


#*************** GetSuccStates() ***************#

def setup_succ_states(grid):
    """
    Helper for the TestSuccStates class. Sets up the environment by creating a node and running getSuccStates.

    Parameters:
        grid (list): The grid for the test case

    Returns:
        list: The successor states aquired by getSuccStates().
    """
    nd = Node(None, grid, hFunc=h_AH1)  # hFunc does not matter

    return nd.getSuccStates()


class TestSuccStates(unittest.TestCase):
    """
    Tests the algorithm to get successor states.
    """

    def test_succ_states_01_no_diagonals(self):
        """
        Verifies that same colour diagonals are not counted as a neighbour.
        """

        states = setup_succ_states([
            list("RB"),
            list("BR")
        ])

        assert len(states) == 0

    def test_succ_states_02_all_same_colours(self):
        """
        Verifies that a 1 item list is returned that is an empty grid if the grid is made up of only one colour.
        """

        states = setup_succ_states([
            list("RR"),
            list("RR")
        ])

        assert len(states) == 1
        assert states == [[["-" for _ in range(2)] for _ in range(2)]]

    def test_succ_states_03_multi_moves(self):
        """
        Verifies the method can return multiple successor states. 
        """
        states = setup_succ_states([
            list("RRRG"),
            list("RGGG"),
            list("BBBY"),
            list("BBYY")
        ])

        assert len(states) == 4
        assert states == [
            [
                list("---G"),
                list("-GGG"),
                list("BBBY"),
                list("BBYY")
            ],
            [
                list("R---"),
                list("RRR-"),
                list("BBBY"),
                list("BBYY")
            ],
            [
                list("---G"),
                list("--RG"),
                list("RRGY"),
                list("RGYY")
            ],
            [
                list("RR--"),
                list("RGR-"),
                list("BBGG"),
                list("BBBG")
            ],
        ]


#*************** Compress() ***************#


class TestCompress(unittest.TestCase):
    """
    Tests the algorithm to compress the grid.
    """

    def test_compress_01_full_grid(self):
        """
        Verifies that a full grid will remain unchanged after being passed through compress().
        """

        grid = [
            list("RGR"),
            list("RRR"),
            list("BGB")
        ]

        res = compress(grid)

        assert grid == res


    def test_compress_02_row_moves(self):
        """
        Checks that compress() will rearrange rows as expected.
        """

        grid = [
            list("RGRR"),
            list("----"),
            list("BGBB"),
            list("----")
        ]

        res = compress(grid)

        assert res == [
            list("----"),
            list("----"),
            list("RGRR"),
            list("BGBB")
        ]

    def test_compress_03_column_moves(self):
        """
        Checks that compress() will rearrange columns as expected.
        """

        grid = [
            list("--AP"),
            list("--YU"),
            list("--UY"),
            list("--PA")
        ]

        res = compress(grid)

        assert res == [
            list("AP--"),
            list("YU--"),
            list("UY--"),
            list("PA--")
        ]

    def test_compress_04_moves(self):
        """
        Checks that compress can rearrange both rows and columns as expected.
        """
        grid = [
            list("-A-P"),
            list("-Y-U"),
            list("----"),
            list("---A")
        ]

        res = compress(grid)

        assert res == [
            list("----"),
            list("-P--"),
            list("AU--"),
            list("YA--")
        ]

if __name__ == "__main__":
    unittest.main()