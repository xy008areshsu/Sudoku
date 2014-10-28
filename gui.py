# Gui.py
# ------
# Licensing Information:
# Created by Ye Xu on 10/25/2014
# copyright (c) 2014 Ye Xu. All rights reserved

"""
In Gui.py, The view and controller parts of the model view controller (MVC) are implemented here. It uses pygame and
tkinter package for python3 to render the simulation of Sudoku puzzle.

To run the gui app, make sure the following are properly installed in your computer (this app was fully tested under
windows and linux, but not yet under mac os):

    1.  Python 3 interpreter: This Sudoku project was developed using python 3, rather than python 2. There are some
        syntax differences between the two versions of python (e.g. print), and some package names are changed (e.g.
        Tkinter for python 2, and tkinter for python 3). To install python 3, see: https://www.python.org/downloads/

    2.  pygame for python 3: Since tkinter is already installed in python by default (although under some OS, you might
        need to make sure tcl/Tk is properly installed to use tkinter), you only need to install pygame for graphical
        simulation of this app. To install pygame under windows, see: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
        To install pygame under ubuntu linux, type in the command line: sudo apt-get install python3-pygame, or you might
        want to see their official website: http://www.pygame.org/download.shtml

To run the app under linux, go to the root directory of the app and type in the command line: python3 gui.py. To run under
windows, you can use any python IDE, for example pyCharm, or use terminal tools like cygwin. After the app starts, there
are following steps to run:

    1.  Click the "load csv file" button and choose the proper csv file as an input. So far, the app only supports a csv
        file as the input, which contains 9 * 9 cells, each with a value of the puzzle. If the value is 0, this square
        or cell is not solved yet, otherwise the value should be any digit from 1 to 9.

    2.  Then the app will try to solve the puzzle. 99% of the Sudoku puzzles are solvable, so if the app finds a valid
        solution, it will automatically pop up a new window showing the two states of the puzzle, initial state and the
        solved final state. You can click the mouse to toggle between the initial and the final state of the puzzle

    3.  The app will also generate an output csv file with the name of initial csv file plus '_sol' (e.g. initial puzzle:
        file.csv, output: file_sol.csv), and store it at the same location as the initial csv file. So it is a good idea
        to put both files into some specific folder, such as the Data folder.

    4.  This app currently uses back-tracking search plus forward checking as the algorithm to solve the puzzle (see the
        solver.py file). Most of the puzzles can be solved less than 50 ms, but some more difficult ones might take 4 to
        5 seconds to solve. So after you choose the csv file, if the result does not show up (the new pop up window)
        immediately, just be patient.

"""


import pygame, sys
from pygame.locals import *
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import utility
from solver import Solver



