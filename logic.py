import tkinter
import copy
import util
from tkinter import *
from board import *
from cell import Cell

class Logic():
    def __init__(self, board):
        self.possible_move_whites = []
        self.possible_move_blacks = []
        self.be_killed_by_whites = []
        self.be_killed_by_blacks = []
        self.whites_need_kill = []
        self.blacks_need_kill = []
        self.need_kill_whites = False
        self.need_kill_blacks = False
        self.first_need_kill_whites = False
        self.first_need_kill_blacks = False
        self.possible_move(board)
        self.need_to_kill(board)
        self.good_moves_whites = []
        self.good_moves_black = []
        self.simple_moves_black = []
        self.simple_moves_whites = []


    def possible_move(self, board):
        for row in board.cells:
            for cell in row:
                if cell.is_white and not cell.queen:
                    if cell.column < len(row):
                        if board.cells[cell.row][cell.column].is_empty():
                            self.possible_move_whites.append([cell.column, cell.row, cell.column+1, cell.row+1])
                    if cell.column > 1:
                        if board.cells[cell.row][cell.column-2].is_empty():
                            self.possible_move_whites.append([cell.column, cell.row, cell.column-1, cell.row+1])            
                if cell.is_black and not cell.queen:
                    if cell.column >1:
                        if board.cells[cell.row-2][cell.column-2].is_empty():
                            self.possible_move_blacks.append([cell.column, cell.row, cell.column-1, cell.row-1])
                    if cell.column < len(row):
                        if board.cells[cell.row-2][cell.column].is_empty():
                            self.possible_move_blacks.append([cell.column, cell.row, cell.column+1, cell.row-1])
                if cell.queen:
                    i = 1
                    while cell.column+i <= len(row) and cell.row+i<= len (board.cells):
                        if board.cells[cell.row - 1 + i][cell.column - 1 + i].is_empty():
                            if cell.is_black:
                                self.possible_move_blacks.append([cell.column, cell.row, cell.column+i, cell.row+i])
                            if cell.is_white:
                                self.possible_move_whites.append([cell.column, cell.row, cell.column+i, cell.row+i])
                            i=i+1
                        else:
                            break
                    i = 1
                    while cell.column-i >= 0 and cell.row+i<= len (board.cells):
                        if board.cells[cell.row - 1 + i][cell.column - 1 - i].is_empty(): 
                            if cell.is_black:
                                self.possible_move_blacks.append([cell.column, cell.row, cell.column-i, cell.row+i])
                            if cell.is_white:
                                self.possible_move_whites.append([cell.column, cell.row, cell.column-i, cell.row+i])
                            i=i+1
                        else:
                            break
                    i = 1
                    while cell.column-i >= 0 and cell.row-i >= 0:
                        if board.cells[cell.row - 1 - i][cell.column - 1 - i].is_empty(): 
                            if cell.is_black:
                                self.possible_move_blacks.append([cell.column, cell.row, cell.column-i, cell.row-i])
                            if cell.is_white:
                                self.possible_move_whites.append([cell.column, cell.row, cell.column-i, cell.row-i])
                            i=i+1
                        else:
                            break

                    i = 1
                    while cell.column+i <= len(row) and cell.row-i >= 0:
                        if board.cells[cell.row - 1 - i][cell.column - 1 + i].is_empty(): 
                            if cell.is_black:
                                self.possible_move_blacks.append([cell.column, cell.row, cell.column+i, cell.row-i])
                            if cell.is_white:
                                self.possible_move_whites.append([cell.column, cell.row, cell.column+i, cell.row-i])
                            i=i+1
                        else:
                            break

    def need_to_kill(self, board):
        
        for row in board.cells:
            for cell in row:
                self.cell_need_kill([cell.column,cell.row],board)

    def cell_need_kill (self, cell_coordinats, board):
        
        need_kill = False
        cell = board.cells[cell_coordinats[1]-1][cell_coordinats[0]-1]
        row = board.cells[0]
        if cell.is_white and not cell.queen:
                    if cell.column < len(row)-1 and cell.row < len(board.cells)-1:
                        if board.cells[cell.row][cell.column].is_black and board.cells[cell.row+1][cell.column+1].is_empty():
                            self.need_kill_whites = True
                            self.whites_need_kill.append([cell.column, cell.row, cell.column+2, cell.row+2])
                            self.be_killed_by_whites.append([cell.column+1, cell.row+1])
                            need_kill = True
                    if cell.column > 2 and cell.row < len(board.cells)-1:
                        if board.cells[cell.row][cell.column-2].is_black and board.cells[cell.row+1][cell.column-3].is_empty():
                            self.need_kill_whites = True
                            self.whites_need_kill.append([cell.column, cell.row, cell.column-2, cell.row+2])
                            self.be_killed_by_whites.append([cell.column-1, cell.row+1])
                            need_kill = True
                    if cell.column >2 and cell.row>2:
                        if board.cells[cell.row-2][cell.column-2].is_black and board.cells[cell.row-3][cell.column-3].is_empty():
                            self.need_kill_whites = True
                            self.whites_need_kill.append([cell.column, cell.row, cell.column-2, cell.row-2])
                            self.be_killed_by_whites.append([cell.column - 1, cell.row - 1])
                            need_kill = True
                    if cell.column < len(row)-1 and cell.row>2:
                        if board.cells[cell.row-2][cell.column].is_black and board.cells[cell.row-3][cell.column+1].is_empty():
                            self.whites_need_kill.append([cell.column, cell.row, cell.column+2, cell.row-2])
                            self.be_killed_by_whites.append([cell.column+1, cell.row -1])
                            self.need_kill_whites = True
                            need_kill = True
	
        if cell.is_black and not cell.queen:
                    if cell.column >2 and cell.row>2:
                        if board.cells[cell.row-2][cell.column-2].is_white and board.cells[cell.row-3][cell.column-3].is_empty():
                            self.need_kill_blacks = True
                            need_kill = True
                            self.blacks_need_kill.append([cell.column, cell.row, cell.column-2, cell.row-2])
                            self.be_killed_by_blacks.append([cell.column - 1, cell.row - 1])
                    if cell.column < len(row)-1 and cell.row > 2:
                        if board.cells[cell.row-2][cell.column].is_white and board.cells[cell.row-3][cell.column+1].is_empty():
                            self.blacks_need_kill.append([cell.column, cell.row, cell.column+2, cell.row-2])
                            self.be_killed_by_blacks.append([cell.column+1, cell.row -1])
                            self.need_kill_blacks = True
                            need_kill = True
                            
                    if cell.column < len(row)-1 and cell.row < len(board.cells)-1:
                        if board.cells[cell.row][cell.column].is_white and board.cells[cell.row+1][cell.column+1].is_empty():
                            self.need_kill_blacks = True
                            need_kill = True
                            self.blacks_need_kill.append([cell.column, cell.row, cell.column+2, cell.row+2])
                            self.be_killed_by_blacks.append([cell.column+1, cell.row+1])
                    if cell.column > 2 and cell.row < len(board.cells)-1:
                        if board.cells[cell.row][cell.column-2].is_white and board.cells[cell.row+1][cell.column-3].is_empty():
                            self.need_kill_blacks = True
                            self.blacks_need_kill.append([cell.column, cell.row, cell.column-2, cell.row+2])
                            self.be_killed_by_blacks.append([cell.column-1, cell.row+1])
                            need_kill = True
        if cell.queen:
                    i = 1
                    while cell.column+i <= len(row)-1 and cell.row+i<= len (board.cells) -1:
                        if (not board.cells[cell.row - 1 + i][cell.column - 1 + i].is_empty()) and board.cells[cell.row - 1 + i+1][cell.column - 1 + i+1].is_empty():
                            if cell.is_black and board.cells[cell.row - 1 + i][cell.column - 1 + i].is_white:
                                j = 1
                                while cell.column+i+j <= len(row) and cell.row+i +j<= len (board.cells):
                                    if board.cells[cell.row - 1 + i+j][cell.column - 1 + i+j].is_empty():
                                        self.blacks_need_kill.append([cell.column, cell.row, cell.column+i+j, cell.row+i+j])
                                        self.be_killed_by_blacks.append([cell.column+i, cell.row +i])
                                        self.need_kill_blacks = True
                                        need_kill = True
                                        j=j+1
                                    else:
                                        break
                            if cell.is_white and board.cells[cell.row - 1 + i][cell.column - 1 + i].is_black:
                                j = 1
                                while cell.column+i+j <= len(row) and cell.row+i +j<= len (board.cells):
                                    if board.cells[cell.row - 1 + i+j][cell.column - 1 + i+j].is_empty():
                                        self.whites_need_kill.append([cell.column, cell.row, cell.column+i+j, cell.row+i+j])
                                        self.be_killed_by_whites.append([cell.column+i, cell.row +i])
                                        self.need_kill_whites = True
                                        need_kill = True
                                        j = j+1
                                    else:
                                        break
                            break
                        elif not board.cells[cell.row - 1 + i][cell.column - 1 + i].is_empty():
                            break
                        else:
                            i= i+1
                    i = 1
                    while cell.column-i >= 1 and cell.row+i<= len (board.cells) -1:
                        if (not board.cells[cell.row - 1 + i][cell.column - 1 - i].is_empty()) and board.cells[cell.row - 1 + i+1][cell.column - 1 - i-1].is_empty():
                            if cell.is_black and board.cells[cell.row - 1 + i][cell.column - 1 - i].is_white:
                                j = 1
                                while cell.column-i-j > 0 and cell.row+i+j<= len (board.cells):
                                    if board.cells[cell.row - 1 + i+j][cell.column - 1 - i-j].is_empty(): 
                                        self.blacks_need_kill.append([cell.column, cell.row, cell.column-i-j, cell.row+i+j])
                                        self.be_killed_by_blacks.append([cell.column-i, cell.row +i])
                                        self.need_kill_blacks = True
                                        need_kill = True
                                        j = j + 1
                                    else:
                                        break
                            if cell.is_white and board.cells[cell.row - 1 + i][cell.column - 1 - i].is_black:
                                j = 1
                                while cell.column-i-j > 0 and cell.row+i+j<= len (board.cells):
                                    if board.cells[cell.row - 1 + i+j][cell.column - 1 - i-j].is_empty():
                                        self.whites_need_kill.append([cell.column, cell.row, cell.column-i-j, cell.row+i+j])
                                        self.be_killed_by_whites.append([cell.column-i, cell.row +i])
                                        self.need_kill_whites = True
                                        need_kill = True
                                        j = j + 1
                                    else:
                                        break
                            break
                        elif not board.cells[cell.row - 1 + i][cell.column - 1 - i].is_empty():
                            break
                        else:
                            i= i+1
                    i = 1
                    while cell.column-i >= 1 and cell.row-i>= 1:
                        if (not board.cells[cell.row - 1 - i][cell.column - 1 - i].is_empty()) and board.cells[cell.row - 1 - i-1][cell.column - 1 - i-1].is_empty():
                            if cell.is_black and board.cells[cell.row - 1 - i][cell.column - 1 - i].is_white:
                                j = 1
                                while cell.column-i-j > 0 and cell.row-i-j > 0:
                                    if board.cells[cell.row - 1 - i - j][cell.column - 1 - i - j].is_empty(): 
                                        self.blacks_need_kill.append([cell.column, cell.row, cell.column-i-j, cell.row-i-j])
                                        self.be_killed_by_blacks.append([cell.column-i, cell.row -i])
                                        self.need_kill_blacks = True
                                        need_kill = True
                                        j = j+1
                                    else:
                                        break
                            if cell.is_white and board.cells[cell.row - 1 - i][cell.column - 1 - i].is_black:
                                j = 1
                                while cell.column-i-j > 0 and cell.row-i-j > 0:
                                    if board.cells[cell.row - 1 - i - j][cell.column - 1 - i - j].is_empty(): 
                                        self.whites_need_kill.append([cell.column, cell.row, cell.column-i-j, cell.row-i-j])
                                        self.be_killed_by_whites.append([cell.column-i, cell.row -i])
                                        self.need_kill_whites = True
                                        need_kill = True
                                        j=j+1
                                    else:
                                        break
                            break
                        elif not board.cells[cell.row - 1 - i][cell.column - 1 - i].is_empty():
                            break
                            
                        else:
                            i= i+1
                    i = 1
                    while cell.column+i <= len(row)-1 and cell.row-i>= 1:
                        if (not board.cells[cell.row - 1 - i][cell.column - 1 + i].is_empty()) and board.cells[cell.row - 1 - i-1][cell.column - 1 + i+1].is_empty():
                            if cell.is_black and board.cells[cell.row - 1 - i][cell.column - 1 + i].is_white:
                                j = 1
                                while cell.column+i+j <= len(row) and cell.row-i-j > 0:
                                    if board.cells[cell.row - 1 - i-j][cell.column - 1 + i+j].is_empty(): 
                                        self.blacks_need_kill.append([cell.column, cell.row, cell.column+i+j, cell.row-i-j])
                                        self.be_killed_by_blacks.append([cell.column+i, cell.row -i])
                                        self.need_kill_blacks = True
                                        need_kill = True
                                        j = j + 1
                                    else:
                                        break
                            if cell.is_white and board.cells[cell.row - 1 - i][cell.column - 1 + i].is_black:
                                j = 1
                                while cell.column+i+j <= len(row) and cell.row-i-j > 0:
                                    if board.cells[cell.row - 1 - i-j][cell.column - 1 + i+j].is_empty(): 
                                        self.whites_need_kill.append([cell.column, cell.row, cell.column+i+j, cell.row-i-j])
                                        self.be_killed_by_whites.append([cell.column+i, cell.row -i])
                                        self.need_kill_whites = True
                                        need_kill = True
                                        j = j + 1
                                    else:
                                        break
                            break
                        elif not board.cells[cell.row - 1 - i][cell.column - 1 + i].is_empty():
                            break
                            
                        else :
                            i= i+1

                            
        if self.need_kill_whites and self.first_need_kill_whites == False:
            self.possible_move_whites = []
            self.possible_move_whites.extend(self.whites_need_kill)
            self.first_need_kill_whites = True
            self.whites_need_kill = []
        elif self.need_kill_whites:
            self.possible_move_whites.extend(self.whites_need_kill)
            self.whites_need_kill = []
            

        if self.need_kill_blacks and self.first_need_kill_blacks == False: 
            self.possible_move_blacks = self.blacks_need_kill
            self.first_need_kill_blacks = True
            self.blacks_need_kill = []
        elif self.need_kill_blacks:
            self.possible_move_blacks.extend(self.blacks_need_kill)
            self.blacks_need_kill = []

        return (need_kill)    


        
        
    def make_best_moves(self, board):
        if not self.need_kill_blacks:
            for move in self.possible_move_blacks:
                lboard = LogicBoard(10,10)
                lboard.make_field(10,10)
                util.copy_board(board,lboard)
                lboard.move_checker(move)
                log = Logic(lboard)
                if len(log.be_killed_by_whites) == 0:
                    self.good_moves_black.append(move)
                else:
                    self.simple_moves_black.append(move)
                
                    
        if not self.need_kill_whites:
            for move in self.possible_move_whites:
                lboard = LogicBoard(10,10)
                lboard.make_field(10,10)
                util.copy_board(board,lboard)
                lboard.move_checker(move)
                log = Logic(lboard)
                if len(log.be_killed_by_blacks) == 0:
                    self.good_moves_whites.append(move)
                else:
                    self.simple_moves_whites.append(move)


        
