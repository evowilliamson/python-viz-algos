from graphviz import Digraph
from pythonalgos.graph.vertex import Vertex
from pythonalgos.util.advisor import Advisor
from os import path
from pythonalgos.util import path_tools as pt
from pythonalgos.graph.directed_graph import DirectedGraph


class VizTracing:

    tracing = False
    path: str
    directed_graph = None
    vertex_states = list()
    edge_states = list()

    IMAGE_NAME_PREFIX = "VIZ_TRACING_"
    DEFAULT = "default"
    IMAGE_TYPE = "png"
    DEFAULT_STATE = None

    ACTIVATED = "activated"
    VISISTED = "visited"
    IN_CYCLE = "in_cycle"
    DISABLED = "disabled"

    @classmethod
    def enable(cls, path, directed_graph, vertex_states=None,
               edge_states=None):
        """ Class method that initialises the tracing functionality

        Args:
            path: the path that will contain the generated trace images
            directed_graph(DirectedGraph): the directed graph
            vertex_states(list): a list of stated definitions (see class) for
                the vertices
            edge_states(list): a list of stated definitions (see class) for
                the edges"""

        VizTracing.tracing = True
        VizTracing.path = path
        VizTracing.directed_graph = directed_graph
        VizTracing.vertex_states = vertex_states or\
            [{VizTracing.DEFAULT: VizTracing.DEFAULT_STATE}]
        VizTracing.edge_states = edge_states or\
            [{VizTracing.DEFAULT: VizTracing.DEFAULT_STATE}]
        VizTracing.snapshot_no = 1

    @classmethod
    def disable(cls, ):
        VizTracing.tracing = False

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
    def change_activated_vertex(cls, directed_graph, vertex: Vertex):
        """ Function that sets the attribute "active" of the vertex to true.
        It deactivates all other vertices

        Args:
            directed_graph(DirectedGraph): directed graph object
            vertex(Vertex): the vertex to be activated
        """

        if not VizTracing.tracing:
            return
        else:
            VizTracing.set_status(
                directed_graph, vertex, VizTracing.ACTIVATED)
            for v in directed_graph.get_vertices():
                if str(v.get_label()) != str(vertex.get_label()):
                    VizTracing.reset_status(
                        directed_graph, v, VizTracing.ACTIVATED)

    @classmethod
    def snapshot(cls, ):
        """ Take a snapshot of the current directed graph

        Args:
            file_name(str): path and file for the file to be generated
            view_type(bool): True if the attached program for the file is to
                be started on

        """

        if not VizTracing.tracing:
            return
        else:
            graph = Digraph(format=VizTracing.IMAGE_TYPE)
            for vertex in VizTracing.directed_graph.get_vertices():
                found, default_state = False, None
                for state in VizTracing.vertex_states:
                    attr_name, attr_values = next(iter(state.items()))
                    if attr_name != VizTracing.DEFAULT and\
                            vertex.get_attr(attr_name):
                        graph.node(str(vertex.get_label()), label=None,
                                   _attributes=None, **attr_values)
                        found = True
                        break
                    elif attr_name == VizTracing.DEFAULT:
                        default_state = attr_values
                if not found:
                    graph.node(str(vertex.get_label()), default_state or
                               VizTracing.DEFAULT_STATE)

                for edge in vertex.get_edges():
                    found, default_state = False, None
                    for state in VizTracing.edge_states:
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
                VizTracing.path, VizTracing.IMAGE_NAME_PREFIX +
                ("{:04d}".format(VizTracing.snapshot_no))))
            VizTracing.snapshot_no += 1

    @classmethod
    def execute(cls, directed_graph: DirectedGraph, resource_path: str):
        """ Main function that takes a number of vertices
        (of a directed graph), invokes the cycle check functionality
        (which in turn creates the traced images), and converts the
        images to a video.

        Args:
            vertices(dict): a dictionar with vertices and for each vertex its
                destination vertices
            resource_path: the path that should contain the generated resources
        """

        pt.create_dir_in_user_home(resource_path)
        VizTracing.enable(
            pt.get_dir_in_user_home(resource_path),
            directed_graph,
            vertex_states=[
                        {VizTracing.ACTIVATED:
                            {"fillcolor": "red", "style": "filled"}},
                        {VizTracing.IN_CYCLE:
                            {"fillcolor": "blue", "style": "filled"}},
                        {VizTracing.VISISTED:
                            {"fillcolor": "gray", "style": "filled"}}],
            edge_states=[{VizTracing.DISABLED: {"color": "red"}}])


class VizTracingAdvisor(Advisor):
    """ Module that contains the logic for inserting advice at join points for
    visualization of the cyclic check algorithm
    """

    @classmethod
    def visit_vertex(cls, directed_graph, vertex):
        """ Function that is used to tag vertices with the state "visisted",
        if these vertices have been visited once. So next time, when another
        predecessor of a tagged vertex is being considered, it is skipped

        Args:
            directed_graph (DirectedGraph): The directed graph
            vertex: the vertex that should get the status "visited"

        """
        VizTracing.change_activated_vertex(directed_graph, vertex)
        VizTracing.set_status(
            directed_graph, vertex, VizTracing.VISISTED)
        VizTracing.snapshot()

    @classmethod
    def vertex_already_visited(cls, directed_graph, edge):
        """ Function that takes a snapshot after having disabled the
        edge. This is to indicate that the transition cannot be taken

        Args:
            directed_graph(DirectedGraph): The directed graph
            edge(Edge): the edge to be disabled
        """

        VizTracing.set_status(
            directed_graph, edge, VizTracing.DISABLED)
        VizTracing.snapshot()
        VizTracing.reset_status(
            directed_graph, edge, VizTracing.DISABLED)
        VizTracing.snapshot()
