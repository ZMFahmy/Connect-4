import numpy as np
import pygame
from game_board import GameBoard
from pruning_minimax import Minimax
import sys
COLS=7
ROWS=6
def boardReshape(state):
    y=np.zeros([6,7])
    counter=0
    for r in range(ROWS):
        for c in range (COLS):
            y[5-r][c]=state[counter]
    return y


def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS+1,0,-1):
            pygame.draw.rect(screen,(0,0,255),(c*squaresize,r*squaresize,squaresize,squaresize))
            if board[(ROWS-r)][c]==' ':
                pygame.draw.circle(screen,(0,0,0),(c*squaresize+squaresize/2,r*squaresize+squaresize/2),radius=(squaresize/2 -5))
            elif board[(ROWS-r)][c]=='r':
                pygame.draw.circle(screen,(255,0,0),(c*squaresize+squaresize/2,r*squaresize+squaresize/2),radius=(squaresize/2 -5))
            elif board[(ROWS-r)][c]=='y':
                pygame.draw.circle(screen,(255,255,0),(c*squaresize+squaresize/2,r*squaresize+squaresize/2),radius=(squaresize/2 -5))
    pass

pygame.init()
squaresize=100
width=COLS*squaresize
height=(ROWS+1)*squaresize
size=(width,height)
screen=pygame.display.set_mode(size)
b=GameBoard()
y=b.get_state_as_2d_list()
print(y)
draw_board(y)

pygame.display.update()
turn='r'
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, squaresize))
            if turn == 'r':
                posx = event.pos[0]

                pygame.draw.circle(screen, (255, 0, 0), (posx + squaresize / 2, squaresize / 2),
                                   radius=(squaresize / 2 - 5))

            if turn == 'y':
                posx = event.pos[0]

                pygame.draw.circle(screen, (255, 255, 0), (posx + squaresize / 2, squaresize / 2),
                                   radius=(squaresize / 2 - 5))
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if turn == 'r':
                    posx = event.pos[0]
                    col = 6-int(round(posx / squaresize))
                    print(col)
                    b.insert_disc(turn, col)
                    turn = 'y'
                    y = b.get_state_as_2d_list()
                    print(y)
                    y = np.flip(y)
                    draw_board(y)
                    pygame.display.update()
        elif turn == 'y':
                    # posx = event.pos[0]
                    # col = 6-int(round(posx / squaresize))
                    # print(col)
                    # if not b.insert_disc(turn, col):
                    #     turn = 'y'
                    # else:
                    #     turn = 'r'
                b.state=Minimax(b.state)
                    # print("dqdqew",k)
                turn='r'
                y = b.get_state_as_2d_list()
                print(y)
                y=np.flip(y)
                draw_board(y)
                pygame.display.update()

