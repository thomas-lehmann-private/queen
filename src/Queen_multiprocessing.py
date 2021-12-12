"""
# @author  Thomas Lehmann
# @file    Queen_multiprocessing.py
#
# Copyright (c) 2016 Thomas Lehmann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
# pylint: disable=E0602,C0325
import sys
import time
import multiprocessing
from contextlib import closing

OUTPUT = False    # enable/disable of printing the solutions


class Queen(object):
    """Queen algorithm."""

    def __init__(self, width):
        self.width = width
        self.last_row = self.width-1
        # locked columns
        self.columns = self.width * [-1]
        # locked diagonals
        number_of_diagonals = 2 * self.width - 1
        self.diagonals1 = number_of_diagonals * [0]
        self.diagonals2 = number_of_diagonals * [0]
        # list of solutions
        self.solutions = set()

    def run(self, column):
        """
        Starts the search with initial parameters and organizing
        to search the half only
        """
        ix_diag1 = column
        ix_diag2 = self.last_row + column
        # occupying column and diagonals depending on current row and column
        self.columns[column] = 0
        self.diagonals1[ix_diag1] = 1
        self.diagonals2[ix_diag2] = 1

        self.calculate(1, [k for k in range(self.width) if not k == column])

        # Freeing column and diagonals depending on current row and column
        self.diagonals1[ix_diag1] = 0
        self.diagonals2[ix_diag2] = 0

    def calculate(self, row, column_range):
        """searches for all possible solutions."""
        for column in column_range:
            # relating diagonale '\' depending on current row and column
            ix_diag1 = row + column

            if self.diagonals1[ix_diag1] == 1:
                continue

            # relating diagonale '/' depending on current row and column
            ix_diag2 = self.last_row - row + column

            # is one of the relating diagonals OCCUPIED by a queen?
            if self.diagonals2[ix_diag2] == 1:
                continue

            # occupying column and diagonals depending on current row and column
            self.columns[column] = row
            self.diagonals1[ix_diag1] = 1
            self.diagonals2[ix_diag2] = 1

            # all queens have been placed?
            if row == self.last_row:
                solution_a = self.columns[0:]
                self.solutions.add(tuple(solution_a))

                # mirrored left <-> right
                solution_b = tuple(reversed(solution_a))
                self.solutions.add(solution_b)

                # mirrored top <-> bottom
                self.solutions.add(tuple(
                    map(lambda n: self.last_row - n, solution_a)))
                # mirrored top <-> bottom and left <-> right
                self.solutions.add(tuple(
                    map(lambda n: self.last_row - n, solution_b)))
            else:
                # trying to place next queen...
                self.calculate(row + 1, [k for k in column_range if k != column])

            # Freeing column and diagonals depending on current row and column
            self.diagonals1[ix_diag1] = 0
            self.diagonals2[ix_diag2] = 0

    @staticmethod
    def print_all_solutions(solutions):
        """
        Printing all solutions where n queens are placed on a nxn board
        without threaten another one.
        """
        for solution in sorted(solutions):
            line = ""
            for idx, value in enumerate(solution):
                line += "(%d,%d)" % (idx+1, value+1)
            print(line)


def worker(data):
    """Thread function."""
    width, column = data
    queen = Queen(width)
    queen.run(column)
    return queen.solutions

def main():
    """Application entry point."""
    width = 8  # default
    if len(sys.argv) == 2:
        width = int(sys.argv[1])

    print("Running %s with %s - version %s" % \
          (sys.argv[0], sys.executable, sys.version))
    print("Queen raster (%dx%d)" % (width, width))

    start = time.time()

    column_range = range(width // 2 + width % 2)
    solutions = set()
    with closing(multiprocessing.Pool(multiprocessing.cpu_count())) as pool:
        for results in pool.map(worker, [(width, column) for column in column_range]):
            for solution in results:
                solutions.add(solution)
        pool.terminate()

    print("...took %f seconds." % (time.time() - start))
    print("...%d solutions found." % (len(solutions)))

    if OUTPUT:
        Queen.print_all_solutions(solutions)

if __name__ == '__main__':
    main()
