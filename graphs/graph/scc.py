from collections import defaultdict

class Graph: 
   
    def __init__(self, vertices): 
        self.vertices = vertices #No. of vertices 
        self.graph = defaultdict(list) # default dictionary to store graph 
        self.scc = dict()
   
    # function to add an edge to graph 
    def add_edge(self,u,v): 
        self.graph[u].append(v) 
   
    # A function used by DFS 
    def visit_DFS(self, v, visited, scc): 
        # Mark the current node as visited 
        visited[v] = True
        scc.add(v)
        #Recur for all the vertices adjacent to this vertex 
        for i in self.graph[v]: 
            if visited[i] == False: 
                self.visit_DFS(i,visited, scc) 
  
    def fill_order_DFS(self,v,visited, stack): 
        # Mark the current node as visited  
        visited[v]= True
        #Recur for all the vertices adjacent to this vertex 
        for i in self.graph[v]: 
            if not visited[i]: 
                self.fill_order_DFS(i, visited, stack) 
        stack = stack.append(v) 
  
    # Function that returns reverse (or transpose) of this graph 
    def get_reversed(self): 
        g = Graph(self.vertices) 
  
        # Recur for all the vertices adjacent to this vertex 
        for i in self.graph: 
            for j in self.graph[i]: 
                g.add_edge(j,i) 
        return g 
   
    # The main function that finds and prints all strongly 
    # connected components 
    def create_SCCs(self): 
        stack = [] 

        visited = [False for i in range(self.vertices)]
        for i in range(self.vertices): 
            if not visited[i]: 
                self.fill_order_DFS(i, visited, stack) 
  
        # Create a reversed graph 
        gr = self.get_reversed() 
           
         # Mark all the vertices as not visited (For second DFS) 
        visited = [False for i in range(self.vertices)]
  
        # Now process all vertices in order defined by Stack 
        scc_id = 0
        while stack: 
            i = stack.pop() 
            if visited[i]==False:
                self.scc[scc_id] = set() 
                gr.visit_DFS(i, visited, self.scc[scc_id]) 
                scc_id += 1
   
# Create a graph given in the above diagram 
g = Graph(8) 
g.add_edge(0, 1) 
g.add_edge(1, 2) 
g.add_edge(1, 3) 
g.add_edge(2, 3) 
g.add_edge(3, 4)
g.add_edge(4, 5)
g.add_edge(4, 2)
g.add_edge(5, 6)
g.add_edge(6, 7)
g.add_edge(7, 5)

g.create_SCCs() 
print(g.scc)