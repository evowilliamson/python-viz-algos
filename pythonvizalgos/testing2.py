import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()

G.add_edge('a', 'b', weight=0.6)
G.add_edge('b', 'c', weight=0.2)
G.add_edge('c', 'd', weight=0.1)
G.add_edge('d', 'a', weight=0.1)

G.add_node('a')
G.add_node('b')
G.add_node('c')
G.add_node('d')
G.add_node('e')

elarge = [(u, v) for (u, v, d) in G.edges(data=True)]
nodes = [n for n in G.nodes]

pos = nx.planar_layout(G)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=700,
                       node_color='white', linewidths=1.0, edgecolors='black')

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge,
                       width=1, edge_color='black', style='dashed', arrowsize=50)

# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

H = nx.Graph()

H.add_edge('a', 'c', weight=0.2)
H.add_edge('c', 'd', weight=0.1)
H.add_edge('d', 'e', weight=0.7)
H.add_node('bla')

esmall = [(u, v) for (u, v, d) in H.edges(data=True)]

pos2 = nx.circular_layout(H)  # positions for all nodes
pos2 = {'a': (1, 0), 'b': (2, 0), 'c': (3, 0), 'd': (4, 0), 'e': (5, 0), 'bla': (6, 0) }

# nodes
nx.draw_networkx_nodes(H, pos2, node_size=1000, node_color='w', linewidths=1.0, edgecolors='b')

# edges
nx.draw_networkx_edges(H, pos2, edgelist=esmall, arrowsize=50, edge_color='w',
                       width=1)

# labels
nx.draw_networkx_labels(H, pos2, font_size=20, font_family='sans-serif')


plt.axis('off')
plt.show()
