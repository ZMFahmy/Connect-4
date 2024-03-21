from game_board import GameBoard
# alpha Beta pruning
import numpy as np
Max_Depth=7
from expectiminimax import get_heuristic_score


BOTCOLOR=2
playerCOLOR=1
BOTCOLOR='r'
playerCOLOR='y'

def calculate_score(board):
    score = 0

    # Horizontal check
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            window = [board[row][col + i] for i in range(4)]
            score += evaluate_windowsc(window)

    # Vertical check
    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            window = [board[row + i][col] for i in range(4)]
            score += evaluate_windowsc(window)

    # Diagonal check (positive slope)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_windowsc(window)

    # Diagonal check (negative slope)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            window = [board[row + 3 - i][col + i] for i in range(4)]
            score += evaluate_windowsc(window)

    return score


def evaluate_windowsc(window):
    if window.count(1) == 4:
        return 1
    elif window.count(1) == 5:
        return 2
    elif window.count(2) == 4:
        return -1
    elif window.count(2) == 5:
        return -2
    else:
        return 0

def get_heuristic_score(board_as_ndarray, player, opponent):
    player_score = 0
    opponent_score = 0
    width = 7
    height = 6
    winning_length = 4

    # Score horizontally
    for r in range(height):
        row_array = [int(i) for i in list(board_as_ndarray[r, :])]
        for c in range(width - 3):
            window = row_array[c:c + winning_length]
            player_score += evaluate_window(window, player, opponent)
            opponent_score += evaluate_window(window, opponent, player)

    # Score vertically
    for c in range(width):
        col_array = [int(i) for i in list(board_as_ndarray[:, c])]
        for r in range(height - 3):
            window = col_array[r:r + winning_length]
            player_score += evaluate_window(window, player, opponent)
            opponent_score += evaluate_window(window, opponent, player)

    # Score diagonally (up-right)
    for r in range(height - 3):
        for c in range(width - 3):
            window = [board_as_ndarray[r + i][c + i] for i in range(winning_length)]
            player_score += evaluate_window(window, player, opponent)
            opponent_score += evaluate_window(window, opponent, player)

    # Score diagonally (up-left)
    for r in range(height - 3):
        for c in range(width - 3):
            window = [board_as_ndarray[r + i][c + winning_length - 1 - i] for i in range(winning_length)]
            player_score += evaluate_window(window, player, opponent)
            opponent_score += evaluate_window(window, opponent, player)

    return player_score - opponent_score


def evaluate_window(window, player, opponent):
    score = 0

    window = [item.tolist() if isinstance(item, np.ndarray) else item for item in window]  # Convert arrays to lists

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 4
    if window.count(opponent) == 4 and window.count(0) == 1:
        score -= 100

    return score




