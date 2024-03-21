import tree_gui
from game_board import GameBoard
import expectiminimax


board = GameBoard()

print("Original board")
board.print_board()


def empty_spaces(state):
    spaces = 0
    for i in range(6):
        for j in range(7):
            if state.get_position(i, j) == ' ':
                spaces += 1
    return spaces


while empty_spaces(board) > 0:
    print("Player turn")
    column = int(input("Enter column: "))
    while not board.insert_disc('r', column-1):
        column = int(input("Enter non empty column: "))
    board.print_board()
    print("Computer turn")
    board.state = expectiminimax.get_next_move('y', 'r', board.state)
    board.print_board()

print("game ended")
print(score_count(board.get_state_as_ndarray()))
