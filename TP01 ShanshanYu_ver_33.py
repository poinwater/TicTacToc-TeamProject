class tic_tac_toc(object):
    def __init__(self):
        self.position_to_row_column = {1:(0,0), 2:(0,1), 3:(0,2),
                                       4:(1,0), 5:(1,1), 6:(1,2),
                                       7:(2,0), 8:(2,1), 9:(2,2)}  
        self.board = [[' ',' ',' '],
                     [' ',' ',' '],
                     [' ',' ',' ']]
        self.is_user_turn = True
        self.user_mark = 'X'
        self.opponent_mark = 'O'
        self.user_is_first = None
        self.step = 0

            
    def Print_board(self):
        # Print a board
        position =   [[1,2,3],
                     [4,5,6],
                     [7,8,9]]
        print("Board:      Positions:")
        for i in range(3):
            print("----------------------------")
            print(" | {} | {} | {} || {} | {} | {} |".format(self.board[i][0],self.board[i][1],self.board[i][2],
                                                      position[i][0],position[i][1],position[i][2]))

    def Start(self):
        from random import choice
        self.board = [[' ',' ',' '],
                     [' ',' ',' '],
                     [' ',' ',' ']]
        self.is_user_turn = True
        self.user_mark = 'X'
        self.opponent_mark = 'O'
        self.step = 0
        self.user_is_first = choice([True,False])
        if not self.user_is_first:
            self.is_user_turn = False
            self.user_mark = 'O'
            self.opponent_mark = 'X'
            print("You get the second!")
        else:
            print("You get the user_is_first!")
            

        
    def Play_successfully(self,cell,mark):
        try:
            cell = int(cell)
            if cell in self.position_to_row_column:
                x,y = self.position_to_row_column[cell]
                if self.board[x][y] == ' ':
                    self.board[x][y] = mark
                    return True
                print("Warning: The position is not empty!")
            else:
                print("Warning: The input number should be in range [1,9]!")
            return False
        except:
            print("Warn: Your input is not an integer.")
            return False

    def Check_complete(self,board):
        step = 0
        for row in board:
            for mark in row:
                if mark != ' ':
                    step += 1
        if step == 9:
            return True    

    def Check_win(self,board):
        #check row
        for row in range(0,3):
            mark1,mark2,mark3 = board[row][0],board[row][1],board[row][2]
            if mark1 != ' ' and mark1 == mark2 and mark1 == mark3:
                return mark1, "done"
        #check column
        for column in range(0,3):
            mark1,mark2,mark3 = board[0][column],board[1][column],board[2][column]
            if mark1 != ' ' and mark1 == mark2 and mark1 == mark3:
                return mark1, "done"
        #check diagonal line
        mark1,mark2,mark3 = board[0][0],board[1][1],board[2][2]
        if mark1 != ' ' and mark1 == mark2 and mark1 == mark3:
                return mark1, "done"
        mark1,mark3 = self.board[0][2],self.board[2][0]
        if mark1 != ' ' and mark1 == mark2 and mark1 == mark3:
                return mark1, "done"
        #check draw
        if self.Check_complete(board):
            return None, "draw"
        return None, "None"
    def score(self,board,depth):
        mark, state = self.Check_win(board)
        if mark == self.opponent_mark and state=="done":
            return 10 - depth
        elif mark == self.user_mark and state=="done":
            return depth - 10
        return 0

    def minimax(self,board,player_is_user,depth):  
        import copy
            
        winner_mark, status = self.Check_win(board)
        if status!="None":
            return self.score(board,depth)
            
        if player_is_user:
            mark = self.user_mark
        else:
            mark = self.opponent_mark
        depth += 1 
        moves = []
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    empty_cells.append(i*3 + (j+1))

        for empty_cell in empty_cells:
            move = {}
            move['index'] = empty_cell
            new_board = copy.deepcopy(board)
            row, column = self.position_to_row_column[empty_cell]
            new_board[row][column] = mark
            if not player_is_user:    
                result = self.minimax(new_board, not player_is_user,depth)    
                move['score'] = result
            else:
                result = -self.minimax(new_board, not player_is_user,depth)    
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
        print("Computer is thinking...")
        if self.step == 0:
            self.Play_successfully(choice(range(1,10)),self.opponent_mark)
            return 
        move = self.minimax(copy.deepcopy(self.board),False,0)
        self.Play_successfully(move,self.opponent_mark)
        with open('tictactoc.txt','a') as ttt:
                    ttt.write(self.opponent_mark+":"+str(move)+'\n')  
        
    def main(self):
        print("Welcome to Tic-tac-toc!")
        user_info = input("Enter anykey to start a new game, enter q to quit: ")
        while user_info!='q':
            if self.user_is_first == None:
                self.Start()
            self.Print_board()
                
            if self.is_user_turn:
                mark = self.user_mark
            else:
                mark = self.opponent_mark

            print("Turn for '{}'".format(mark))
                
            if self.is_user_turn:
                user_info = input("Move on which space? (Enter the number in the board or enter 'q' to quit): ")
                if self.Play_successfully(user_info,mark):
                    self.is_user_turn = not self.is_user_turn
                    self.step += 1
                    with open('tictactoc.txt','a') as ttt:
                        ttt.write(mark+":"+user_info+'\n')  
            else:
                self.AI_play()
                self.is_user_turn = not self.is_user_turn
                self.step += 1
                
                    
                            
                    
            mark, status = self.Check_win(self.board)        
            if status == "done":
                self.Print_board()
                if mark == self.user_mark:
                    print("You Win!")
                else:
                    print("You lose!")
            elif status == "draw":
                self.Print_board()
                print("Tie!")
  
            if status != "None":    
                user_info = input("Do you want to start a new game? (Enter q to quit/ any key to start): ")
                if user_info != 'q':
                    self.Start()
                else:
                    break
                with open('tictactoc.txt','a') as ttt:
                    ttt.write("-- New Turn -- \n")



#TEST

newgame = tic_tac_toc()
newgame.main()