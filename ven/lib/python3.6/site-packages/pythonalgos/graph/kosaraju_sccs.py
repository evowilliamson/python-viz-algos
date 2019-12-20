from pythonalgos.util.logging import Logging

""" Module that contains the logic for kosaraju's SCCs algorithm
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
            fill_order_dfd_sccs(directed_graph, vertex, visited, stack)
        else:
            Logging.log("Vertex {0} already visited, skipping", vertex)

    reversed_graph = directed_graph.get_reversed_graph()

    visited = dict()
    for i in reversed(stack):
        if visited.get(i) is None:
            sccs_trivial.append(set())
            visit_dfs_sccs(reversed_graph, i, visited, sccs_trivial[-1])

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


def visit_dfs_sccs(directed_graph, vertex, visited, scc):
    """ Function that performs a recursive depth first search on the directed graph
    to check whether vertices have been visisted

    Args:
        directed_graph(DirectedGraph): The directed graph 
        vertex (label): The current vertex
        visited (dict): A dictionary that maintains whether vertices have been visisted
        scc (set): The current scc being constructed

    """

    visited[vertex] = True
    scc.add(vertex)
    for head in directed_graph.get_vertices()[vertex].get_heads():
        if visited.get(head.get_label()) is None:
            visit_dfs_sccs(directed_graph, head.get_label(), visited, scc)


def fill_order_dfd_sccs(directed_graph, vertex, visited, stack):
    """ Function that covers the first part of the algorith by determining
    the order of vertices, traversing the graph with a depth first search, recursively

    Args:
        directed_graph (DirectedGraph): The directed graph 
        vertex: The current vertex
        visited (dict): A dictionary that maintains whether vertices have been visisted
        stack (list): stack that will be processed, used to inverse the order

    """

    visited[vertex] = True
    for head in directed_graph.get_vertices()[vertex].get_heads():
        if visited.get(head.get_label()) is None:
            fill_order_dfd_sccs(directed_graph, head.get_label(), visited, stack)
    stack = stack.append(vertex)



    