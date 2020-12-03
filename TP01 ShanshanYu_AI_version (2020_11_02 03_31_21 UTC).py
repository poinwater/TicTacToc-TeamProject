class tic_tac_toc(object):
    

    def __init__(self):
        self.Move = {1:(0,0), 2:(0,1), 3:(0,2),
                     4:(1,0), 5:(1,1), 6:(1,2),
                     7:(2,0), 8:(2,1), 9:(2,2)}  
        self.board = [[1,2,3],
                     [4,5,6],
                     [7,8,9]]
        self.user_turn = True
        self.user_chess = 'X'
        self.opponent_chess = 'O'
        self.first = None
        self.move = -1
        self.step = 0

            
    def Print_board(self):
        # Print a board
        for i in range(3):
            print("{}, {}, {}".format(self.board[i][0],self.board[i][1],self.board[i][2]))

    def Start(self):
        print("Welcome to Tic-tac-toc!")
        self.board = [[1,2,3],
                     [4,5,6],
                     [7,8,9]]
        self.user_turn = True
        self.user_chess = 'X'
        self.opponent_chess = 'O'
        self.step = 0
        from random import choice
        self.first = choice([True,False])
        if not self.first:
            self.user_turn = False
            self.user_chess = 'O'
            self.opponent_chess = 'X'
            print("You get the second!")
        else:
            print("You get the first!")
            

        
    def Play(self,number,chess):
        try:
            number = int(number)
            if number in self.Move:
                x,y = self.Move[number]
                if self.board[x][y] in self.Move:
                    self.board[x][y] = chess
                    return True
                print("Warning: The chess already exists at the location")
            else:
                print("Warning: The input number should be in range [1,9]!")
            return False
        except:
            print("Warn: Your input is not an integer.")
            return False
        
    def Check_win(self,board):
        #check row
        for row in range(0,3):
            chess1,chess2,chess3 = board[row][0],board[row][1],board[row][2]
            if chess1 == chess2 and chess1 == chess3:
                if chess1 == self.user_chess:
                    return 1
                else:
                    return -1
        #check column
        for column in range(0,3):
            chess1,chess2,chess3 = board[0][column],board[1][column],board[2][column]
            if chess1 == chess2 and chess1 == chess3:
                if chess1 == self.user_chess:
                    return 1
                else:
                    return -1
        #check diagonal line
        chess1,chess2,chess3 = board[0][0],board[1][1],board[2][2]
        if chess1 == chess2 and chess1 == chess3:
                if chess1 == self.user_chess:
                    return 1
                else:
                    return -1
        chess1,chess3 = self.board[0][2],self.board[2][0]
        if chess1 == chess2 and chess1 == chess3:
                if chess1 == self.user_chess:
                    return 1
                else:
                    return -1
        return 0
    def minimax(self,board,player_is_user): 
        import copy
        check_win = self.Check_win(board)
        if check_win !=0:
            if check_win == 1 and player_is_user:
                return 1
            elif check_win == -1 and not player_is_user:
                return 1
            else:
                return -1
             
       
        
    def AI_play(self,chess):
        from random import choice
        import copy
        if self.step == 0:
            self.Play(choice(range(1,10)),self.opponent_chess)
            return 
        Bestscore = -2
        Bestmove = -1
        for i in range(1,10):
            row,column = self.Move[i]
            if board[row][column] in self.Move:
                boardForNewMove = copy.deepcopy(self.board)
                score = self.minimax(boardForNewMove,False)
                if score > Bestscore:
                    Bestscore = score
                    Bestmove = i
        self.Play(Bestmove,self.opponent_chess)
         
    def main(self):
        print("Welcom to Tic-Tac-Toc!")
        user_info = input("Enter anykey to start a new game, enter q to quit: ")
        self.Start()
        while user_info!='q':
            print("The current board:")
            self.Print_board()

            if self.user_turn:
                chess = self.user_chess
            else:
                chess = self.opponent_chess

            print("Turn for '{}'".format(chess))
            
            if self.user_turn:
                user_info = input("Move on which space? (Enter the number in the board or enter 'q' to quit): ")
                if self.Play(user_info,chess):
                    self.user_turn = not self.user_turn
                    self.step += 1
                    with open('tictactoc.txt','a') as ttt:
                        ttt.write(chess+":"+user_info+'\n')  
            else:
                self.AI_play(chess)
                self.user_turn = not self.user_turn
                self.step += 1
                with open('tictactoc.txt','a') as ttt:
                    ttt.write(chess+":"+str(self.move)+'\n')  
                
                        
                
                
            print(self.step)
            if self.Check_win(self.board)!=0 or self.step==10:
                check_win = self.Check_win(self.board)
                print("The current board:")
                self.Print_board()
                if check_win == 1:
                    print("You win!")
                elif self.step == 9:
                    print("Tie!")
                else:
                    print("You lose!")
                user_info = input("Do you want to start a new game? (Enter q to quit/ any key to start): ")
                if user_info != 'q':
                    self.Start()
                else:
                    break
                with open('tictactoc.txt','a') as ttt:
                    ttt.write("-- New Turn -- \n")

                
        print("Bye!")


#TEST

newgame = tic_tac_toc()
newgame.main()