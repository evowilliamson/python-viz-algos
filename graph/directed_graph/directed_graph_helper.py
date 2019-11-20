""" Helper module for DirectedGraph class
"""


def create_SCCs(directed_graph, nontrivial): 
    """ Function that creates a list of strongly connected components

    Args: 
        directed_graph (DirectedGraph): The directed graph for which the SCCS should be calculated
        nontrivial(bool): If True, only nontrivial sccs will be returned, otherwise all sccs

    Returns:
        list(set()) of SCCs: Each SCC is a set of vertices

    """

    stack = []; sccs_trivial, visited = list(), dict()
    for i in range(directed_graph.get_vertices_count()): 
        if visited.get(i) is None: 
            fill_order_DFS_SCCS(directed_graph, i, visited, stack) 

    reversed_graph = get_reversed_graph(directed_graph) 
    visited = dict()
    for i in reversed(stack):
        if visited.get(i) is None:
            sccs_trivial.append(set())
            visit_DFS_SCCs(reversed_graph, i, visited, sccs_trivial[-1]) 

    if nontrivial:
        # A scc is nontrivial, iff there are at least two vertices in it, 
        # or there is only one vertex with a self-loop. A self-loop means
        # that the indegree and the outdegree are both 1 and the head is equal
        # to the tail
        sccs_non_trivial = list()
        for scc in sccs_trivial:
            vertex = directed_graph.get_vertex(list(scc)[0])
            if (len(scc) >= 2) or \
            (len(scc) == 1 and vertex.get_indegree() == 1 and \
            vertex.get_outdegree() == 1) and list(vertex.get_tails())[0] == list(scc)[0]:
                sccs_non_trivial.append(scc)
        return sccs_non_trivial
    else:
        return sccs_trivial


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

    reversed = directed_graph.__class__()
    for i in directed_graph._vertices.keys(): 
        reversed.add_vertex(i)

    for i in directed_graph._vertices.keys(): 
        vertex = directed_graph.get_vertex(i)
        for j in vertex.get_tails():
            reversed.add_edge(j, i) 

    return reversed 


def is_cyclic_dfs(directed_graph, vertex, traversed, found): 
    """ Function that recursively searches the directed graph depth first and checks
    if a vertex was already found before. 

    It checks all vertices that have not been traversed before. The tails of those 
    vertices are followed. If in that traversal, a vertex is found that is present in 
    the dict "found", then a cycle is present

    Args:
        directed_graph (DirectedGraph): The directed graph 
        vertex: The current vertex
        traversed (dict): A dictionary that maintains whether vertices have been traversed
        found (list): a list that contains all vertices already found in the path

    Returns:
        bool: True if the vertex was found before, False otherwise

    """

    traversed[vertex] = True
    found[vertex] = True

    for i in directed_graph._vertices[vertex].get_tails(): 
        if traversed.get(i) is None: 
            if is_cyclic_dfs(directed_graph, i, traversed, found): 
                return True
        elif found[i]: 
            return True

    found[vertex] = False
    return False


def is_cyclic(directed_graph): 
    """ Function that checks whether a directed graph contains a cycle or not

    Args:
        directed_graph (DirectedGraph): The directed graph

    Returns:
        bool: True if the directed graph contains a cycle, otherwise False

    """    

    traversed = dict()
    found = [False for i in range(directed_graph.get_vertices_count())]
    for i in range(directed_graph.get_vertices_count()): 
        if traversed.get(i) is None: 
            if is_cyclic_dfs(directed_graph, i, traversed, found): 
                return True
                
    return False

