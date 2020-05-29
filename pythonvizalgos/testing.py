import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_nodes_from([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(2, 4)
G.add_edge(3, 5)
G.add_edge(4, 6)
G.add_edge(7, 8)
G.add_edge(8, 9)
G.add_edge(9, 2)
G.add_edge(8, 10)
G.add_edge(10, 1)
G.add_edge(11, 2)
G.add_edge(10, 3)
G.add_edge(11, 2)
G.add_edge(9, 6)
G.add_edge(10, 5)
G.add_edge(10, 6)

pos = nx.random_layout(G)
labels = {1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'fdfdf', 8: 'fff', 9: 'k', 10: 'j', 11: 'z', 12: 'x', 13: 'u'}
nx.draw(G, pos, with_labels=False)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=16)
plt.show()
