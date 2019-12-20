""" Module that contains the definition of a directed graph as a class
"""

from pythonalgos.graph.vertex import Vertex
from pythonalgos.graph import kosaraju_sccs
from pythonalgos.graph import cyclic as cyclic
from copy import deepcopy
from pythonalgos.util.advisor import Advisor

class DirectedGraph(object):
    """ Class to represent directed graphs. https://en.wikipedia.org/wiki/Directed_graph """

    def __init__(self, vertices=None):
        """ Initialises a directed graph (with the provided vertices)

        Args:
            vertices(dict): a dict with the vertices and their tails in it

        """

        self._vertices = dict()        
        if vertices is not None:
            for label in vertices.keys():
                self.add_vertex(label)
            for label, heads in vertices.items():
                for head in heads:
                    self.add_edge(label, head)

    def copy(self):
        """ Copies the directed graph and returns it

        Returns:
            the copied directed graph
        """
        
        return deepcopy(self)

    def add_vertex(self, label):
        """ Adds a vertex to the dictionary of vertices 

        Args:
            label: a vertex represented by its label
        """

        if label in self._vertices:
            raise RuntimeError("vertex = '{}'".format(label) + 
                               " is already a vertex in this directed graph")
        self._vertices[label] = Vertex(label)

    def get_vertex(self, label):
        """ Returns the vertex that coincides with the label 

        Args:
            label: a vertex represented by its label

        Returns:
            Vertex: the requested vertex

        """

        return self._vertices[label]

    def get_vertices(self):
        """ Returns the vertices dictionary 

        Returns:
            self._vertices (dict)

        """

        return self._vertices
        
    def add_edge(self, tail, head):
        """ Adds an edge to the graph, the edge is identified by a tail and a head vertex

        Args:
            tail: the edge that represents the start vertex
            head: the edge that represents the destination vertex

        """

        if tail not in self._vertices or head not in self._vertices:
            raise RuntimeError("Destination or source of edge ('{}'".format(head) +
                                       ",'{}'".format(tail) + ") cannot be found as a vertex")
        else:
            self._vertices[tail].add_edge(self._vertices[head])
            self._vertices[head].increase_indegree()

    def get_vertices_count(self):
        return len(self._vertices)

    def __str__(self):
        res = ""
        for label in self._vertices:
            res += "\n" + str(label) + ": " + str(self._vertices[label])

        return res

    def get_reversed_graph(self):
        """ Function that returns the reverse of this graph  

        Args:
            directed_graph (DirectedGraph): The directed graph 

        Returns:
            DirectedGraph: The reversed graph

        """

        reversed = DirectedGraph()
        for i in self.get_vertices().keys():
            reversed.add_vertex(i)

        for i in self.get_vertices().keys():
            vertex = self.get_vertex(i)
            for j in vertex.get_heads():
                reversed.add_edge(j.get_label(), i)

        return reversed

    def create_sccs_kosaraju_dfs(self, nontrivial=True): 
        return kosaraju_sccs.create_sccs_kosaraju_dfs(self, nontrivial)

    def is_cyclic(self, advisor=Advisor()):
        """ Method that uses a helper module to check for cycles in the directed graph

        Args:
            advisor(Advisor): The class that implements the advice that is to be inserted
                at join points in the algorith. The default advice is empty
        
        """

        return cyclic.is_cyclic(self, advisor)
