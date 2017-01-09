import copy
import tkinter
from cell import *
from util import *

class LogicBoard:

        def __init__(self, rows, columns):
            self.cells = []
            self.victory_cond = False

        def make_field(self, x, y):
            for i in range(x):
                row = []
                self.cells.append(row)
                for j in range (y):
                        self.cells[i].append(Logic_Cell(color=define_color(i+1,j+1) ,  row = i+1, column = j+1))       

        def move_checker (self, coordinats):
            column1 = coordinats[0]
            row1 = coordinats[1]
            column2= coordinats [2]
            row2 = coordinats[3]
            if  self.cells[row1-1][column1-1].is_black:
                self.cells[row2-1][column2-1].put_black()
            if  self.cells[row1-1][column1-1].is_white:
                self.cells[row2-1][column2-1].put_white()
            if is_queen(self,column2,row2,column1,row1):
                self.cells[row2-1][column2-1].became_queen()
            self.cells[row1-1][column1-1].clear()
                
        def kill_checker (self, coordinats):
            column = coordinats[0]
            row = coordinats[1]
            self.cells[row-1][column-1].clear()

        def stand_checkers(board, num_of_rows):
            for i in range (len(board.cells)):
                if i < num_of_rows:
                    for cell in board.cells[i]:
                        if cell.color == "black":
                            cell.put_white()
                if i >= len(board.cells)-num_of_rows:
                    for cell in board.cells[i]:
                        if cell.color == "black":
                            cell.put_black()
                            
        def victory(self):
            self.victory_cond = True
            self.victory = True


            



class Board (tkinter.Frame, LogicBoard):
        
        def __init__(self, window, rows, columns):
            tkinter.Frame.__init__(self, window)
            LogicBoard.__init__(self, rows, columns)
            self.window = window
            self.empty = tkinter.PhotoImage(file ='empty.gif')

        def make_usability(self, button_function):
            self.bind_class('Button', '<1>', button_function)

        def make_field(board, x, y):
            for i in range(x):
                row = []
                board.cells.append(row)
                for j in range (y):
                        board.cells[i].append(Cell(board,  color=define_color(i+1,j+1) , width=50,height=50, row = i+1, column = j+1))
                        board.cells[i][j]['image']=board.empty
            for rows in range(x):
                for cell in range(y):
                        board.cells[rows][cell].grid(row=x-board.cells[rows][cell].row,column=board.cells[rows][cell].column)
        
        def victory(self, text):
                LogicBoard.victory(self)
                for row in self.cells:
                        for cell in row:
                                cell.destroy()
                message = tkinter.Label(self, text = text, width = 50, height = 50)
                message.grid(column = 2, row = 0)

