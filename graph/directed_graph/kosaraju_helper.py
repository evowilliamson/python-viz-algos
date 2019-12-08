from util.logging import Logging

""" Helper module for Kosaraju's scc algorithm 
"""


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
    the order of vertices, traversing the graph with a depth first search, recursively

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
