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
                return
            else:
                row_start -= 7

    def print_board(self):
        print("  -------------------------------------------")
        for i in range(6):
            row_start = i * 7
            line = ""
            for j in range(7):
                line += '  |  ' + self.state[row_start + j]
            line += '  |  '
            print(line)
            print("  -------------------------------------------")

    def get_position(self, row_number, column_number):
        row_start = row_number * 7
        char_index = row_start + column_number
        return self.state[char_index]

    def get_children_states(self, next_player):
        for i in range(7):
            if self.state[i] == ' ':
                original_state = self.state
                self.insert_disc(next_player, i)
                self.child_states.append(self.state)
                self.state = original_state
