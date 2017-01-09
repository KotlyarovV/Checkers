from board import Board
from cell import Cell
from logic import Logic
from datamaker import Data_Maker
import json


class Log_Handler:
        
    def undo (self, board, game):
        if game.regim == "player_vs_player":
            game.log_cancelled_steps.append(game.log.pop())
            data_str = game.log[len(game.log)-1]
            data = json.loads( data_str )
            d = Data_Maker()
            d.decode_board(board,game,data)
        elif game.regim == "whites_vs_player" or game.regim == "blacks_vs_player":
            game.log_cancelled_steps.append(game.log.pop())
            game.log_cancelled_steps.append(game.log.pop())
            data_str = game.log[len(game.log)-1]
            data = json.loads( data_str )
            d = Data_Maker()
            d.decode_board(board,game,data)
        else:
            win = tkinter.Toplevel(board.window)
            lab = tkinter.Label(win,text="Нельзя \n отменить ход!")
            lab.pack()
        

    def redo (self, board, game):
        if game.regim == "player_vs_player" or game.regim == "al_vs_al":
            data_str = game.log_cancelled_steps[len(game.log_cancelled_steps)-1]
            game.log.append(game.log_cancelled_steps.pop())
            data = json.loads( data_str )
            d = Data_Maker()
            d.decode_board(board,game,data)
        elif game.regim == "whites_vs_player" or game.regim == "blacks_vs_player":
            data_str = game.log_cancelled_steps[len(game.log_cancelled_steps)-2]
            game.log.append(game.log_cancelled_steps.pop())
            game.log.append(game.log_cancelled_steps.pop())
            data = json.loads( data_str )
            d = Data_Maker()
            d.decode_board(board,game,data)

                    
