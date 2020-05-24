from typing import List
from pythonalgos.graph.vertex import Vertex
from pythonalgos.util import path_tools as pt
from pythonvizalgos.util import video_tools as vt
from pythonalgos.graph.directed_graph import DirectedGraph
from pythonvizalgos.graph.viz_tracing import VizTracing, VizTracingAdvisor


""" Module that defines a tracing class to be used for tracing of kosoraju
sccs algorithms in relation to directed graphs """


class VizSccsKosarajuTracing(VizTracing):
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

    SCC_IDX = "C"
    STACK_IDX = "S"

    label_attributes = [STACK_IDX, SCC_IDX]

    @classmethod
    def get_vertex_label_attributes(cls) -> List[str]:
        """ This classmethod retrieves the list of vertex label attributes
        of this class.

        """

        return VizSccsKosarajuTracing.label_attributes

    @classmethod
    def execute(cls, directed_graph: DirectedGraph, resource_path: str,
                nontrivial: bool = True) -> None:
        """ Main function that takes a number of vertices
        (of a directed graph), invokes the kosaraju sccs functionality
        (which in turn creates the traced images), and converts the images
        to a video.

        Args:
            vertices(dict): a dictionar with vertices and for each vertex its
                destination vertices
            resource_path: the path that should contain the generated resources
        """

        VizTracing.execute(directed_graph, resource_path)
        directed_graph.\
            create_sccs_kosaraju_dfs(nontrivial,
                                     VizSccsKosarajuTracingAdvisor())
        vt.convert_images_to_video(pt.get_dir_in_user_home(resource_path))


class VizSccsKosarajuTracingAdvisor(VizTracingAdvisor):
    """ Module that contains the logic for inserting advice at join points for
    visualization of the sccs kosaraju algorithm
    """

    @classmethod
    def add_vertex_to_stack(cls, directed_graph: DirectedGraph,
                            vertex: Vertex,
                            idx: int) -> None:
        """ Advice that adds the vertex to the stack.

        Args:
            directed_graph(DirectedGraph): The directed graph
            vertex: the vertex that should get the status
            idx: the index of the vertex in the stack

        """

        VizSccsKosarajuTracing.set_status(
            directed_graph, vertex, VizSccsKosarajuTracing.STACK_IDX, idx)
        VizSccsKosarajuTracing.snapshot()

    @classmethod
    def reverse_directed_graph(cls, directed_graph: DirectedGraph) -> None:
        """ Advice that handles the reversing of the directed graph

        Args:
            directed_graph(DirectedGraph): The directed graph
        """

        pass
