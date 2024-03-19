import matplotlib.pyplot as plt
import networkx as nx


def draw_expectiminimax_tree():
    G = nx.Graph()

    # Add nodes
    G.add_node("Chance_1")
    G.add_node("Chance_2")
    G.add_node("Min_1")
    G.add_node("Min_2")
    G.add_node("Min_3")
    G.add_node("Min_4")

    # Add edges
    G.add_edges_from([("Max_1", "Chance_1"),
                      ("Max_1", "Chance_2"),
                      ("Chance_1", "Min_1"),
                      ("Chance_1", "Min_2"),
                      ("Chance_2", "Min_3"),
                      ("Chance_2", "Min_4"),
                      ])

    # Draw tree
    pos = {
        "Max_1": [0, 0],
        "Chance_1": [-5, 10],
        "Chance_2": [5, 10],
        "Min_1": [-7.5, 20],
        "Min_2": [-2.5, 20],
        "Min_3": [2.5, 20],
        "Min_4": [7.5, 20],
    }
    print(pos)
    nx.draw(G, pos, with_labels=True, node_size=8000, node_color="skyblue", font_size=10, font_weight="bold")
    plt.title("Expectiminimax Tree")
    plt.xlim(-50, 50)
    plt.xlim(-10, 30)
    plt.show()


if __name__ == "__main__":
    draw_expectiminimax_tree()