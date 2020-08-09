import math
from copy import deepcopy

rows=6
columns=7

RED='1'
YELLOW='2'
EMPTY=None

def create_board():
    board=[[EMPTY]*columns for _ in range(rows)]
    return board

def is_valid_location(board,col):
    if board[0][col]==EMPTY:
        return True
    return False

def drop(board,move):
    value = player(board)
    board[move[0]][move[1]]=value

def available(board):
    for i in board:
        for j in i:
            if j==EMPTY:
                return True
    return False

def player(board):
    count_r=0
    count_y=0
    for i in board:
        for j in i:
            if j==RED:
                count_r+=1
            if j==YELLOW:
                count_y+=1
    if count_r==count_y:
        return RED
    return YELLOW

def next_row(board,col):
    for i in range(rows-1,-1,-1):
        if board[i][col]==EMPTY:
            return i

def check_win(board):
    for check in [RED,YELLOW]:
    #horizontal
        for i in range(rows):
            count=0
            for j in range(columns):
                if board[i][j]==check:
                    count+=1
                    if count==4:
                        return check
                else:
                    count=0
        #vertical
        for i in range(columns):
            count=0
            for j in range(rows):
                if board[j][i]==check:
                    count+=1
                    if count==4:
                        return check
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
                    return check
        #diagnol positive slope
        for i in range(rows-3):
            for j in range(3,columns):
                flag=1
                for k in range(4):
                    if board[i+k][j-k]!=check:
                        flag=0
                        break
                if flag==1:
                    return check
    return EMPTY

def print_board(board):
    print()
    for i in board:
        print(*i)

def make_move(board,row,col):
    res=deepcopy(board)
    res[row][col]=player(board)
    return res

def get_move(board):
    moves=[]
    for i in range(columns):
        for j in range(rows-1,-1,-1):
            if board[j][i]==EMPTY:
                moves.append((j,i))
                break
    return moves

def terminal(board):
    if len(get_move(board))==0:
        return True
    if check_win(board)!=EMPTY:
        return True
    return False

def current_score(window,player):

    score=0
    if window.count(player)==4:
        score+=1000
    if window.count(player)==3 and window.count(EMPTY)==1:
        score+=5
    if window.count(player)==2 and window.count(EMPTY)==2:
        score+=2
    if window.count(player)==0 and window.count(EMPTY)==1:
        score-=4

    return score

def eval(board,player):
    if check_win(board)!=EMPTY:
        if check_win(board)==player:
            return 1000
        else:
            return -1000
    score=0
    #center
    score+=[board[i][columns//2] for i in range(rows)].count(player)*3
    #horizontal
    for i in range(rows):
        for j in range(columns-3):
            score+=current_score(board[i][j:j+4],player)
    # vertical
    for i in range(columns):
        for j in range(rows-3):
            temp=[board[k][i] for k in range(j,j+4)]
            score+=current_score(temp,player)
    # diagonal negative
    for i in range(rows-3):
        for j in range(columns-3):
            temp=[board[i+k][j+k] for k in range(4)]
            score+=current_score(temp,player)
    #diagnol positive
    for i in range(rows-3):
        for j in range(columns-3-1,-1,-1):
            temp=[board[i+k][j-k] for k in range(4)]
            score+=current_score(temp,player)
    return score


def minimax(board,depth,alpha,beta,isMaximising,ai):
    if terminal(board) or depth==5:
        return eval(board,ai)
    if isMaximising:
        best_score=-math.inf
        for move in get_move(board):
            score=minimax(make_move(board,move[0],move[1]),depth+1,alpha,beta,False,ai)
            best_score=max(best_score,score)
            alpha=max(alpha,score)
            if beta<=alpha:
                break
    else:
        best_score=math.inf
        for move in get_move(board):
            score=minimax(make_move(board,move[0],move[1]),depth+1,alpha,beta,True,ai)
            best_score=min(best_score,score)
            beta=min(beta,score)
            if beta<=alpha:
                break
    return best_score

def AI(board):
    best_score=-math.inf
    best_move=None
    for move in get_move(board):
        score=minimax(make_move(board,move[0],move[1]),0,-math.inf,math.inf,False,player(board))
        if score>best_score:
            best_score=score
            best_move=move
    return best_move
