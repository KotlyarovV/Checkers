import tkinter
import threading
import copy
import server
import json
import client
from datamaker import *
import shelve
from tkinter import *
from cell import Cell
from util import *
from board import Board
from step import Step
import sys
import log_worker

class Menu (Frame):        
        def __init__(self,window):
            super(Menu, self).__init__(window)
            self.window = window
            self.board = None
            self.game = None
            self.variant = None
            self.level = None
            self.button1=Button(self,text='Blacks vs Player',width=25,height=5,bg='black',fg='red',font='arial 14')
            self.button1.bind("<Button-1>",self.blacks_vs_player)
            self.button1.pack()
            self.button2=Button(self,text='Whites vs Player',width=25,height=5,bg='black',fg='red',font='arial 14')
            self.button2.bind("<Button-1>",self.whites_vs_player)
            self.button2.pack()
            self.button3=Button(self,text='Player vs Player',width=25,height=5,bg='black',fg='red',font='arial 14')
            self.button3.bind("<Button-1>",self.player_vs_player)
            self.button3.pack()
            self.button4=Button(self,text='Al vs Al',width=25,height=5,bg='black',fg='red',font='arial 14')
            self.button4.bind("<Button-1>",self.al_vs_al)
            self.button4.pack()
            self.button5=Button(self,text='Load game',width=25,height=5,bg='black',fg='red',font='arial 14')
            self.button5.bind("<Button-1>",self.load_game)
            self.button5.pack()
            self.button6=Button(self,text='Exit',width=25,height=5,bg='black',fg='red',font='arial 14')
            self.button6.bind("<Button-1>",self.exit_menu)
            self.button6.pack()
            self.buttons = [self.button1,self.button2,self.button3,self.button4,self.button5,self.button6]
            self.pack()

        def choose_level(self,event):
            for button in self.buttons:
                    button.destroy()
            button1 = Button(self,text='Level 1',width=25,height=5,bg='black',fg='red',font='arial 14')
            button1.bind("<Button-1>",self.level1)
            button1.pack()
            button2 = Button(self,text='Level 2',width=25,height=5,bg='black',fg='red',font='arial 14')
            button2.bind("<Button-1>",self.level2)
            button2.pack()



        def choose_regim(self,event):
            for button in self.buttons:
                    button.destroy()
            button1 = Button(self,text='Multiplayer server \n whites',width=25,height=5,bg='black',fg='red',font='arial 14')
            button1.bind("<Button-1>",self.multiplayer_server)
            button1.pack()
            button2 = Button(self,text='Multiplayer client \n blacks',width=25,height=5,bg='black',fg='red',font='arial 14')
            button2.bind("<Button-1>",self.input_client)
            button2.pack()
            button3 = Button(self,text='One computer',width=25,height=5,bg='black',fg='red',font='arial 14')
            button3.bind("<Button-1>",self.player_vs_player_s)
            button3.pack()
            self.buttons = [button1,button2,button3]


        def two_players_variant(self,string):
            self.variant = string
            self.make_board_for_game()
            self.game.regim = string
            self.board.make_usability(self.game.step_maker(self.board,self.game.regim,1))
            self.game.log.append(self.game.log_maker.make_log(self.board,self.game))


        def input_client (self,event):
            for button in self.buttons:
                    button.destroy()
            self.entr = Entry(self,width=30,bd=30)
            self.entr.pack()
            self.button_get_text = Button(self,text='Start game',width=30,height=5,bg='black',fg='red',font='arial 14')
            self.button_get_text.bind("<Button-1>",self.multiplayer_client)
            self.button_get_text.pack()

        def player_vs_player_s(self,event):
            self.two_players_variant('player_vs_player')

        def multiplayer_server(self, event):
            self.two_players_variant('multiplayer_server')
            server.wait_connection(self.board)
            
        def multiplayer_client(self,event):
            self.ip = self.entr.get()
            
            if not client.check_connection(self.ip):
                    win = tkinter.Toplevel(self.window)
                    lab = tkinter.Label(win,text="Wrong IP")
                    lab.pack()
                    return None


                
            save_ip(self.ip)        
            self.two_players_variant('multiplayer_client')

            
             
            d = Data_Maker()
            def blocking_board(event):
                    pass
            self.board.make_usability(blocking_board)
            state = client.get_state(self.board, load_ip())
            
            state = json.loads(state)
            state[1]['regim'] = 'multiplayer_client'
            d.decode_board(self.board, self.game, state)
            
        def exit_menu(self,event):            
            self.destroy()
            self.window.destroy()

        def level1 (self,event):
            self.level = 1
            self.l_choosed = True
            self.make_board_for_game()
            if self.variant == 'whites_vs_player':
                    self.game.moving_whites(self.board)
            self.game.regim = self.variant
            if self.variant == 'al_vs_al':
                self.game.step_maker(self.board,self.game.regim,self.level )
            else:
                self.board.make_usability(self.game.step_maker(self.board,self.game.regim,self.level))
                self.game.log.append(self.game.log_maker.make_log(self.board,self.game))


        def level2 (self,event):
            self.level = 2
            self.l_choosed = True
            self.make_board_for_game()
            if self.variant == 'whites_vs_player':
                self.game.moving_whites(self.board)        
            self.game.regim = self.variant
            if self.variant == 'al_vs_al':
                self.game.step_maker(self.board,self.game.regim,self.level )
            else:
                self.board.make_usability(self.game.step_maker(self.board,self.game.regim,self.level))
                self.game.log.append(self.game.log_maker.make_log(self.board,self.game))

    
        def blacks_vs_player (self,event):
            self.variant = 'blacks_vs_player'
            self.choose_level(event)
            
            
        def whites_vs_player (self,event):
            self.variant = 'whites_vs_player'
            self.choose_level(event)

        def player_vs_player (self,event):
            self.choose_regim(event)

        def al_vs_al(self,event):
            self.variant = 'al_vs_al'            
            self.choose_level(event)
            
        def make_board_for_game (self):
            self.destroy()
            self.game = Step()
            m = tkinter.Menu(self.window) #создается объект Меню на главном окне
            self.window.config(menu=m) #окно конфигурируется с указанием меню для него
 
            fm = tkinter.Menu(m) #создается пункт меню с размещением на основном меню (m)
            m.add_cascade(label="File",menu=fm) #пункту располагается на основном меню (m)
            fm.add_command(label="Open...") #формируется список команд пункта меню
                 
            hm = tkinter.Menu(m) #второй пункт меню
            m.add_cascade(label="Help",menu=hm)
            hm.add_command(label="Help")
            
            def load():
            
                                 
                    try:
                            data = json.load( open('save', 'r') )
                            d = Data_Maker()
                            d.decode_board(self.board,self.game,data)
                    except Exception:
                            win = tkinter.Toplevel(self.window)
                            lab = tkinter.Label(win,text="Файла сохранения \n не существует!")
                            lab.pack()


            def window_top(string):
                    win = tkinter.Toplevel(self.window)
                    lab = tkinter.Label(win,text=string)
                    lab.pack()

            def close_win():
                    self.destroy()
                    self.window.destroy()
                 
            def about():
                    win = tkinter.Toplevel(self.window)
                    lab = tkinter.Label(win,text="Это просто программа-тест \n меню в Tkinter")
                    lab.pack()
            def save():
                    d = Data_Maker()
                    string = d.encode_board(self.board,self.game)
                    json.dump(string, open('save', 'w'))

            def undo():
                    if self.variant == 'multiplayer_server' or self.variant == 'multiplayer_client':
                            window_top("Невозможно отменить ход!")
                            return None 
                    try:
                            a = log_worker.Log_Handler()
                            a.undo(self.board, self.game)
                    except Exception:
                            window_top("Невозможно отменить ход!")

                    
            def redo():
                    if self.variant == 'multiplayer_server' or self.variant == 'multiplayer_client':
                            window_top("Невозможно отменить ход!")
                            return None
                    try:
                            a = log_worker.Log_Handler()
                            a.redo(self.board, self.game)
                    except Exception:
                            window_top("Невозможно перейти \n на ход вперед!")


            fm.add_command(label="Load",command=load)
            fm.add_command(label="Save...",command=save)
            fm.add_command(label="Exit",command=close_win)
            hm.add_command(label="About",command=about)    
            m.add_command (label="Undo",command=undo)
            m.add_command (label="Redo",command=redo)
            
            self.board = Board(self.window,10,10)
            self.board.grid(row=0,column=2)
            self.board.make_field(10,10)
            self.board.stand_checkers(4)
            #текстовое поле и его первоначальные настройки
            self.window.tx = Text(self.window,font=('times',12),width=13,height=28,wrap=WORD)
            scrollbar = Scrollbar()
            scrollbar['command'] = self.window.tx.yview
            self.window.tx['yscrollcommand'] = scrollbar.set

            self.window.tx.grid(row=0, column = 0)
            scrollbar.grid(row=0, column = 1,ipady=265)
                        
        def load_game (self,event):
            try:
                    data = json.load( open('save', 'r') )
                    d = Data_Maker()
                    self.make_board_for_game()
                    d.decode_board(self.board,self.game,data)
            except Exception:
                    win = tkinter.Toplevel(self.window)
                    lab = tkinter.Label(win,text="Файла сохранения \n не существует!")
                    lab.pack()
                    



             


            
                 

            
            
            
