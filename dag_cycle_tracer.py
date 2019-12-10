from graph.directed_graph.viz_tracing import VizTracing
from util.logging import Logging
import util.path_tools as pt
from graph.directed_graph.directed_graph import DirectedGraph

print("hellloooo")
if __name__ == '__main__':

    RESOURCES_PATH = "python-resources"
    vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [7, 8] ,6:[7, 8, 9], 
                         7: [9, 10, 11], 8: [11, 12], 9: [10, 11], 
                         10: [11], 11: [12], 12: [6]}
    directed_graph = DirectedGraph(vertices)
    pt.create_dir_in_user_home(RESOURCES_PATH)
    VizTracing.enable(
        pt.get_dir_in_user_home(RESOURCES_PATH), 
        directed_graph,
        vertex_states=[
                    {VizTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                    {VizTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}},
                    {VizTracing.IN_CYCLE: {"fillcolor":"gray", "style": "filled"}}])
    directed_graph.is_cyclic()