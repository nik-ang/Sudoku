class Cell:
    def __init__(self, sudokuSate, row, column, square):
        self.sudokuSate = sudokuSate
        self.row = row
        self.column = column
        self.square = square
        self.possibleValues = []
        self.nonPossibleValues = []

class SudokuState:
    def __init__(self, parent = None, depth = 0):
        self.parent = parent #Class SudokuState
        self.depth = depth
        self.children = [] #Array of nodes