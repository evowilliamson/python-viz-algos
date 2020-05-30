from pythonvizalgos.graph.viz_tracing import VizTracing, DEFAULT, DEFAULT_STATE
from pythonalgos.graph.vertex import Vertex
from pythonalgos.graph.edge import Edge
from pythonalgos.graph.directed_graph import DirectedGraph
from typing import List, Mapping, Dict
import matplotlib.pyplot as plt
import networkx as nx

""" Module that defines a tracing class to be used for tracing of all sorts
of algorithms in relation to directed graphs """


class VizTracingNetworkx(VizTracing):

    NODE_FILL_COLOR: str = 'white'
    NODE_LINE_WITH: float = 1.0
    NODE_LINE_COLOR = 'black'
    NODE_SIZE: int = 2000

    EDGE_WIDTH: float = 1.0
    EDGE_COLOR: str = 'black'
    EDGE_STYLE: str = 'dashed'
    EDGE_ARROW_SIZE: int = 20

    IMAGE_NAME_PREFIX: str = "VIZ_TRACING_"
    IMAGE_TYPE: str = "png"

    NODE_FONT_SIZE: int = 15
    NODE_FONT_FAMILY: str = 'sans-serif'

    def __init__(self, path: str, directed_graph: DirectedGraph,
                 vertex_states: List[Mapping[str, Mapping[str, str]]],
                 edge_states: List[Mapping[str, Mapping[str, str]]]) \
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
            dg.add_node(
                vertex.get_label())

        edge: Edge
        for edge in directed_graph.get_edges():
            dg.add_edge(
                edge.get_tail().get_label(), edge.get_head().get_label())

        nodes, edges = [n for n in dg.nodes()], \
                       [(u, v) for (u, v, _) in dg.edges(data=True)]

        pos = nx.planar_layout(dg)

        self.draw_nodes(dg, pos, nodes, VizTracing.ACTIVATED)
        self.draw_nodes(dg, pos, nodes, VizTracing.ACTIVATED)

        nx.draw_networkx_edges(
            G=dg, pos=pos, edgelist=edges,
            width=VizTracingNetworkx.EDGE_WIDTH,
            edge_color=VizTracingNetworkx.EDGE_COLOR,
            style=VizTracingNetworkx.EDGE_STYLE,
            arrowsize=VizTracingNetworkx.EDGE_ARROW_SIZE)

        nx.draw_networkx_labels(
            G=dg, pos=pos,
            font_size=VizTracingNetworkx.NODE_FONT_SIZE,
            font_family=VizTracingNetworkx.NODE_FONT_FAMILY)

        plt.axis('off')
        plt.show()

    def create_node_buckets(self, directed_graph: DirectedGraph) ->\
            Dict[str, List[Vertex]]:
        """ Create different buckets that fit nodes with the
        same characteristics

        Args:
            directed_graph: The directed graph

        Returns:
            A dictionary that contains lists of vertices per
            characteristic
        """

        mapping: Dict[str, List[Vertex]] = dict()
        for vertex in directed_graph.get_vertices():
            if VizTracing.ACTIVATED in vertex.get_attrs():
                mapping[VizTracing.ACTIVATED].append(vertex)
            elif VizTracing.VISITED in vertex.get_attrs():
                mapping[VizTracing.VISITED].append(vertex)
            else:
                mapping[DEFAULT].append(vertex)

        return mapping

    def draw_nodes(self, dg: nx.DiGraph, pos, node_list: List[Vertex],
                   state: str) -> None:
        """ Method that draws the nodes

        """

        # TODO: refactor to dict
        fill_color: str = "white"
        for mapping in self.get_vertex_states():
            if mapping[state] == state:
                fill_color = mapping[state]["fill_color"]
                break

        nx.draw_networkx_nodes(
            G=dg, pos=pos, nodelist=node_list,
            node_size=VizTracingNetworkx.NODE_SIZE,
            node_color=fill_color,
            linewidths=VizTracingNetworkx.NODE_LINE_WITH,
            edgecolors=VizTracingNetworkx.NODE_LINE_COLOR
            )





