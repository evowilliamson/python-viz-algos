from util.logging import Logging

""" Helper module for DirectedGraph class
"""


def create_sccs(directed_graph, nontrivial):
    """ Function that creates a list of strongly connected components

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

    reversed_graph = get_reversed_graph(directed_graph)

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
    that the indegree and the outdegree are both 1 and the head is equal
    to the tail

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
             vertex.get_outdegree() == 1) and list(vertex.get_tails())[0] == list(scc)[0]:
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
    for i in directed_graph.get_vertices()[vertex].get_tails():
        if visited.get(i) is None:
            visit_dfs_sccs(directed_graph, i, visited, scc)


def fill_order_dfd_sccs(directed_graph, vertex, visited, stack):
    """ Function that covers the first part of the algorith by determining
    the order of vertices, traversing the graph with a depth first search, recursivelu

    Args:
        directed_graph (DirectedGraph): The directed graph 
        vertex: The current vertex
        visited (dict): A dictionary that maintains whether vertices have been visisted
        stack (list): stack that will be processed, used to inverse the order

    """

    visited[vertex] = True
    for i in directed_graph.get_vertices()[vertex].get_tails():
        Logging.log("Vertex {0}, tail {1} in fill order starting", vertex, i)
        if visited.get(i) is None:
            Logging.log(
                "Vertex {0}, tail {1} not visited, go to fill order rec.", vertex, i)
            Logging.inc_indent()
            fill_order_dfd_sccs(directed_graph, i, visited, stack)
            Logging.dec_indent()
            Logging.log(
                "Vertex {0}, tail {1} returned from fill order", vertex, i)
            Logging.log(
                "Vertex {0}, tail {1} in fill order finished", vertex, i)
        else:
            Logging.log(
                "Vertex {0}, tail {1} already visited, skipping", vertex, i)
            Logging.log(
                "Vertex {0}, tail {1} in fill order finished", vertex, i)
    stack = stack.append(vertex)


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
        for j in vertex.get_tails():
            reversed.add_edge(j, i)

    return reversed


def is_cyclic_dfs(directed_graph, vertex, traversed, in_cycle):
    """ Function that recursively searches the directed graph depth first and checks
    if a vertex was already in_cycle before. 

    It checks all vertices that have not been traversed before. The tails of those 
    vertices are followed. If in that traversal, a vertex is found that is present in 
    the dict "in_cycle" with a value of true, then a cycle is present

    Args:
        directed_graph (DirectedGraph): The directed graph 
        vertex: The current vertex
        traversed (dict): A dictionary that maintains whether vertices have been traversed
        in_cycle (list): a list that, if a vertex has been found to part be part of cycle,
            for that vertex, has a value of true. If that vertex is not part of a cycle, it's
            value is false

    Returns:
        bool: True if the vertex was in_cycle before, False otherwise

    """

    traversed[vertex] = True
    in_cycle[vertex] = True

    Logging.inc_indent()
    for i in directed_graph.get_vertices()[vertex].get_tails():
        Logging.log("Vertex {0}, tail {1}", vertex, i)
        Logging.inc_indent()
        if traversed.get(i) is None:
            Logging.log("Tail {0} not yet traversed", i)
            if is_cyclic_dfs(directed_graph, i, traversed, in_cycle):
                Logging.log(
                    "Vertex {0}, tail {1} just reported a cyclic", vertex, i)
                return True
        elif in_cycle[i]:
            Logging.log("Vertex {0}, tail {1} cycle just found", vertex, i)
            return True
        elif traversed.get(i):
            Logging.log("Tail {0} traversed already", i)
        Logging.dec_indent

    in_cycle[vertex] = False
    Logging.dec_indent()
    return False


def is_cyclic(directed_graph):
    """ Function that checks whether a directed graph contains a cycle or not

    Args:
        directed_graph (DirectedGraph): The directed graph

    Returns:
        bool: True if the directed graph contains a cycle, otherwise False

    """

    Logging.log("\nStarting cycle check")
    traversed = dict()
    in_cycle = [False for i in range(directed_graph.get_vertices_count())]
    for vertex in directed_graph.get_vertices().keys():
        Logging.log("Vertex {0}", vertex)
        if traversed.get(vertex) is None:
            if is_cyclic_dfs(directed_graph, vertex, traversed, in_cycle):
                return True

    return False
