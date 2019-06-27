import math
import queue

class Cell(object):
    def __init__(self, sudokuSate, row, column, value, fixed = False):
        self.sudokuSate = sudokuSate
        self.row = row
        self.column = column
        self.quadrant = self.setQuadrant()
        self.nonPossibleValues = []
        self.possibleValues = []
        self.value = value
        self.fixed = fixed

    def setValue(self, value):
        self.value = value
    
    def getValue(self):
        return self.value

    def getQuadrant(self):
        return self.quadrant

    def setFixed(self, value):
        self.setFixed = value

    def isFixed(self):
        return self.fixed

    def getSudokuState(self):
        return self.sudokuSate

    def setQuadrant(self):
        rowIndex = math.ceil( 3*self.row / 9)
        columnIndex = math.ceil( 3*self.column / 9)
        return (rowIndex - 1) * 3 + columnIndex
    
    def findNonPossibleValues(self):

        #Rows
        for x in range(len(self.sudokuSate.sudoku)):
            selectedCell = self.sudokuSate.getCell(x, self.column - 1)
            if (selectedCell.getValue() is not 0 and selectedCell is not self):
                if (selectedCell.getValue() not in self.nonPossibleValues):
                    self.nonPossibleValues.append(selectedCell.getValue())

        #Columns
        for y in range(len(self.sudokuSate.sudoku)):
            selectedCell = self.sudokuSate.getCell(self.row - 1, y)
            if (selectedCell.getValue() is not 0 and selectedCell is not self):
                if (selectedCell.getValue() not in  self.nonPossibleValues):
                    self.nonPossibleValues.append(selectedCell.getValue())

        #Quadrants
        for x in range(len(self.sudokuSate.sudoku)):
            for y in range(len(self.sudokuSate.sudoku)):
                selectedCell = self.sudokuSate.getCell(x, y)
                if (selectedCell.getValue() is not 0 and selectedCell.getQuadrant() == self.quadrant and selectedCell is not self):
                    if (selectedCell.getValue() not in self.nonPossibleValues):
                        self.nonPossibleValues.append(selectedCell.getValue())

    def findPossibleValues(self):
        if (self.isFixed()):
            self.possibleValues.append(self.value)
        else:
            self.findNonPossibleValues()
            for x in range(10):
                if (x not in self.nonPossibleValues and x > 0):
                    self.possibleValues.append(x)
        #print(self.possibleValues)


class SudokuState(object):
    def __init__(self, parent = None, depth: int = 0, configArray = None, isInitial: bool = False, x: int = 0, y: int = 0, value: int =0):
        if isInitial:
            self.sudoku: Cell = [[Cell for i in range(9)] for j in range(9)] #Array of Cells
            self.configuration = configArray
            self.initiCells(configArray)
            self.parent: SudokuState = parent #Class SudokuState
            self.depth: int = depth
            self.children: SudokuState = [] #Array of nodes
            self.findPossibleValues()
            self.printSudoku()
        else:
            self.sudoku: Cell = [[Cell for i in range(9)] for j in range(9)] #Array of Cells
            self.initiCells(configArray)
            self.parent: SudokuState = parent #Class SudokuState
            self.depth: int = depth
            self.children: SudokuState = [] #Array of nodes
            self.getCell(x, y).setValue(value)
            self.getCell(x, y).setFixed(True)
            self.configuration = self.getConfig()
            #print(self.configuration)
            self.findPossibleValues()
            #self.printSudoku()

    def initiCells(self, configArray):
        k = 0
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (configArray[k] != 0):
                    self.sudoku[x][y] = Cell(self, x + 1, y + 1, configArray[k], True)
                else:
                    self.sudoku[x][y] = Cell(self, x + 1, y + 1, configArray[k])
                k += 1

    def findPossibleValues(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                self.getCell(x, y).findPossibleValues()

    def getCell(self, x, y):
        return self.sudoku[x][y]

    def getConfig(self):
        configuration = []
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                configuration.append(self.getCell(x, y).getValue())
        return configuration

    def printSudoku(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                print("{:<4}".format(self.getCell(x, y).getValue()), end="")
            print()
        print("--------------------------------")

    def isSolved(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (self.getCell(x, y).getValue() is 0):
                    return False
        return True           

    def countPossibleValues(self):
        num = 0
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                num += len(self.getCell(x, y).possibleValues)
        #print(num)
        return num

    def leadsToSolution(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (len(self.getCell(x, y).possibleValues) == 0):
                    return False
        return True

    def createNode(self, x, y, value):
        if (value in self.getCell(x, y).possibleValues and not self.getCell(x, y).isFixed()):
            newSudoku = []
            for i in range(len(self.sudoku)):
                for j in range(len(self.sudoku)):
                    newSudoku.append(self.getCell(i, j).getValue())
            newSudokuState = SudokuState(self, self.depth + 1, newSudoku, False, x, y, value)
            return newSudokuState
        return None
 

    def expandNode(self):
        nodes = []
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (not self.getCell(x, y).isFixed()):
                    nodes.append(self.getCell(x, y))
        nodes.sort(key=lambda x: x.value)
        nodeToExpand = nodes[0]
        for value in nodeToExpand.possibleValues:
            self.children.append(self.createNode(nodeToExpand.row - 1, nodeToExpand.column - 1, value))
        return self.children

class Solver(object):
    def __init__(self, config):
        self.configArray = config.split(",")
        self.configArray = list(map(int, self.configArray))
        print("Start!")
        self.rootState = SudokuState(None, 0, self.configArray, True)
        #self.rootState.printSudoku()
        self.ast_search()

    def ast_search(self):
        initialState = self.rootState
        q = queue.PriorityQueue()
        counter = 0
        visited = []
        frontier = []
        q.put((1, 0, initialState))
        while not q.empty():
            currentState = q.get()[2]
            if currentState.isSolved():
                print("Solved")
                currentState.printSudoku()
                return currentState
            else:
                visited.append(currentState.configuration)
                if currentState.configuration in frontier: frontier.remove(currentState.configuration)
                children = currentState.expandNode()
                #print(len(children))
                for child in children:
                    counter += 1
                    if (child.configuration not in visited and child.configuration not in frontier and child.leadsToSolution()):
                        q.put((child.countPossibleValues(), counter, child))
                        frontier.append(child.configuration)
                    else:
                        continue
        print("No solution found")
        return None

 
        


S = Solver("5,3,0,0,7,0,0,0,0,6,0,0,1,9,5,0,0,0,0,9,8,0,0,0,0,6,0,8,0,0,0,6,0,0,0,3,4,0,0,8,0,3,0,0,1,7,0,0,0,2,0,0,0,6,0,6,0,0,0,0,2,8,0,0,0,0,4,1,9,0,0,5,0,0,0,0,8,0,0,7,9")
#S = Solver("5,3,4,6,7,8,9,1,2,6,7,2,1,9,5,3,4,8,1,9,8,3,4,2,5,6,7,8,5,9,7,6,1,4,2,3,4,2,6,8,5,3,7,9,1,7,1,3,9,2,4,8,5,6,9,6,1,5,3,7,2,8,4,2,8,7,4,1,9,6,3,5,3,4,5,2,8,6,1,7,9")