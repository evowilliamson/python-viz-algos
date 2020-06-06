import unittest
from pythonalgos.graph.directed_graph import DirectedGraph, Vertex
from pythonalgos.graph.algorithm_ordering import AlgorithmOrdering
from pythonvizalgos.graph.viz_scc_kosaraju_tracing\
    import VizSccsKosarajuTracing
from pythonvizalgos.graph.viz_tracing import VizTracing
import pythonalgos.util.path_tools as pt
import inspect


class TestVizSccsKosarajuTracing(unittest.TestCase):

    DIGRAPH_VIZ = "digraph_viz"
    RESOURCES_PATH = "python-test-resources/scc_kosaraju"

    @classmethod
    def setUpClass(cls):
        pt.clean_dir_in_user_home(TestVizSccsKosarajuTracing.RESOURCES_PATH)

    def setUp(self):
        self.vertices = {1: [2], 2: [3, 6], 3: [4], 4: [5], 5: [1],
                         6: [7], 7: [8], 8: [9, 12], 9: [6, 10], 10: [],
                         11: [11], 12: [13], 13: []}
        self.directed_graph = DirectedGraph(self.vertices)

    def test_VizSccTracing_nontrivial(self):
        """ Functions more as a demonstration than as a test. It will create
        the animation for an acyclic graph"""

        self.directed_graph = \
            DirectedGraph(self.vertices,
                          algorithm_ordering=AlgorithmOrdering.ASC)
        dir = TestVizSccsKosarajuTracing.RESOURCES_PATH + "/" + \
            inspect.currentframe().f_code.co_name
        viz_sccs_kosaraju_tracing: VizSccsKosarajuTracing =\
            VizSccsKosarajuTracing(
                path=pt.get_dir_in_user_home(dir),
                directed_graph=self.directed_graph,
                vertex_states=[
                    {VizTracing.ACTIVATED:
                        {"fillcolor": "red", "style": "filled"}},
                    {VizTracing.VISITED:
                        {"fillcolor": "gray", "style": "filled"}},
                    {VizTracing.DEFAULT:
                        {"fillcolor": "white", "style": "filled"}}
                    ],
                edge_states={})
        viz_sccs_kosaraju_tracing.execute(resource_path=dir,
                                          nontrivial=True)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
