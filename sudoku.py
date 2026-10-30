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
        self.quadrant = self.set_quadrant()
        self.non_possible_values = []
        self.possible_values = []
        self.value = value
        self.fixed = fixed

    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

    def get_quadrant(self):
        return self.quadrant

    def set_fixed(self, value):
        self.fixed = value

    def is_fixed(self):
        return self.fixed

    def get_sudoku_state(self):
        return self.sudokuSate

    #Set the quadrant by numeration Thorem
    def set_quadrant(self):
        row_index = math.ceil(3 * self.row / 9)
        col_index = math.ceil(3 * self.column / 9)
        return (row_index - 1) * 3 + col_index
    
    #Compare each self with the ones in its own row, column and quadrant. Excludes self.
    #Save non repeating values only
    def find_non_possible_values(self):
        #Rows
        for x in range(len(self.sudokuSate.sudoku)):
            selected_cell = self.sudokuSate.getCell(x, self.column - 1)
            if (selected_cell.get_value() is not 0 and selected_cell is not self):
                if (selected_cell.get_value() not in self.non_possible_values):
                    self.non_possible_values.append(selected_cell.get_value())

        #Columns
        for y in range(len(self.sudokuSate.sudoku)):
            selected_cell = self.sudokuSate.getCell(self.row - 1, y)
            if (selected_cell.get_value() is not 0 and selected_cell is not self):
                if (selected_cell.get_value() not in  self.non_possible_values):
                    self.non_possible_values.append(selected_cell.get_value())

        #Quadrants
        for x in range(len(self.sudokuSate.sudoku)):
            for y in range(len(self.sudokuSate.sudoku)):
                selected_cell = self.sudokuSate.getCell(x, y)
                if (selected_cell.get_value() is not 0 and selected_cell.get_quadrant() == self.quadrant and selected_cell is not self):
                    if (selected_cell.get_value() not in self.non_possible_values):
                        self.non_possible_values.append(selected_cell.get_value())

    #Every digit from 1 to 9 that is not in Non Possible Values
    def find_possible_values(self):
        if (self.is_fixed()):
            self.possible_values.append(self.value)
        else:
            self.find_non_possible_values()
            for x in range(10):
                if (x not in self.non_possible_values and x > 0):
                    self.possible_values.append(x)
        #print(self.possible_values)


#----------------------------------------------SUDOKUSTATE------------------------------------------------------------------------------------

