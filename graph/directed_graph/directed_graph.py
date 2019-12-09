""" Module that contains the definition of a directed graph as a class
"""

from graph.directed_graph.vertex import Vertex
import graph.directed_graph.directed_graph_helper as directed_graph_helper
from graphviz import Digraph
from copy import deepcopy


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

    def render(self, file_name="digraph", view_type=False, format="pdf"):
        """ Renders the directed with the Graphviz library

        Args: 
            file_name(str): path and file for the file to be generated
            view_type(bool): True if the attached program for the file is to be started on

        """ 

        graph = Digraph(format=format)
        for label, vertex in self._vertices.items():
            for head in vertex.get_heads():
                graph.edge(str(label), str(head.get_label()))

        graph.render(file_name, view=view_type)


    def __str__(self):
        res = ""
        for label in self._vertices:
            res += "\n" + str(label) + ": " + str(self._vertices[label])

        return res

    """
    The following methods call functions in the "directed_graph_helper" module. These functions
    were moved from this class to a separate module in order to keep the class lean
    """

    def create_sccs_kosaraju_dfs(self, nontrivial=True): 
        return directed_graph_helper.create_sccs_kosaraju_dfs(self, nontrivial)

    def get_reversed_graph(self):
        return directed_graph_helper.get_reversed_graph(self)

    def is_cyclic(self):
        return directed_graph_helper.is_cyclic(self)
