""" Module that contains the definition of a vertex in a generic graph
"""

class Vertex:
    """ Class to represent details about a vertex in a generic graph """

    def __init__(self):
        self._neighbours = set() ## the edges of this vertex point to these other vertices (tails)

    def add_neighbour(self, neighbour):
        """ This method adds a neighbour to the set of tails maintained by the vertex

        Args: 
            neighbour: the neighbour to be added
        """

        self._neighbours.add(neighbour)

    def get_neighbours(self):
        """ This method retrieves the tails from the vertex """

        return self._neighbours

    def __str__(self):
        return "neighbours: " + str(self._neighbours)

    
