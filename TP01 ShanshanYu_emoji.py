import numpy as np
import random
class tic_tac_toc(object):
    def __init__(self):
        self.board = np.zeros((5, 5))
        self.rows = self.board.shape[0]
        self.columns = self.board.shape[1]
        self.is_user_turn = True
        self.user_is_first = None
        self.user_mark = 1
        self.opponent_mark = 2
        self.inrow = 5

    def print_board(self):
        # Print a board
        print("-------------------------------")
        for row in range(self.rows):
            row_list = []
            for column in range(self.columns):
                cell = self.board[row][column]
                row_list.append(self.transfer_cell(cell))
            print(' | '.join(row_list))
        print("-------------------------------")
    
    def transfer_cell(self, cell):
            if cell == 0:
                return '_'
            if cell == 1:
                return 'X'
            if cell == 2:
                return 'O'
            return ''

    def start(self):
        self.board = np.zeros((5, 5))
        self.is_user_turn = True
        self.user_is_first = random.choice([True, False])
        self.user_mark = 1
        self.opponent_mark = 2
        if not self.user_is_first:
            self.is_user_turn = False
            self.user_mark = 2
            self.opponent_mark = 1
            print('You get the second!')
        else:
            print('You get the first!')
    
    def get_input(self):
        try:
            row = input('please enter your input 1 -- 5 😊')
            column = input('please enter your input 1 -- 5 😊')
            if row == 'q' or column == 'q':
                return 'q', 'q'
            row = int(row) - 1
            column = int(column) - 1
            if column not in range(self.columns) or row not in range( self.rows):
                print('You must enter one digit from 1 -- 5 only and Zero not Allowed 😟 😟  !!')
                return -1, -1
            if self.board[row][column] != 0:
                print('\n $$$$ This cell is taken? try an empty one 😅 😅  "-" $$$')     
                return -1, -1     
            return row, column
        except:
            print('Hey please only numbers between 1-25 🤬 🤬')
            return -1, -1

    def move(self, row, column, mark):
        self.board[row][column] = mark
 

    def check_complete(self, board):
        empty_cells = self.compute_empty_cells(board)
        return len(empty_cells) == 0

    def check_win(self, board, mark):
        # input board: np array; mark: int32
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
        diagonal1 = []
        for i in range(self.rows):
            diagonal1.append(board[i][i])
            if len(diagonal1) < 5:
                continue
            if len(diagonal1) > 5:
                diagonal1.pop(0)
            if len(set(diagonal1)) == 1 and diagonal1[0] == mark:
                return True

        diagonal2 = []
        for i in range(self.rows):
            diagonal2.append(board[self.rows - 1 - i][i])
            if len(diagonal2) < 5:
                continue
            if len(diagonal2) > 5:
                diagonal2.pop(0)
            if len(set(diagonal2)) == 1 and diagonal2[0] == mark:
                return True
        return False
        
    def compute_empty_cells(self, board):
        empty_cells = []
        for row in range(self.rows):
            for column in range(self.columns):
                if board[row][column] == 0:
                    empty_cells.append((row, column))
        return empty_cells

    def AI_play(self):
        empty_cells = self.compute_empty_cells(self.board)
        new_board = self.board.copy()
        for row, column in empty_cells:
            new_board[row][column] = self.opponent_mark
            if self.check_win(new_board, self.opponent_mark):
                return (row, column)
            new_board[row][column] = self.user_mark
            if self.check_win(new_board, self.user_mark):
                return (row, column)
            new_board[row][column] = 0
        return random.choice(empty_cells)

    def main(self):
        """
        Author: Shanshan Yu
        Created: 11/13/2020
        Updated: 12/02/2020
        """
        print("Welcome to Tic-tac-toc!")
        user_info = input("Enter anykey to start a new game, q to quit: ")
        while user_info!='q':
            if self.user_is_first is None:
                self.start()
            if self.is_user_turn:
                mark = self.user_mark
            else:
                mark = self.opponent_mark
            print("Turn for '{}'".format(self.transfer_cell(mark)))
            self.print_board()
            if self.is_user_turn:
                row, column = -1, -1
                while row == -1 and column == -1:
                    row, column = self.get_input()
                # Break point
                if row == 'q' or column == 'q':
                    user_info = 'q'
                    continue
                self.move(row, column, mark)
                self.is_user_turn = not self.is_user_turn
            else:
                row, column = self.AI_play()
                self.move(row, column, mark)
                self.is_user_turn = not self.is_user_turn
            # Record moves
            with open('tictactoc.txt','a') as ttt:
                ttt.write("{}: row {}, column {}\n".format(self.transfer_cell(mark), row, column)) 

            if self.check_win(self.board, mark):
                print('{} has won!!  YaaY 🥳 🥳'.format(self.transfer_cell(mark)))
            elif self.check_complete(self.board):
                print('\nGame is Tie !! Play it again 😫 😫')
            else:
                continue
            user_info = input("Start a new game? ('q' to quit): ")
            if user_info != 'q':
                self.start()
            else:
                break
            with open('tictactoc.txt','w') as ttt:
                ttt.write("-- New Turn -- \n")

#TEST
newgame = tic_tac_toc()
newgame.main()
