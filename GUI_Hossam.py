import pygame
import sys
from Backend import Connect4, AI

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def create_board():
    return Connect4()


def draw_board(screen, game):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                               int((ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if game.board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                  height - int((ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif game.board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                     height - int((ROW_COUNT - 1 - r) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()



def get_mouse_pos(posx):
    col = posx // SQUARESIZE
    return col


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect Four")
    myfont = pygame.font.SysFont("monospace", 75)

    board = create_board()
    draw_board(screen, board)

    depth = int(input("Enter the depth for the AI player: "))
    ai = AI(depth=depth)
    game_over = False
    turn = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                if turn == 0:
                    col = get_mouse_pos(event.pos[0])
                    if board.is_valid_location(col):
                        for r in range(ROW_COUNT):
                            if board.board[ROW_COUNT - 1 - r][col] == 0:
                                board.board[ROW_COUNT - 1 - r][col] = 1

                                if board.is_draw() or turn == ROW_COUNT * COLUMN_COUNT - 1:
                                    label = myfont.render("Draw!", 1, BLACK)
                                    screen.blit(label, (40, 10))
                                    game_over = True

                                turn += 1
                                turn = turn % 2

                                draw_board(screen, board)
                                board.print_board()
                                break

            # AI's turn
            if turn == 1 and not game_over:
                col = ai.get_move(board)
                if board.is_valid_location(col):
                    for r in range(ROW_COUNT):
                        if board.board[ROW_COUNT - 1 - r][col] == 0:
                            board.board[ROW_COUNT - 1 - r][col] = 2

                            if board.is_draw() or turn == ROW_COUNT * COLUMN_COUNT - 1:
                                label = myfont.render("Draw!", 1, BLACK)
                                screen.blit(label, (40, 10))
                                game_over = True

                            draw_board(screen, board)
                            board.print_board()

                            turn += 1
                            turn = turn % 2
                            break

        if game_over:
            # Game over, determine the winner based on heuristic score
            player1_score = board.get_heuristic_score(1)
            player2_score = board.get_heuristic_score(2)

            if player1_score > player2_score:
                label = myfont.render("Player 1 Wins!", 1, BLUE)
            elif player1_score < player2_score:
                label = myfont.render("Player 2 Wins!", 1, BLUE)
            else:
                label = myfont.render("Draw!", 1, BLUE)

            screen.blit(label, (40, 10))
            pygame.display.update()
            pygame.time.wait(7000)



if __name__ == '__main__':
    main()