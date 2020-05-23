from pythonalgos.util import path_tools as pt
from pythonvizalgos.util import video_tools as vt
from pythonalgos.graph.directed_graph import DirectedGraph
from pythonvizalgos.graph.viz_tracing import VizTracing, VizTracingAdvisor


""" Module that defines a tracing class to be used for tracing of cyclic
algorithms in relation to directed graphs """


class VizCyclicTracing(VizTracing):
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
                        {VizCyclicTracing.VISISTED:
                            {"fillcolor":"gray", "style": "filled"}}])

    VizCyclicTracing.ACTIVATED takes precedence over VizCyclicTracing.IN_CYCLE
    takes predecence over VizCyclicTracing.VISITED by definition of the list

    """

    @classmethod
    def execute(cls, directed_graph: DirectedGraph, resource_path: str):
        """ Main function that takes a number of vertices
        (of a directed graph), invokes the cycle check functionality
        (which in turn creates the traced images), and converts the images
        to a video.

        Args:
            vertices(dict): a dictionar with vertices and for each vertex its
                destination vertices
            resource_path: the path that should contain the generated resources
        """

        VizTracing.execute(directed_graph, resource_path)
        directed_graph.is_cyclic(VizCyclicTracingAdvisor())
        vt.convert_images_to_video(pt.get_dir_in_user_home(resource_path))


class VizCyclicTracingAdvisor(VizTracingAdvisor):
    """ Module that contains the logic for inserting advice at join points for
    visualization of the cyclic check algorithm
    """

    @classmethod
    def cycle_reported_recursive(cls, directed_graph, vertex):
        """ Function that is used along the way back from the origin
        of the cycle detection to the initial state. Along the way,
        all vertices are tagged with the state in_cycle

        Args:
            directed_graph (DirectedGraph): The directed graph
            vertex: the vertex that should get the status activated

        """

        VizCyclicTracing.set_status(
            directed_graph, vertex, VizCyclicTracing.IN_CYCLE)
        VizCyclicTracing.change_activated_vertex(directed_graph, vertex)
        VizCyclicTracing.snapshot()

    @classmethod
    def cycle_found(cls, directed_graph, tail, head):
        """ Changes the state of a vertex when the vertex is part of a cycle

        Args:
            directed_graph (DirectedGraph): The directed graph
            tail: the tail vertex that should get the status activated
            head: the head vertex that should get the in_cycle status

        """

        VizCyclicTracing.set_status(
            directed_graph, head, VizCyclicTracing.IN_CYCLE)
        VizCyclicTracing.change_activated_vertex(directed_graph, head)
        VizCyclicTracing.snapshot()

    @classmethod
    def no_cycle_reported_recursive(cls, directed_graph, vertex):
        """ Changes focus to the vertex and takes a snapshot

        Args:
            directed_graph(DirectedGraph): The directed graph
            vertex: the vertex that should get the status activated

        """

        VizCyclicTracing.change_activated_vertex(directed_graph, vertex)
        VizCyclicTracing.snapshot()

