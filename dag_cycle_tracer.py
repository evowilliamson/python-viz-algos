from os import path
from graph.directed_graph.viz_tracing import VizTracing
from util.logging import Logging
import util.path_tools as pt
from graph.directed_graph.directed_graph import DirectedGraph

RESOURCES_PATH = "python-resources"

def init():
    pt.clean_dir_in_user_home(RESOURCES_PATH)
    pt.create_dir_in_user_home(RESOURCES_PATH)

def viztrace_log_finish(directed_graph):
    starting_vertex = next(iter(directed_graph.get_vertices().items()))[1]
    VizTracing.change_activated_vertex(directed_graph, starting_vertex)    
    VizTracing.snapshot()

def viztrace(vertices, resource_path):
    directed_graph = DirectedGraph(vertices)
    work_path = path.join(RESOURCES_PATH, resource_path)
    pt.create_dir_in_user_home(work_path)
    VizTracing.enable(
        pt.get_dir_in_user_home(work_path), 
        directed_graph,
        vertex_states=[
                    {VizTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                    {VizTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}},
                    {VizTracing.VISISTED: {"fillcolor":"gray", "style": "filled"}}])
    directed_graph.is_cyclic()
    viztrace_log_finish(directed_graph)

def viztrace_cycle():
    viztrace({0: [1], 1: [2], 2: [3],
              3: [4, 11], 4: [5], 5:[6], 6:[7, 8], 7: [], 8: [9], 9: [10], 10:[],
              11: [12], 12: [13], 13:[14], 14:[3]}, "cycle")


def viztrace_no_cycle():
    viztrace({0: [1], 1: [2], 2: [3],
              3: [4, 11], 4: [5], 5:[6], 6:[7, 8], 7: [], 8: [9], 9: [10], 10:[],
              11: [12], 12: [13, 8], 13:[14], 14:[]}, "no_cycle")
    

if __name__ == '__main__':
    init()
    viztrace_cycle()
    viztrace_no_cycle()