class GraphicInterface(Tk):
    """
    This class is for GUI interface, using tkinter and pygame.
    """

    def __init__(self, **kwargs):
        """
        Setup windows, input fields, buttons, etc, for rendering
        """

        ## Set up couple of class constants, used for rendering
        # Sets size of grid
        self.WINDOWMULTIPLIER = 5 # Modify this number to change size of grid
        self.WINDOWSIZE = 81
        self.WINDOWWIDTH = self.WINDOWSIZE * self.WINDOWMULTIPLIER
        self.WINDOWHEIGHT = self.WINDOWSIZE * self.WINDOWMULTIPLIER
        self.SQUARESIZE = (self.WINDOWSIZE * self.WINDOWMULTIPLIER) // 3
        self.CELLSIZE = self.SQUARESIZE // 3
        self.NUMBERSIZE = self.CELLSIZE // 3 # Position of unsolved number
        self.BASICFONTSIZE = 15
        self.LARGEFONTSIZE = 55

        # Set up the colours
        self.BLACK = (0,  0,  0)
        self.WHITE = (255,255,255)
        self.LIGHTGRAY = (200, 200, 200)
        self.GREEN = (0,255,0)
        self.RED = (255, 0, 0)

        self.FPS = 10


        # window setup
        super().__init__(**kwargs)
        self.wm_title("Sudoku Graphical Interface")
        self.resizable(0,0)
        self.filename = ''
        self.grid = ''
        interface = Frame()
        interface.grid(padx=2, pady=2)

        # Fields setup
        tLabel = Label(interface, text='Welcome to Sudoku Graphical User Interface')
        tLabel.grid(row = 0, column = 0)
        tLabel2 = Label(interface, text="Please click 'Load csv file' button, select a csv file for input and run")
        tLabel2.grid(row = 1, column = 0)
        tLabel3 = Label(interface, text = 'This app currently only supports csv files as inputs, with 9 * 9 grid representing the puzzle')
        tLabel3.grid(row = 2, column = 0)
        tLabel4 = Label(interface, text = ' ')
        tLabel4.grid(row = 3, column = 0)
        tLabel4 = Label(interface, text = ' ')
        tLabel4.grid(row = 4, column = 0)
        tLabel4 = Label(interface, text = 'Copyright (c) Ye Xu. All rights reserved!')
        tLabel4.grid(row = 5, column = 0)
        tButton = Button(interface, text="Load csv file", command=lambda:self.on_click())
        tButton.grid(row=1, column=3, padx=2, pady=2)
        tButton1 = Button(interface, text='Quit', width=17, command= self.destroy)
        tButton1.grid(row=5, column=3, padx=2, pady=2)

    def start(self):
        # Shows the Gui
        self.winfo_children()
        self.mainloop()


    def on_click(self):
        """
        'Load csv file' button's on_click call-back listener. It will do a couple of things:
        1. Get the filename of the csv file
        2. Load csv file, and convert the data into the grid data for the Sudoku solver class
        3. Open up a pygame graph to show the simulation of solving the puzzle
        """
        init_dir = './Data'
        name = 'Choose your file'
        filetype = (("csv files","*.csv"))

        self.get_filename(init_dir, name, filetype)
        self.grid = utility.load_csv(self.filename)

        while len(self.grid) != 81 or len(set(self.grid).difference(set('1234567890'))) != 0:
            """
            This part checks if the csv file is in correct format: 9 * 9 grid with only '1234567890' digits
            """
            self.pop_up("Wrong content in csv file. Make sure it is a 9 * 9 grid with only '1234567890' digits")
            self.get_filename(init_dir, name, filetype)
            self.grid = utility.load_csv(self.filename)

        # Solve the puzzle here
        self.sudoku = Solver(self.grid)
        t, final_values = self.sudoku.solve()
        if final_values == False:
            self.pop_up('There is no solution for this puzzle. Try another one!')
            return
        else:
            # If puzzle is successfully solved, write to csv file and open pygame to demo the result
            output = self.filename[:-4] + '_sol.csv'
            utility.write_csv(output, self.sudoku.final_values)
            self.open_pygame()


    def open_pygame(self):
        """
        This function will open up pygame graphs and run the Sudoku simulation
        """

        pygame.init()

        # set up a bunch of parameters for pygame
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', self.BASICFONTSIZE)
        self.LARGEFONT = pygame.font.Font('freesansbold.ttf', self.LARGEFONTSIZE)
        pygame.display.set_caption('Sudoku Solver: click mouse to see results')

        self.DISPLAYSURF.fill(self.WHITE)

        # fonts
        pygame.font.init()
        font = pygame.font.Font(None, 28)
        version = font.render("Initial Values", False, self.BLACK)

        # mouse click events, we use this to detect if a mouse is clicked
        mouse_clicked = False

        # main step of pygame rendering starts here
        currentGrid = self.setCellValues(self.sudoku.init_values)
        self.displayCells(currentGrid, self.RED)
        self.drawGrid()
        self.DISPLAYSURF.blit(version, (0, 0))
        count = 0
        mouse_detect = 0
        while True: # main game loop, if mouse clicked, window will toggle between initial and solved values
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    mouse_clicked = True

            # mouse-clicked event handler
            if mouse_clicked == True:
                mouse_clicked = False
                mouse_detect += 1
                if mouse_detect % 2 == 1:
                    currentGrid = self.setCellValues(self.sudoku.final_values)
                    version = font.render("Solved: click mouse to go back", False, self.BLACK)
                    self.DISPLAYSURF.fill(self.WHITE)
                    self.displayCells(currentGrid, self.GREEN)
                    self.drawGrid()
                    self.DISPLAYSURF.blit(version, (0, 0))
                else:
                    currentGrid = self.setCellValues(self.sudoku.init_values)
                    version = font.render("Unsolved: now click mouse", False, self.BLACK)
                    self.DISPLAYSURF.fill(self.WHITE)
                    self.displayCells(currentGrid, self.RED)
                    self.drawGrid()
                    self.DISPLAYSURF.blit(version, (0, 0))

            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)


    def get_filename(self, init_dir, name, filetype):
        """
        This function sets the filename of the input csv file

        :param init_dir: Initial directory to look for input csv files
        :param name: Name of the selecting button
        :param filetype: File type allowed as the input
        """
        try:
            self.filename =  filedialog.askopenfilename(initialdir = init_dir,title = name,filetypes = (filetype,("csv files","*.csv")))
        except Exception as inst:
            self.pop_up(inst)
            self.filename =  filedialog.askopenfilename(initialdir = init_dir,title = name,filetypes = (filetype,("csv files","*.csv")))


    def pop_up(self, _text = ''):
        """
        This function shows a pop up windows with certain messages, using tkinter TopLevel widget
        :param _text: Message to be shown
        """
        toplevel = Toplevel()
        top_label = Label(toplevel, text = ' ')
        top_label.grid(row = 0, column = 0)
        top_label2 = Label(toplevel, text = ' ')
        top_label2.grid(row = 1, column = 0)
        label = Label(toplevel, text=_text)
        label.grid(row=2, column=0)
        bottom_label = Label(toplevel, text = ' ')
        bottom_label.grid(row = 3, column = 0)
        bottom_label2 = Label(toplevel, text = ' ')
        bottom_label2.grid(row = 4, column = 0)



    def drawGrid(self):
        """
        This function draws grid lines on the Sudoku box
        """

        ### Draw Minor Lines
        for x in range(0, self.WINDOWWIDTH, self.CELLSIZE): # draw vertical lines
            pygame.draw.line(self.DISPLAYSURF, self.LIGHTGRAY, (x,0),(x,self.WINDOWHEIGHT))
        for y in range (0, self.WINDOWHEIGHT, self.CELLSIZE): # draw horizontal lines
            pygame.draw.line(self.DISPLAYSURF, self.LIGHTGRAY, (0,y), (self.WINDOWWIDTH, y))

        ### Draw Major Lines
        for x in range(0, self.WINDOWWIDTH, self.SQUARESIZE): # draw vertical lines
            pygame.draw.line(self.DISPLAYSURF, self.BLACK, (x,0),(x,self.WINDOWHEIGHT))
        for y in range (0, self.WINDOWHEIGHT, self.SQUARESIZE): # draw horizontal lines
            pygame.draw.line(self.DISPLAYSURF, self.BLACK, (0,y), (self.WINDOWWIDTH, y))


    def setCellValues(self, sudoku_values):
        """
        This function map from the format from solver.py to the format used here in the gui. In solver.py, for efficiency,
        the sudoku_values are represented as a dictionary with the keys as a string such as 'D4'; whereas here in the gui,
        the sudoku_values are represented as a dictionary with the keys as a tuple such as (7, 3). So, 'D' will be mapped
        into 7 and '4' will be mapped into 3 here.

        :param sudoku_values: this is from the solver.py representation
        :return: updated cell values
        """
        currentGrid = {}
        c2d_map = {'A': 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G' : 6, 'H' : 7, 'I' : 8}
        for key, item in sudoku_values.items():
            xCoord = int(key[1]) - 1
            yCoord = c2d_map[key[0]]
            currentGrid[xCoord,yCoord] = [int(v) for v in item]
        return currentGrid

    def populateCells(self, cellData, x, y, color):
        """
        writes cellData at given x, y co-ordinates
        """
        cellSurf = self.LARGEFONT.render('%s' %(cellData), True, color)
        cellRect = cellSurf.get_rect()
        cellRect.topleft = (x, y)
        self.DISPLAYSURF.blit(cellSurf, cellRect)


    def displayCells(self, currentGrid, color):
        """
        Displays the cells with the values assigned to them, and specify the color
        """
        xFactor = 0
        yFactor = 0
        for item in currentGrid: # item is x,y co-ordinate from 0 - 8
            cellData = currentGrid[item] # isolates the numbers still available for that cell
            for number in cellData: #iterates through each number
                if number != 0: # ignores those already dismissed
                    xFactor = ((number-1)%3) # 1/4/7 = 0 2/5/8 = 1 3/6/9 =2
                    if number <= 3:
                        yFactor = 0
                    elif number <=6:
                        yFactor = 1
                    else:
                        yFactor = 2
                    self.populateCells(number,(item[0]*self.CELLSIZE),(item[1]*self.CELLSIZE), color)
        return None




if __name__ == '__main__':
    """
    The main function called when gui.py is run
    from the command line:

    > python3 gui.py
    """

    interface = GraphicInterface()
    interface.start()

