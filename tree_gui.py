import matplotlib.pyplot as plt
import networkx
import networkx as nx
from expectiminimax import Node


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


def get_child_nodes(node, layers, edges):
    chance_nodes = node.chance_nodes

    if chance_nodes == []:
        return

    for c in chance_nodes:
        layers[c["height"]].append(c["name"])
        edges.append((node.get_printable_state(), c["name"]))
        child_states = c["states"]
        for s in child_states:
            get_child_nodes(s["node"], layers, edges)
            edges.append((c["name"], s["node"].get_printable_state()))


def construct_expectiminimax_tree(root, max_height):
    G = nx.Graph()
    layers = []
    edges = []
    pos = {}

    for i in range(2 * max_height):
        layers.append([])

    layers[0].append(root.get_printable_state())
    get_child_nodes(root, layers, edges)

    for i, layer in enumerate(layers):
        G.add_nodes_from(layer)
        for j, node in enumerate(layer):
            pos[node] = (i*10, j*10)

    print(G.nodes())
    G.add_edges_from(edges)
    nx.draw(G, pos, with_labels=True, node_size=8000, node_color="skyblue", font_size=10, font_weight="bold")
    plt.title("Expectiminimax Tree")
    plt.xlim(-50, 50)
    plt.xlim(-10, 30)
    plt.show()
