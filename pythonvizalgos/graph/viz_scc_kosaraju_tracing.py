from typing import List, Mapping, Set
from pythonalgos.graph.vertex import Vertex
from pythonalgos.util import path_tools as pt
from pythonvizalgos.util import video_tools as vt
from pythonalgos.graph.directed_graph import DirectedGraph
from pythonvizalgos.graph.viz_tracing_networkx import\
    VizTracingNetworkx
from pythonvizalgos.graph.viz_tracing import\
    VizTracingAdvisor
from pythonvizalgos.graph.viz_tracing import VizTracing


""" Module that defines a tracing class to be used for tracing of kosoraju
sccs algorithms in relation to directed graphs """


class VizSccsKosarajuTracing(VizTracingNetworkx):
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

    SCC_IDX = "C"
    STACK_IDX = "S"

    LABEL_ATTRIBUTES = [STACK_IDX, SCC_IDX]

    def get_vertex_label_attributes(self) -> List[str]:
        """ This classmethod retrieves the list of vertex label attributes
        of this class.

        """

        return VizSccsKosarajuTracing.LABEL_ATTRIBUTES

    def __init__(self, path: str, directed_graph: DirectedGraph,
                 vertex_states: List[Mapping[str, Mapping[str, str]]],
                 edge_states: List[Mapping[str, Mapping[str, str]]]) -> None:
        super().__init__(path=path, directed_graph=directed_graph,
                         vertex_states=vertex_states, edge_states=edge_states)
        self.check_states(vertex_states, edge_states)

    def check_states(self,
                     vertex_states: List[Mapping[str, Mapping[str, str]]],
                     edge_states: List[Mapping[str, Mapping[str, str]]]):
        """ This method checks whether the vertex states have the correct
        properties """

        if VizTracing.ACTIVATED not in vertex_states:
            raise Exception(
                VizTracing.ACTIVATED + " not found in vertex states")

        if VizTracing.VISITED not in vertex_states:
            raise Exception(
                VizTracing.VISITED + " not found in vertex states")

        if VizTracing.DEFAULT not in vertex_states:
            raise Exception(
                VizTracing.DEFAULT + " not found in vertex states")

    def execute(self, resource_path: str, nontrivial: bool):
        """ Method that takes a number of vertices
        (of a directed graph), invokes the kosaraju sccs functionality
        (which in turn creates the traced images), and converts the images
        to a video.

        Args:
            vertices(dict): a dictionar with vertices and for each vertex its
                destination vertices
            resource_path: the path that should contain the generated resources
        """

        super().execute(resource_path)
        self.get_directed_graph().\
            create_sccs_kosaraju_dfs(
                nontrivial, VizSccsKosarajuTracingAdvisor(self))


class VizSccsKosarajuTracingAdvisor(VizTracingAdvisor):
    """ Module that contains the logic for inserting advice at join points for
    visualization of the sccs kosaraju algorithm
    """

    def add_vertex_to_stack(self, directed_graph: DirectedGraph,
                            vertex: Vertex,
                            idx: int) -> None:
        """ Advice that adds the vertex to the stack.

        Args:
            directed_graph(DirectedGraph): The directed graph
            vertex: the vertex that should get the status
            idx: the index of the vertex in the stack
        """

        self.viz_tracing.set_status(vertex, VizSccsKosarajuTracing.STACK_IDX,
                                    idx)
        self.viz_tracing.snapshot(directed_graph)

    def reverse_directed_graph(self, directed_graph: DirectedGraph) -> None:
        """ Advice that handles the reversing of the directed graph.
        Basically resetting the whole graph, clearing all stastusses

        Args:
            directed_graph(DirectedGraph): The directed graph
        """

        self.viz_tracing.reset_attrs(directed_graph)
        self.viz_tracing.activate_graph(directed_graph)
        self.viz_tracing.snapshot(directed_graph)
        self.viz_tracing.deactivate_graph(directed_graph)
        self.viz_tracing.snapshot(directed_graph)
