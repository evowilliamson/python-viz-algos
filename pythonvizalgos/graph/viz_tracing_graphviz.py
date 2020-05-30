from pythonvizalgos.graph.viz_tracing import VizTracing
from graphviz import Digraph
from pythonalgos.graph.vertex import Vertex
from pythonalgos.graph.edge import Edge
from pythonalgos.util.advisor import Advisor
from os import path
from pythonalgos.util import path_tools as pt
from pythonalgos.graph.directed_graph import DirectedGraph
from typing import List, Mapping, Union, Any

""" Module that defines a tracing class to be used for tracing of all sorts
of algorithms in relation to directed graphs """


class VizTracingGraphviz(VizTracing):

    IMAGE_NAME_PREFIX: str = "VIZ_TRACING_"
    IMAGE_TYPE: str = "png"

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
        self.snapshot_no = 1

    def snapshot(self, directed_graph: DirectedGraph):
        """ Take a snapshot of the current directed graph

        Args:
            directed_graph (DirectedGraph): The directed graph
        """

        graph = Digraph(format=VizTracingGraphviz.IMAGE_TYPE)
        for vertex in directed_graph.get_vertices():
            found = False
            default_state: Union[Mapping[str, str], None] = {}
            for state in self.vertex_states:
                attr_name, attr_values = next(iter(state.items()))
                if attr_name != VizTracing.DEFAULT and\
                        vertex.get_attr(attr_name):
                    graph.node(name=str(vertex.get_label()),
                               label=self.get_extended_label(vertex),
                               _attributes=None, **attr_values)
                    found = True
                    break
                elif attr_name == VizTracing.DEFAULT:
                    default_state = attr_values
            if not found:
                graph.node(name=str(vertex.get_label()),
                           label=self.get_extended_label(vertex),
                           _attributes=None, **default_state or {})

            for edge in vertex.get_edges():
                found = False
                default_state: Union[Mapping[str, str], None] = {}
                for state in self.edge_states:
                    attr_name, attr_values = next(iter(state.items()))
                    if attr_name != VizTracing.DEFAULT and \
                            edge.get_attr(attr_name):
                        graph.edge(
                            str(edge.get_tail().get_label()),
                            str(edge.get_head().get_label()),
                            label=None, _attributes=None, **attr_values)
                        found = True
                        break
                    elif attr_name == VizTracing.DEFAULT:
                        default_state = attr_values
                if not found:
                    graph.edge(
                        str(edge.get_tail().get_label()),
                        str(edge.get_head().get_label()))
        graph.render(path.join(
            self.path, VizTracingGraphviz.IMAGE_NAME_PREFIX +
            ("{:04d}".format(self.snapshot_no))))
        self.snapshot_no += 1
