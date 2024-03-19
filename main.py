from game_board import GameBoard
import minimax_with_pruning

"""
board = GameBoard()

board.insert_disc('r', 0)
board.insert_disc('r', 0)
board.insert_disc('r', 0)
board.insert_disc('r', 1)
board.insert_disc('r', 1)
board.insert_disc('r', 2)

print("Original board")
board.print_board()

board.get_children_states('y')
i = 1

print("Child states ")
for child in board.child_states:
    print(f"child no {i}")
    state = child["state"]
    child_board = GameBoard(state=state)
    child_board.print_board()
    i += 1

print(board.get_state_as_2d_list())
"""

minimax_with_pruning.get_next_move('c', 'h')
