import numpy as np

class Connect4:
    def __init__(self, width=7, height=6):
        self.width = width
        self.height = height
        self.board = np.zeros((height, width))
        self.player1 = 1
        self.player2 = 2
        self.winning_length = 4

    def drop_piece(self, col, player):
        for row in range(self.height-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return True
        return False

    def is_valid_location(self, col):
        return self.board[0][col] == 0

    def is_winner(self, player):
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] == player:
                    # horizontal
                    if c + self.winning_length <= self.width:
                        if np.all(self.board[r, c:c+self.winning_length] == player):
                            return True
                    # vertical
                    if r + self.winning_length <= self.height:
                        if np.all(self.board[r:r+self.winning_length, c] == player):
                            return True
                    # diagonal up-right
                    if c + self.winning_length <= self.width and r - self.winning_length >= 0:
                        if np.all(self.board[r:r-self.winning_length:-1, c:c+self.winning_length] == player):
                            return True
                    # diagonal up-left
                    if c - self.winning_length >= 0 and r - self.winning_length >= 0:
                        if np.all(self.board[r:r-self.winning_length:-1, c:c-self.winning_length:-1] == player):
                            return True
        return False

    def is_draw(self):
        return np.all(self.board != 0)

    def get_valid_locations(self):
        return [col for col in range(self.width) if self.is_valid_location(col)]

    def print_board(self):
        print(np.flip(self.board, 0))

    def copy(self):
        copy_board = Connect4(self.width, self.height)
        copy_board.board = np.copy(self.board)
        return copy_board

    def get_heuristic_score(self, player):
        opponent = self.player1 if player == self.player2 else self.player2
        player_score = 0
        opponent_score = 0

        # Score horizontally
        for r in range(self.height):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(self.width - 3):
                window = row_array[c:c+self.winning_length]
                player_score += self.evaluate_window(window, player)
                opponent_score += self.evaluate_window(window, opponent)

        # Score vertically
        for c in range(self.width):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(self.height - 3):
                window = col_array[r:r+self.winning_length]
                player_score += self.evaluate_window(window, player)
                opponent_score += self.evaluate_window(window, opponent)

        # Score diagonally
        for r in range(self.height - 3):
            for c in range(self.width - 3):
                window = [self.board[r+i][c+i] for i in range(self.winning_length)]
                player_score += self.evaluate_window(window, player)
                opponent_score += self.evaluate_window(window, opponent)

        for r in range(self.height - 3):
            for c in range(self.width - 3):
                window = [self.board[r+3-i][c+i] for i in range(self.winning_length)]
                player_score += self.evaluate_window(window, player)
                opponent_score += self.evaluate_window(window, opponent)

        return player_score - opponent_score

    def evaluate_window(self, window, player):
        score = 0
        opponent = self.player1 if player == self.player2 else self.player2

        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(0) == 1:
            score -= 4

        return score

class AI:
    def __init__(self, depth, use_alpha_beta):
        self.depth = depth

    def get_move(self, game):

        return self.minimax(game, self.depth, True)[0]

    def minimax(self, state, depth, maximizing_player):
        valid_locations = state.get_valid_locations()
        is_terminal = state.is_winner(state.player1) or state.is_winner(state.player2) or len(valid_locations) == 0
        if depth == 0 or is_terminal:
            if is_terminal:
                if state.is_winner(state.player2):
                    return (None, 100000000000000)
                elif state.is_winner(state.player1):
                    return None, -10000000000000
                else: # Draw
                    return (None, 0)
            else: # Depth is zero
                return (None, state.get_heuristic_score(state.player2))
        if maximizing_player:
            value = -np.Inf
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                child_state = state.copy()
                child_state.drop_piece(col, state.player2)
                new_score = self.minimax(child_state, depth-1, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value
        else: # Minimizing player
            value = np.Inf
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                child_state = state.copy()
                child_state.drop_piece(col, state.player1)
                new_score = self.minimax(child_state, depth-1, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value

