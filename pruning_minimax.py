from game_board import GameBoard
# alpha Beta pruning
Max_Depth=4

BOTCOLOR='r'
playerCOLOR='y'



# def get_3s_score(state, color):
#     score = 0
#     #  horizontal
#     i = 0  # row
#     for j in range(7):  # column
#         while i < 4:
#             if state.get_position(i, j) == color and state.get_position(i + 1, j) == color and state.get_position(i + 2, j) == color:
#                 score += 1
#                 i += 3
#             else:
#                 i += 1
#         i = 0
#
#     #  vertical
#     j = 0  # column
#     for i in range(6):
#         while j < 5:
#             if state.get_position(i, j) == color and state.get_position(i, j + 1) == color and state.get_position(i, j + 2) == color:
#                 score += 1
#                 j += 3
#             else:
#                 j += 1
#         j = 0
#
#     return score
#
#
# def get_4s_score(state, color):
#     score = 0
#     #  horizontal
#     i = 0  # row
#     for j in range(7):  # column
#         while i < 3:
#             if state.get_position(i, j) == color and state.get_position(i + 1, j) == color and state.get_position(i + 2, j) == color and state.get_position(i + 3, j) == color:
#                 score += 1
#                 i += 4
#             else:
#                 i += 1
#         i = 0
#
#     #  vertical
#     j = 0  # column
#     for i in range(6):
#         while j < 4:
#             if state.get_position(i, j) == color and state.get_position(i, j + 1) == color and state.get_position(i, j + 2) == color and state.get_position(i, j + 3) == color:
#                 score += 1
#                 j += 4
#             else:
#                 j += 1
#         j = 0
#
#     return score


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
        k = heuristic_score(N.board, N.current_player_color, N.opponet_player_color)
        print(k)
        return None, k
    minchild, minutility = None, 1000000
    N.get_children()
    for child in N.board.child_states:
        board = GameBoard()
        board.state = child
        ch = Node(board.state,playerCOLOR, BOTCOLOR, 'max', Depth=parent.Depth + 1)
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
        k=heuristic_score(N.board,N.current_player_color,N.opponet_player_color)
        print(k)
        return None, k
    maxchild, maxutility = None, -1000000
    N.get_children()
    for child in N.board.child_states:
        board = GameBoard()
        board.state = child
        ch = Node(board.state, BOTCOLOR, playerCOLOR, 'max', Depth=parent.Depth + 1)
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

p = GameBoard()


p.print_board()

p.insert_disc('r',0)
p.insert_disc('r',0)
# p.insert_disc('y',3)
p.insert_disc('r',0)
p.insert_disc('r',1)
# p.insert_disc('r',1)
# p.insert_disc('y',3)
p.insert_disc('r',0)
# p.insert_disc('r',3)
p.insert_disc('r',2)
p.insert_disc('r',6)
# p.insert_disc('y',3)
# p.insert_disc('r',6)
# p.insert_disc('r',4)
# p.insert_disc('r',4)
# p.insert_disc('r',5)
# p.insert_disc('r',4)

# p.insert_disc('y',3)
# p.insert_disc('r',3)

g=GameBoard()

g.state=Minimax(p.state)

g.print_board()
