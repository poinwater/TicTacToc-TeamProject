from BoardClass import Board
import random
class tic_tac_toc(object):
    def __init__(self):
        self.board = Board(5, 5, 5)
        self.is_user_turn = True
        self.user_is_first = None
        self.user_mark = 1
        self.opponent_mark = 2

    def start(self):
        self.board = Board(5, 5, 5)
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
            row = input('please enter the number of row 1 -- 5 ')
            column = input('please enter the number of column 1 -- 5 ')
            if row == 'q' or column == 'q':
                return 'q', 'q'
            row = int(row) - 1
            column = int(column) - 1
            if column not in range(self.board.columns) or row not in range(self.board.rows):
                print('You must enter one digit from 1 -- 5 only and Zero not Allowed !!')
                return -1, -1
            if self.board.board[row][column] != 0:
                print('\n $$$$ This cell is taken? try an empty one  "-" $$$')     
                return -1, -1     
            return row, column
        except:
            print('Hey please only numbers between 1 - 5')
            return -1, -1

    def AI_play(self):
        # return tuple
        empty_cells = self.board.compute_empty_cells(self.board.board)
        new_board = self.board.board.copy()
        for row, column in empty_cells:
            new_board[row][column] = self.opponent_mark
            if self.board.check_win(new_board, self.opponent_mark):
                return (row, column)
            new_board[row][column] = self.user_mark
            if self.board.check_win(new_board, self.user_mark):
                return (row, column)
            # undo
            new_board[row][column] = 0
        return random.choice(empty_cells)

    def main(self):
        """
        Author: Shanshan Yu
        Created: 11/13/2020
        Updated: 12/05/2020
        """
        print("Welcome to Tic-tac-toc!")
        user_info = input("Enter anykey to start a new game, q to quit: ")
        while user_info != 'q':
            if self.user_is_first is None:
                self.start()
            mark = self.user_mark if self.is_user_turn else self.opponent_mark
            self.board.print_board()
            print("Turn for '{}'".format(self.board.transfer_cell(mark)))
            row, column = -1, -1
            # Make movement
            if self.is_user_turn:
                # Loop if input is invalid
                while row == -1 and column == -1:
                    row, column = self.get_input()
                # Break point
                if row == 'q' or column == 'q':
                    user_info = 'q'
                    continue
            else:
                row, column = self.AI_play()
            self.board.move(row, column, mark)
            self.is_user_turn = not self.is_user_turn
            # Checking Game Status
            if self.board.check_win(self.board.board, mark):
                # Win or Lose
                self.board.print_board()
                print('{} has won!!  YaaY'.format(self.board.transfer_cell(mark)))
            elif self.board.check_complete(self.board.board):
                # Tie
                self.board.print_board()
                print('\nGame is Tie !! Play it again')
            else:
                # Keep Playing
                continue
            # Replay or not
            user_info = input("Start a new game? ('q' to quit): ")
            if user_info != 'q':
                self.start()
                with open('tictactoc.txt','w') as ttt:
                    ttt.write("-- New Turn -- \n")

#TEST
newgame = tic_tac_toc()
newgame.main()
