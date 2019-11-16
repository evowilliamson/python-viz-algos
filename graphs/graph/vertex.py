""" Module that contains the definition of a vertex
"""

class Vertex:

    def __init__(self):
        self._indegree = 0
        self._tails = set() ## the edges of this vertex point to these other vertices (tails)

    def increase_indegree(self):
        self._indegree += 1

    def decrease_indegree(self):
        self._indegree -= 1

    def get_indegree(self):
        return self._indegree

    def get_outdegree(self):
        return len(self._tails)

    def __str__(self):
        return "outdegree: {}".format(self.get_outdegree()) + ", indegree: {}".format(self.get_indegree()) + ", tails: " + str(self._tails)

    
