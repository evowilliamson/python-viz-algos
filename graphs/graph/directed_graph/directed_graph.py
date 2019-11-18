""" Module that contains the definition of a directed graph as a class
"""

from graph.directed_graph.vertex import Vertex
import graph.directed_graph.directed_graph_helper as dg_helper

class DirectedGraph(object):
    """ Class to represent directed graphs. https://en.wikipedia.org/wiki/Directed_graph """

    def __init__(self, vertices):
        """ Initialises a directed graph with the provided vertices

        Args:
            directed_graph: an initialised directe graph to be used

        """

        self._vertices = dict()        
        if vertices is not None:
            for label in vertices.keys():
                self.add_vertex(label)
            for label, tails in vertices.items():
                for tail in tails:
                    self.add_edge(label, tail)

    def create_new(self, vertices):
        return DirectedGraph(vertices)

    def add_vertex(self, label):
        """ Adds a vertex to the dictionary of vertices 

        Args:
            label: a vertex represented by its label
        """

        if label in self._vertices:
            raise RuntimeError("vertex = '{}'".format(label) + 
                               " is already a vertex in this directed graph")
        self._vertices[label] = Vertex()

    def get_vertex(self, label):
        """ Returns the vertex that coincides with the label """

        return self._vertices[label]

    def add_edge(self, head, tail):
        """ Adds an edge to the graph, the edge is identified by a head and a tail vertex

        Args:
            head: the edge that represents the start vertex
            tail: the edge that represents the destination vertex
        """

        if head not in self._vertices or tail not in self._vertices:
            raise RuntimeError("Destination or source of edge ('{}'".format(head) +
                                       ",'{}'".format(tail) + ") cannot be found as a vertex")
        else:
            self._vertices[head].add_tail(tail)
            self._vertices[tail].increase_indegree()

    def get_vertices_count(self):
        return len(self._vertices)

    def __str__(self):
        res = ""
        for label in self._vertices:
            res += "\n" + str(label) + ": " + str(self._vertices[label])

        return res

    # The main function that finds and prints all strongly 
    # connected components 
    def create_SCCs(self): 
        return dg_helper.create_SCCs(self)

    def get_reversed_graph(self):
        return dg_helper.get_reversed_graph(self)

    def is_cyclic(self):
        return dg_helper.is_cyclic(self)
