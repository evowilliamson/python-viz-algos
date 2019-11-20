""" Module that contains the definition of a vertex in the context of a directed graph
"""

from graph.vertex import Vertex as GraphVertex

class Vertex(GraphVertex):
    """ Class to represent details about a vertex in the context of a directed graph, 
    being the indegree, outdegree and the tails that are its successors. It inherits from the 
    generic Vertex class
    """

    def __init__(self):
        """ Initialises the vertex by calling the __init__ of the parent
        """
        
        super().__init__()
        self._indegree = 0

    def add_tail(self, tail):
        """ This method adds a tail to the set of tails maintained by the vertex

        Args: 
            tail: the tail to be added

        """

        super().add_neighbour(tail)

    def get_tails(self):
        """ This method retrieves the tails from the vertex 
        """

        return super().get_neighbours()

    def increase_indegree(self):
        """ This method increases the indegree for the incumbent vertex """
        self._indegree += 1

    def decrease_indegree(self):
        """ This method decreases the indegree for the incumbent vertex """
        
        self._indegree -= 1

    def get_indegree(self):
        return self._indegree

    def get_outdegree(self):
        return len(self.get_tails())

    def __str__(self):
        return  "outdegree: {}".format(self.get_outdegree()) + \
                ", indegree: {}".format(self.get_indegree()) + \
                ", tails: " + str(super().get_neighbours())

    
