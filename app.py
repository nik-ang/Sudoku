from tkinter import *
import sudoku as susuSolver

#Canvas Variables
HEIGHT = 700
WIDTH = 1600

#Main Window
window = Tk()
window.title("Sudoku Solver")
window.configure(bg="black")



#Canvas ---------------------------------------------------------------------------------------------------
canvas = Canvas(window, height=HEIGHT, width=WIDTH, bg='#32384f')
canvas.pack()

#Main Frame -----------------------------------------------------------------------------------------------
mainFrame = Frame(window, bg='black')
mainFrame.place(relx = 0.05, rely = 0.1, relwidth = 0.9, relheight = 0.8)

#Greet ----------------------------------------------------------------------------------------------------
greetFrame = Frame(mainFrame)
greetFrame.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.05)

greet = Label(greetFrame, text='Hello there! Please enter your Sudoku configuration')
greet.place(relheight = 1, relwidth = 1)

#Sudoku Main Frame ---------------------------------------------------------------------------------------
sudokuMainFrame = Frame(mainFrame, bg='black')
sudokuMainFrame.place(rely = 0.05, relheight = 1, relwidth = 1)

#SudokuInputFrame ----------------------------------------------------------------------------------------
sudokuInputFrame = Frame(sudokuMainFrame, bg='#15161f')
sudokuInputFrame.place(relx = 0, relwidth = 0.5, relheight = 1)

sudokuInputRect = Frame(sudokuInputFrame, bg='black')
sudokuInputRect.place(relx = 0.1, relwidth = 0.8, rely = 0.1, relheight = 0.8)


sudokuInputEntries = [[0 for i in range(9)] for j in range(9)]
for i in range(9):
    for j in range(9):
        sudokuInputEntries[i][j] = Entry(sudokuInputRect, bg='#a8a8a8', justify = 'center', borderwidth = 0.5, relief = 'groove')
        sudokuInputEntries[i][j].place(relx = (j/9), rely = (i/9), relheight = 1/9, relwidth = 1/9)


sudokuInputMarkersI = [None for i in range(3)]
for i in range(3):
	sudokuInputMarkersI[i] = Frame(sudokuInputRect, bg = 'black')
	sudokuInputMarkersI[i].place(relx = (i+1)/3, relheight = 1, relwidth = 0.01)

sudokuInputMarkersJ = [None for i in range(3)]
for j in range(3):
	sudokuInputMarkersJ[j] = Frame(sudokuInputRect, bg = 'black')
	sudokuInputMarkersJ[j].place(rely = (j+1)/3, relwidth = 1, relheight = 0.01)


        
#SudokuOutputFrame ---------------------------------------------------------------------------------------
sudokuOutputFrame = Frame(sudokuMainFrame, bg='#42444f')
sudokuOutputFrame.place(relx = 0.5, relwidth = 0.5, relheight = 1)

sudokuOutputRect = Frame(sudokuOutputFrame, bg = 'black')
sudokuOutputRect.place(relx = 0.1, relwidth = 0.8, rely = 0.1, relheight = 0.8)

sudokuOutputSquare = [[None for i in range (9)] for j in range(9)]
k = 0
for i in range(9):
    for j in range(9):
        sudokuOutputSquare[i][j] = Label(sudokuOutputRect, text=0, bg='white', borderwidth = 2, relief = 'groove')
        sudokuOutputSquare[i][j].place(relx = (j/9), rely = (i/9), relheight = 1/9, relwidth = 1/9)


sudokuOutputMarkersI = [None for i in range(3)]
for i in range(3):
	sudokuOutputMarkersI[i] = Frame(sudokuOutputRect, bg = 'black')
	sudokuOutputMarkersI[i].place(relx = (i+1)/3, relheight = 1, relwidth = 0.01)

sudokuOutputMarkersJ = [None for i in range(3)]
for j in range(3):
	sudokuOutputMarkersJ[j] = Frame(sudokuOutputRect, bg = 'black')
	sudokuOutputMarkersJ[j].place(rely = (j+1)/3, relwidth = 1, relheight = 0.01)


#METHODS ------------------------------------------------------------------------------------------------

def getEntry2D():
	inputConfig = [[None for i in range (9)] for j in range(9)]
	for i in range(len(sudokuInputEntries)):
		for j in range(len(sudokuInputEntries[i])):
			if (sudokuInputEntries[i][j].get() == None or sudokuInputEntries[i][j].get() == ''):
				inputConfig[i][j] = 0
			else: 
				inputConfig[i][j] = sudokuInputEntries[i][j].get()
	#print(inputConfig)
	return(inputConfig)


def parseInputToString(entry):
	inputConfig = ''
	for i in range(len(entry)):
		for j in range(len(entry[i])):
			inputConfig = inputConfig + str(entry[i][j])
	return(inputConfig)

def solveSudoku(event):
	configuration = parseInputToString(getEntry2D())
	S = susuSolver.Solver(configuration, '')
	solvedConfig = S.getSolvedConfig()
	k = 0
	for i in range(9):
		for j in range(9):
			sudokuOutputSquare[i][j]['text'] = solvedConfig[k]
			k = k + 1


window.bind('<Return>', solveSudoku)

window.mainloop()



	