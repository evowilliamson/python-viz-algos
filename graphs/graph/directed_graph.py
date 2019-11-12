""" Module that contains the definition of a directed graph as a class
"""

class DirectedGraph(object):
    """ Class to represent directed graphs. https://en.wikipedia.org/wiki/Directed_graph """
    

    def __init__(self, vertices=None, edges=None):
        """ Initialises a directed graph

        Args:
            vertices(set): a set of vertices
            edges(set): a set of edges

        """

        self._vertices = dict()
        if vertices is not None:
            for vertex in vertices:
                self._vertices[vertex] = set()

        if edges is not None:
            for source, destination in edges:
                self.add_edge(source, destination)

    def add_vertex(self, vertex):
        """ Adds a vertex to the dictionary of vertices 

        Args:
            vertex: a vertex
        """

        if vertex in self._vertices:
            raise RuntimeError("vertex = '{}'".format(vertex) + 
                               "is already a vertex in this directed graph")
        self._vertices[vertex] = set()

    def add_edge(self, source, destination):
        """ Adds an edge to the graph

        Args:
            source: the edge that represents the source
            destination: the edge that represents the destination
        """

        if source not in self._vertices or destination not in self._vertices:
            raise RuntimeError("Destination or source of edge ('{}'".format(source) +
                                       ",'{}'".format(destination) + ") cannot be found as vertices")
        else:
            self._vertices[source].add(destination)

    def vertices_count(self):
        return len(self._vertices)

