import numpy as np
import pygame
import subprocess
from game_board import GameBoard
from pruning_minimax import Minimax
from expectiminimax import get_next_move
import GUI_Hossam
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
num=input("enter the number of algorithm type 1.minimax 2.aphabeta  3.expected minimax ")
screen=pygame.display.set_mode(size)
b=GameBoard()
y=b.get_state_as_2d_list()
print(y)
draw_board(y)
count=0
pygame.display.update()
turn='r'
if num=="1":
    subprocess.run(['python', 'GUI_Hossam.py'])
if num=="2":
    while count<=20:
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
                        if not b.insert_disc(turn, col):
                            turn = 'r'
                        else:
                            turn = 'y'
                            count+=1
                        y = b.get_state_as_2d_list()
                        print(y)
                        y = np.flip(y)
                        draw_board(y)
                        pygame.display.update()
            elif turn == 'y':

                    b.state=Minimax(b.state)

                    turn='r'
                    y = b.get_state_as_2d_list()
                    print(y)
                    y=np.flip(y)
                    draw_board(y)
                    pygame.display.update()

if num=="3":
    while count<=20:
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
                        if not b.insert_disc(turn, col):
                            turn = 'r'
                        else:
                            turn = 'y'
                            count+=1
                        y = b.get_state_as_2d_list()
                        print(y)
                        y = np.flip(y)
                        draw_board(y)
                        pygame.display.update()
            elif turn == 'y':

                    b.state=get_next_move('r','y',b.state)

                    turn='r'
                    y = b.get_state_as_2d_list()
                    print(y)
                    y=np.flip(y)
                    draw_board(y)
                    pygame.display.update()
