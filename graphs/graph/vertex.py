""" Module that contains the definition of a vertex
"""

class Vertex:
    """ Class to represent details about a vertex, being the indegree and the tails that are its successors """

    def __init__(self):
        self._indegree = 0
        self._tails = set() ## the edges of this vertex point to these other vertices (tails)

    def add_tail(self, tail):
        """ This method adds a tail to the set of tails maintained by the vertex

        Args: 
            tail: the tail to be added
        """

        self._tails.add(tail)

    def increase_indegree(self):
        """ This method increases the indegree for the incumbent vertex """
        self._indegree += 1

    def decrease_indegree(self):
        """ This method decreases the indegree for the incumbent vertex """
        self._indegree -= 1

    def get_indegree(self):
        return self._indegree

    def get_outdegree(self):
        return len(self._tails)

    def __str__(self):
        return  "\n   outdegree: {}".format(self.get_outdegree()) + \
                "\n   indegree: {}".format(self.get_indegree()) + \
                "\n   tails: " + str(self._tails)

    
