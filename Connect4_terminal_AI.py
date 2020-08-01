import math
from copy import deepcopy

rows=6
columns=7

def create_board():
    board=[[0]*columns for _ in range(rows)]
    return board
    # print_board(board)

def is_valid_location(board,col):
    if board[0][col]==0:
        return True
    return False

def next_row(board,col):
    for i in range(rows-1,-1,-1):
        if board[i][col]==0:
            return i

def drop(board,col,turn):
    value = 2 if turn&1 else 1
    pos_row=next_row(board,col)
    board[pos_row][col]=value

def available(board):
    for i in board:
        for j in i:
            if j==0:
                return True
    return False

def check_win(board,turn):
    check = 2 if turn&1 else 1
    #horizontal
    for i in range(rows):
        count=0
        for j in range(columns):
            if board[i][j]==check:
                count+=1
                if count==4:
                    return True
            else:
                count=0
    #vertical
    for i in range(columns):
        count=0
        for j in range(rows):
            if board[j][i]==check:
                count+=1
                if count==4:
                    return True
            else:
                count=0
    #diagnol negative slope
    for i in range(rows-3):
        for j in range(columns-3):
            flag=1
            for k in range(4):
                if board[i+k][j+k]!=check:
                    flag=0
                    break
            if flag==1:
                return True
    #diagnol positive slope
    for i in range(rows-3):
        for j in range(3,columns):
            flag=1
            for k in range(4):
                if board[i+k][j-k]!=check:
                    flag=0
                    break
            if flag==1:
                return True
    return False

def print_board(board):
    print()
    for i in board:
        print(*i)

def make_move(board,row,col,turn):
    val = 2 if turn&1 else 1
    res=deepcopy(board)
    res[row][col]=val
    return res

def undo(board,row,col):
    board[row][col]=0
    print('yes')
def get_move(board):
    moves=[]
    for i in range(columns):
        for j in range(rows-1,-1,-1):
            if board[j][i]==0:
                moves.append((j,i))
    return moves

def terminal(board,turn):
    if len(get_move(board))==0:
        return True
    if check_win(board,turn):
        return True
    return False


def eval(board,turn):
    if check_win(board,turn):
        if turn&1:
            return 1000
        else:
            return -1000
    score=0
    def row_check(board):
        score=0
        for i in board:
            count_1,count_2=0,0
            for j in range(len(i)):
                if i[j]==2:
                    count_2+=1
                elif i[j]==1:
                    count_1+=1
                else:
                    if j==0 and i[j+1]==1:
                        score-=10
                    if j==0 and i[j+1]==2:
                        score+=10
                    if j==len(i)-1 and i[j-1]==1:
                        score-=10
                    if j==len(i)-1 and i[j-1]==2:
                        score+=10
                    if j>0 and i[j-1]==1 and count_1>count_2:
                        score-=10
                    if j>0 and i[j-1]==2 and count_2>count_1:
                        score+=10
                    if j<len(i)-1 and i[j+1]==1 and count_1>count_2:
                        score-=10
                    if j<len(i)-1 and i[j+1]==2 and count_2>count_1:
                        score+=10
        return score
    trans=[]
    for i in range(len(board[0])):
        trans.append([board[j][i] for j in range(len(board))])
    score+=row_check(trans)
    score+=row_check(board)
    return score


def minimax(board,depth,alpha,beta,turn):
    if terminal(board,turn) or depth==2:
        return eval(board,turn)
    if turn&1:
        best_score=-math.inf
        for move in get_move(board):
            # drop(board,move[1],turn)
            score=minimax(make_move(board,move[0],move[1],turn),depth+1,alpha,beta,turn^1)
            best_score=max(best_score,score)
            alpha=max(alpha,score)
            # undo(board,move[0],move[1])
            if beta<=alpha:
                break
    else:
        best_score=math.inf
        for move in get_move(board):
            # drop(board,move[1],turn)
            score=minimax(make_move(board,move[0],move[1],turn),depth+1,alpha,beta,turn^1)
            best_score=min(best_score,score)
            beta=min(beta,score)
            # undo(board,move[0],move[1])
            if beta<=alpha:
                break
    return best_score

def AI(board,cols,turn):
    best_score=-math.inf
    best_move=None
    for move in get_move(board):
        # drop(board,move[1],turn)
        score=minimax(make_move(board,move[0],move[1],turn),0,-math.inf,math.inf,turn^1)
        # undo(board,move[0],move[1])
        if score>best_score:
            best_score=score
            best_move=move
    drop(board,best_move[1],turn)

def game():
    print('NEW GAME')

    board=create_board()
    game_over=False
    turn=0
    print_board(board)

    while not game_over:
        if turn&1==0:
            col = int(input(f'Player 1 turn, enter between 1,{columns}: '))
            if is_valid_location(board,col-1):
                drop(board,col-1,turn)
            else:
                print('Enter valid location...')
                continue
        else:
            print('AI turn.....')
            AI(board,columns,turn)

        if check_win(board,turn):
            game_over=True
            player = 'AI' if turn&1 else 1
            print(f'Player {player} wins...!!!')
            print_board(board)

            continue
        if terminal(board,turn):
            game_over=True
            print_board(board)
            print('DRAW')
            continue
        print_board(board)
        turn^=1


    again=input('Play again Y/N: ')
    return again
while(True):
    again=game()
    if again=='Y':
        continue
    break
