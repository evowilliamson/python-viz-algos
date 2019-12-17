""" Module that contains the logic for inserting advice at join points for visualization
of the cyclic check algorithm
"""

from graph.directed_graph.viz_tracing import VizTracing
from util.advisor import Advisor

class VizTracingAdvisor(Advisor):

    def __init__(self):
        super().__init__()

    def cycle_reported_recursive(self, directed_graph, vertex):
        """ Function that is used along the way back from the origin
        of the cycle detection to the initial state. Along the way,
        all vertices are tagged with the state in_cycle

        Args:
            directed_graph (DirectedGraph): The directed graph
            vertex: the vertex that should get the status activated

        """    
        VizTracing.set_status(directed_graph, vertex, VizTracing.IN_CYCLE)
        VizTracing.change_activated_vertex(directed_graph, vertex)    
        VizTracing.snapshot()


    def visit_vertex(self, directed_graph, vertex):
        """ Function that is used to tag vertices with the state "visisted", 
        if these vertices have been visited once. So next time, when another predecessor
        of a tagged vertex is being considered, it is skipped

        Args:
            directed_graph (DirectedGraph): The directed graph
            vertex: the vertex that should get the status "visited"

        """
        VizTracing.change_activated_vertex(directed_graph, vertex)
        VizTracing.set_status(directed_graph, vertex, VizTracing.VISISTED)
        VizTracing.snapshot()


    def cycle_found(self, directed_graph, tail, head):
        """ Changes the state of a vertex when the vertex is part of a cycle

        Args:
            directed_graph (DirectedGraph): The directed graph
            tail: the tail vertex that should get the status activated
            head: the head vertex that should get the in_cycle status

        """
            
        VizTracing.set_status(directed_graph, head, VizTracing.IN_CYCLE)
        VizTracing.change_activated_vertex(directed_graph, head)    
        VizTracing.snapshot()


    def no_cycle_reported_recursive(self, directed_graph, vertex):
        """ Changes focus to the vertex and takes a snapshot

        Args:
            directed_graph(DirectedGraph): The directed graph
            vertex: the vertex that should get the status activated

        """

        VizTracing.change_activated_vertex(directed_graph, vertex)
        VizTracing.snapshot()


    def vertex_already_visited(self, directed_graph, edge):
        """ Function that takes a snapshot after having disabled the
        edge. This is to indicate that the transition cannot be taken

        Args:
            directed_graph(DirectedGraph): The directed graph
            edge(Edge): the edge to be disabled
        """

        VizTracing.set_status(directed_graph, edge, VizTracing.DISABLED)
        VizTracing.snapshot()
        VizTracing.reset_status(directed_graph, edge, VizTracing.DISABLED)
        VizTracing.snapshot()    

