from pythonvizalgos.graph.viz_tracing import VizTracingAdvisor
from typing import List, Mapping
from pythonalgos.graph.vertex import Vertex
from pythonalgos.util import path_tools as pt
from pythonvizalgos.util import video_tools as vt
from pythonalgos.graph.directed_graph import DirectedGraph
from pythonvizalgos.graph.viz_tracing_graphviz import\
    VizTracingGraphviz
from pythonvizalgos.graph.viz_tracing import VizTracingAdvisor


""" Module that defines a tracing class to be used for tracing of cyclic
algorithms in relation to directed graphs """


class VizCyclicTracing(VizTracingGraphviz):

    IN_CYCLE: str = "in_cycle"

    """ Class that is accessed in a static way. It contains functions for
    tracing cyclic algorithms in relation to directed graphs

    states structure:

    [ {"some_state": {**args} ..., {"default": {**args} ]

    For example:
        vertex_states=[
                        {VizCyclicTracing.ACTIVATED:
                            {"fillcolor":"red", "style": "filled"}},
                        {VizCyclicTracing.IN_CYCLE:
                            {"fillcolor":"blue", "style": "filled"}},
                        {VizCyclicTracing.VISITED:
                            {"fillcolor":"gray", "style": "filled"}}])

    VizCyclicTracing.ACTIVATED takes precedence over VizCyclicTracing.IN_CYCLE
    takes predecence over VizCyclicTracing.VISITED by definition of the list
    """

    def __init__(self, path: str, directed_graph: DirectedGraph,
                 vertex_states: List[Mapping[str, Mapping[str, str]]] = None,
                 edge_states: List[Mapping[str, Mapping[str, str]]] = None) \
            -> None:
        super().__init__(path=path, directed_graph=directed_graph,
                         vertex_states=vertex_states, edge_states=edge_states)

    def execute(self, resource_path: str):
        """ Main function that takes a number of vertices
        (of a directed graph), invokes the cycle check functionality
        (which in turn creates the traced images), and converts the images
        to a video.

        Args:
            vertices(dict): a dictionar with vertices and for each vertex its
                destination vertices
            resource_path: the path that should contain the generated resources
        """

        super().execute(resource_path)
        self.get_directed_graph().is_cyclic(VizCyclicTracingAdvisor(self))
        vt.convert_images_to_video(pt.get_dir_in_user_home(resource_path))


class VizCyclicTracingAdvisor(VizTracingAdvisor):
    """ Module that contains the logic for inserting advice at join points for
    visualization of the cyclic check algorithm
    """

    def __init__(self, viz_tracing: VizTracingGraphviz):
        super().__init__(viz_tracing)

    def cycle_reported_recursive(self, directed_graph: DirectedGraph,
                                 vertex: Vertex) -> None:
        """ Function that is used along the way back from the origin
        of the cycle detection to the initial state. Along the way,
        all vertices are tagged with the state in_cycle

        Args:
            directed_graph (DirectedGraph): The directed graph
            vertex: the vertex that should get the status activated
        """

        self.viz_tracing.set_status(vertex, VizCyclicTracing.IN_CYCLE)
        self.viz_tracing.change_activated_vertex(directed_graph, vertex)
        self.viz_tracing.snapshot(directed_graph)

    def cycle_found(self, directed_graph: DirectedGraph, tail: Vertex,
                    head: Vertex) -> None:
        """ Changes the state of a vertex when the vertex is part of a cycle

        Args:
            directed_graph (DirectedGraph): The directed graph
            tail: the tail vertex that should get the status activated
            head: the head vertex that should get the in_cycle status
        """

        self.viz_tracing.set_status(head, VizCyclicTracing.IN_CYCLE)
        self.viz_tracing.change_activated_vertex(directed_graph, head)
        self.viz_tracing.snapshot(directed_graph)

    def no_cycle_reported_recursive(self, directed_graph: DirectedGraph,
                                    vertex: Vertex) -> None:
        """ Changes focus to the vertex and takes a snapshot

        Args:
            directed_graph(DirectedGraph): The directed graph
            vertex: the vertex that should get the status activated

        """

        self.viz_tracing.change_activated_vertex(directed_graph, vertex)
        self.viz_tracing.snapshot(directed_graph)
