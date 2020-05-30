from pythonvizalgos.graph.viz_tracing import VizTracing
from pythonalgos.graph.vertex import Vertex
from pythonalgos.graph.edge import Edge
from pythonalgos.graph.directed_graph import DirectedGraph
from typing import List, Mapping
import matplotlib.pyplot as plt
import networkx as nx

""" Module that defines a tracing class to be used for tracing of all sorts
of algorithms in relation to directed graphs """


class VizTracingNetworkx(VizTracing):

    NODE_FILL_COLOR: str = 'white'
    NODE_LINE_WITH: float = 1.0
    NODE_LINE_COLOR = 'black'
    NODE_SIZE: int = 500

    EDGE_WIDTH: float = 1.0
    EDGE_COLOR: str = 'black'
    EDGE_STYLE: str = 'dashed'
    EDGE_ARROW_SIZE: int = 20

    IMAGE_NAME_PREFIX: str = "VIZ_TRACING_"
    IMAGE_TYPE: str = "png"

    NODE_FONT_SIZE: int = 15
    NODE_FONT_FAMILY: str = 'sans-serif'

    def __init__(self, path: str, directed_graph: DirectedGraph,
                 vertex_states: List[Mapping[str, Mapping[str, str]]] = None,
                 edge_states: List[Mapping[str, Mapping[str, str]]] = None) \
            -> None:
        """ Method that initialises the tracing functionality

        Args:
            path: the path that will contain the generated trace images
            directed_graph(DirectedGraph): the directed graph
            vertex_states(list): a list of stated definitions (see class) for
                the vertices
            edge_states(list): a list of stated definitions (see class) for
                the edges"""

        super().__init__(path=path, directed_graph=directed_graph,
                         vertex_states=vertex_states, edge_states=edge_states)

    def snapshot(self, directed_graph: DirectedGraph):
        """ Take a snapshot of the current directed graph

        Args:
            directed_graph (DirectedGraph): The directed graph
        """

        dg = nx.DiGraph()
        vertex: Vertex
        for vertex in directed_graph.get_vertices():
            dg.add_node(vertex.get_label())

        edge: Edge
        for edge in directed_graph.get_edges():
            dg.add_edge(
                edge.get_tail().get_label(), edge.get_head().get_label())

        nodes, edges = [n for n in dg.nodes()], \
                       [(u, v) for (u, v, _) in dg.edges(data=True)]

        pos = nx.planar_layout(dg)

        nx.draw_networkx_nodes(
            dg, pos=pos, nodelist=nodes,
            node_size=VizTracingNetworkx.NODE_SIZE,
            node_color=VizTracingNetworkx.NODE_FILL_COLOR,
            linewidths=VizTracingNetworkx.NODE_LINE_WITH,
            edgecolors=VizTracingNetworkx.NODE_LINE_COLOR)

        nx.draw_networkx_edges(
            dg, pos=pos, edgelist=edges,
            width=VizTracingNetworkx.EDGE_WIDTH,
            edge_color=VizTracingNetworkx.EDGE_COLOR,
            style=VizTracingNetworkx.EDGE_STYLE,
            arrowsize=VizTracingNetworkx.EDGE_ARROW_SIZE)

        nx.draw_networkx_labels(
            dg, pos=pos,
            font_size=VizTracingNetworkx.NODE_FONT_SIZE,
            font_family=VizTracingNetworkx.NODE_FONT_FAMILY)

        plt.axis('off')
        plt.show()
