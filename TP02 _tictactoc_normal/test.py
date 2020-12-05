from BoardClass import Board

new_board = Board(5, 5, 5)
for row in range(new_board.rows):
    new_board.board[row][0] = 1
print(new_board.check_win(new_board.board, 1))