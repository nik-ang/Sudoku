import math

class Cell(object):
    def __init__(self, sudokuSate, row, column, value, fixed = False):
        self.sudokuSate = sudokuSate
        self.row = row
        self.column = column
        self.quadrant = self.setQuadrant()
        self.nonPossibleValues = []
        self.value = value
        self.fixed = fixed
        self.findNonPossibleValues()

    def setValue(self, value):
        self.value = value
    
    def getValue(self):
        return self.value

    def getQuadrant(self):
        return self.quadrant

    def getSudokuState(self):
        return self.sudokuSate

    def setQuadrant(self):
        rowIndex = math.ceil( 3*self.row / 9)
        columnIndex = math.ceil( 3*self.column / 9)
        return rowIndex * columnIndex
    
    def findNonPossibleValues(self):

        print(self.getSudokuState().getCell(2, 2).getValue())

        """
        for x in range(len(self.sudokuSate.sudoku)):
            selectedCell = self.sudokuSate.getCell(x, self.column - 1)
            if (selectedCell.getValue() is not 0):
                self.nonPossibleValues.append(selectedCell.getValue())

        #Columns
        for y in range(len(self.sudokuSate.sudoku)):
            selectedCell = self.sudokuSate.getCell(self.row - 1, y)
            if (selectedCell.getValue() is not 0):
                self.nonPossibleValues.append(selectedCell.getValue())

        #Quadrants
        for x in range(len(self.sudokuSate.sudoku)):
            for y in range(len(self.sudokuSate.sudoku)):
                selectedCell = self.sudokuSate.getCell(x, y)
                if (selectedCell.getValue() is not 0 and selectedCell.getQuadrant() == self.quadrant):
                    self.nonPossibleValues.append(selectedCell.getValue())
        """
        


class SudokuState(object):
    def __init__(self, parent = None, depth = 0, configArray = None):
        self.sudoku = [[None for i in range(9)] for j in range(9)] #Array of Cells
        self.initiCells(configArray)
        self.parent = parent #Class SudokuState
        self.depth = depth
        self.children = [] #Array of nodes
    
    def initiCells(self, configArray):
        k = 0
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                self.sudoku[x][y] = Cell(self, x + 1, y + 1, configArray[k])
                k += 1


    def getCell(self, x, y):
        return self.sudoku[x][y]

    def printSudoku(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                print("{:<4}".format(self.getCell(x, y).getValue()), end="")
            print()
        print("--------------------------------")

    #Debugging purposes
    def printQuadrants(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                print("{:<4}".format(self.getCell(x, y).getQuadrant), end="")
            print()
        print("--------------------------------")


class Solver(object):
    def __init__(self, config):
        self.configArray = config.split(",")
        self.configArray = list(map(int, self.configArray))
        self.rootState = SudokuState(None, 0, self.configArray)
        self.rootState.printSudoku()

S = Solver("1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,2,1")
