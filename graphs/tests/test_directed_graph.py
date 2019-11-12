import unittest
from graph.directed_graph import DirectedGraph


class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        self.vertices = set([0, 2, 1, 3, 4, 5, 6, 7])
        self.edges = set([(0, 2), (2, 3), (0, 1), (2, 1)])
        self.graph = DirectedGraph(self.vertices, self.edges)

    def test_init(self):
        graph = DirectedGraph(self.vertices, self.edges)
        self.assertEqual(len(self.vertices), graph.vertices_count())

if __name__ == '__main__':
    unittest.main()
