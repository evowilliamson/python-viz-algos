import unittest
from graph.directed_graph import DirectedGraph


class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        self.directed_graph = DirectedGraph({0: [1, 2], 1: [], 2: [3], 3: [], 4: [], 5: [], 6: []})

    def test_init(self):
        vertices = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(len(vertices), self.directed_graph.vertices_count())
        print(self.directed_graph)


if __name__ == '__main__':
    unittest.main()
