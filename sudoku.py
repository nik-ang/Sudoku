"""
---------------------------------------------------------- HOW THIS CODE WORKS-----------------------------------------------------------------
    
    1. Look for every possible value for every cell
    2. Take the cell with fewer possible values and create nodes by creating new configurations with every value it cat get
    3. Take the new nodes and count every possible value every cell can get, the sum that amount (Heuristic: smaller sums are priority)
    4. Check if it leads to a solution or is a dead end
    5. Add to search tree with the heuristic only if it leads to a solution
    6. Repeat 2 to 5 until you find the solution
    7. Print Solution

NICO FERREIRA
-----------------------------------------------------------------------------------------------------------------------------------------------

"""


import math
import queue

# ---------------------------------------------------------- CELL ------------------------------------------------------------------

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
        self.fixed = value

    def isFixed(self):
        return self.fixed

    def getSudokuState(self):
        return self.sudokuSate

    #Set the quadrant by numeration Thorem
    def setQuadrant(self):
        rowIndex = math.ceil( 3*self.row / 9)
        columnIndex = math.ceil( 3*self.column / 9)
        return (rowIndex - 1) * 3 + columnIndex
    
    #Compare each self with the ones in its own row, column and quadrant. Excludes self.
    #Save non repeating values only
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

    #Every digit from 1 to 9 that is not in Non Possible Values
    def findPossibleValues(self):
        if (self.isFixed()):
            self.possibleValues.append(self.value)
        else:
            self.findNonPossibleValues()
            for x in range(10):
                if (x not in self.nonPossibleValues and x > 0):
                    self.possibleValues.append(x)
        #print(self.possibleValues)


#----------------------------------------------SUDOKUSTATE------------------------------------------------------------------------------------

class SudokuState(object):
    def __init__(self, parent = None, depth: int = 0, configArray = None, isInitial: bool = False, x: int = 0, y: int = 0, value: int =0):

        #Generate Initial State
        if isInitial:
            self.sudoku: Cell = [[Cell for i in range(9)] for j in range(9)] #Array of Cells
            self.configuration = configArray
            self.initiCells(configArray)
            self.parent: SudokuState = parent #Class SudokuState
            self.depth: int = depth
            self.children: SudokuState = [] #Array of nodes
            self.findPossibleValues()
            #print(self.configuration)
            self.printSudoku()

        #Generate Child Node
        #Copy exact configuration, change the targeted cell and set it to fixed.
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
            #self.printFixedConfig()
            self.findPossibleValues()
            #self.printSudoku()

    #Initialize Cell Objects in Array
    #Non 0 cells are initialized as fixed
    def initiCells(self, configArray):
        k = 0
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (configArray[k] != 0):
                    self.sudoku[x][y] = Cell(self, x + 1, y + 1, configArray[k], True)
                else:
                    self.sudoku[x][y] = Cell(self, x + 1, y + 1, configArray[k])
                k += 1

    #Find the possible values of every cell object
    def findPossibleValues(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                self.getCell(x, y).findPossibleValues()

    def getCell(self, x, y):
        return self.sudoku[x][y]

    #Return sudoku in a 1D array. For comparing.
    def getConfig(self):
        configuration = []
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                configuration.append(self.getCell(x, y).getValue())
        return configuration

    def printFixedConfig(self):
        configuration = []
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (self.getCell(x, y).isFixed()):
                    configuration.append(1)
                else:
                    configuration.append(0)
        print(configuration)

    def printSudoku(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (y % 3 == 0):
                    print("|", end = '')
                print("{:<4}".format(self.getCell(x, y).getValue()), end="")
            print()
            if ((x+1) % 3 == 0):
                print('------------------------------------')
        print('------------------------------------')

    #If no cell object has a value of 0, it is solved
    #This works only because of how the node expansion works
    def isSolved(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (self.getCell(x, y).getValue() is 0):
                    return False
        return True           

    #-------------------------------------------------- HEURISTICS --------------------------------------------------

    #Sum the length of every possible values array of cells
    def countPossibleValues(self):
        num = 0
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                num += len(self.getCell(x, y).possibleValues)
        #print(num)
        return num

    #If a cell runs of out possible solutions, this node does not lead to a solution
    def leadsToSolution(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (len(self.getCell(x, y).possibleValues) == 0):
                    return False
        return True

    #--------------------------------------------------SEARCH TREE FUNCTIONS-----------------------------------------------------------

    #Create node by creating a copy of the Sudoku State, then modify the x,y cell and set it to fixed.
    #The changes are made by the Cell Constructor
    #Create it only if the cell is not fixed
    def createNode(self, x, y, value):
        if (value in self.getCell(x, y).possibleValues and not self.getCell(x, y).isFixed()):
            newSudoku = []
            for i in range(len(self.sudoku)):
                for j in range(len(self.sudoku)):
                    newSudoku.append(self.getCell(i, j).getValue())
            newSudokuState = SudokuState(self, self.depth + 1, newSudoku, False, x, y, value)
            return newSudokuState
        return None
 
    #Search for the non fixed cell with fewer possible values and create nodes with its values
    #Sort the cells in an array, ordered by the lengths of possible values array and take the first element
    def expandNode(self):
        nodes = []
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (not self.getCell(x, y).isFixed()):
                    nodes.append(self.getCell(x, y))
        nodes.sort(key=lambda x: len(x.possibleValues))
        nodeToExpand = nodes[0]
        for value in nodeToExpand.possibleValues:
            self.children.append(self.createNode(nodeToExpand.row - 1, nodeToExpand.column - 1, value))
        return self.children


#------------------------------------------------------------ SOLVER ---------------------------------------------------------------------------------------

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

 # SOLVER CONSTRUCTORS

#S = Solver("5,3,0,0,7,0,0,0,0,6,0,0,1,9,5,0,0,0,0,9,8,0,0,0,0,6,0,8,0,0,0,6,0,0,0,3,4,0,0,8,0,3,0,0,1,7,0,0,0,2,0,0,0,6,0,6,0,0,0,0,2,8,0,0,0,0,4,1,9,0,0,5,0,0,0,0,8,0,0,7,9")
#S = Solver("5,3,4,6,7,8,9,1,2,6,7,2,1,9,5,3,4,8,1,9,8,3,4,2,5,6,7,8,5,9,7,6,1,4,2,3,4,2,6,8,5,3,7,9,1,7,1,3,9,2,4,8,5,6,9,6,1,5,3,7,2,8,4,2,8,7,4,1,9,6,3,5,3,4,5,2,8,6,1,7,9")

#S = Solver("0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,8,5,0,0,1,0,2,0,0,0,0,0,0,0,5,0,7,0,0,0,0,0,4,0,0,0,1,0,0,0,9,0,0,0,0,0,0,0,5,0,0,0,0,0,0,7,3,0,0,2,0,1,0,0,0,0,0,0,0,0,4,0,0,0,9")

    
