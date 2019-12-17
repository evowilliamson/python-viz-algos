from util.logging import Logging
from graph.directed_graph.viz_tracing import VizTracing


def is_cyclic(directed_graph):
    """ Function that checks whether a directed graph contains a cycle or not

    Args:
        directed_graph (DirectedGraph): The directed graph

    Returns:
        bool: True if the directed graph contains a cycle, otherwise False

    """

    Logging.log("\nStarting cycle check")
    traversed_already = dict()
    in_cycle = {i:False for i in directed_graph.get_vertices().keys()}
    for label, vertex in directed_graph.get_vertices().items():
        if traversed_already.get(label) is None:
            if _is_cyclic_dfs(directed_graph, vertex, traversed_already, in_cycle):
                return True

    return False

def _is_cyclic_dfs(directed_graph, vertex, traversed_already, in_cycle):
    """ Function that recursively searches the directed graph depth first and checks
    if a vertex was already in_cycle before. 

    It checks all vertices that have not been traversed before. The heads of those 
    vertices are followed. If in that traversal, a vertex is found that is present in 
    the dict "in_cycle" with a value of true, then a cycle is present

    Args:
        directed_graph (DirectedGraph): The directed graph 
        vertex(Vertex): The current vertex
        traversed_already (dict): A dictionary that maintains whether vertices have been 
            traversed already. It's a performance measure put in place in order to shortcut 
            processing if a vertex was already processed by another subtree
        in_cycle (list): A list that, if a vertex has been found to part be part of cycle,
            for that vertex, has a value of true. If that vertex is not part of a cycle, it's
            value is false

    Returns:
        bool: True if the vertex was in_cycle before, False otherwise

    """

    traversed_already[vertex.get_label()] = True
    in_cycle[vertex.get_label()] = True
    viztrace_visit_tail(directed_graph, vertex)

    for edge in vertex.get_edges():
        if traversed_already.get(edge.get_head().get_label()) is None:
            if _is_cyclic_dfs(directed_graph, edge.get_head(), traversed_already, in_cycle):
                viztrace_cycle_reported(directed_graph, edge.get_head())
                return True
            else:
                viztrace_vertex(directed_graph, vertex)
        elif in_cycle[edge.get_head().get_label()]:
            viztrace_cycle_found(directed_graph, vertex, edge.get_head())
            return True
        elif traversed_already.get(edge.get_head().get_label()):
            viztrace_already_traversed(directed_graph, edge)

    in_cycle[vertex.get_label()] = False
    return False


def viztrace_cycle_reported(directed_graph, vertex):
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


def viztrace_visit_tail(directed_graph, vertex):
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


def viztrace_cycle_found(directed_graph, tail, head):
    """ Changes the state of a vertex when the vertex is part of a cycle

    Args:
        directed_graph (DirectedGraph): The directed graph
        tail: the tail vertex that should get the status activated
        head: the head vertex that should get the in_cycle status

    """
        
    VizTracing.set_status(directed_graph, head, VizTracing.IN_CYCLE)
    VizTracing.change_activated_vertex(directed_graph, head)    
    VizTracing.snapshot()


def viztrace_vertex(directed_graph, vertex):
    """ Changes focus to the vertex and takes a snapshot

    Args:
        directed_graph(DirectedGraph): The directed graph
        vertex: the vertex that should get the status activated

    """

    VizTracing.change_activated_vertex(directed_graph, vertex)
    VizTracing.snapshot()


def viztrace_already_traversed(directed_graph, edge):
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

