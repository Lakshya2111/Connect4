import numpy as np

class Board():
    #initialise the board
    def __init__(self,row,col):
        self.board=np.zeros((row,col),dtype=int)
        self.rows=row
        self.columns=col

    #check for valid lacation for next move
    def is_valid_location(self,col):
        if col>=0 and col<=6 and self.board[0][col]==0:
            return True
        return False

    #get the location for next move
    def get_next_open_row(self,col):
        for i in range(self.rows):
            if self.board[i][col]!=0:
                return i-1
        return self.rows-1

    #Drop the piece of the current player
    def drop_piece(self,col,turn):
        pos=self.get_next_open_row(col)
        if turn&1==0:
            self.board[pos][col]=1
        else:
            self.board[pos][col]=2

    #check if current player wins the game
    def check_win(self,turn):
        check = 2 if turn&1 else 1

        #horizontal
        for i in range(self.rows):
            count=0
            for j in range(self.columns):
                if self.board[i][j]==check:
                    count+=1
                    if count==4:
                        return True
                else:
                    count=0

        #vertical
        for i in range(self.columns):
            count=0
            for j in range(self.rows):
                if self.board[j][i]==check:
                    count+=1
                    if count==4:
                        return True
                else:
                    count=0

        #diagnol negative slope
        for i in range(self.rows-3):
            for j in range(self.columns-3):
                flag=1
                for k in range(4):
                    if self.board[i+k][j+k]!=check:
                        flag=0
                        break
                if flag==1:
                    return True

        #diagnol positive slope
        for i in range(self.rows-3):
            for j in range(3,self.columns):
                flag=1
                for k in range(4):
                    if self.board[i+k][j-k]!=check:
                        flag=0
                        break
                if flag==1:
                    return True

        return False
def game():
    while(True):
        rows=int(input('Enter no. of rows (>=4): '))
        columns=int(input('Enter no. of columns (>=4): '))
        if rows>=4 and columns>=4:
            break
        else:
            print('Enter valid values.')

    board=Board(rows,columns)
    game_over=False
    turn=0

    while not game_over:
        if turn&1==0:
            col = int(input(f'Player 1 turn, enter between 1,{columns}: '))
        else:
            col = int(input(f'Player 2 turn, enter between 1,{columns}: '))

        if board.is_valid_location(col-1):
            board.drop_piece(col-1,turn)
            if board.check_win(turn):
                game_over=True
                print(board.board)
                continue
        else:
            print('Enter valid location...')
            continue
        print(board.board)
        turn^=1
        
    player = 2 if turn&1 else 1
    print(f'Player {player} wins...!!!')
    again=input('Play again Y/N: ')
    return again
while(True):
    again=game()
    if again=='Y':
        continue
    break
