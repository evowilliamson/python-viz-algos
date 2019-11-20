""" Module that contains the definition of a directed acyclic graph 
"""

from graph.directed_graph.directed_graph import DirectedGraph

class DirectedAcyclicGraph(DirectedGraph):
    """ Class to represent a directed acyclic graph. It inherits from DirectedGraph  
    """

    def __init__(self, vertices):
        """ Initializer that calls the super() initializer and then performs the cyclic test to 
        check whether it is a directed acyclic graph

        """

        super().__init__(vertices)
        if super().is_cyclic():
            raise RuntimeError("Directed graph has a cycle")