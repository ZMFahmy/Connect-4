from game_board import GameBoard

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
    child_board = GameBoard(state=child)
    child_board.print_board()
    i += 1
