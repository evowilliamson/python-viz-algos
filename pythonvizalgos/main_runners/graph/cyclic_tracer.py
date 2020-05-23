import os
import sys
from typing import List, Mapping, Any
from pythonalgos.graph.algorithm_ordering import AlgorithmOrdering
from pythonalgos.util import path_tools as pt
from pythonvizalgos.util import video_tools as vt
from pythonvizalgos.graph.viz_cyclic_tracing import VizCyclicTracing
from pythonalgos.graph.directed_graph import DirectedGraph
from pythonvizalgos.main_runners.graph.advisors.viz_tracing_advisor \
    import VizCyclicTracingAdvisor

RESOURCES_PATH = "python-resources"

""" Class that contains static methods to group together logic that pertains to the
visualization of cycles in directed graphs """


class CyclicTracer:

    @staticmethod
    def execute(vertices: Mapping[Any, List[Any]], resource_path: str):
        """ Main function that takes a number of vertices (of a directed graph),
        invokes the cycle check functionality (which in turn creates the traced
        images), and converts the images to a video

        Args:
            vertices(dict): a dictionar with vertices and for each vertex its
                destination vertices
            resource_path: the path that should contain the generated resources
        """

        directed_graph = DirectedGraph(
            vertices, algorithm_ordering=AlgorithmOrdering.ASC)
        work_path = os.path.join(RESOURCES_PATH, resource_path)
        pt.create_dir_in_user_home(work_path)
        VizCyclicTracing.enable(
            pt.get_dir_in_user_home(work_path),
            directed_graph,
            vertex_states=[
                        {VizCyclicTracing.ACTIVATED:
                            {"fillcolor": "red", "style": "filled"}},
                        {VizCyclicTracing.IN_CYCLE:
                            {"fillcolor": "blue", "style": "filled"}},
                        {VizCyclicTracing.VISISTED:
                            {"fillcolor": "gray", "style": "filled"}}],
            edge_states=[{VizCyclicTracing.DISABLED: {"color": "red"}}])
        directed_graph.is_cyclic(VizCyclicTracingAdvisor())
        vt.convert_images_to_video(pt.get_dir_in_user_home(work_path))
