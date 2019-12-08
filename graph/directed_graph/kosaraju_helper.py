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
        Logging.log("Vertex {0}, head {1} in fill order starting", vertex, head.get_label())
        if visited.get(head.get_label()) is None:
            Logging.log(
                "Vertex {0}, head {1} not visited, go to fill order rec.", vertex, head.get_label())
            Logging.inc_indent()
            fill_order_dfd_sccs(directed_graph, head.get_label(), visited, stack)
            Logging.dec_indent()
            Logging.log(
                "Vertex {0}, head {1} returned from fill order", vertex, head.get_label())
            Logging.log(
                "Vertex {0}, head {1} in fill order finished", vertex, head.get_label())
        else:
            Logging.log(
                "Vertex {0}, head {1} already visited, skipping", vertex, head.get_label())
            Logging.log(
                "Vertex {0}, head {1} in fill order finished", vertex, head.get_label())
    stack = stack.append(vertex)