class SudokuState(object):
    def __init__(self, parent = None, depth: int = 0, configArray = None, isInitial: bool = False, x: int = 0, y: int = 0, value: int =0):

        #Generate Initial State
        if isInitial:
            self.sudoku: Cell = [[Cell for _ in range(9)] for _ in range(9)] #Array of Cells
            self.configuration = configArray
            self.initiCells(configArray)
            self.parent: SudokuState = parent #Class SudokuState
            self.depth: int = depth
            self.children: SudokuState = [] #Array of nodes
            self.find_possible_values()
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
            self.getCell(x, y).set_value(value)
            self.getCell(x, y).set_fixed(True)
            self.configuration = self.get_config()
            #print(self.configuration)
            #self.printFixedConfig()
            self.find_possible_values()
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
    def find_possible_values(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                self.getCell(x, y).find_possible_values()

    def getCell(self, x, y):
        return self.sudoku[x][y]

    #Return sudoku in a 1D array. For comparing.
    def get_config(self):
        configuration = []
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                configuration.append(self.getCell(x, y).get_value())
        return configuration

    def printFixedConfig(self):
        configuration = []
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (self.getCell(x, y).is_fixed()):
                    configuration.append(1)
                else:
                    configuration.append(0)
        print(configuration)

    def printSudoku(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (y % 3 == 0):
                    print("|", end = '')
                print("{:<4}".format(self.getCell(x, y).get_value()), end="")
            print()
            if ((x+1) % 3 == 0):
                print('------------------------------------')
        print('------------------------------------')

    #If no cell object has a value of 0, it is solved
    #This works only because of how the node expansion works
    def is_solved(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (self.getCell(x, y).get_value() is 0):
                    return False
        return True           

    #-------------------------------------------------- HEURISTICS --------------------------------------------------

    #Sum the length of every possible values array of cells
    def countpossible_values(self):
        num = 0
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                num += len(self.getCell(x, y).possible_values)
        #print(num)
        return num

    #If a cell runs of out possible solutions, this node does not lead to a solution
    def leadsToSolution(self):
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (len(self.getCell(x, y).possible_values) == 0):
                    return False
        return True

    #--------------------------------------------------SEARCH TREE FUNCTIONS-----------------------------------------------------------

    #Create node by creating a copy of the Sudoku State, then modify the x,y cell and set it to fixed.
    #The changes are made by the Cell Constructor
    #Create it only if the cell is not fixed
    def createNode(self, x, y, value):
        if (value in self.getCell(x, y).possible_values and not self.getCell(x, y).is_fixed()):
            new_sudoku = []
            for i in range(len(self.sudoku)):
                for j in range(len(self.sudoku)):
                    new_sudoku.append(self.getCell(i, j).get_value())
            new_sudoku_state = SudokuState(self, self.depth + 1, new_sudoku, False, x, y, value)
            return new_sudoku_state
        return None
 
    #Search for the non fixed cell with fewer possible values and create nodes with its values
    #Sort the cells in an array, ordered by the lengths of possible values array and take the first element
    def expand_node(self):
        nodes = []
        for x in range(len(self.sudoku)):
            for y in range(len(self.sudoku)):
                if (not self.getCell(x, y).is_fixed()):
                    nodes.append(self.getCell(x, y))
        nodes.sort(key=lambda x: len(x.possible_values))
        node_to_expand = nodes[0]
        for value in node_to_expand.possible_values:
            self.children.append(self.createNode(node_to_expand.row - 1, node_to_expand.column - 1, value))
        return self.children


#------------------------------------------------------------ SOLVER ---------------------------------------------------------------------------------------

class Solver(object):

    def __init__(self, config, string_separator):

        self.is_solvable = True
        if (string_separator == ''):
            self.configArray = list(config)
        else:
            self.configArray = config.split(string_separator)
        self.configArray = list(map(int, self.configArray))

        if (not self.config_is_null(self.configArray)):
            print("Start!")
            self.root_state = SudokuState(None, 0, self.configArray, True)
            #self.root_state.printSudoku()
            #self.ast_search()
        else:
            print('Invalid configuration')
            self.is_solvable = False
        

    def config_is_null(self, configList):
        someSum = 0
        for i in configList:
            if (i < 0 or i > 9 or i is None):
                return True
            else:
                someSum = someSum + i
        if (someSum == 0):
            return True
        else:
            return False

    def get_solved_config(self):
        if (not self.is_solvable):
            print("Configuration is not solvable")
            raise Exception("Configuration is not solvable") 
        solved_state = self.ast_search()
        return solved_state.get_config()


    def ast_search(self):
        initial_state = self.root_state
        q = queue.PriorityQueue()
        counter = 0
        visited = []
        frontier = []
        q.put((1, 0, initial_state))
        while not q.empty():
            current_state = q.get()[2]
            if current_state.is_solved():
                print("Solved")
                current_state.printSudoku()
                return current_state
            else:
                visited.append(current_state.configuration)
                if current_state.configuration in frontier: frontier.remove(current_state.configuration)
                children = current_state.expand_node()
                #print(len(children))
                for child in children:
                    counter += 1
                    if (child.configuration not in visited and child.configuration not in frontier and child.leadsToSolution()):
                        q.put((child.countpossible_values(), counter, child))
                        frontier.append(child.configuration)
        print("No solution found")
        return None


if __name__ == '__main__':
    # SOLVER CONSTRUCTORS

    S = Solver("5,3,0,0,7,0,0,0,0,6,0,0,1,9,5,0,0,0,0,9,8,0,0,0,0,6,0,8,0,0,0,6,0,0,0,3,4,0,0,8,0,3,0,0,1,7,0,0,0,2,0,0,0,6,0,6,0,0,0,0,2,8,0,0,0,0,4,1,9,0,0,5,0,0,0,0,8,0,0,7,9", ",")
    #S = Solver("5,3,4,6,7,8,9,1,2,6,7,2,1,9,5,3,4,8,1,9,8,3,4,2,5,6,7,8,5,9,7,6,1,4,2,3,4,2,6,8,5,3,7,9,1,7,1,3,9,2,4,8,5,6,9,6,1,5,3,7,2,8,4,2,8,7,4,1,9,6,3,5,3,4,5,2,8,6,1,7,9")

    #S = Solver("0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,8,5,0,0,1,0,2,0,0,0,0,0,0,0,5,0,7,0,0,0,0,0,4,0,0,0,1,0,0,0,9,0,0,0,0,0,0,0,5,0,0,0,0,0,0,7,3,0,0,2,0,1,0,0,0,0,0,0,0,0,4,0,0,0,9", ",")
    S.get_solved_config()

    
