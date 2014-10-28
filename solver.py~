# solver.py
# ------
# Licensing Information:
# Created by Ye Xu on 10/25/2014
# copyright (c) 2014 Ye Xu. All rights reserved

"""
In solver.py, The model parts of the model view controller (MVC) are implemented here. It uses Constraints Satisfaction
Problem (CSP) in AI to solve the simulation of Sudoku puzzle.
"""

import time, random
import utility


class Solver:
    """
    This class can solve every Sudoku puzzle. The problem is a classic Constraints Satisfaction Problem (CSP).
    To model this problem, we have the following notations:
        Rows are represented as: 'ABCDEFGHI'
        Cols are represented as: '123456789'
        Each square of the 81 squares can be represented as a combination of row number of column number, e.g., 'A1'
        The value of each square can be a number from 1 to 9, or 0 for unsolved square.

        A1 A2 A3| A4 A5 A6| A7 A8 A9    4 0 0 |0 0 0 |8 0 5     4 1 7 |3 6 9 |8 2 5
        B1 B2 B3| B4 B5 B6| B7 B8 B9    0 3 0 |0 0 0 |0 0 0     6 3 2 |1 5 8 |9 4 7
        C1 C2 C3| C4 C5 C6| C7 C8 C9    0 0 0 |7 0 0 |0 0 0     9 5 8 |7 2 4 |3 1 6
       ---------+---------+---------    ------+------+------    ------+------+------
        D1 D2 D3| D4 D5 D6| D7 D8 D9    0 2 0 |0 0 0 |0 6 0     8 2 5 |4 3 7 |1 6 9
        E1 E2 E3| E4 E5 E6| E7 E8 E9    0 0 0 |0 8 0 |4 0 0     7 9 1 |5 8 6 |4 3 2
        F1 F2 F3| F4 F5 F6| F7 F8 F9    0 0 0 |0 1 0 |0 0 0     3 4 6 |9 1 2 |7 5 8
       ---------+---------+---------    ------+------+------    ------+------+------
        G1 G2 G3| G4 G5 G6| G7 G8 G9    0 0 0 |6 0 3 |0 7 0     2 8 9 |6 4 3 |5 7 1
        H1 H2 H3| H4 H5 H6| H7 H8 H9    5 0 0 |2 0 0 |0 0 0     5 7 3 |2 9 1 |6 8 4
        I1 I2 I3| I4 I5 I6| I7 I8 I9    1 0 4 |0 0 0 |0 0 0     1 6 4 |8 7 5 |2 9 3

        Each square has exactly 3 units, which are the row collection, the column collection and the box of the same square.
        The peers of a square are the elements that share the same units with the square.
        E.g. 'C2' has the following units and peers:

        A2   |         |                    |         |            A1 A2 A3|         |
        B2   |         |                    |         |            B1 B2 B3|         |
        C2   |         |            C1 C2 C3| C4 C5 C6| C7 C8 C9   C1 C2 C3|         |
    ---------+---------+---------  ---------+---------+---------  ---------+---------+---------
        D2   |         |                    |         |                    |         |
        E2   |         |                    |         |                    |         |
        F2   |         |                    |         |                    |         |
    ---------+---------+---------  ---------+---------+---------  ---------+---------+---------
        G2   |         |                    |         |                    |         |
        H2   |         |                    |         |                    |         |
        I2   |         |                    |         |                    |         |


        We use a dictionary data structure to represent the possible values of each square. E.g.{'A1':'12349', 'A2':'8', ...}

    A common way to solve it is to use recursive back-tracking search, plus forward checking. There are two rules of thumb can be
    used for forward checking:
    (1) If a square has only one possible value, then eliminate that value from the square's peers.
    (2) If a unit has only one possible place for a value, then put the value there.
    """


    def __init__(self, grid):
        """
        Initialization: convert grid from a string to a dictionary data structure to represent the possible values of
        each square. E.g.{'A1':'12349', 'A2':'8', ...}. For each unsolved element in grid, '0' or '.', they have
        '123456789' as possible values initially.
        :param grid: A string of 81 chars representing the values for each square, '0' or '.' for unsolved squares
        """

        # Class constants
        self.DIGITS = '123456789'
        self.ROWS = 'ABCDEFGHI'
        self.COLS = self.DIGITS
        self.SQUARES = utility.cross(self.ROWS, self.COLS)

        self.UNITLISTS = ([utility.cross(self.ROWS, c) for c in self.COLS] +
                          [utility.cross(r, self.COLS) for r in self.ROWS] +
                          [utility.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])

        self.UNITS = dict((square, [unit for unit in self.UNITLISTS if square in unit]) for square in self.SQUARES)
        self.PEERS = dict((square, set(sum(self.UNITS[square], [])) - set([square])) for square in self.SQUARES)

        self.possible_values = self.initialize_possible_values(grid)
        self.init_values = self.grid_values(grid)
        self.final_values = {}


    def initialize_possible_values(self, grid):
        """
        Initialize the grid string into a dictionary format for the solver
        :param grid:
        :return: Initialized dictionary of possible values.
        """
        possible_values = dict((square, self.DIGITS) for square in self.SQUARES)
        partial_sol = self.grid_values(grid)
        for square, d in partial_sol.items():
            if d not in '0.':
                possible_values[square] = d
        return possible_values


    def grid_values(self, grid):
        """
        Convert grid into a dict of {square: char} with '0' or '.' for empties.
        :param grid: A string of 81 chars representing the values for each square, '0' or '.' for unsolved squares
        """
        chars = [c for c in grid if c in self.DIGITS or c in '0.']
        assert len(chars) == 81
        return dict(zip(self.SQUARES, chars))


    def display(self, values):
        """
        Helper function to display these values as a 2-D grid.
        E.g.:
        1 3 5 |2 9 7 |8 6 4
        9 8 2 |4 1 6 |7 5 3
        7 6 4 |3 8 5 |1 9 2
        ------+------+------
        2 1 8 |7 3 9 |6 4 5
        5 9 7 |8 6 4 |2 3 1
        6 4 3 |1 5 2 |9 7 8
        ------+------+------
        4 2 6 |5 7 1 |3 8 9
        3 5 9 |6 2 8 |4 1 7
        8 7 1 |9 4 3 |5 2 6

        If values is None, it will print some warning message
        """
        if values is None:
            print('There is no possible solution for this puzzle')
            return

        width = 1 + max(len(values[square]) for square in self.SQUARES)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in self.ROWS:
            print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                          for c in self.COLS))
            if r in 'CF':
                print(line)
        #print()


    def forward_check(self, possible_values):
        """
        Forward checking of CSP. Call first_strategy and second
        :param possible_values:
        :return: Updated possible values with potential lots of values  eliminated
        """

        init_possible_values = possible_values.copy()
        init_possible_values = self.first_strategy(init_possible_values)

        if init_possible_values == False:
            return False
        possible_values, changed = self.second_strategy(init_possible_values.copy())

        # If some more values are eliminated using second strategy, must use first strategy again to see if even more
        # values can be eliminated
        while changed:
            init_possible_values = possible_values.copy()
            init_possible_values = self.first_strategy(init_possible_values)
            if init_possible_values == False:
                return False
            possible_values, changed = self.second_strategy(init_possible_values.copy())


        return possible_values


    def first_strategy(self, possible_values):
        """
        1st strategy to rule out impossible values: If a square has only one possible value, then eliminate that value
        from the square's peers.

        :param possible_values:
        :return:Updated possible values with potential lots of values  eliminated
        """

        for square, d in possible_values.items():
            if len(d) == 0:
                return False
            elif len(d) == 1:
                for s2 in self.PEERS[square]:
                    new_possible_vals = set(possible_values[s2]).difference(set(d))
                    new_possible_vals = ''.join(new_possible_vals)
                    if len(new_possible_vals) > 0:
                        possible_values[s2] = new_possible_vals
                    else:
                        return False

        return possible_values

    def second_strategy(self, possible_values):
        """
        2nd strategy to rule out impossible values: If a unit has only one possible place for a value, then put the
        value there.

        :param possible_values:
        :return:Updated possible values with potential lots of values eliminated
        """
        changed = False
        for square in self.SQUARES:
            for unit in self.UNITS[square]:
                unit_values = {d for s2 in unit if s2 != square for d in possible_values[s2]}
                remaining_value_for_s = set(possible_values[square]).difference(unit_values)
                if len(remaining_value_for_s) == 1:
                    if len(remaining_value_for_s) != len(possible_values[square]):
                        changed = True
                    possible_values[square] = remaining_value_for_s.pop()
        return possible_values, changed



    def backtracking_search(self,possible_values):
        """
        Use back-tracking search to search a solution.
        :param possible_values:
        :return: False if no solution, or final values otherwise
        """
        possible_values = self.forward_check(possible_values)

        if possible_values == False:
            return False

        values = self.recursive_backtracking(possible_values)
        return values


    def recursive_backtracking(self, possible_values):
        """
        Recursive backtracking
        :param possible_values:
        :return: False if no solution, or final values otherwise
        """

        if possible_values == False:
            return False

        if all(len(possible_values[square]) == 1 for square in self.SQUARES):
            return possible_values    # solved

        # use minimum remaining value square as next candidate to try
        n,square = min((len(possible_values[square]), square) for square in self.SQUARES if len(possible_values[square]) > 1)

        for d in possible_values[square]:
            possible_values_copy = possible_values.copy()
            possible_values_copy[square] = d
            possible_values_copy = self.forward_check(possible_values_copy)
            if possible_values_copy != False:
                possible_values_copy = self.recursive_backtracking(possible_values_copy)

                if possible_values_copy != False:  # If stuck in this way, back track to search other ways
                    return possible_values_copy

                possible_values_copy = possible_values

        return False



    def solve(self):
        """
        Solve the puzzle!!!
        :return: Final assignment of values for each square
        """
        start = time.clock()
        self.final_values = self.backtracking_search(self.possible_values)
        t = time.clock()-start  # Record the time it takes to solve
        if self.solved(self.final_values):
            self.display(self.init_values)
            print('#####################')
            self.display(self.final_values)
            print('(%.2f seconds)\n' % t)
            return (t, self.final_values)

        return (t, False)


    def solved(self, values):
        """
        A puzzle is solved if each unit is a permutation of the digits 1 to 9.
        :param values:
        :return: True if it is solved, False otherwise
        """
        def unitsolved(unit): return set(values[square] for square in unit) == set(self.DIGITS)
        return values is not False and all(unitsolved(unit) for unit in self.UNITLISTS)

grid = '...57..3.1......2.7...234......8...4..7..4...49....6.5.42...3.....7..9....18.....'
grid = grid.replace('.', '0')
solver = Solver(grid)
utility.write_csv('./Data/hard4.csv', solver.init_values)

## References used:
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://norvig.com/sudoku.html
