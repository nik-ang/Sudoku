import math

class Cell(object):
    def __init__(self, sudokuSate, row, column, fixed = False):
        self.sudokuSate = sudokuSate
        self.row = row
        self.column = column
        self.quadrant = self.setQuadrant()
        self.possibleValues = []
        self.nonPossibleValues = []
        self.value = 0
        self.fixed = fixed

    def setQuadrant(self):
        rowIndex = math.ceil( 3*self.row / 9)
        columnIndex = math.ceil( 3*self.column / 9)
        return rowIndex * columnIndex


class SudokuState(object):
    def __init__(self, parent = None, depth = 0):
        self.sudoku = [[None for i in range(9)] for j in range(9)] #Array of Cells
        self.initiCells()
        self.parent = parent #Class SudokuState
        self.depth = depth
        self.children = [] #Array of nodes
    
    def initiCells(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                self.sudoku[x][y] = Cell(self, x + 1, y + 1)

    def printSudoku(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                print("{:<4}".format(self.sudoku[x][y].value), end="")
            print()
        print("--------------------------------")

    def printQuadrants(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                print("{:<4}".format(self.sudoku[x][y].quadrant), end="")
                #print(self.sudoku[x][y].quadrant)
            print()
        print("--------------------------------")

class Solver(object):
    def __init__(self, config):
        self.configArray = config.split(",")
        self.configArray = list(map(int, self.configArray))
        self.rootState = SudokuState(self, 0)
        k = 0
        for x in range(9):
            for y in range(9):
                self.rootState.sudoku[x][y].value = self.configArray[k]
                k += 1
        self.rootState.printSudoku()

S = Solver("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
