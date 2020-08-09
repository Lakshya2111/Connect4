import pygame
import sys
import time

import game as C4

pygame.init()
size = width, height = 700, 700

# Colors
BLUE=(0,0,255)
RED=(255,0,0)
BLACK=(0,0,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
square_size=100
radius=int(square_size/2-5)

screen = pygame.display.set_mode(size)
mediumFont = pygame.font.SysFont("calibri", 28)
largeFont = pygame.font.SysFont("calibri", 40)
moveFont = pygame.font.SysFont("calibri", 60)

user = None
board = C4.create_board()
ai_turn = False
ai=True
while True:
    flag=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Let user choose a player.
    if user is None:
        screen.fill(BLACK)
        # Draw title
        title = largeFont.render("Play Connect4", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playAIButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playAI = mediumFont.render("Play vs AI", True, BLACK)
        playAIRect = playAI.get_rect()
        playAIRect.center = playAIButton.center
        pygame.draw.rect(screen, WHITE, playAIButton)
        screen.blit(playAI, playAIRect)

        playHButton = pygame.Rect(5 * (width / 9), (height / 2), width / 3, 50)
        playH = mediumFont.render("Play vs Human", True, BLACK)
        playHRect = playH.get_rect()
        playHRect.center = playHButton.center
        pygame.draw.rect(screen, WHITE, playHButton)
        screen.blit(playH, playHRect)

        quitButton = pygame.Rect(10,30,width/5,50)
        quit = mediumFont.render('Quit',True,BLACK)
        quitRect = quit.get_rect()
        quitRect.center = quitButton.center
        pygame.draw.rect(screen, WHITE, quitButton)
        screen.blit(quit, quitRect)

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:

                mouse = event.pos
                if playAIButton.collidepoint(mouse):
                    flag=1
                    break

                elif playHButton.collidepoint(mouse):
                    flag=2
                    break

                elif quitButton.collidepoint(mouse):
                    sys.exit()
        if flag==1:
            ai=True
            screen.fill(BLACK)
            # Draw title
            title = largeFont.render("Play Connect4", True, WHITE)
            titleRect = title.get_rect()
            titleRect.center = ((width / 2), 50)
            screen.blit(title, titleRect)

            playRedButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
            playRed = mediumFont.render("Play as RED", True, RED)
            playRedRect = playRed.get_rect()
            playRedRect.center = playRedButton.center
            pygame.draw.rect(screen, YELLOW, playRedButton)
            screen.blit(playRed, playRedRect)

            playYellowButton = pygame.Rect(5 * (width / 9), (height / 2), width / 3, 50)
            playYellow = mediumFont.render("Play as YELLOW", True, YELLOW)
            playYellowRect = playYellow.get_rect()
            playYellowRect.center = playYellowButton.center
            pygame.draw.rect(screen, RED, playYellowButton)
            screen.blit(playYellow, playYellowRect)

            quitButton = pygame.Rect(10,30,width/5,50)
            quit = mediumFont.render('Quit',True,BLACK)
            quitRect = quit.get_rect()
            quitRect.center = quitButton.center
            pygame.draw.rect(screen, WHITE, quitButton)
            screen.blit(quit, quitRect)
            pygame.display.update()

            while user==None:
                for event in pygame.event.get():
                    if event.type==pygame.MOUSEBUTTONDOWN:

                        mouse = event.pos
                        if playRedButton.collidepoint(mouse):
                            user = C4.RED
                            user_color=RED
                            ai_color=YELLOW
                            break
                        elif playYellowButton.collidepoint(mouse):
                            user = C4.YELLOW
                            user_color=YELLOW
                            ai_color=RED
                            break
                        elif quitButton.collidepoint(mouse):
                            sys.exit()

        if flag==2:
            user = C4.RED
            user_color = RED
            player2 = C4.YELLOW
            player2_color = YELLOW
            ai=False


    else:
        game_over = C4.terminal(board)
        player = C4.player(board)
        for c in range(C4.columns):
            for r in range(C4.rows):
                pygame.draw.rect(screen, BLUE, (c*square_size, r*square_size+square_size, square_size, square_size))
                pygame.draw.circle(screen, BLACK, (c*square_size+square_size//2, r*square_size+square_size+square_size//2), radius)

        for c in range(C4.columns):
            for r in range(C4.rows):
                if board[r][c] == C4.RED:
                    pygame.draw.circle(screen, RED, (c*square_size+square_size//2, r*square_size+square_size+square_size//2), radius)
                elif board[r][c] == C4.YELLOW:
                    pygame.draw.circle(screen, YELLOW, (c*square_size+square_size//2, r*square_size+square_size+square_size//2), radius)

        pygame.display.flip()

        if game_over:
            pygame.draw.rect(screen,BLACK,(0,0,width,square_size))

            winner = C4.check_win(board)
            if ai:
                if winner is None:
                    title = f"Game Over: Tie."
                else:
                    if winner==user:
                        winner='You'
                        winner_color=user_color
                    else:
                        winner='AI'
                        winner_color=ai_color
                    title = f"{winner} won."
            else:
                if winner is None:
                    title = f"Game Over: Tie."
                else:
                    if winner==user:
                        winner='Player1'
                        winner_color=RED
                    else:
                        winner='Player2'
                        winner_color=YELLOW
                    title = f"{winner} won."
            title = largeFont.render(title, True, winner_color)
            titleRect = title.get_rect()
            titleRect.center = (width//2, 50)
            screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over and ai:
            if ai_turn:
                pygame.draw.rect(screen,BLACK,(0,0,width,square_size))
                title="AI thinking..."
                title = largeFont.render(title, True, ai_color)
                titleRect = title.get_rect()
                titleRect.center = (width//2, 50)
                screen.blit(title, titleRect)
                pygame.display.flip()
                time.sleep(0.5)
                (row,col) = C4.AI(board)
                board = C4.make_move(board,row,col)
                pygame.draw.rect(screen,BLACK,(0,0,width,square_size))
                title="Your Turn..."
                title = largeFont.render(title, True, user_color)
                titleRect = title.get_rect()
                titleRect.center = (width//2, 50)
                screen.blit(title, titleRect)
                pygame.display.flip()

                if C4.terminal(board):
                    pygame.draw.rect(screen,BLACK,(0,0,width,square_size))
                    pygame.display.flip()

                ai_turn = False
            else:
                ai_turn = True

        ok=0
        if not ai and not game_over:
            pygame.draw.rect(screen,BLACK,(0,0,width,square_size))
            title="Player1 Turn..."
            title = largeFont.render(title, True, user_color)
            titleRect = title.get_rect()
            titleRect.center = (width//2, 50)
            screen.blit(title, titleRect)
            pygame.display.flip()
        while user==player and ok==0 and not game_over:
            for event in pygame.event.get():
                if event.type==pygame.MOUSEMOTION:
                    pygame.draw.rect(screen,BLACK,(0,0,width,square_size))
                    posx=event.pos[0]
                    if user==C4.player(board):
                        pygame.draw.circle(screen,user_color,(posx,square_size//2),radius)

                pygame.display.flip()
                if event.type==pygame.MOUSEBUTTONDOWN and not game_over:
                    col = event.pos[0]//square_size
                    row = C4.next_row(board,col)
                    board = C4.make_move(board,row,col)
                    ok=1
                    break
        if not ai:
            ok=0
            game_over = C4.terminal(board)
            if not game_over:
                pygame.draw.rect(screen,BLACK,(0,0,width,square_size))
                title="Player2 Turn..."
                title = largeFont.render(title, True, player2_color)
                titleRect = title.get_rect()
                titleRect.center = (width//2, 50)
                screen.blit(title, titleRect)
                pygame.display.flip()

            while player2==player and ok==0 and not game_over:
                for event in pygame.event.get():
                    if event.type==pygame.MOUSEMOTION:
                        pygame.draw.rect(screen,BLACK,(0,0,width,square_size))
                        posx=event.pos[0]
                        if player2==C4.player(board):
                            pygame.draw.circle(screen,player2_color,(posx,square_size//2),radius)

                    pygame.display.flip()
                    if event.type==pygame.MOUSEBUTTONDOWN and not game_over:
                        col = event.pos[0]//square_size
                        row = C4.next_row(board,col)
                        board = C4.make_move(board,row,col)
                        ok=1
                        break
        if game_over:
            againButton = pygame.Rect(width-150, 30, width / 5, 50)
            again = mediumFont.render("Play Again", True, BLACK)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, WHITE, againButton)
            screen.blit(again, againRect)

            quitButton = pygame.Rect(10,30,width/5,50)
            quit = mediumFont.render('Quit',True,BLACK)
            quitRect = quit.get_rect()
            quitRect.center = quitButton.center
            pygame.draw.rect(screen, WHITE, quitButton)
            screen.blit(quit, quitRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = C4.create_board()
                    ai_turn = False
                    screen.fill(BLACK)
                if quitButton.collidepoint(mouse):
                    sys.exit()

    pygame.display.flip()
