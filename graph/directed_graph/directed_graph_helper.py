from util.logging import Logging
import graph.directed_graph.kosaraju_helper as kh
from graph.directed_graph.viz_tracing import VizTracing

""" Helper module for DirectedGraph class
"""


def create_sccs_kosaraju_dfs(directed_graph, nontrivial):
    """ Function that creates a list of strongly connected components according to 
    Kosaraju's algorithm (https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm) with a
    depth-first-search approach.

    Args: 
        directed_graph (DirectedGraph): The directed graph for which the SCCS should be calculated
        nontrivial(bool): If True, only nontrivial sccs will be returned, otherwise all sccs

    Returns:
        list(set()) of SCCs: Each SCC is a set of vertices

    """

    Logging.log("\nStarting")
    stack = []
    sccs_trivial, visited = list(), dict()
    for vertex in directed_graph.get_vertices().keys():
        if visited.get(vertex) is None:
            Logging.log("Vertex {0} not visited, go deep", vertex)
            kh.fill_order_dfd_sccs(directed_graph, vertex, visited, stack)
        else:
            Logging.log("Vertex {0} already visited, skipping", vertex)

    reversed_graph = get_reversed_graph(directed_graph)

    visited = dict()
    for i in reversed(stack):
        if visited.get(i) is None:
            sccs_trivial.append(set())
            kh.visit_dfs_sccs(reversed_graph, i, visited, sccs_trivial[-1])

    if nontrivial:
        return filter_nontrivial(sccs_trivial, directed_graph)
    else:
        return sccs_trivial


def filter_nontrivial(sccs_trivial, directed_graph):
    """ This function filters out the trivial sccs

    A scc is nontrivial, iff there are at least two vertices in it, 
    or there is only one vertex with a self-loop. A self-loop means
    that the indegree and the outdegree are both 1 and the tail is equal
    to the head

    Args:
        sccs_trivial(list): The list of trivial sccs
        directed_graph(DirectedGraph): The directed graph

    Returns:
        sccs_nontrivial(list): The list of nontrivial sccs

    """

    sccs_non_trivial = list()
    for scc in sccs_trivial:
        vertex = directed_graph.get_vertex(list(scc)[0])
        if (len(scc) >= 2) or \
            (len(scc) == 1 and vertex.get_indegree() == 1 and
            vertex.get_outdegree() == 1) and list(vertex.get_heads())[0] == list(scc)[0]:
            sccs_non_trivial.append(scc)

    return sccs_non_trivial


def get_reversed_graph(directed_graph):
    """ Function that returns the reverse of this graph  

    Args:
        directed_graph (DirectedGraph): The directed graph 

    Returns:
        DirectedGraph: The reversed graph

    """

    reversed = directed_graph.__class__()
    for i in directed_graph.get_vertices().keys():
        reversed.add_vertex(i)

    for i in directed_graph.get_vertices().keys():
        vertex = directed_graph.get_vertex(i)
        for j in vertex.get_heads():
            reversed.add_edge(j.get_label(), i)

    return reversed


def is_cyclic_dfs(directed_graph, vertex, traversed_already, in_cycle):
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

    Logging.inc_indent()
    for head in vertex.get_heads():
        Logging.log("Vertex {0}, head {1}", vertex.get_label(), head.get_label())
        if traversed_already.get(head.get_label()) is None:
            Logging.log("Head {0} not yet traversed", head.get_label())
            if is_cyclic_dfs(directed_graph, head, traversed_already, in_cycle):
                viztrace_log_cycle_reported(directed_graph, head)
                return True
            else:
                VizTracing.change_activated_vertex(directed_graph, vertex)
                VizTracing.snapshot()
        elif in_cycle[head.get_label()]:
            viztrace_log_cycle_found(directed_graph, vertex, head)
            return True
        elif traversed_already.get(head.get_label()):
            Logging.log("Head {0} traversed already", head.get_label())

    in_cycle[vertex.get_label()] = False
    # viztrace_log_finish_dfs(directed_graph, vertex)
    return False


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
            if is_cyclic_dfs(directed_graph, vertex, traversed_already, in_cycle):
                return True

    return False


def viztrace_log_activated_vertex(directed_graph, vertex):
    Logging.log("Vertex {0}", vertex.get_label())
    VizTracing.change_activated_vertex(directed_graph, vertex)
    VizTracing.snapshot()


def viztrace_log_cycle_reported(directed_graph, vertex):
    Logging.log("Vertex {0} just reported a cyclic", vertex.get_label())
    Logging.dec_indent()
    VizTracing.set_status(directed_graph, vertex, VizTracing.IN_CYCLE)
    VizTracing.change_activated_vertex(directed_graph, vertex)    
    VizTracing.snapshot()


def viztrace_visit_tail(directed_graph, vertex):
    VizTracing.change_activated_vertex(directed_graph, vertex)
    VizTracing.set_status(directed_graph, vertex, VizTracing.VISISTED)
    VizTracing.snapshot()


def viztrace_log_cycle_found(directed_graph, tail, head):
    Logging.log("Vertex {0}, head {1} cycle just found", tail.get_label(), head.get_label())
    Logging.dec_indent()
    VizTracing.set_status(directed_graph, head, VizTracing.IN_CYCLE)
    VizTracing.change_activated_vertex(directed_graph, head)    
    VizTracing.snapshot()


def viztrace_log_finish_dfs(directed_graph, vertex):
    Logging.dec_indent()
    if len(vertex.get_heads()) != 0:
        VizTracing.change_activated_vertex(directed_graph, vertex)
        VizTracing.snapshot()
