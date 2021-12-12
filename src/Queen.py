"""
  @author  Thomas Lehmann
  @file    Queen.py
 
  Copyright (c) 2016 Thomas Lehmann
 
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
  documentation files (the "Software"), to deal in the Software without restriction, including without limitation
  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
  The above copyright notice and this permission notice shall be included in all copies
  or substantial portions of the Software.
 
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
  DAMAGES OR OTHER LIABILITY,
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
# pylint: disable=E0602
import sys
import time

OUTPUT = False    # enable/disable of printing the solutions


class Queen:
    """Queen algorithm."""
    def __init__(self, width):
        self.width = width
        self.lastRow = self.width-1
        # locked columns
        self.columns = self.width * [-1]
        # locked diagonals
        numberOfDiagonals = 2 * self.width - 1
        self.diagonals1 = numberOfDiagonals * [0]
        self.diagonals2 = numberOfDiagonals * [0]
        # list of solutions
        self.solutions = set()

    # starts the search with initial parameters and organizing
    # to search the half only
    def run(self):
        for column in range(self.width // 2 + self.width % 2):
            ixDiag1 = column
            ixDiag2 = self.lastRow + column
            # occupying column and diagonals depending on current row and column
            self.columns[column] = 0
            self.diagonals1[ixDiag1] = 1
            self.diagonals2[ixDiag2] = 1

            self.calculate(1, [k for k in range(self.width) if not k == column])

            # Freeing column and diagonals depending on current row and column
            self.diagonals1[ixDiag1] = 0
            self.diagonals2[ixDiag2] = 0

    # searches for all possible solutions
    def calculate(self, row, columnRange):
        for column in columnRange:
            # relating diagonale '\' depending on current row and column
            ixDiag1 = row + column

            if self.diagonals1[ixDiag1] == 1:
                continue

            # relating diagonale '/' depending on current row and column
            ixDiag2 = self.lastRow - row + column

            # is one of the relating diagonals OCCUPIED by a queen?
            if self.diagonals2[ixDiag2] == 1:
                continue

            # occupying column and diagonals depending on current row and column
            self.columns[column] = row
            self.diagonals1[ixDiag1] = 1
            self.diagonals2[ixDiag2] = 1

            # all queens have been placed?
            if row == self.lastRow:
                solutionA = self.columns[0:]
                self.solutions.add(tuple(solutionA))

                # mirrored left <-> right
                solutionB = tuple(reversed(solutionA))
                self.solutions.add(solutionB)

                # mirrored top <-> bottom
                self.solutions.add(tuple(map(lambda n: self.lastRow - n, solutionA)))
                # mirrored top <-> bottom and left <-> right
                self.solutions.add(tuple(map(lambda n: self.lastRow - n, solutionB)))
            else:
                # trying to place next queen...
                self.calculate(row + 1, [k for k in columnRange if k != column])

            # Freeing column and diagonals depending on current row and column
            self.diagonals1[ixDiag1] = 0
            self.diagonals2[ixDiag2] = 0

    # printing all solutions where n queens are placed on a nxn board
    # without threaten another one.
    def printAllSolutions(self):
        for solution in sorted(self.solutions):
            line = ""
            for ix in range(len(solution)):
                line += "(%d,%d)" % (ix+1, solution[ix]+1)
            print(line)


def main():
    """Application entry point."""
    width = 8  # default
    if len(sys.argv) == 2:
        width = int(sys.argv[1])

    instance = Queen(width)
    print("Running %s with %s - version %s" % \
          (sys.argv[0], sys.executable, sys.version))
    print("Queen raster (%dx%d)" % (instance.width, instance.width))

    Start = time.time()
    instance.run()
    print("...took %f seconds." % (time.time() - Start))
    print("...%d solutions found." % (len(instance.solutions)))

    if OUTPUT:
        instance.printAllSolutions()

if __name__ == '__main__':
    main()
