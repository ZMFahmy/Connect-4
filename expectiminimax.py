import random

import numpy as np

import expectiminimax_tree
import tree_gui
from game_board import GameBoard

chance_nodes_counter = 1
tree_height = 2


class Node:

    def __init__(self, optimizer_type, state, current_player_color, opponent_player_color, height, indentation, tree_list):
        self.optimizer_type = optimizer_type
        self.board_object = GameBoard(state)
        self.state = self.board_object.state
        self.chance_nodes = []
        self.optimal_chance_node = None
        self.height = height
        self.utility_score = None

        self.board_object.get_children_states(current_player_color)
        child_states = self.board_object.child_states if height <= tree_height else None

        print(self.get_printable_state(indentation))
        tree_list.append(self.get_printable_state(indentation))
        tree_string_index_for_state = len(tree_list) - 1
        indentation += "                 "

        if child_states is None:
            player = 1 if current_player_color == 'y' else 2
            opponent = 2 if current_player_color == 'y' else 1
            self.utility_score = get_heuristic_score(self.board_object.get_state_as_ndarray(), player, opponent)

        if child_states is not None:
            global chance_nodes_counter
            if self.optimizer_type == "max":
                upcoming_optimizer_type = "min"
            else:
                upcoming_optimizer_type = "max"

            for i in range(7):
                chance_node = {}
                chance_node_states = []

                print(f"{indentation}chance, score=")
                tree_list.append(f"{indentation}chance, score=")
                tree_string_index_for_chance = len(tree_list) - 1

                for child_map in child_states:
                    if child_map["column_index"] == i - 1:
                        chance_state = {
                            "column_index": i - 1,
                            "node": Node(upcoming_optimizer_type, child_map["state"], opponent_player_color, current_player_color, height + 2, indentation + "          ", tree_list),
                        }
                        chance_node_states.append(chance_state)
                        break

                for child_map in child_states:
                    if child_map["column_index"] == i:
                        chance_state = {
                            "column_index": i,
                            "node": Node(upcoming_optimizer_type, child_map["state"], opponent_player_color, current_player_color, height + 2, indentation + "          ", tree_list),
                        }
                        chance_node_states.append(chance_state)
                        break

                for child_map in child_states:
                    if child_map["column_index"] == i + 1:
                        chance_state = {
                            "column_index": i + 1,
                            "node": Node(upcoming_optimizer_type, child_map["state"], opponent_player_color, current_player_color, height + 2, indentation + "          ", tree_list),
                        }
                        chance_node_states.append(chance_state)
                        break

                if len(chance_node_states) == 3:
                    for c in chance_node_states:
                        if c["column_index"] == i:
                            c["probability"] = 0.6
                        else:
                            c["probability"] = 0.2
                else:
                    for c in chance_node_states:
                        if c["column_index"] == i:
                            c["probability"] = 0.6
                        else:
                            c["probability"] = 0.4

                chance_node["states"] = chance_node_states
                chance_node["name"] = f"chance {chance_nodes_counter}"
                chance_node["height"] = height + 1
                if chance_node_states == []:
                    utility_value = -1
                else:
                    utility_value = 0
                for child in chance_node_states:
                    child_node = child["node"]
                    utility_value += child["probability"] * child_node.utility_score
                chance_node["utility_value"] = utility_value
                tree_list[tree_string_index_for_chance] += "{:.2f}".format(utility_value)

                chance_nodes_counter += 1

                self.chance_nodes.append(chance_node)
            self.get_utility_score()
            tree_list[tree_string_index_for_state] += "{:.2f}".format(self.utility_score)

    def get_utility_score(self):
        if self.optimizer_type == "max":
            score = -99999999
            for child in self.chance_nodes:
                if child["utility_value"] > score:
                    score = child["utility_value"]
                    best_chance_node = child
        else:
            score = 99999999
            for child in self.chance_nodes:
                if child["utility_value"] < score:
                    score = child["utility_value"]
                    best_chance_node = child
        self.utility_score = score
        self.optimal_chance_node = best_chance_node

    def get_printable_state(self, indentation):
        state_formatted_string = indentation + '|'
        k = 0
        for i in range(6):
            for j in range(7):
                state_formatted_string += self.state[k] + '|'
                k += 1
            state_formatted_string += f'\n{indentation}|'
        state_formatted_string += f'\n{indentation}utility value = '
        return state_formatted_string


def get_2s_score(state, color):
    score = 0
    #  horizontal
    i = 0  # row
    for j in range(7):  # column
        while i < 5:
            if state.get_position(i, j) == color and state.get_position(i + 1, j) == color:
                score += 1
                i += 2
            else:
                i += 1
        i = 0

    #  vertical
    j = 0  # column
    for i in range(6):
        while j < 6:
            if state.get_position(i, j) == color and state.get_position(i, j + 1) == color:
                score += 1
                j += 2
            else:
                j += 1
        j = 0

    return score


def get_3s_score(state, color):
    score = 0
    #  horizontal
    i = 0  # row
    for j in range(7):  # column
        while i < 4:
            if state.get_position(i, j) == color and state.get_position(i + 1, j) == color and state.get_position(i + 2, j) == color:
                score += 1
                i += 3
            else:
                i += 1
        i = 0

    #  vertical
    j = 0  # column
    for i in range(6):
        while j < 5:
            if state.get_position(i, j) == color and state.get_position(i, j + 1) == color and state.get_position(i, j + 2) == color:
                score += 1
                j += 3
            else:
                j += 1
        j = 0

    return score


def get_4s_score(state, color):
    score = 0
    #  horizontal
    i = 0  # row
    for j in range(7):  # column
        while i < 3:
            if state.get_position(i, j) == color and state.get_position(i + 1, j) == color and state.get_position(i + 2, j) == color and state.get_position(i + 3, j) == color:
                score += 1
                i += 4
            else:
                i += 1
        i = 0

    #  vertical
    j = 0  # column
    for i in range(6):
        while j < 4:
            if state.get_position(i, j) == color and state.get_position(i, j + 1) == color and state.get_position(i, j + 2) == color and state.get_position(i, j + 3) == color:
                score += 1
                j += 4
            else:
                j += 1
        j = 0

    return score


def old_heuristic_score(state, current_player_color, opponent_player_color):
    current_player_score = 0
    opponent_player_score = 0

    current_player_score += get_2s_score(state, current_player_color)
    current_player_score += get_3s_score(state, current_player_color)
    current_player_score += get_4s_score(state, current_player_color)

    opponent_player_score += get_2s_score(state, opponent_player_color)
    opponent_player_score += get_3s_score(state, opponent_player_color)
    opponent_player_score += get_4s_score(state, opponent_player_color)

    return current_player_score - opponent_player_score


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

    return score


def get_next_move(computer_player_color, human_player_color, current_state=None):
    tree_list = []
    root = Node("max", current_state, computer_player_color, human_player_color, 0, "", tree_list)
    print(root.optimal_chance_node["utility_value"])
    choice_moves = root.optimal_chance_node["states"]

    choice_states = []
    choice_probabilities = []

    for c in choice_moves:
        choice_states.append(c["node"].state)
        choice_probabilities.append(c["probability"])

    if sum(choice_probabilities) < 1:
        max_index = choice_probabilities.index(max(choice_probabilities))
        choice_probabilities[max_index] = 1 - sum(choice_probabilities)

    next_state = random.choices(choice_states, weights=choice_probabilities, k=1)[0]
    expectiminimax_tree.print_list_of_strings(tree_list)
    return next_state
