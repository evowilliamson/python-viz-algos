import unittest
from graph.directed_graph.directed_graph import DirectedGraph
import os
import time
from util.logging import Logging


class TestDirectedGraph(unittest.TestCase):

    DIGRAPH_VIZ = "digraph_viz"

    def setUp(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)

    def test_init(self):
        self.assertEqual(len(self.vertices.keys()),
                         self.directed_graph.get_vertices_count())

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
        self.assertSetEqual(vertex.get_tails(), set())

    def test_add_duplicate_vertex(self):
        label = 7
        self.directed_graph.add_vertex(label)
        with self.assertRaises(RuntimeError):
            self.directed_graph.add_vertex(label)

    def test_add_tails(self):
        vertex_to_test = 7
        self.directed_graph.add_vertex(vertex_to_test)
        vertex = self.directed_graph.get_vertex(vertex_to_test)
        no_tails = 3
        for i in range(no_tails):
            vertex.add_tail(i)
        self.assertEqual(len(vertex.get_tails()), no_tails)
        self.assertEqual(vertex.get_outdegree(), len(vertex.get_tails()))

    def test_outdegree(self):
        vertex = self.directed_graph.get_vertex(1)
        self.assertEqual(vertex.get_outdegree(), len(vertex.get_tails()))

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
        self.directed_graph.render(file_name=TestDirectedGraph.DIGRAPH_VIZ)
        self.assertTrue(os.path.exists(TestDirectedGraph.DIGRAPH_VIZ))
        self.assertTrue(os.path.exists(TestDirectedGraph.DIGRAPH_VIZ + ".pdf"))

    @unittest.skipIf(True, "Set to False for viewing the graphviz representation")
    def test_graphviz_view(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4], 4: [5, 2], 5: [6], 6: [7], 7: [5]}
        self.directed_graph = DirectedGraph(self.vertices)
        self.directed_graph.render(
            file_name=TestDirectedGraph.DIGRAPH_VIZ, view_type=True)
        time.sleep(1)
        self.assertTrue(os.path.exists(TestDirectedGraph.DIGRAPH_VIZ))
        self.assertTrue(os.path.exists(TestDirectedGraph.DIGRAPH_VIZ + ".pdf"))

    def tearDown(self):

        try:
            os.remove(TestDirectedGraph.DIGRAPH_VIZ + ".pdf")
            os.remove(TestDirectedGraph.DIGRAPH_VIZ)
            self.assertFalse(os.path.exists(TestDirectedGraph.DIGRAPH_VIZ))
            self.assertFalse(os.path.exists(
                TestDirectedGraph.DIGRAPH_VIZ + ".pdf"))
        except:
            pass


if __name__ == '__main__':
    unittest.main()
