import numpy as np
import time

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

    def is_draw(self):
        return np.all(self.board != 0)

    def get_valid_locations(self):
        return [col for col in range(self.width) if self.is_valid_location(col)]

    def print_board(self):
        print(self.board)

    def copy(self):
        copy_board = Connect4(self.width, self.height)
        copy_board.board = np.copy(self.board)
        return copy_board

    def get_heuristic_score(self, player):
        player_score = 0
        opponent_score = 0

        # Score horizontally
        for r in range(self.height):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(self.width - 3):
                window = row_array[c:c + self.winning_length]
                player_score += self.evaluate_window(window, player)
                opponent_score += self.evaluate_window(window, 1 if player == 2 else 2)

        # Score vertically
        for c in range(self.width):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(self.height - 3):
                window = col_array[r:r + self.winning_length]
                player_score += self.evaluate_window(window, player)
                opponent_score += self.evaluate_window(window, 1 if player == 2 else 2)

        # Score diagonally (up-right)
        for r in range(self.height - 3):
            for c in range(self.width - 3):
                window = [self.board[r + i][c + i] for i in range(self.winning_length)]
                player_score += self.evaluate_window(window, player)
                opponent_score += self.evaluate_window(window, 1 if player == 2 else 2)

        # Score diagonally (up-left)
        for r in range(self.height - 3):
            for c in range(self.width - 3):
                window = [self.board[r + i][c + self.winning_length - 1 - i] for i in range(self.winning_length)]
                player_score += self.evaluate_window(window, player)
                opponent_score += self.evaluate_window(window, 1 if player == 2 else 2)

        return player_score - opponent_score

    def evaluate_window(self, window, player):
        score = 0
        opponent = self.player1 if player == self.player2 else self.player2

        window = [item.tolist() if isinstance(item, np.ndarray) else item for item in window]  # Convert arrays to lists

#        print("Window:", window)  # Print the window to debug

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
    def __init__(self, depth):
        self.depth = depth
        self.expanded_nodes = 0

    def get_move(self, game):
        start_time = time.time()
        move, value = self.minimax(game, self.depth, True)
        end_time = time.time()
        print("Time taken:", end_time - start_time, "seconds")
        print("Expanded nodes:", self.expanded_nodes)
        return move

    def minimax(self, state, depth, maximizing_player):
        indentation = "|  " * (self.depth - depth)
        print(indentation + "---" + ("Max" if maximizing_player else "Min") + " node")

        valid_locations = state.get_valid_locations()
        is_terminal = state.is_draw() or depth == 0
        if is_terminal:
            return None, state.get_heuristic_score(state.player2)

        if maximizing_player:
            value = -np.Inf
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                self.expanded_nodes += 1
                child_state = state.copy()
                child_state.drop_piece(col, state.player2)
                new_score = self.minimax(child_state, depth - 1, False)[1]

                if new_score > value:
                    value = new_score
                    column = col
                print(indentation + "---Child:", col + 1, "Score:", new_score)
                child_state.print_board()  # Print the board for this child state
            return column, value
        else:  # Minimizing player
            value = np.Inf
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                self.expanded_nodes += 1
                child_state = state.copy()
                child_state.drop_piece(col, state.player1)
                new_score = self.minimax(child_state, depth - 1, True)[1]

                if new_score < value:
                    value = new_score
                    column = col
                print(indentation + "---Child:", col + 1, "Score:", new_score)
                child_state.print_board()  # Print the board for this child state

            return column, value

