from logic import *
import random
import datamaker
import util
import json
import client
import server

class Step():
    def __init__(self):
        self.move_whites = True
        self.seria = False
        self.first_touch = True
        self.touched_cell_row = -1
        self.touched_cell_column = -1
        self.l = None
        self.regim = ''
        self.log = []
        self.log_cancelled_steps = []
        self.log_maker = datamaker.Data_Maker()
        self.simple_log = ""
        self.level = 1


    def change_side(self,board):
        def blocking_board(event):
            pass
        self.move_whites = not self.move_whites
        if self.regim == 'multiplayer_client':
            d = datamaker.Data_Maker()
            state = json.dumps(d.encode_board(board,self))
            board.make_usability(blocking_board)
            client.send_state(state,board, load_ip())
            state = client.get_state(board,load_ip())
            state = json.loads(state)
            state[1]['regim'] = 'multiplayer_client'
            d.decode_board(board, self, state)
        if self.regim == 'multiplayer_server':
            d = datamaker.Data_Maker()
            state = json.dumps(d.encode_board(board,self))
            board.make_usability(blocking_board)
            server.send_state(state,board)
            state = server.get_state(board)
            state = json.loads(state)
            state[1]['regim'] = 'multiplayer_server'
            d.decode_board(board, self, state)
        
    def step_maker (self,board, regim, level):
        self.level = level   
        if regim == 'player_vs_player' or regim == 'multiplayer_client' or regim == 'multiplayer_server':
            self.regim = regim
            def button_clicked(event):
                if not self.seria:
                    self.l = Logic (board)
                if self.move_whites:
                    self.player_step_whites(board,event)
                elif not self.move_whites:
                    self.player_step_blacks(board,event)
            return button_clicked
        
        if regim == 'blacks_vs_player':
            self.regim = 'blacks_vs_player'
            def button_clicked(event):
                if not self.seria:
                    self.l = Logic (board)
                if self.move_whites:
                    self.player_step_whites(board,event)
                if not self.move_whites:
                    self.moving_blacks(board)
            return button_clicked

        if regim == 'whites_vs_player':            
            self.regim = 'whites_vs_player'
            def button_clicked(event):
                if not self.seria:
                    self.l = Logic (board)
                if not self.move_whites:
                    self.player_step_blacks(board,event)
                if self.move_whites:
                    self.moving_whites(board)
            return button_clicked

        if regim == 'al_vs_al':
            self.regim = 'al_vs_al'
            while board.victory_cond == False:
                if not self.seria:
                    self.l = Logic (board)
                if self.move_whites:
                    try:
                        self.moving_whites(board)
                    except Exception:
                        break
                    util.timer_tk(1,board.window)
                    
                if not self.move_whites and not board.victory_cond:
                    try:
                        self.moving_blacks(board)
                    except Exception:
                        break
                    util.timer_tk(1,board.window)



    def moving_blacks(self,board):
        if not self.seria:
            self.l = Logic (board)

        if self.level == 2 and not self.l.need_kill_blacks and not self.seria:
            self.l.make_best_moves(board)
            if len(self.l.good_moves_black) != 0:
                step_blacks = random.choice(self.l.good_moves_black)
            else:
                step_blacks = random.choice(self.l.simple_moves_black)
        else:
            step_blacks = random.choice(self.l.possible_move_blacks)
        board.move_checker(step_blacks)
        board.window.tx.insert(END,util.print_step(step_blacks))
        self.simple_log = self.simple_log + util.print_step(step_blacks)
        if self.l.need_kill_blacks:
            board.kill_checker(self.l.be_killed_by_blacks[self.l.possible_move_blacks.index(step_blacks)])
            self.l = Logic(board)
            if self.l.cell_need_kill (step_blacks[2:], board):
                self.seria = True
                self.moving_blacks(board)

            else:
                self.move_whites = True
                self.seria = False
                if len(self.l.possible_move_whites)==0:
                    board.victory("Blacks WIN!!!")
                            
        else:
            self.move_whites = True
            self.seria = False
            if len(self.l.possible_move_whites)==0:
                board.victory("Blacks WIN!!!")

        self.log.append(self.log_maker.make_log(board,self))
        self.log_cancelled_steps = []
        
    def moving_whites (self,board):
        if not self.seria:
            self.l = Logic (board)

        if self.level == 2 and not self.l.need_kill_whites and not self.seria:
            self.l.make_best_moves(board)
            if len(self.l.good_moves_whites) != 0:
                step_whites = random.choice(self.l.good_moves_whites)
            else:
                step_whites = random.choice(self.l.simple_moves_whites)
        else:
            step_whites = random.choice(self.l.possible_move_whites)
            
        board.move_checker(step_whites)
        board.window.tx.insert(END,util.print_step(step_whites))
        self.simple_log = self.simple_log + util.print_step(step_whites)
        if self.l.need_kill_whites:
            board.kill_checker(self.l.be_killed_by_whites[self.l.possible_move_whites.index(step_whites)])
            self.l = Logic(board)
            if self.l.cell_need_kill (step_whites[2:], board):
                self.seria = True
                self.moving_whites(board)
            else:
                self.seria = False
                self.move_whites = False
                if len(self.l.possible_move_blacks)==0:
                    board.victory("WHITES WIN!!!")
        else:
            self.move_whites = False
            self.seria = False
            if len(self.l.possible_move_blacks)==0:
                board.victory("WHITES WIN!!!")
        self.log.append(self.log_maker.make_log(board,self))
        self.log_cancelled_steps = []
        

    def player_step_blacks(self,board,event):
        if not self.seria:
            self.l = Logic (board)
            
        if self.first_touch and event.widget.is_black:
            self.touched_cell_row = event.widget.row
            self.touched_cell_column = event.widget.column
            self.first_touch = False
                
        elif [self.touched_cell_column, self.touched_cell_row, event.widget.column, event.widget.row] in self.l.possible_move_blacks:
            board.move_checker([self.touched_cell_column, self.touched_cell_row, event.widget.column, event.widget.row])
            board.window.tx.insert(END,util.print_step([self.touched_cell_column, self.touched_cell_row, event.widget.column, event.widget.row]))
            self.simple_log = self.simple_log + util.print_step([self.touched_cell_column, self.touched_cell_row, event.widget.column, event.widget.row])
            if self.l.need_kill_blacks:
                board.kill_checker(self.l.be_killed_by_blacks[self.l.possible_move_blacks.index([self.touched_cell_column, self.touched_cell_row, event.widget.column, event.widget.row])])
                self.l = Logic(board)
                if self.l.cell_need_kill ([event.widget.column, event.widget.row], board):
                    self.first_touch = True
                    self.seria = True

                else:
                    self.first_touch = True
                    self.seria = False
                    if len(self.l.possible_move_whites)==0:
                        board.victory("Blacks WIN!!!")
                    self.change_side(board)
                            
            else:
                self.first_touch = True
                self.seria = False
                if len(self.l.possible_move_whites)==0:
                    board.victory("Blacks WIN!!!")
                self.change_side(board)
            self.log.append(self.log_maker.make_log(board,self))
            self.log_cancelled_steps = []
                        
        else:
            self.first_touch = True


    def player_step_whites(self,board,event):
        if not self.seria:
            self.l = Logic (board)
            
        if self.first_touch and event.widget.is_white:
            self.touched_cell_row = event.widget.row
            self.touched_cell_column = event.widget.column
            self.first_touch = False
        elif [self.touched_cell_column, self.touched_cell_row, event.widget.column, event.widget.row] in self.l.possible_move_whites:
            board.move_checker([self.touched_cell_column, self.touched_cell_row, event.widget.column, event.widget.row])
            board.window.tx.insert(END,util.print_step([self.touched_cell_column, self.touched_cell_row, event.widget.column, event.widget.row]))
            self.simple_log = self.simple_log + util.print_step([self.touched_cell_column, self.touched_cell_row, event.widget.column, event.widget.row])
            if self.l.need_kill_whites:
                board.kill_checker(self.l.be_killed_by_whites[self.l.possible_move_whites.index([self.touched_cell_column, self.touched_cell_row, event.widget.column, event.widget.row])])
                self.l = Logic(board)
                if self.l.cell_need_kill ([event.widget.column, event.widget.row], board):
                    self.first_touch = True
                    self.seria = True
                else:
                    self.seria = False
                    self.first_touch = True
                    if len(self.l.possible_move_blacks)==0:
                        board.victory("WHITES WIN!!!")
                    self.change_side(board)
            else:
                self.first_touch = True
                self.seria = False
                if len(self.l.possible_move_blacks)==0:
                    board.victory("WHITES WIN!!!")
                self.change_side(board)
            self.log.append(self.log_maker.make_log(board,self))
            self.log_cancelled_steps = []
                
        else:
            self.first_touch = True
           
