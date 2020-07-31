import pygame
import sys
import time

BLUE=(0,0,255)
RED=(255,0,0)
BLACK=(0,0,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
square_size=100
radius=int(square_size/2-5)

def create_board(rows,columns):
    board=[[0]*columns for _ in range(rows)]
    return board
    # print_board(board)

def is_valid_location(board,col):
    if board[0][col]==0:
        return True
    return False

def next_row(board,col,rows):
    for i in range(rows-1,-1,-1):
        if board[i][col]==0:
            return i

def drop(board,col,turn,rows):
    value = 2 if turn&1 else 1
    pos_row=next_row(board,col,rows)
    board[pos_row][col]=value

def available(board):
    for i in board:
        for j in i:
            if j==0:
                return True
    return False

def check_win(board,turn,rows,columns):
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
    # print('-'*columns)

def game():
    pygame.init()
    myfont=pygame.font.SysFont('monospace',75)
    while(True):
        rows=int(input('Enter no. of rows (>=4): '))
        columns=int(input('Enter no. of columns (>=4): '))
        if rows>=4 and columns>=4:
            break
        else:
            print('Enter valid values.')
    width=columns*square_size
    height=(rows+1)*square_size
    size=(width,height)
    screen=pygame.display.set_mode(size)

    def draw_board(board):
        for c in range(columns):
            for r in range(rows):
                pygame.draw.rect(screen, BLUE, (c*square_size, r*square_size+square_size, square_size, square_size))
                pygame.draw.circle(screen, BLACK, (c*square_size+square_size//2, r*square_size+square_size+square_size//2), radius)

        for c in range(columns):
            for r in range(rows):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (c*square_size+square_size//2, r*square_size+square_size+square_size//2), radius)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (c*square_size+square_size//2, r*square_size+square_size+square_size//2), radius)
        pygame.display.update()

    board=create_board(rows,columns)
    print_board(board)
    draw_board(board)
    game_over=False
    turn=0

    while not game_over:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.MOUSEMOTION:
                pygame.draw.rect(screen,BLACK,(0,0,width,square_size))
                posx=event.pos[0]
                if turn&1==0:
                    pygame.draw.circle(screen,RED,(posx,square_size//2),radius)
                else:
                    pygame.draw.circle(screen,YELLOW,(posx,square_size//2),radius)
            pygame.display.update()

            if event.type==pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, square_size))

                col=event.pos[0]//square_size

                if is_valid_location(board,col):
                    drop(board,col,turn,rows)

                    if check_win(board,turn,rows,columns):
                        game_over=True
                        print_board(board)
                        draw_board(board)
                        break


                    if not available(board):
                        pygame.draw.rect(screen,BLACK,(0,0,width,square_size))
                        pygame.display.update()
                        label=myfont.render('Game Draw',1,WHITE)
                        screen.blit(label,(40,10))
                        draw_board(board)
                        game_over=True
                        again=input('Play again Y/N: ')
                        return again
                else:
                    print('Enter valid location...')
                    continue
                draw_board(board)
                print_board(board)
                turn^=1

    player = 2 if turn&1 else 1
    color = YELLOW if turn&1 else RED
    pygame.draw.rect(screen,BLACK,(0,0,width,square_size))
    pygame.display.update()
    label=myfont.render(f'Player {player} wins!!',1,color)
    screen.blit(label,(40,10))
    draw_board(board)
    print()
    print(f'Player {player} wins...!!!')
    again=input('Play again Y/N: ')
    return again
while(True):
    again=game()
    if again=='Y':
        continue
    break
