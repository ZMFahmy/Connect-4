import tree_gui
from game_board import GameBoard

chance_nodes_counter = 1


class Node:
    def __init__(self, optimizer_type, state, current_player_color, opponent_player_color, height):
        self.optimizer_type = optimizer_type
        self.board_object = GameBoard(state)
        self.state = self.board_object.state
        self.chance_nodes = []
        self.height = height
        self.utility_score = None

        self.board_object.get_children_states(opponent_player_color)
        child_states = self.board_object.child_states if height <= 2 else None

        if child_states is not None:
            global chance_nodes_counter
            if self.optimizer_type == "max":
                upcoming_optimizer_type = "min"
            else:
                upcoming_optimizer_type = "max"

            for i in range(7):
                chance_node = {}
                chance_node_states = []

                for child_map in child_states:
                    if child_map["column_index"] == i - 1:
                        chance_state = {
                            "column_index": i - 1,
                            "node": Node(upcoming_optimizer_type, child_map["state"], opponent_player_color, current_player_color, height + 2),
                        }
                        chance_node_states.append(chance_state)
                        break

                for child_map in child_states:
                    if child_map["column_index"] == i:
                        chance_state = {
                            "column_index": i,
                            "node": Node(upcoming_optimizer_type, child_map["state"], opponent_player_color, current_player_color, height + 2),
                        }
                        chance_node_states.append(chance_state)
                        break

                for child_map in child_states:
                    if child_map["column_index"] == i + 1:
                        chance_state = {
                            "column_index": i + 1,
                            "node": Node(upcoming_optimizer_type, child_map["state"], opponent_player_color, current_player_color, height + 2),
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
                chance_node["utility_value"] = 0
                chance_node["name"] = chance_nodes_counter
                chance_node["height"] = height + 1

                chance_nodes_counter += 1

                self.chance_nodes.append(chance_node)

    def get_printable_state(self):
        state_formatted_string = ""
        k = 0
        for i in range(6):
            for j in range(7):
                state_formatted_string += self.state[k]
                k += 1
            state_formatted_string += '\n'
        return state_formatted_string


def construct_tree(root):
    pass


def get_next_move(computer_player_color, human_player_color, current_state=None):
    root = Node("max", current_state, computer_player_color, human_player_color, 0)
    print(root.chance_nodes[0]["height"])
    tree_gui.construct_expectiminimax_tree(root, 6)
