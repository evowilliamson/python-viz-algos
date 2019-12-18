import os
import sys
""" This python file is being run as main, so packages don't exist. Append the root path
of the project """
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(root_dir)
import cv2
from graph.viz_cyclic_tracing import VizCyclicTracing
from pythonalgos.util.logging import Logging
from pythonalgos.util import path_tools as pt
from util import video_tools as vt
from pythonalgos.graph.directed_graph import DirectedGraph
from main_runners.viz_tracing_advisor import VizCyclicTracingAdvisor

RESOURCES_PATH = "python-resources"

""" This module should be run as a python script. It generates videos for both 
cases, first case being a directed graph containing a cycle, and the other case
where not a cycle is present
"""

def init():
    """ Cleans and creates again the target directory 
    """

    pt.clean_dir_in_user_home(RESOURCES_PATH)
    pt.create_dir_in_user_home(RESOURCES_PATH)

def viztrace_log_finish(directed_graph):
    """ Viz traces the first vertex 

    Args:
        directed_graph(DirectedGraph): the directed graph in question

    """

    starting_vertex = next(iter(directed_graph.get_vertices().items()))[1]
    VizCyclicTracing.change_activated_vertex(directed_graph, starting_vertex)    
    VizCyclicTracing.snapshot()

def viztrace(vertices, resource_path):
    """ Main function that takes a number of vertices (of a directed graph),
    invokes the cycle check functionality (which in turn creates the traced images),
    and converts the images to a video
    
    Args:
        vertices(dict): a dictionar with vertices and for each vertex its destination
            vertices
        resource_path: the path that should contain the generated resources

    """

    directed_graph = DirectedGraph(vertices)
    work_path = os.path.join(RESOURCES_PATH, resource_path)
    pt.create_dir_in_user_home(work_path)
    VizCyclicTracing.enable(
        pt.get_dir_in_user_home(work_path), 
        directed_graph,
        vertex_states=[
                    {VizCyclicTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                    {VizCyclicTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}},
                    {VizCyclicTracing.VISISTED: {"fillcolor":"gray", "style": "filled"}}],
        edge_states=[{VizCyclicTracing.DISABLED: {"color":"red"}}])
    directed_graph.is_cyclic(VizCyclicTracingAdvisor())
    viztrace_log_finish(directed_graph)
    vt.convert_images_to_video(pt.get_dir_in_user_home(work_path))
   

def viztrace_cycle():
    """ Function that performs the tracing for a directed graph with a cycle
    """

    viztrace({0: [1], 1: [2], 2: [3],
              3: [4, 11], 4: [5], 5:[6], 6:[7, 8], 7: [], 8: [9], 9: [10], 10:[],
              11: [12], 12: [13], 13:[14], 14:[3]}, "cycle")


def viztrace_no_cycle():
    """ Function that performs the tracing for a directed graph without a cycle
    """
    viztrace({0: [1], 1: [2], 2: [3],
              3: [4, 11], 4: [5], 5:[6], 6:[7, 8], 7: [], 8: [9], 9: [10], 10:[],
              11: [12], 12: [8, 13], 13:[14], 14:[]}, "no_cycle")
    

if __name__ == '__main__':
    init()
    viztrace_cycle()
    viztrace_no_cycle()


