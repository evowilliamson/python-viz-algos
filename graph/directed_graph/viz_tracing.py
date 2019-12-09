from graphviz import Digraph
from graph.directed_graph.vertex import Vertex
from graph.directed_graph.edge import Edge
from os import path

""" Module that defines a tracing class to be used for tracing of algorithms in relation
to directed graphs
"""

class VizTracing:
    """ Class that is accessed in a static way. It contains functions for tracing algorithms
    in relation to directed graphs 

    states structure:

    [ {"some_state": {**args} ..., {"default": {**args} ]

    """

    tracing = False
    path = None
    directed_graph = None
    vertex_states = list()
    edge_states = list()

    IMAGE_NAME_PREFIX = "VIZ_TRACING_"
    DEFAULT = "default"
    IMAGE_TYPE = "png"
    DEFAULT_STATE = None

    snapshot_no = 1

    @classmethod
    def enable(cls, path, directed_graph, vertex_states=None, edge_states=None):
        VizTracing.tracing = True
        VizTracing.path = path
        VizTracing.directed_graph = directed_graph
        VizTracing.vertex_states = vertex_states or [{VizTracing.DEFAULT: VizTracing.DEFAULT_STATE}]
        VizTracing.edge_states = edge_states or [{VizTracing.DEFAULT: VizTracing.DEFAULT_STATE}]

    @classmethod
    def disable(cls):
        VizTracing.tracing = False

    @classmethod
    def activate_vertex(cls, directed_graph, vertex: Vertex):
        """ Function that sets the attribute "active" of the vertex to true. It deactivates all
        other vertices

        Args:
            directed_graph(DirectedGraph): directed graph object
            vertex(Vertex): the vertex to be activated
        """

        if not VizTracing.tracing:
            return

        for v in directed_graph.get_vertices():
            if v.get_label() == vertex.get_label:
                vertex.set_attr("activated", True)
            else:
                vertex.set_attr("activated", False)

    @classmethod
    def activate_edge(cls, directed_graph, edge: Edge):
        """ Function that sets the "active" of the edge to true. It deactivates all
        other edges

        Args:
            directed_graph(DirectedGraph): directed graph object
            vertex(Vertex): the edge to be activated
        """

        if not VizTracing.tracing:
            return

        for v in directed_graph.get_vertices():
            for e in v.get_heads():
                if e.get_label() == edge.get_head:
                    e.set_attr("activate", True)
                else:
                    e.set_attr("activate", False)

    @classmethod
    def snapshot(cls):
        """ Take a snapshot of the current directed graph

        Args: 
            file_name(str): path and file for the file to be generated
            view_type(bool): True if the attached program for the file is to be started on

        """ 

        graph = Digraph(format=VizTracing.IMAGE_TYPE)
        for label, vertex in VizTracing.directed_graph._vertices.items():
            found = False; default_state = None
            for state in VizTracing.vertex_states:
                attr_name, attr_values = next(iter(state.items()))
                if attr_name != VizTracing.DEFAULT and vertex.get_attr(attr_name):
                    graph.node(str(label), label=None, _attributes=None, **attr_values)
                    found = True
                    break
                elif attr_name == VizTracing.DEFAULT:
                    default_state = attr_values
            if not found:
                graph.node(str(label), default_state or VizTracing.DEFAULT_STATE)

            for head in vertex.get_heads():
                graph.edge(str(label), str(head.get_label()))

        graph.render(path.join(VizTracing.path, 
            VizTracing.IMAGE_NAME_PREFIX + str(VizTracing.snapshot_no)))
        VizTracing.snapshot_no += 1
