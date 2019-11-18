# The main function that finds and prints all strongly 
# connected components 
def create_SCCs(directed_graph): 

    stack = [] 
    scc = dict()

    visited = [False for i in range(directed_graph.get_vertices_count())]
    for i in range(directed_graph.get_vertices_count()): 
        if not visited[i]: 
            fill_order_DFS_SCCS(directed_graph, i, visited, stack) 

    # Create a reversed graph 
    reversed_graph = get_reversed_graph(directed_graph) 
        
    # Mark all the vertices as not visited (For second DFS) 
    visited = [False for i in range(directed_graph.get_vertices_count())]

    # Now process all vertices in order defined by Stack 
    scc_id = 0
    while stack: 
        i = stack.pop() 
        if not visited[i]:
            scc[scc_id] = set() 
            visit_DFS_SCCs(reversed_graph, i, visited, scc[scc_id]) 
            scc_id += 1

    return scc

# A function used by DFS 
def visit_DFS_SCCs(directed_graph, vertex, visited, scc): 
    # Mark the current node as visited 
    visited[vertex] = True
    scc.add(vertex)
    #Recur for all the vertices adjacent to this vertex 
    for i in directed_graph._vertices[vertex].get_tails(): 
        if not visited[i]: 
            visit_DFS_SCCs(directed_graph, i, visited, scc) 

def fill_order_DFS_SCCS(directed_graph, vertex, visited, stack): 
    # Mark the current node as visited  
    visited[vertex] = True
    #Recur for all the vertices adjacent to this vertex 
    for i in directed_graph._vertices[vertex].get_tails(): 
        if not visited[i]: 
            fill_order_DFS_SCCS(directed_graph, i, visited, stack) 
    stack = stack.append(vertex) 
   
# Function that returns reverse of this graph 
def get_reversed_graph(directed_graph): 

    reversed = directed_graph.create_new(None)
    # Recur for all the vertices adjacent to this vertex 

    for i in directed_graph._vertices.keys(): 
        reversed.add_vertex(i)

    for i in directed_graph._vertices.keys(): 
        vertex = directed_graph.get_vertex(i)
        for j in vertex.get_tails():
            reversed.add_edge(j, i) 
    return reversed 

def is_cyclic_dfs(directed_graph, vertex, visited, stack): 
  
    # Mark current node as visited and  
    # adds to recursion stack 
    visited[vertex] = True
    stack[vertex] = True

    # Recur for all neighbours 
    # if any neighbour is visited and in  
    # stack then graph is cyclic 
    for i in directed_graph._vertices[vertex].get_tails(): 
        if not visited[i]: 
            if is_cyclic_dfs(directed_graph, i, visited, stack): 
                return True
        elif stack[i] == True: 
            return True

    # The node needs to be poped from  
    # recursion stack before function ends 
    stack[vertex] = False
    return False

# Returns true if graph is cyclic else false 
def is_cyclic(directed_graph): 
    visited = [False for i in range(directed_graph.get_vertices_count())]
    stack = [False for i in range(directed_graph.get_vertices_count())]
    for node in range(directed_graph.get_vertices_count()): 
        if not visited[node]: 
            if is_cyclic_dfs(directed_graph, node, visited, stack): 
                return True
    return False

