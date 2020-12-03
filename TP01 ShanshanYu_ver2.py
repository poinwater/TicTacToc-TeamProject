import numpy as np
class tic_tac_toc(object):
    def __init__(self):
        self.board = [[' '] * 9 for _ in range(9)]
        self.is_user_turn = True
        self.user_is_first = None
        self.user_mark = 'X'
        self.opponent_mark = 'O'

    def print_board(self):
        # Print a board

        for i in range(9):
            print("-------------------------------")
            print(' | '.join(self.board[i][:]))

    def start(self):
        from random import choice
        self.board = [[' '] * 9 for _ in range(9)]
        self.is_user_turn = True
        self.user_mark = 'X'
        self.opponent_mark = 'O'
        self.user_is_first = choice([True, False])

        self.print_board()
        if not self.user_is_first:
            self.is_user_turn = False
            self.user_mark = 'O'
            self.opponent_mark = 'X'
            print("You get the second!")
        else:
            print("You get the first!")

    def move(self, row, column, mark):
        try:
            row = int(row)
            column = int(column)
            if column not in range(1,10) or row not in range(1,10):
                print("Warning: The input number should be in range [1,9]!")
                return False            
            if self.board[row - 1][column - 1] != ' ':
                print("Warning: The position is not empty!")
                return False           
            self.board[row - 1][column - 1] = mark
            return True  
        except:
            print("Warn: Your input is not an integer.")
            return False

    def check_complete(self,board):
        empty_cells = self.compute_empty_cells(board)
        return len(empty_cells) == 81

    def check_win(self,board):
        #check row
        for row in range(9):
            for index in range(5):
                if len(set(board[row][index : index + 5])) == 1 and board[row][index] != ' ':
                    return board[row][0], "done"
        #check column
        for column in range(9):
            stack = []
            for index in range(5):
                stack.append(board[index][column])
                if len(stack) < 5:
                    continue
                if len(stack) > 5:
                    stack.pop(0)
                if len(set(stack)) == 1 and board[index][column] != ' ':
                    return board[0][column], "done"
        #check diagonal line
        diagonal1 = []
        for i in range(9):
            diagonal1.append(board[i][i])
            if len(diagonal1) < 5:
                continue
            if len(diagonal1) > 5:
                diagonal1.pop(0)
            if len(set(diagonal1)) == 1 and diagonal1[0] != ' ':
                return diagonal1[0], "done"

        diagonal2 = []
        for i in range(9):
            diagonal2.append(board[8-i][i])
            if len(diagonal2) < 5:
                continue
            if len(diagonal2) > 5:
                diagonal2.pop(0)
            if len(set(diagonal2)) == 1 and diagonal2[0] != ' ':
                return diagonal2[0], "done"
        #check draw
        if self.check_complete(board):
            return None, "draw"
        return None, "None"

    def score(self,board,depth):
        winner_mark, state = self.check_win(board)
        if winner_mark == self.opponent_mark and state == "done":
            return 10 - depth
        if winner_mark == self.user_mark and state == "done":
            return depth - 10
        return 0
        
    def compute_empty_cells(self, board):
        empty_cells = []
        for row in range(9):
            for column in range(9):
                if board[row][column] == ' ':
                    empty_cells.append((row  + 1, column + 1))
        return empty_cells

    def minimax(self,board,player_is_user,depth):
        from copy import deepcopy
        mark, status = self.check_win(board)
        if status != "None":
            return self.score(board,depth)
        depth += 1
        if player_is_user:
            mark = self.user_mark
        else:
            mark = self.opponent_mark

        moves = []
        empty_cells = self.compute_empty_cells(board)
        for empty_cell in empty_cells:
            move = {}
            move['index'] = empty_cell
            new_board = deepcopy(board)
            row, column = empty_cell
            self.move(new_board, row, column)
            result = self.minimax(new_board, not player_is_user,depth)
            move['score'] = result
            moves.append(move)

        best_move = None
        if player_is_user:
            best = float('inf')
            for move in moves:
                if move['score'] < best:
                    best = move['score']
                    best_move = move['index']
        else:
            best = float('-inf')
            for move in moves:
                if move['score'] > best:
                    best = move['score']
                    best_move = move['index']
        return best_move

    def AI_play(self):
        from random import choice
        import copy
        empty_cells = self.compute_empty_cells(self.board)
        if len(empty_cells) == 81:
            self.move(choice(range(9)), choice(range(9)), self.opponent_mark)
            return 
        print("Computer is thinking...")
        best_move = self.minimax(copy.deepcopy(self.board),False,-1)
        self.move(best_move[0],best_move[1],self.opponent_mark)
        with open('tictactoc.txt','a') as ttt:
            ttt.write(self.opponent_mark+":"+str(move)+'\n')

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

            print("Turn for '{}'".format(mark))
            # if self.is_user_turn:
            row = input("Enter the number of row: ")
            column = input("Enter the number of column: ")
            if self.move(row, column, mark):
                self.is_user_turn = not self.is_user_turn
                with open('tictactoc.txt','a') as ttt:
                    ttt.write(mark+":"+user_info+'\n')
            # else:
            #     self.AI_play()
            #     self.is_user_turn = not self.is_user_turn
               

            mark, status = self.check_win(self.board)
            self.print_board()
            if status == "None":
                continue
            if status == "done" and mark == self.user_mark:
                print("You Win!")
            if status == "done" and mark == self.opponent_mark:
                print("You Lose!")
            if status == "draw":
                print("Tie!")
            user_info = input("Start a new game? ('q' to quit): ")
            if user_info != 'q':
                self.start()
            else:
                break
            with open('tictactoc.txt','a') as ttt:
                ttt.write("-- New Turn -- \n")

#TEST
newgame = tic_tac_toc()
newgame.main()
