import unittest
from graph.directed_graph import DirectedGraph


class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3], 3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)

    def test_init(self):
        self.assertEqual(len(self.vertices.keys()), self.directed_graph.vertices_count())

    def test_outdegree(self):
        vertex = self.directed_graph.get_vertex(1)
        self.assertEqual(vertex.get_outdegree(), len(vertex.get_tails()))

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

    def test_indegree(self):
        vertex = self.directed_graph.get_vertex(6)
        self.assertEqual(vertex.get_outdegree(), len(vertex.get_tails()))


if __name__ == '__main__':
    unittest.main()
