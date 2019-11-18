from collections import defaultdict
   
# The main function that finds and prints all strongly 
# connected components 
def create_SCCs(directed_graph): 

    # function to add an edge to graph 
    def add_edge(self,u,v): 
        directed_graph[u].append(v) 

    # A function used by DFS 
    def visit_DFS(self, v, visited, scc): 
        # Mark the current node as visited 
        visited[v] = True
        scc.add(v)
        #Recur for all the vertices adjacent to this vertex 
        for i in directed_graph[v]: 
            if not visited[i]: 
                visit_DFS(i,visited, scc) 

    def fill_order_DFS(self,v,visited, stack): 
        # Mark the current node as visited  
        visited[v]= True
        #Recur for all the vertices adjacent to this vertex 
        for i in directed_graph[v]: 
            if not visited[i]: 
                fill_order_DFS(i, visited, stack) 
        stack = stack.append(v) 

    # Function that returns reverse (or transpose) of this graph 
    def get_reversed(self, g): 
        #g = Graph(self.vertices) 

        # Recur for all the vertices adjacent to this vertex 
        for i in self.graph: 
            for j in self.graph[i]: 
                g.add_edge(j,i) 
        return g 

    stack = [] 
    vertices = vertices #No. of vertices 
    graph = defaultdict(list) # default dictionary to store graph 
    scc = dict()

    visited = [False for i in range(vertices)]
    for i in range(vertices): 
        if not visited[i]: 
            fill_order_DFS(i, visited, stack) 

    # Create a reversed graph 
    gr = get_reversed(99) 
        
        # Mark all the vertices as not visited (For second DFS) 
    visited = [False for i in range(vertices)]

    # Now process all vertices in order defined by Stack 
    scc_id = 0
    while stack: 
        i = stack.pop() 
        if not visited[i]:
            scc[scc_id] = set() 
            gr.visit_DFS(i, visited, scc[scc_id]) 
            scc_id += 1


