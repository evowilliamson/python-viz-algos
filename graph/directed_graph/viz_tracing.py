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

    For example:
        vertex_states=[
                        {VizTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                        {VizTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}},
                        {VizTracing.VISISTED: {"fillcolor":"gray", "style": "filled"}}])

    VizTracing.ACTIVATED takes precedence over VizTracing.IN_CYCLE takes predecence over
    VizTracing.VISITED by definition of the list

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

    ACTIVATED = "activated"
    IN_CYCLE = "in_cycle"
    VISISTED = "visited"
    DISABLED = "disabled"

    @classmethod
    def enable(cls, path, directed_graph, vertex_states=None, edge_states=None):
        """ Class method that initialises the tracing functionality

        Args:
            path: the path that will contain the generated trace images
            directed_graph(DirectedGraph): the directed graph
            vertex_states(list): a list of stated definitions (see class) for the vertices
            edge_states(list): a list of stated definitions (see class) for the edges

        """

        VizTracing.tracing = True
        VizTracing.path = path
        VizTracing.directed_graph = directed_graph
        VizTracing.vertex_states = vertex_states or [{VizTracing.DEFAULT: VizTracing.DEFAULT_STATE}]
        VizTracing.edge_states = edge_states or [{VizTracing.DEFAULT: VizTracing.DEFAULT_STATE}]
        VizTracing.snapshot_no = 1


    @classmethod
    def disable(cls):
        VizTracing.tracing = False

    @classmethod
    def change_activated_vertex(cls, directed_graph, vertex: Vertex):
        """ Function that sets the attribute "active" of the vertex to true. It deactivates all
        other vertices

        Args:
            directed_graph(DirectedGraph): directed graph object
            vertex(Vertex): the vertex to be activated
        """

        if not VizTracing.tracing:
            return
        else:
            VizTracing.set_status(directed_graph, vertex, VizTracing.ACTIVATED)
            for label, v in directed_graph.get_vertices().items():
                if label != vertex.get_label():
                    VizTracing.reset_status(directed_graph, v, VizTracing.ACTIVATED)

    @classmethod
    def set_status(cls, directed_graph, object, status):
        """ Function that tags the vertex as with the provided status
        
        Args:
            directed_graph(DirectedGraph): directed graph object
            object: the vertex of edge for which the status must be set
            status(str): the status to be set
        """

        if not VizTracing.tracing:
            return
        else:
            object.set_attr(status, True)

    @classmethod
    def reset_status(cls, directed_graph, object, status):
        """ Function that resets the status of the object
        
        Args:
            directed_graph(DirectedGraph): directed graph object
            object: the vertex of edge for which the status must be reset
            status(str): the status to be reset
        """

        if not VizTracing.tracing:
            return
        else:
            object.set_attr(status, False)

    @classmethod
    def snapshot(cls):
        """ Take a snapshot of the current directed graph

        Args: 
            file_name(str): path and file for the file to be generated
            view_type(bool): True if the attached program for the file is to be started on

        """ 

        if not VizTracing.tracing:
            return
        else:
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

                for edge in vertex.get_edges():
                    found = False; default_state = None
                    for state in VizTracing.edge_states:
                        attr_name, attr_values = next(iter(state.items()))
                        if attr_name != VizTracing.DEFAULT and edge.get_attr(attr_name):
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
             
            graph.render(path.join(VizTracing.path, 
                VizTracing.IMAGE_NAME_PREFIX + ("{:04d}".format(VizTracing.snapshot_no))))
            VizTracing.snapshot_no += 1
    
