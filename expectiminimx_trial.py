import tree_gui
from game_board import GameBoard
import expectiminimax


board = GameBoard()

print("Original board")
board.print_board()


def evaluate_final_score(state, current_player_color, opponent_player_color):
    current_player_score = 0
    opponent_player_score = 0

    # Define weights for different connection lengths
    weights = {
        4: 1,
        5: 10,
        6: 1000
    }

    # Check horizontal connections
    for row in range(6):
        for col in range(4):
            window = [state.get_position(row, col + i) for i in range(4)]
            current_count = window.count(current_player_color)
            opponent_count = window.count(opponent_player_color)
            if current_count >= 4:
                current_player_score += weights[current_count]
            elif opponent_count >= 4:
                opponent_player_score += weights[opponent_count]

    # Check vertical connections
    for col in range(7):
        for row in range(3):
            window = [state.get_position(row + i, col) for i in range(4)]
            current_count = window.count(current_player_color)
            opponent_count = window.count(opponent_player_color)
            if current_count >= 4:
                current_player_score += weights[current_count]
            elif opponent_count >= 4:
                opponent_player_score += weights[opponent_count]

    # Check diagonal (\) connections
    for row in range(3):
        for col in range(4):
            window = [state.get_position(row + i, col + i) for i in range(4)]
            current_count = window.count(current_player_color)
            opponent_count = window.count(opponent_player_color)
            if current_count >= 4:
                current_player_score += weights[current_count]
            elif opponent_count >= 4:
                opponent_player_score += weights[opponent_count]

    # Check diagonal (/) connections
    for row in range(3):
        for col in range(3, 7):
            window = [state.get_position(row + i, col - i) for i in range(4)]
            current_count = window.count(current_player_color)
            opponent_count = window.count(opponent_player_color)
            if current_count >= 4:
                current_player_score += weights[current_count]
            elif opponent_count >= 4:
                opponent_player_score += weights[opponent_count]

    print(f"Human player score = {current_player_score}")
    print(f"Computer player score = {current_player_score}")

    # Determine the winner based on scores
    if current_player_score > opponent_player_score:
        print("Human player wins")
    elif current_player_score < opponent_player_score:
        print("Computer player wins")
    else:
        print("Draw")


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
evaluate_final_score(board, 'r', 'y')

