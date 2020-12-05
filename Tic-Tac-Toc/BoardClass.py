import numpy as np
class Board(object):
    def __init__(self, rows, columns, inrow):
        # rows: int
        # columns: int
        # inrow: int  **the number of marks for winning the game**
        self.board = np.zeros((rows, columns))
        self.rows = rows
        self.columns = columns
        self.inrow = inrow
    
    def print_board(self):
        # Print a board
        # return nothing
        print("--------------------")
        for row in range(self.rows):
            row_list = []
            for column in range(self.columns):
                cell = self.board[row][column]
                row_list.append(self.transfer_cell(cell))
            print(' | '.join(row_list))
        print("--------------------")

    def transfer_cell(self, cell):
        # cell: int
        # return: string
            if cell == 0:
                return '_'
            if cell == 1:
                return 'X'
            if cell == 2:
                return 'O'
            return ''

    def move(self, row, column, mark):
        self.board[row][column] = mark
        self.write_file(row, column, mark)

    def check_complete(self, board):
        # board: np array
        # return: bool
        empty_cells = self.compute_empty_cells(board)
        return len(empty_cells) == 0

    def check_win(self, board, mark):
        # board: np array
        # mark: int32
        # return: bool
        #check row
        for row in range(self.rows):
            if list(board[row][:]).count(mark) == self.inrow:
                return True
        #check column
        for column in range(self.columns):
            if list([board[row][column] for row in range(self.rows)]).count(mark) == self.inrow:
                return True
        #check diagonal line
        diagonal1 = [board[i][i] for i in range(self.rows)]
        if len(set(diagonal1)) == 1 and diagonal1[0] == mark:
            return True
        diagonal2 = [board[self.rows-i-1][i] for i in range(self.rows)]
        if len(set(diagonal2)) == 1 and diagonal2[0] == mark:
            return True
        return False
        
    def compute_empty_cells(self, board):
        # board: np array
        # return: list
        empty_cells = []
        for row in range(self.rows):
            for column in range(self.columns):
                if board[row][column] == 0:
                    empty_cells.append((row, column))
        return empty_cells

    def write_file(self, row, column, mark):
        # recording moves
        # return: nothing
        with open('tictactoc.txt','a') as ttt:
            ttt.write("{}: row {}, column {}\n".format(self.transfer_cell(mark), row, column))