from board import Board
from tkinter import BOTH, END
from cell import Cell
from logic import Logic
import json
class Data_Maker:
    
    def encode_board(self,board,game):
        board_string = ''    
        for row in board.cells:
            for i in range (len(row)):
                if row[i].is_black:
                    if row[i].queen:
                        board_string = board_string + "*"
                    else:
                        board_string = board_string + "@"
                elif row[i].is_white:
                    if row[i].queen:
                        board_string = board_string + "#"
                    else:
                        board_string = board_string + "&"
                else:
                    board_string = board_string + "0"
                if i == (len(row) - 1):
                    board_string = board_string + "\n"
        game_state = {"move_whites":game.move_whites, "seria":game.seria, "first_touch": True, "touched_cell_row": -1, "touched_cell_column": -1, 'regim' : game.regim,  'simple_log' : game.simple_log, 'level' :game.level }
        if not game.l is None:
            game_logic = { 'possible_move_whites':game.l.possible_move_whites,'possible_move_blacks':game.l.possible_move_blacks, 'be_killed_by_whites':game.l.be_killed_by_whites, 'be_killed_by_blacks':game.l.be_killed_by_blacks }
        else:
            game_logic = { 'possible_move_whites':[],'possible_move_blacks':[], 'be_killed_by_whites':[], 'be_killed_by_blacks':[]}
        data = [ board_string, game_state, game_logic]
        return data

    def make_log (self,board,game):
        data = self.encode_board(board,game)
        string = json.dumps(data)
        return string
                
    def decode_board (self,board,game,data):
        for row in board.cells:
            for cell in row:
                cell.clear()
        strings = data[0].split('\n')
        b_strings = strings[:-1]
        for row in range(len(b_strings)):
            for i in range (len(b_strings[row])):
                if b_strings[row][i] == "*":
                    board.cells[row][i].put_black()
                    board.cells[row][i].became_queen()
                if b_strings[row][i] == "@":
                    board.cells[row][i].put_black()
                if b_strings[row][i] == "#":
                    board.cells[row][i].put_white()
                    board.cells[row][i].became_queen()
                if b_strings[row][i] == "&":
                    board.cells[row][i].put_white()
        if type(board) is Board:
            board.make_usability(game.step_maker(board,data[1]['regim'],data[1]['level']))
            board.window.tx.delete(1.0,END)
            board.window.tx.insert(END,data[1]['simple_log'])
                    
        game.move_whites = data[1]['move_whites']
        game.seria= data[1]['seria']
        game.simple_log = data[1]['simple_log']
        game.first_touch = data[1]['first_touch']
        game.touched_cell_row = data[1]['touched_cell_row']
        game.touched_cell_row = data[1]['touched_cell_column']
        game.level = data[1]['level']

        game.l = Logic (board)
        game.l.possible_move_whites = data[2]['possible_move_whites']
        game.l.possible_move_blacks = data[2]['possible_move_blacks']
        game.l.be_killed_by_whites = data[2]['be_killed_by_whites']
        game.l.be_killed_by_blacks = data[2]['be_killed_by_blacks']
        

                    
        
