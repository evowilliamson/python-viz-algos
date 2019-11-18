from graph.directed_graph.directed_graph import DirectedGraph

class DirectedAcyclicGraph(DirectedGraph):

    def __init__(self, vertices):
        super().__init__(vertices)
        if super().is_cyclic():
            raise RuntimeError("Directed graph has a cycle")