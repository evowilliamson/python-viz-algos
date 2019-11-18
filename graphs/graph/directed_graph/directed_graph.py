""" Module that contains the definition of a directed graph as a class
"""

from graph.directed_graph.vertex import Vertex

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
                                       ",'{}'".format(tail) + ") cannot be found as vertices")
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

    # A function used by DFS 
    def visit_DFS(self, vertex, visited, scc): 
        # Mark the current node as visited 
        visited[vertex] = True
        scc.add(vertex)
        #Recur for all the vertices adjacent to this vertex 
        for i in self._vertices[vertex].get_tails(): 
            if not visited[i]: 
                self.visit_DFS(i, visited, scc) 

    def fill_order_DFS(self, vertex, visited, stack): 
        # Mark the current node as visited  
        visited[vertex] = True
        #Recur for all the vertices adjacent to this vertex 
        for i in self._vertices[vertex].get_tails(): 
            if not visited[i]: 
                self.fill_order_DFS(i, visited, stack) 
        stack = stack.append(vertex) 

    # Function that returns reverse of this graph 
    def get_reversed_graph(self): 

        reversed = DirectedGraph(None)
        # Recur for all the vertices adjacent to this vertex 

        for i in self._vertices.keys(): 
            reversed.add_vertex(i)

        for i in self._vertices.keys(): 
            vertex = self.get_vertex(i)
            for j in vertex.get_tails():
                reversed.add_edge(j, i) 
        return reversed 


    # The main function that finds and prints all strongly 
    # connected components 
    def create_SCCs(self): 

        stack = [] 
        scc = dict()

        visited = [False for i in range(self.get_vertices_count())]
        for i in range(self.get_vertices_count()): 
            if not visited[i]: 
                self.fill_order_DFS(i, visited, stack) 

        # Create a reversed graph 
        reversed_graph = self.get_reversed_graph() 
            
        # Mark all the vertices as not visited (For second DFS) 
        visited = [False for i in range(self.get_vertices_count())]

        # Now process all vertices in order defined by Stack 
        scc_id = 0
        while stack: 
            i = stack.pop() 
            if not visited[i]:
                scc[scc_id] = set() 
                reversed_graph.visit_DFS(i, visited, scc[scc_id]) 
                scc_id += 1

        return scc
