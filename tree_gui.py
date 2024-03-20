import matplotlib.pyplot as plt
import networkx
import networkx as nx
from expectiminimax import Node


def get_child_nodes(node, layers, edges):
    chance_nodes = node.chance_nodes

    if chance_nodes == []:
        return

    for c in chance_nodes:
        layers[c["height"]].append(c["name"])
        edges.append((node.get_printable_state(), c["name"]))
        child_states = c["states"]
        for s in child_states:
            layers[c["height"] + 1].append(s["node"].get_printable_state())
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

    x_step = 10
    x = x_step * len(layers)
    for i in range(len(layers)-1, -1, -1):
        G.add_nodes_from(layers[i])

        y = 0
        y_step = len(layers[i]) * 10
        for j, node in enumerate(layers[i]):
            pos[node] = (x, y)
            y -= y_step
        x -= x_step

    print(len(G.nodes()))
    G.add_edges_from(edges)
    nx.draw(G, pos, with_labels=True, node_size=8000, node_color="skyblue", font_size=10, font_weight="bold")
    plt.title("Expectiminimax Tree")
    plt.xlim(0, 200)
    plt.ylim(0, 200)
    plt.show()
