import unittest
from graph.directed_graph.directed_acyclic_graph import DirectedAcyclicGraph


class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3], 3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_acyclic_graph = DirectedAcyclicGraph(self.vertices)

    def test_init(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
