/**
 * @author  Thomas Lehmann
 * @file    Queen.java
 *
 * Copyright (c) 2016 Thomas Lehmann
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
 * and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies
 * or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
import java.util.List;
import java.util.ArrayList;

/**
    @class Queen
    @brief Calculates the positions of "n" queens on a n x n field; no queen
           should attack each other.
 */
public class Queen {
    /**
        Two possible states for each diagonal.
    */
    enum Diagonal {
        FREE,
        OCCUPIED
    }

    private int                  width;       // is width(=height) of board
    private int                  lastRow;     // is last row index
    private List<Integer>        columns;     // occupied/free columns
    private Diagonal[]           diagonals1;  // occupied/free diagonals "\"
    private Diagonal[]           diagonals2;  // occupied/free diagonals "/"
    private List<List<Integer>>  solutions;   // found solutions

    /**
        Initializes all relevant fields for calculation

        @param width is width(=height) of the board
     */
    public Queen(int width) {
        this.width      = width;
        this.lastRow    = this.width - 1;

        final int numberOfDiagonals = 2 * this.width - 1;

        this.columns    = new ArrayList<Integer>();
        this.diagonals1 = new Diagonal[numberOfDiagonals];
        this.diagonals2 = new Diagonal[numberOfDiagonals];
        this.solutions  = new ArrayList<List<Integer>>();


        for (int index = 0; index < numberOfDiagonals; ++index) {
            if (index < this.width) {
                this.columns.add(-1);
            }
            this.diagonals1[index] = Diagonal.FREE;
            this.diagonals2[index] = Diagonal.FREE;
        }
    }

    /**
        @return width(=height) of the board.
     */
    public int getWidth() {
        return  this.width;
    }

    /**
        @return number of found solutions (example: 8x8 -> 92).
     */
    public int getNumberOfSolutions() {
        return this.solutions.size();
    }

    /**
        Implements the queen algorithm.

        @param row represents current row (initially starting by zero).
     */
    public void runAlgorithm(final int row) {
        for (int column = 0; column < this.width; ++column) {
            // is column occupied?
            if (this.columns.get(column) >= 0) {
                continue;
            }

            final int ixDiag1 = row + column;
            if (this.diagonals1[ixDiag1] == Diagonal.OCCUPIED) {
                continue;
            }

            final int ixDiag2 = this.lastRow - row + column;
            if (this.diagonals2[ixDiag2] == Diagonal.OCCUPIED) {
                continue;
            }

            // occupying one column and two diagonals
            this.columns.set(column, row);
            this.diagonals1[ixDiag1] = Diagonal.OCCUPIED;
            this.diagonals2[ixDiag2] = Diagonal.OCCUPIED;

            // solution found?
            if (row == this.lastRow) {
                solutions.add(new ArrayList<Integer>(this.columns));
            } else {
                // walking next row...
                this.runAlgorithm(row + 1);
            }

            // freeing one column and two diagonals
            this.columns.set(column, -1);
            this.diagonals1[ixDiag1] = Diagonal.FREE;
            this.diagonals2[ixDiag2] = Diagonal.FREE;
        }
    }

    public void printSolutions() {
        for (List<Integer> solution: solutions) {
            for (int column = 0; column < this.width; ++column) {
                System.out.print("(" + (column+1) + "," + (solution.get(column)+1) + ")");
            }
            System.out.println("");
        }
    }

    /**
        Application entry point.

        @param arguments command line options
     */
    public static void main(String[] arguments) {
        int width = 8; // default

        if (arguments.length == 1) {
            width = Integer.valueOf(arguments[0]).intValue();
        }

        final Queen instance = new Queen(width);
        System.out.println("Running with Java " + System.getProperty("java.version"));
        System.out.println("Queen raster (" + instance.getWidth() + "x"
                                           + instance.getWidth() + ")");
        final long start = System.currentTimeMillis();
        instance.runAlgorithm(0);
        System.out.println("...took " + ((System.currentTimeMillis() - start) / 1000.0) + " seconds.");
        System.out.println("..." + instance.getNumberOfSolutions() + " solutions found.");

        //instance.printSolutions();
    }
}

