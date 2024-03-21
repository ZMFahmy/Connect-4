import numpy as np
import pygame
import subprocess
from game_board import GameBoard
from pruning_minimax import Minimax
from expectiminimax import get_next_move
import GUI_Hossam
import sys
import time
from GUI_Hossam import main
COLS=7
ROWS=6


def calculate_score(board, color):
  """
  Calculates the score for a given color on a Connect Four board.

  Args:
      board: A list of lists representing the Connect Four board.
              board[i][j] represents the color at row i, column j.
              Empty cells are represented by None.
      color: The color to calculate the score for (e.g., "red" or "yellow").

  Returns:
      The score for the given color.
  """

  rows, cols = len(board), len(board[0])
  score = 0

  # Check for horizontal streaks
  for row in range(rows):
    consecutive_count = 0
    for col in range(cols):
      if board[row][col] == color:
        consecutive_count += 1
      else:
        consecutive_count = 0
      if consecutive_count == 4:
        score += 1
      elif consecutive_count == 5:
        score += 2

  # Check for vertical streaks (similar logic)
  for col in range(cols):
    consecutive_count = 0
    for row in range(rows):
      if board[row][col] == color:
        consecutive_count += 1
      else:
        consecutive_count = 0
      if consecutive_count == 4:
        score += 1
      elif consecutive_count == 5:
        score += 2

  # Check for diagonal streaks (upward and downward)
  for row in range(rows - 3):
    for col in range(cols - 3):
      # Upward diagonal streak
      if (board[row][col] == color and
          board[row + 1][col + 1] == color and
          board[row + 2][col + 2] == color and
          board[row + 3][col + 3] == color):
        score += 1
      elif (board[row][col] == color and
            board[row + 1][col + 1] == color and
            board[row + 2][col + 2] == color and
            board[row + 3][col + 3] == color and
            board[row + 4][col + 4] == color):
        score += 2

      # Downward diagonal streak (similar logic)

  return score



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
myfont = pygame.font.SysFont("monospace", 75)
turn='r'
if num=="1":
    subprocess.run(['python', 'GUI_Hossam.py'])
if num=="2":
    while count<21:
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
                    t1=time.time()

                    b.state=Minimax(b.state)
                    t2 = time.time()
                    print("search time",t2-t1)
                    turn='r'
                    y = b.get_state_as_2d_list()
                    print(y)
                    y=np.flip(y)
                    draw_board(y)
                    pygame.display.update()
                    print(count)
    b.state = Minimax(b.state)

    turn = 'r'
    y = b.get_state_as_2d_list()
    print(y)
    y = np.flip(y)
    draw_board(y)
    pygame.display.update()
    game_over=True
    print(count)
    from expectiminimax import get_heuristic_score
    if game_over:
        state=b.get_state_as_ndarray()
        # Game over, determine the winner based on heuristic score

        player1_score = get_heuristic_score(state,2,1)
        player2_score = get_heuristic_score(state, 1, 2)
        print(player1_score,player2_score)

        if player1_score > player2_score:
            label = myfont.render("Player 1 Wins!", 1,(0,0,255) )
        elif player1_score < player2_score:
            label = myfont.render("Player 2 Wins!", 1, (0,0,255))
        else:
            label = myfont.render("Draw!", 1, (0,0,255))

        screen.blit(label, (40, 10))
        pygame.display.update()
        pygame.time.wait(6000)


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