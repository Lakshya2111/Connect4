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


def eval(board):
    if check_win(board)!=EMPTY:
        if player(board)==RED:
            return 1000
        else:
            return -1000
    score=0
    def row_check(board):
        score=0
        for i in board:
            count_1,count_2=0,0
            for j in range(len(i)):
                if i[j]==YELLOW:
                    count_2+=1
                elif i[j]==RED:
                    count_1+=1
                else:
                    if j==0 and i[j+1]==RED:
                        score-=10
                    if j==0 and i[j+1]==YELLOW:
                        score+=10
                    if j==len(i)-1 and i[j-1]==RED:
                        score-=10
                    if j==len(i)-1 and i[j-1]==YELLOW:
                        score+=10
                    if j>0 and i[j-1]==RED and count_1>count_2:
                        score-=10
                    if j>0 and i[j-1]==YELLOW and count_2>count_1:
                        score+=10
                    if j<len(i)-1 and i[j+1]==RED and count_1>count_2:
                        score-=10
                    if j<len(i)-1 and i[j+1]==YELLOW and count_2>count_1:
                        score+=10
        return score
    trans=[]
    for i in range(len(board[0])):
        trans.append([board[j][i] for j in range(len(board))])
    score+=row_check(trans)
    score+=row_check(board)
    return score


def minimax(board,depth,alpha,beta,isMaximising):
    if terminal(board) or depth==2:
        return eval(board)
    if isMaximising:
        best_score=-math.inf
        for move in get_move(board):
            score=minimax(make_move(board,move[0],move[1]),depth+1,alpha,beta,False)
            best_score=max(best_score,score)
            alpha=max(alpha,score)
            if beta<=alpha:
                break
    else:
        best_score=math.inf
        for move in get_move(board):
            score=minimax(make_move(board,move[0],move[1]),depth+1,alpha,beta,True)
            best_score=min(best_score,score)
            beta=min(beta,score)
            if beta<=alpha:
                break
    return best_score

def AI(board):
    best_score=-math.inf
    best_move=None
    for move in get_move(board):
        score=minimax(make_move(board,move[0],move[1]),0,-math.inf,math.inf,False)
        if score>best_score:
            best_score=score
            best_move=move
    return best_move
