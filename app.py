from tkinter import *

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
sudokuInputFrame = Frame(sudokuMainFrame, bg='red')
sudokuInputFrame.place(relx = 0, relwidth = 0.5, relheight = 1)





window.mainloop()