""" Module that contains the logic for inserting advice at join points for visualization
of the cyclic check algorithm
"""
from graph.viz_cyclic_tracing import VizCyclicTracing
from pythonalgos.util.advisor import Advisor

class VizCyclicTracingAdvisor(Advisor):

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
        VizCyclicTracing.set_status(directed_graph, vertex, VizCyclicTracing.IN_CYCLE)
        VizCyclicTracing.change_activated_vertex(directed_graph, vertex)    
        VizCyclicTracing.snapshot()


    def visit_vertex(self, directed_graph, vertex):
        """ Function that is used to tag vertices with the state "visisted", 
        if these vertices have been visited once. So next time, when another predecessor
        of a tagged vertex is being considered, it is skipped

        Args:
            directed_graph (DirectedGraph): The directed graph
            vertex: the vertex that should get the status "visited"

        """
        VizCyclicTracing.change_activated_vertex(directed_graph, vertex)
        VizCyclicTracing.set_status(directed_graph, vertex, VizCyclicTracing.VISISTED)
        VizCyclicTracing.snapshot()


    def cycle_found(self, directed_graph, tail, head):
        """ Changes the state of a vertex when the vertex is part of a cycle

        Args:
            directed_graph (DirectedGraph): The directed graph
            tail: the tail vertex that should get the status activated
            head: the head vertex that should get the in_cycle status

        """
            
        VizCyclicTracing.set_status(directed_graph, head, VizCyclicTracing.IN_CYCLE)
        VizCyclicTracing.change_activated_vertex(directed_graph, head)    
        VizCyclicTracing.snapshot()


    def no_cycle_reported_recursive(self, directed_graph, vertex):
        """ Changes focus to the vertex and takes a snapshot

        Args:
            directed_graph(DirectedGraph): The directed graph
            vertex: the vertex that should get the status activated

        """

        VizCyclicTracing.change_activated_vertex(directed_graph, vertex)
        VizCyclicTracing.snapshot()


    def vertex_already_visited(self, directed_graph, edge):
        """ Function that takes a snapshot after having disabled the
        edge. This is to indicate that the transition cannot be taken

        Args:
            directed_graph(DirectedGraph): The directed graph
            edge(Edge): the edge to be disabled
        """

        VizCyclicTracing.set_status(directed_graph, edge, VizCyclicTracing.DISABLED)
        VizCyclicTracing.snapshot()
        VizCyclicTracing.reset_status(directed_graph, edge, VizCyclicTracing.DISABLED)
        VizCyclicTracing.snapshot()    

