import tkinter
import threading
import copy
import json
from datamaker import *
import shelve
from tkinter import *
from cell import Cell
from util import *
from board import Board
from step import Step
import sys
import log_worker

class Packet_Menu ():        
        def __init__():
            self.board = None
            self.game = None
            self.variant = None
            print('Blacks vs Player')
            print('Whites vs Player')
            print('Player vs Player')
            print('Al vs Al')
            print('Load game')
            print('Exit')
            inp = input()
            self.handling(inp)


        def handling(self,inp):
                
                if inp == 'Exit':
                        sys.exit()
                if inp == 'Blacks vs Player':
                        self.blacks_vs_player (self)
                
                        
        
            
        def blacks_vs_player (self):
            self.variant = 'blacks_vs_player'
            self.make_board_for_game()
            self.game.regim = 'blacks_vs_player'
            self.game.log.append(self.game.log_maker.make_log(self.board,self.game))

        def whites_vs_player (self,event):
            self.variant = 'whites_vs_player'
            self.make_board_for_game()
            self.game.moving_whites(self.board)
            self.game.log.append(self.game.log_maker.make_log(self.board,self.game))

        def player_vs_player (self,event):
            self.variant = 'player_vs_player'            
            self.make_board_for_game()
            self.game.regim = 'player_vs_player'
            self.game.log.append(self.game.log_maker.make_log(self.board,self.game))

        def al_vs_al(self,event):
            self.variant = 'al_vs_al'            
            self.make_board_for_game()
            self.game.regim = 'al_vs_al'
            self.game.step_maker(self.board,self.game.regim )
                
        def make_board_for_game (self):
            self.game = Step_Packet()
            #m.add_cascade(label="File",menu=fm) 
                 
            #hm = tkinter.Menu(m) #второй пункт меню
            #m.add_cascade(label="Help",menu=hm)
            #hm.add_command(label="Help")
            
            #def load():
             #       try:
              #              data = json.load( open('save', 'r') )
               #             d = Data_Maker()
                #            d.decode_board(self.board,self.game,data)
                 #   except Exception:
                  #          win = tkinter.Toplevel(self.window)
                   #         lab = tkinter.Label(win,text="Файла сохранения \n не существует!")
                    #        lab.pack()

                 '''
            def save():
                    d = Data_Maker()
                    string = d.encode_board(self.board,self.game)
                    json.dump(string, open('save', 'w'))

            def undo():
                    try:
                            a = log_worker.Log_Handler()
                            a.undo(self.board, self.game)
                    except Exception:
                            win = tkinter.Toplevel(self.window)
                            lab = tkinter.Label(win,text="Невозможно отменить ход!")
                            lab.pack()

                    
            def redo():
                    try:
                            a = log_worker.Log_Handler()
                            a.redo(self.board, self.game)
                    except Exception:
                            win = tkinter.Toplevel(self.window)
                            lab = tkinter.Label(win,text="Невозможно перейти \n на ход вперед!")
                            lab.pack()


            fm.add_command(label="Load",command=load)
            fm.add_command(label="Save...",command=save)
            fm.add_command(label="Exit",command=close_win)
            hm.add_command(label="About",command=about)    
            m.add_command (label="Undo",command=undo)
            m.add_command (label="Redo",command=redo)
            '''
            self.board = LogicBoard(10,10)
            self.board.make_field(10,10)
            self.board.stand_checkers(4)
            
        #def load_game (self,event):
         #   try:
          #          data = json.load( open('save', 'r') )
           #         d = Data_Maker()
            #        self.make_board_for_game()
             #       d.decode_board(self.board,self.game,data)
            #except Exception:
             #       win = tkinter.Toplevel(self.window)
              #      lab = tkinter.Label(win,text="Файла сохранения \n не существует!")
               #     lab.pack()
                    



             


            
                 

            
            
            
