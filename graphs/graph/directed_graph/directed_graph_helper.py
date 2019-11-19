""" Helper module for DirectedGraph class
"""


def create_SCCs(directed_graph): 
    """ Function that creates a list of strongly connected components

    Args: 
        directed_graph (DirectedGraph): The directed graph for which the SCCS should be calculated

    Returns:
        list(set()) of SCCs: Each SCC is a set of vertices

    """

    stack = []; scc, visited = list(), dict()
    for i in range(directed_graph.get_vertices_count()): 
        if visited.get(i) is None: 
            fill_order_DFS_SCCS(directed_graph, i, visited, stack) 

    reversed_graph = get_reversed_graph(directed_graph) 
    visited = dict()
    for i in reversed(stack):
        if visited.get(i) is None:
            scc.append(set())
            visit_DFS_SCCs(reversed_graph, i, visited, scc[-1]) 

    return scc


def visit_DFS_SCCs(directed_graph, vertex, visited, scc): 
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
    for i in directed_graph._vertices[vertex].get_tails(): 
        if visited.get(i) is None: 
            visit_DFS_SCCs(directed_graph, i, visited, scc) 


def fill_order_DFS_SCCS(directed_graph, vertex, visited, stack): 
    """ Function that covers the first part of the algorith by determining
    the order of vertices, traversing the graph with a depth first search, recursivelu

    Args:
        directed_graph (DirectedGraph): The directed graph 
        vertex: The current vertex
        visited (dict): A dictionary that maintains whether vertices have been visisted
        stack (list): stack that will be processed, used to inverse the order

    """

    visited[vertex] = True
    for i in directed_graph._vertices[vertex].get_tails(): 
        if visited.get(i) is None: 
            fill_order_DFS_SCCS(directed_graph, i, visited, stack) 
    stack = stack.append(vertex) 

   
def get_reversed_graph(directed_graph): 
    """ Function that returns the reverse of this graph  

    Args:
        directed_graph (DirectedGraph): The directed graph 

    Returns:
        DirectedGraph: The reversed graph

    """

    reversed = directed_graph.create_new(None)

    for i in directed_graph._vertices.keys(): 
        reversed.add_vertex(i)

    for i in directed_graph._vertices.keys(): 
        vertex = directed_graph.get_vertex(i)
        for j in vertex.get_tails():
            reversed.add_edge(j, i) 

    return reversed 


def is_cyclic_dfs(directed_graph, vertex, visited, stack): 
    """ Function that recursively searches the directed graph depth first and checks
    if a vertex was already stacked before

    Args:
        directed_graph (DirectedGraph): The directed graph 
        vertex: The current vertex
        visited (dict): A dictionary that maintains whether vertices have been visisted
        stack (list): 

    Returns:
        bool: True if the vertex was stacked before, False otherwise

    """

    visited[vertex] = True
    stack[vertex] = True

    for i in directed_graph._vertices[vertex].get_tails(): 
        if visited.get(i) is None: 
            if is_cyclic_dfs(directed_graph, i, visited, stack): 
                return True
        elif stack[i]: 
            return True

    stack[vertex] = False
    return False


def is_cyclic(directed_graph): 
    """ Function that checks whether a directed graph contains a cycle or not

    Args:
        directed_graph (DirectedGraph): The directed graph

    Returns:
        bool: True if the directed graph contains a cycle, otherwise False

    """    

    visited = dict()
    stack = [False for i in range(directed_graph.get_vertices_count())]
    for i in range(directed_graph.get_vertices_count()): 
        if visited.get(i) is None: 
            if is_cyclic_dfs(directed_graph, i, visited, stack): 
                return True
                
    return False

