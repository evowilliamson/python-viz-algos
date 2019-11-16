from graph.directed_graph.directed_graph_helper import DirectedGraphHelper
from graph.directed_graph.directed_graph import DirectedGraph

class DirectedAcyclicGraph(DirectedGraph):

    def __init__(self, vertices):
        super().__init__(vertices)
        self.a = 100
