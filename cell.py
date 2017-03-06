import copy
from tkinter import *

class Logic_Cell():
    
    def __init__(self,  color, row, column):
        self.row = row
        self.column = column
        self.is_white = False
        self.is_black = False
        self.color=color
        self.queen = False
        
    def put_white(self):
        self.is_white = True
        self.is_black = False
        
    def clear (self):
        self.is_white = False
        self.is_black = False
        self.queen = False

    def became_queen(self):
        self.queen = True
        
    def put_black(self):
        self.is_black = True
        self.is_white = False
    
    def is_empty(self):
        return not (self.is_white or self.is_black)


class Cell(Button, Logic_Cell):
    
    def __init__(self, root, color, width,height,row, column):
        Button.__init__(self,root, bg=color, width=width,height=height)
        Logic_Cell.__init__(self,color=color, row=row,column=column)
        self.empty_image = PhotoImage(file ='empty.gif')
        self.white_picture = PhotoImage(file ='white.gif')
        self.white_damka_picture = PhotoImage(file ='damkaWhite.gif')
        self.black_damka_picture = PhotoImage(file ='damkaBlack.gif')
        self.black_picture = PhotoImage(file ='black.gif')        
        
    def put_white(self):
        Logic_Cell.put_white(self)
        self['image'] = self.white_picture

    def put_black(self):
        Logic_Cell.put_black(self)
        self['image'] = self.black_picture
                
    def clear (self):
        Logic_Cell.clear(self)
        self['image'] = self.empty_image
        
    def became_queen(self):
        Logic_Cell.became_queen(self)
        self['image'] = self.white_damka_picture if self.is_white else self.black_damka_picture
