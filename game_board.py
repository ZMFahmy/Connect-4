import numpy as np


class GameBoard:
    def __init__(self, state=None):
        if state is None:
            self.state = "                                          "
        else:
            if isinstance(state, list):
                self.state = ""
                for i in range(6):
                    for j in range(7):
                        self.state += state[i][j]
            else:
                self.state = state
        self.child_states = []

    def insert_disc(self, color, column_number):
        row_start = 35
        for i in range(6, 0, -1):
            if self.state[row_start + column_number] == ' ':
                self.state = self.state[:row_start + column_number] + color + self.state[row_start + column_number + 1:]
                return self.state
            else:
                row_start -= 7
        return False

    def print_board(self):
        print("   -------------------------------------------")
        for i in range(6):
            row_start = i * 7
            line = f"{i + 1}"
            for j in range(7):
                line += '  |  ' + self.state[row_start + j]
            line += '  |  '
            print(line)
            print("   -------------------------------------------")
        print("      1     2     3     4     5     6     7")

    def get_position(self, row_number, column_number):
        row_start = row_number * 7
        char_index = row_start + column_number
        return self.state[char_index]

    def get_children_states(self, next_player):
        for i in range(7):
            if self.state[i] == ' ':
                original_state = self.state
                self.insert_disc(next_player, i)
                child_node = {
                    "state": self.state,
                    "column_index": i,
                }
                self.child_states.append(child_node)
                self.state = original_state

    def get_children_states_alphaBeta(self, next_player):
        positions=[]
        for i in range(7):
            if self.state[i] == ' ':
                original_state = self.state
                self.insert_disc(next_player, i)
                child_node = {
                    "state": self.state,
                    "column_index": i,
                }
                self.child_states.append(self.state)
                positions.append(i)

                self.state = original_state
        return positions

    def get_state_as_2d_list(self):
        arr = []
        for i in range(6):
            row_start = i * 7
            row = []
            for j in range(7):
                row.append(self.state[row_start + j])
            arr.append(row)
        return arr

    def get_state_as_ndarray(self):
        arr = np.array(self.get_state_as_2d_list())
        for i in range(6):
            for j in range(7):
                if arr[i][j] == ' ':
                    arr[i][j] = 0
                elif arr[i][j] == 'r':
                    arr[i][j] = 1
                if arr[i][j] == 'y':
                    arr[i][j] = 2

        return np.array(arr)
