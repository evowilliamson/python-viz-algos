from graphviz import Digraph
from pythonalgos.graph.vertex import Vertex
from pythonalgos.graph.edge import Edge
from pythonalgos.util.advisor import Advisor
from os import path
from pythonalgos.util import path_tools as pt
from pythonalgos.graph.directed_graph import DirectedGraph
from typing import List, Mapping, Union, Any, Optional

""" Module that defines a tracing class to be used for tracing of all sorts
of algorithms in relation to directed graphs """


class VizTracing:

    IMAGE_NAME_PREFIX: str = "VIZ_TRACING_"
    DEFAULT: str = "default"
    IMAGE_TYPE: str = "png"
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

    def set_status(self, directed_graph: DirectedGraph,
                   object: Union[Vertex, Edge], status: str,
                   value: Any = True):
        """ Method that tags the vertex with the provided status

        Args:
            directed_graph(DirectedGraph): directed graph object
            object: the vertex or edge for which the status must be set
            status(str): the status to be set
        """

        object.set_attr(status, value)

    def reset_status(self, directed_graph: DirectedGraph,
                     object: Union[Vertex, Edge], status: str,
                     value: Any = False):
        """ Method that resets the status of the object

        Args:
            directed_graph(DirectedGraph): directed graph object
            object: the vertex of edge for which the status must be reset
            status(str): the status to be reset
        """

        object.set_attr(status, value)

    def reset_attrs(self, directed_graph: DirectedGraph):
        """ Method that resets all attributes of a vertex

        Args:
            directed_graph(DirectedGraph): directed graph object
        """

        for v in directed_graph.get_vertices():
            v.reset_attrs

    def change_activated_vertex(self, directed_graph: DirectedGraph,
                                vertex: Vertex):
        """ Method that sets the attribute "active" of the vertex to true.
        It deactivates all other vertices

        Args:
            directed_graph(DirectedGraph): directed graph object
            vertex(Vertex): the vertex to be activated
        """

        self.set_status(
            directed_graph, vertex, VizTracing.ACTIVATED)
        for v in directed_graph.get_vertices():
            if str(v.get_label()) != str(vertex.get_label()):
                self.reset_status(directed_graph, v, VizTracing.ACTIVATED)

    def deactivate_graph(self, directed_graph: DirectedGraph):
        """ Method that resets the whole graph

        Args:
            directed_graph: the directed graph
        """

        for v in directed_graph.get_vertices():
            self.reset_status(directed_graph, v, VizTracing.ACTIVATED)

    def activate_graph(self, directed_graph: DirectedGraph):
        """ Function that sets the attribute "active" of all vertices to
        true.

        Args:
            directed_graph(DirectedGraph): directed graph object
        """

        for v in directed_graph.get_vertices():
            self.set_status(directed_graph, v, VizTracing.ACTIVATED)

    def snapshot(self, DirectedGraph: DirectedGraph):
        """ Take a snapshot of the current directed graph

        Args:
            file_name(str): path and file for the file to be generated
            view_type(bool): True if the attached program for the file is to
                be started on

        """

        graph = Digraph(format=VizTracing.IMAGE_TYPE)
        for vertex in self.directed_graph.get_vertices():
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
            self.path, VizTracing.IMAGE_NAME_PREFIX +
            ("{:04d}".format(self.snapshot_no))))
        self.snapshot_no += 1

    def execute(self, directed_graph: DirectedGraph, resource_path: str):
        """ Template method that prepares the generation of the tracing.
        It's called by the child classes of this class.

        Args:
            vertices(dict): a dictionar with vertices and for each vertex its
                destination vertices
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
        self.viz_tracing.set_status(
            directed_graph, vertex, VizTracing.VISITED)
        self.viz_tracing.snapshot(directed_graph)

    def vertex_already_visited(self, directed_graph: DirectedGraph,
                               edge: Edge):
        """ Function that takes a snapshot after having disabled the
        edge. This is to indicate that the transition cannot be taken

        Args:
            directed_graph(DirectedGraph): The directed graph
            edge(Edge): the edge to be disabled
        """

        self.viz_tracing.set_status(
            directed_graph, edge, VizTracing.DISABLED)
        self.viz_tracing.snapshot(directed_graph)
        self.viz_tracing.reset_status(
            directed_graph, edge, VizTracing.DISABLED)
        self.viz_tracing.snapshot(directed_graph)
