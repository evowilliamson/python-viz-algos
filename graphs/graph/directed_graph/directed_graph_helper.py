from collections import defaultdict

class DirectedGraphHelper: 
   
    def __init__(self, directed_grap): 
        self.graph = defaultdict(list) # default dictionary to store graph 
        self.scc = dict()
   