def heuristic_score(state, current_player_color, opponent_player_color):
    current_player_score = 0
    opponent_player_score = 0

    # Define weights for different patterns
    weights = {
        "2-in-a-row": 1,
        "3-in-a-row": 10,
        "4-in-a-row": 1000,
        "center": 2,
        "edge": 1
    }

    # Horizontal and vertical patterns
    for i in range(6):
        for j in range(7):
            color = state.get_position(i, j)
            if color == current_player_color:
                # Check horizontal patterns
                if j <= 3:
                    current_player_score += weights["2-in-a-row"]
                    if j <= 2:
                        current_player_score += weights["3-in-a-row"]
                        if j == 0:
                            current_player_score += weights["4-in-a-row"]
                # Check vertical patterns
                if i <= 2:
                    current_player_score += weights["2-in-a-row"]
                    if i <= 1:
                        current_player_score += weights["3-in-a-row"]
                        if i == 0:
                            current_player_score += weights["4-in-a-row"]
            elif color == opponent_player_color:
                # Check horizontal patterns
                if j <= 3:
                    opponent_player_score += weights["2-in-a-row"]
                    if j <= 2:
                        opponent_player_score += weights["3-in-a-row"]
                        if j == 0:
                            opponent_player_score += weights["4-in-a-row"]
                # Check vertical patterns
                if i <= 2:
                    opponent_player_score += weights["2-in-a-row"]
                    if i <= 1:
                        opponent_player_score += weights["3-in-a-row"]
                        if i == 0:
                            opponent_player_score += weights["4-in-a-row"]

    # Diagonal patterns (/ and \)
    for i in range(3):
        for j in range(4):
            # Upward diagonal (/)
            if state.get_position(i, j) == current_player_color and \
                    state.get_position(i + 1, j + 1) == current_player_color and \
                    state.get_position(i + 2, j + 2) == current_player_color and \
                    state.get_position(i + 3, j + 3) == current_player_color:
                current_player_score += weights["4-in-a-row"]
            elif state.get_position(i, j) == opponent_player_color and \
                    state.get_position(i + 1, j + 1) == opponent_player_color and \
                    state.get_position(i + 2, j + 2) == opponent_player_color and \
                    state.get_position(i + 3, j + 3) == opponent_player_color:
                opponent_player_score += weights["4-in-a-row"]

            # Downward diagonal (\)
            if state.get_position(i + 3, j) == current_player_color and \
                    state.get_position(i + 2, j + 1) == current_player_color and \
                    state.get_position(i + 1, j + 2) == current_player_color and \
                    state.get_position(i, j + 3) == current_player_color:
                current_player_score += weights["4-in-a-row"]
            elif state.get_position(i + 3, j) == opponent_player_color and \
                    state.get_position(i + 2, j + 1) == opponent_player_color and \
                    state.get_position(i + 1, j + 2) == opponent_player_color and \
                    state.get_position(i, j + 3) == opponent_player_color:
                opponent_player_score += weights["4-in-a-row"]

    # Center and edge positions
    center_positions = [(2, 3), (3, 3), (2, 4), (3, 4)]
    edge_positions = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 5), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]

    for position in center_positions:
        if state.get_position(*position) == current_player_color:
            current_player_score += weights["center"]
        elif state.get_position(*position) == opponent_player_color:
            opponent_player_score += weights["center"]

    for position in edge_positions:
        if state.get_position(*position) == current_player_color:
            current_player_score += weights["edge"]
        elif state.get_position(*position) == opponent_player_color:
            opponent_player_score += weights["edge"]

    return current_player_score - opponent_player_score


class Node():
    def __init__(self,state,current_player_color,opponet_player_color,optimizer,Depth=0):
        self.optimizer=optimizer
        self.current_player_color=current_player_color
        self.opponet_player_color = opponet_player_color
        self.state=state
        self.Depth=Depth
        self.Searchscore=None
        self.board=GameBoard()
        self.board.state=state
        self.children=[]
    def get_children(self):
            if self.Depth<Max_Depth:
                self.board.get_children_states_alphaBeta(self.opponet_player_color)

def Minimize(N, alpha, beta):
    parent = N
    if N.Depth >= Max_Depth:

        k = get_heuristic_score(N.board.get_state_as_ndarray(),1,2 )
        print(k)
        return None, k
    minchild, minutility = None, 1000000
    N.get_children()
    for child in N.board.child_states:
        board = GameBoard()
        board.state = child
        print("Depth", N.Depth+1)
        board.print_board()
        ch = Node(board.state, BOTCOLOR,playerCOLOR, 'max', Depth=parent.Depth + 1)
        childret, utility = Maximize(ch, alpha, beta)
        if utility < minutility:
            minchild = child
            minutility = utility
        if minutility <= alpha:
            break
        if minutility <= beta:
            beta = minutility
    return minchild, minutility

def Maximize(N, alpha, beta):
    parent = N
    if N.Depth >= Max_Depth:
        k=heuristic_score(N.board.get_state_as_ndarray(),1,2)
        print(k)
        return None, k
    maxchild, maxutility = None, -1000000
    N.get_children()
    for child in N.board.child_states:
        board = GameBoard()
        board.state = child
        print("Depth",N.Depth+1)
        board.print_board()
        ch = Node(board.state, playerCOLOR, BOTCOLOR, 'max', Depth=parent.Depth + 1)
        childret, utility = Minimize(ch, alpha, beta)
        if utility > maxutility:
            maxchild = child
            maxutility = utility
            if N.Depth==0:
                k=GameBoard()
                k.state=child
                k.print_board()
                print("the util",utility)


        if maxutility >= beta:
            break
        if maxutility >= alpha:
            alpha = maxutility
    return maxchild, maxutility

def Minimax(state):
    root = Node(state,BOTCOLOR,playerCOLOR, 'max', 0)
    child, utility = Maximize(root, -1000000, 1000000)

    return child




