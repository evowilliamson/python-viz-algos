import unittest
from graph.directed_graph.directed_graph import DirectedGraph
from graph.directed_graph.viz_tracing import VizTracing
import os
import time
from util.logging import Logging
import util.path_tools as pt
from os import path


class TestDirectedGraph(unittest.TestCase):

    DIGRAPH_VIZ = "digraph_viz"
    RESOURCES_PATH = "python-test-resources"

    def setUp(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)

    def test_init(self):
        self.assertEqual(len(self.vertices.keys()),
                         self.directed_graph.get_vertices_count())

    def test_str(self):
        print(self.directed_graph)

    def test_one_vertex_self_loop(self):
        self.vertices = {0: [0]}
        self.directed_graph = DirectedGraph(self.vertices)
        a = 100

    def test_add_vertex(self):
        label = 7
        self.directed_graph.add_vertex(label)
        vertex = self.directed_graph.get_vertex(label)
        self.assertIsNotNone(vertex)
        self.assertEqual(vertex.get_outdegree(), 0)
        self.assertEqual(vertex.get_indegree(), 0)
        self.assertListEqual(vertex.get_heads(), list())

    def test_add_duplicate_vertex(self):
        label = 7
        self.directed_graph.add_vertex(label)
        with self.assertRaises(RuntimeError):
            self.directed_graph.add_vertex(label)

    def test_add_heads(self):
        vertex_to_test = 7
        self.directed_graph.add_vertex(vertex_to_test)
        vertex = self.directed_graph.get_vertex(vertex_to_test)
        no_heads = 3
        for i in range(no_heads):
            vertex.add_edge(self.directed_graph.get_vertex(i))
        self.assertEqual(len(vertex.get_heads()), no_heads)
        self.assertEqual(vertex.get_outdegree(), len(vertex.get_heads()))

    def test_outdegree(self):
        vertex = self.directed_graph.get_vertex(1)
        self.assertEqual(vertex.get_outdegree(), len(vertex.get_heads()))

    def test_indegree(self):
        vertex_to_test = 6
        self.vertices = {0: [1], 1: [2, 3], 2: [3], 3: [4, vertex_to_test], 4: [
            5, vertex_to_test], 5: [5], vertex_to_test: []}
        self.directed_graph = DirectedGraph(self.vertices)
        vertex = self.directed_graph.get_vertex(vertex_to_test)
        self.assertEqual(vertex.get_indegree(), 2)

    def test_create_sccs_nontrivial(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3], 3: [4],
                         4: [5, 2], 5: [6], 6: [7], 7: [5], 8: [8], 9: []}
        self.directed_graph = DirectedGraph(self.vertices)
        sccs = self.directed_graph.create_sccs_kosaraju_dfs()
        sccs_expected = [[2, 3, 4], [5, 6, 7], [8]]
        for vertices in sccs:
            sorted_vertices = sorted(list(vertices))
            if sorted_vertices not in sccs_expected:
                self.assertFalse(True, msg=str(
                    sorted_vertices) + " not in expected sccs")

    def test_create_sccs_extra(self):
        # Logging.enable()
        self.vertices = {"A": ["B"], "B": ["C", "D"], "C": ["A"], "D": ["E"], "E": ["F"],
                         "F": ["D"], "G": ["F", "H"], "H": ["I"], "I": ["J"], "J": ["G", "K"], "K": []}
        self.directed_graph = DirectedGraph(self.vertices)
        sccs = self.directed_graph.create_sccs_kosaraju_dfs(nontrivial=False)
        sccs_expected = [["A", "B", "C"], [
            "D", "E", "F"], ["G", "H", "I", "J"], ["K"]]
        for vertices in sccs:
            sorted_vertices = sorted(list(vertices))
            if sorted_vertices not in sccs_expected:
                self.assertFalse(True, msg=str(
                    sorted_vertices) + " not in expected sccs")

    def test_cyclic(self):
        Logging.enable()
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4], 4: [5, 2], 5: [6], 6: [7], 7: [5]}
        self.directed_graph = DirectedGraph(self.vertices)
        self.assertTrue(self.directed_graph.is_cyclic())

    def test_acyclic(self):
        Logging.enable()
        self.vertices = {0: [1], 1: [2, 3], 2: [
            3], 3: [4, 6], 4: [5, 6], 5: [], 6: []}
        self.directed_graph = DirectedGraph(self.vertices)
        self.assertFalse(self.directed_graph.is_cyclic())

    def test_graphviz_no_view(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4], 4: [5, 2], 5: [6], 6: [7], 7: [5]}
        self.directed_graph = DirectedGraph(self.vertices)
        pt.create_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)
        digraph_file = path.join(pt.get_dir_in_user_home(
            TestDirectedGraph.RESOURCES_PATH), TestDirectedGraph.DIGRAPH_VIZ)
        self.directed_graph.render(file_name=digraph_file)
        self.assertTrue(os.path.exists(digraph_file))
        self.assertTrue(os.path.exists(digraph_file + ".pdf"))

    @unittest.skipIf(True, "Set to False for viewing the graphviz representation")
    def test_graphviz_view(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4], 4: [5, 2], 5: [6], 6: [7], 7: [5]}
        self.directed_graph = DirectedGraph(self.vertices)
        pt.create_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)
        digraph_file = path.join(pt.get_dir_in_user_home(
            TestDirectedGraph.RESOURCES_PATH), TestDirectedGraph.DIGRAPH_VIZ)        
        self.directed_graph.render(
            file_name=TestDirectedGraph.DIGRAPH_VIZ, view_type=True)
        time.sleep(1)
        self.assertTrue(os.path.exists(digraph_file))
        self.assertTrue(os.path.exists(digraph_file + ".pdf"))

    def test_viztracing_default(self):
        pt.create_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)
        VizTracing.enable(
            pt.get_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH), 
            self.directed_graph)
        VizTracing.snapshot()
        self.assertTrue(True)

    def test_viztracing_vertex_only(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)        
        vertex_1 = self.directed_graph.get_vertex(1)
        vertex_1.set_attr("activated", True)
        vertex_2 = self.directed_graph.get_vertex(2)
        vertex_2.set_attr("in_cycle", True)
        pt.create_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)
        VizTracing.enable(pt.get_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH),
            self.directed_graph,
            vertex_states=[
                {VizTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                {VizTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}}])
        VizTracing.snapshot()
        self.assertTrue(True)

    def test_viztracing_activate_vertex(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)        
        vertex_1 = self.directed_graph.get_vertex(1)
        pt.create_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)
        VizTracing.enable(pt.get_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH), 
            self.directed_graph,
            vertex_states=[
                {VizTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                {VizTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}}])        
        VizTracing.change_activated_vertex(self.directed_graph, vertex_1)
        for label, vertex in self.directed_graph.get_vertices().items():
            if vertex_1.get_label() == label:
                self.assertTrue(vertex.get_attr(VizTracing.ACTIVATED))
            else:
                self.assertFalse(vertex.get_attr(VizTracing.ACTIVATED))

    def test_viztracing_set_status(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)        
        vertex_5 = self.directed_graph.get_vertex(5)
        vertex_6 = self.directed_graph.get_vertex(6)
        pt.create_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)        
        VizTracing.enable(pt.get_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH), 
            self.directed_graph,
            vertex_states=[
                {VizTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                {VizTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}}])        
        VizTracing.set_status(self.directed_graph, vertex_5, VizTracing.IN_CYCLE)
        VizTracing.set_status(self.directed_graph, vertex_6, VizTracing.IN_CYCLE)
        for label, vertex in self.directed_graph.get_vertices().items():
            if vertex_5.get_label() == label or vertex_6.get_label() == label:
                self.assertTrue(vertex.get_attr(VizTracing.IN_CYCLE))
            else:
                self.assertFalse(vertex.get_attr(VizTracing.IN_CYCLE))

    def test_viztracing_snapshot(self):
        pt.create_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)
        VizTracing.enable(pt.get_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH), self.directed_graph)
        VizTracing.snapshot() 
        self.assertTrue(os.path.exists(path.join(pt.get_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH),
            VizTracing.IMAGE_NAME_PREFIX + str(VizTracing.snapshot_no - 1) + "." + 
            VizTracing.IMAGE_TYPE)))
        VizTracing.snapshot() 
        self.assertTrue(os.path.exists(path.join(pt.get_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH),
            VizTracing.IMAGE_NAME_PREFIX + str(VizTracing.snapshot_no - 1) + "." + 
            VizTracing.IMAGE_TYPE)))

    def test_viztracing_acyclic(self):
        Logging.enable()
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [7, 8],6:[7, 8], 
                         7: [9, 10, 11], 8: [11, 12], 9: [], 
                         10: [11], 11: [12], 12: []}
        self.directed_graph = DirectedGraph(self.vertices)        
        pt.create_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)
        VizTracing.enable(
            pt.get_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH), 
            self.directed_graph,
            vertex_states=[
                    {VizTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                    {VizTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}},
                    {VizTracing.VISISTED: {"fillcolor":"gray", "style": "filled"}}])
        self.assertFalse(self.directed_graph.is_cyclic())       

    def test_viztracing_cyclic(self):
        Logging.enable()
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [7, 8], 6:[7, 8], 
                         7: [9, 10, 11], 8: [3], 9: [], 
                         10: [11], 11: [12], 12: []}
        self.directed_graph = DirectedGraph(self.vertices)        
        pt.create_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)
        VizTracing.enable(
            pt.get_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH), 
            self.directed_graph,
            vertex_states=[
                    {VizTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                    {VizTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}},
                    {VizTracing.VISISTED: {"fillcolor":"gray", "style": "filled"}}])
        self.assertTrue(self.directed_graph.is_cyclic())       
                
    def tearDown(self):
        try:
            pt.clean_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)
            self.assertFalse(os.path.exists(pt.get_dir_in_user_home(TestDirectedGraph.RESOURCES_PATH)))
        except:
            pass


if __name__ == '__main__':
    unittest.main()
