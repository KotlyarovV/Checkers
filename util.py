import datetime
import cell


def define_color(row,column):
    if (row % 2 == 1 and column % 2 == 1) or (row%2== 0 and column % 2 == 0):
        return "black"
    else:
        return "white"


def is_queen(board, column, row, column1, row1):
    if board.cells [row-1][column-1].is_white and row == len(board.cells):
        return True
    if board.cells [row-1][column-1].is_black and row == 1:
        return True
    return board.cells[row1-1][column1-1].queen


def timer_tk(seconds, window):
    now = datetime.datetime.now()
    delta =  datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() - now < delta:
        try:
            window.update()
        except Exception:
            break
        continue


def upcast_logic_cell(logic_cell, root , width, height):
    this_cell = cell.Cell(root,color = logic_cell.color, width = width, height = height, row = logic_cell.row , column = logic_cell.column) 
    return this_cell


def stand_checkers(board, num_of_rows):
    for i in range (len(self.cells)):
        if i < num_of_rows:
            for cell in self.cells[i]:
                if cell.color == "black":
                    cell.put_white()
        if i >= len(self.cells)-num_of_rows:
            for cell in self.cells[i]:
                if cell.color == "black":
                    cell.put_black()


def print_step(arr):
    letters = {1:"A",
               2:"B",
               3:"C",
               4:"D",
               5:"E",
               6:"F",
               7:"G",
               8:"H",
               9:"I",
               10:"J"}
    return letters[arr[0]]+str(arr[1]) + " - "+letters[arr[2]]+str(arr[3])+ '\n'


def copy_board(board1,board2):
    for i in range (len(board1.cells)):
        for j in range (len(board1.cells[i])):
            if board1.cells[i][j].is_white:
                board2.cells[i][j].put_white()
            if board1.cells[i][j].is_black:
                board2.cells[i][j].put_black()
            if board1.cells[i][j].queen:
                board2.cells[i][j].became_queen()

  
def save_ip(string):
    f = open('ip', 'w')
    f.write(string)
    f.close()


def load_ip():
    f = open('ip', 'r')
    s = f.read()
    f.close()
    return s
        
