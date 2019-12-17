from util.advisor import Advisor


def is_cyclic(directed_graph, advisor: Advisor):
    """ Function that checks whether a directed graph contains a cycle or not

    Args:
        directed_graph (DirectedGraph): The directed graph
        advisor(Advisor): Object that contains advice which can be inserted at join points

    Returns:
        bool: True if the directed graph contains a cycle, otherwise False

    """

    _advisor = advisor

    def _is_cyclic_dfs(directed_graph, vertex, visited_already, in_cycle):
        """ Function that recursively searches the directed graph depth first and checks
        if a vertex was already in_cycle before. 

        It checks all vertices that have not been traversed before. The heads of those 
        vertices are followed. If in that traversal, a vertex is found that is present in 
        the dict "in_cycle" with a value of true, then a cycle is present

        Args:
            directed_graph (DirectedGraph): The directed graph 
            vertex(Vertex): The current vertex
            visited_already (dict): A dictionary that maintains whether vertices have been 
                traversed already. It's a performance measure put in place in order to shortcut 
                processing if a vertex was already processed by another subtree
            in_cycle (list): A list that, if a vertex has been found to part be part of cycle,
                for that vertex, has a value of true. If that vertex is not part of a cycle, it's
                value is false

        Returns:
            bool: True if the vertex was in_cycle before, False otherwise

        """

        visited_already[vertex.get_label()] = True
        in_cycle[vertex.get_label()] = True
        advisor.advise("visit_vertex", directed_graph, vertex)

        for edge in vertex.get_edges():
            if visited_already.get(edge.get_head().get_label()) is None:
                if _is_cyclic_dfs(directed_graph, edge.get_head(), visited_already, in_cycle):
                    advisor.advise("cycle_reported_recursive", directed_graph, edge.get_head())                    
                    return True
                else:
                    advisor.advise("no_cycle_reported_recursive", directed_graph, vertex)  
            elif in_cycle[edge.get_head().get_label()]:
                advisor.advise("cycle_found", directed_graph, vertex, edge.get_head())  
                return True
            elif visited_already.get(edge.get_head().get_label()):
                advisor.advise("vertex_already_visited", directed_graph, edge)

        in_cycle[vertex.get_label()] = False
        return False


    def _is_cyclic_inner(directed_graph):
        visited_already = dict()
        in_cycle = {i:False for i in directed_graph.get_vertices().keys()}
        for label, vertex in directed_graph.get_vertices().items():
            if visited_already.get(label) is None:
                if _is_cyclic_dfs(directed_graph, vertex, visited_already, in_cycle):
                    return True

        return False

    return _is_cyclic_inner(directed_graph)

