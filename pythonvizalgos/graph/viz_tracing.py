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


class VizTracing:

    DEFAULT: str = "default"
    DEFAULT_STATE = None

    ACTIVATED: str = "activated"
    VISITED: str = "visited"
    IN_CYCLE: str = "in_cycle"
    DISABLED: str = "disabled"

    def get_vertex_label_attributes(self) -> List[str]:
        return []

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

        self.path = path
        self.directed_graph = directed_graph
        self.vertex_states = vertex_states or\
            [{VizTracing.DEFAULT: VizTracing.DEFAULT_STATE}]
        self.edge_states = edge_states or\
            [{VizTracing.DEFAULT: VizTracing.DEFAULT_STATE}]
        self.snapshot_no = 1

    def get_directed_graph(self) -> DirectedGraph:
        return self.directed_graph

    def set_status(self, object: Union[Vertex, Edge], status: str,
                   value: Any = True):
        """ Method that tags the vertex with the provided status

        Args:
            object: the vertex or edge for which the status must be set
            status(str): the status to be set
        """

        object.set_attr(status, value)

    def reset_status(self, object: Union[Vertex, Edge], status: str,
                     value: Any = False):
        """ Method that resets the status of the object

        Args:
            object: the vertex of edge for which the status must be reset
            status(str): the status to be reset
        """

        object.set_attr(status, value)

    def reset_attrs(self, directed_graph: DirectedGraph):
        """ Method that resets all attributes of a vertex

        Args:
            directed_graph (DirectedGraph): The directed graph
            vertex(Vertex): the vertex to be activated
        """

        for v in directed_graph.get_vertices():
            v.reset_attrs()

    def change_activated_vertex(self, directed_graph: DirectedGraph,
                                vertex: Vertex):
        """ Method that sets the attribute "active" of the vertex to true.
        It deactivates all other vertices

        Args:
            directed_graph (DirectedGraph): The directed graph
            vertex(Vertex): the vertex to be activated
        """

        self.set_status(vertex, VizTracing.ACTIVATED)
        for v in directed_graph.get_vertices():
            if str(v.get_label()) != str(vertex.get_label()):
                self.reset_status(v, VizTracing.ACTIVATED)

    def deactivate_graph(self, directed_graph: DirectedGraph):
        """ Method that resets the whole graph

        Args:
            directed_graph (DirectedGraph): The directed graph
        """

        for v in directed_graph.get_vertices():
            self.reset_status(v, VizTracing.ACTIVATED)

    def activate_graph(self, directed_graph: DirectedGraph):
        """ Method that sets the attribute "active" of all vertices to
        true.

        Args:
            directed_graph (DirectedGraph): The directed graph
        """

        for v in directed_graph.get_vertices():
            self.set_status(v, VizTracing.ACTIVATED)

    def snapshot(self, directed_graph: DirectedGraph):
        """ Take a snapshot of the current directed graph
        
        Args:
            directed_graph (DirectedGraph): The directed graph
        """

    pass

    def execute(self, resource_path: str):
        """ Template method that prepares the generation of the tracing.
        It's called by the child classes of this class.

        Args:
            resource_path: the path that should contain the generated resources
        """

        pt.create_dir_in_user_home(resource_path)

    def get_extended_label(self, vertex: Vertex) -> str:
        """ This method, possibly, extends the passed label by
        adding more information, if available, dependending on the
        visualizer class
        """

        label = vertex.get_label()

        l: List[str] =\
            [label + str(vertex.get_attrs()[label])
             for label in self.get_vertex_label_attributes()
             if label in vertex.get_attrs()]
        if l:
            return str(label) + " " + ",".join(l)
        else:
            return str(label)


class VizTracingAdvisor(Advisor):
    """ Module that contains the logic for inserting advice at join points for
    visualization of the cyclic check algorithm
    """

    def __init__(self, viz_tracing: VizTracing):
        super().__init__()
        self.viz_tracing = viz_tracing

    def visit_vertex(self, directed_graph: DirectedGraph, vertex: Vertex):
        """ Function that is used to tag vertices with the state "VISITED",
        if these vertices have been visited once. So next time, when another
        predecessor of a tagged vertex is being considered, it is skipped

        Args:
            directed_graph (DirectedGraph): The directed graph
            vertex: the vertex that should get the status "visited"

        """
        self.viz_tracing.change_activated_vertex(directed_graph, vertex)
        self.viz_tracing.set_status(vertex, VizTracing.VISITED)
        self.viz_tracing.snapshot(directed_graph)

    def vertex_already_visited(self, directed_graph: DirectedGraph,
                               edge: Edge):
        """ Function that takes a snapshot after having disabled the
        edge. This is to indicate that the transition cannot be taken

        Args:
            directed_graph(DirectedGraph): The directed graph
            edge(Edge): the edge to be disabled
        """

        self.viz_tracing.set_status(edge, VizTracing.DISABLED)
        self.viz_tracing.snapshot(directed_graph)
        self.viz_tracing.reset_status(edge, VizTracing.DISABLED)
        self.viz_tracing.snapshot(directed_graph)
