import unittest
from pythonalgos.graph.directed_graph import DirectedGraph
from pythonalgos.graph.directed_graph import DirectedGraph
from pythonvizalgos.graph.viz_cyclic_tracing import VizCyclicTracing
import os
import pythonalgos.util.path_tools as pt
from os import path
import inspect


class TestVizCyclicTracing(unittest.TestCase):

    DIGRAPH_VIZ = "digraph_viz"
    RESOURCES_PATH = "python-test-resources"
    RESOURCES_PATH_RECYCLE = RESOURCES_PATH + "/recycle"

    @classmethod
    def setUpClass(cls):
        pt.clean_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH)

    def setUp(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)

    def test_VizCyclicTracing_vertex_only(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)
        vertex_1 = self.directed_graph.get_vertex(1)
        vertex_1.set_attr("activated", True)
        vertex_2 = self.directed_graph.get_vertex(2)
        vertex_2.set_attr("in_cycle", True)
        dir = TestVizCyclicTracing.RESOURCES_PATH + "/" + \
            inspect.currentframe().f_code.co_name
        pt.create_dir_in_user_home(dir)
        viz_cyclic_tracing: VizCyclicTracing = VizCyclicTracing(
            path=pt.get_dir_in_user_home(dir),
            directed_graph=self.directed_graph,
            vertex_states=[
                    {VizCyclicTracing.ACTIVATED:
                        {"fillcolor": "red", "style": "filled"}},
                    {VizCyclicTracing.IN_CYCLE:
                        {"fillcolor": "blue", "style": "filled"}}])
        viz_cyclic_tracing.snapshot(self.directed_graph)
        self.assertTrue(True)

    def test_VizCyclicTracing_activate_vertex(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)
        vertex_1 = self.directed_graph.get_vertex(1)
        dir = TestVizCyclicTracing.RESOURCES_PATH + "/" + \
            inspect.currentframe().f_code.co_name
        viz_cyclic_tracing: VizCyclicTracing = VizCyclicTracing(
            path=pt.get_dir_in_user_home(dir),
            directed_graph=self.directed_graph,
            vertex_states=[
                    {VizCyclicTracing.ACTIVATED:
                        {"fillcolor": "red", "style": "filled"}},
                    {VizCyclicTracing.IN_CYCLE:
                        {"fillcolor": "blue", "style": "filled"}}])
        viz_cyclic_tracing.change_activated_vertex(self.directed_graph,
                                                   vertex_1)
        for vertex in self.directed_graph.get_vertices():
            if str(vertex_1.get_label()) == str(vertex.get_label()):
                self.assertTrue(vertex.get_attr(VizCyclicTracing.ACTIVATED))
            else:
                self.assertFalse(vertex.get_attr(VizCyclicTracing.ACTIVATED))

    def test_VizCyclicTracing_set_status(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)
        vertex_5 = self.directed_graph.get_vertex(5)
        vertex_6 = self.directed_graph.get_vertex(6)
        dir = TestVizCyclicTracing.RESOURCES_PATH + "/" + \
            inspect.currentframe().f_code.co_name
        viz_cyclic_tracing: VizCyclicTracing = VizCyclicTracing(
            path=pt.get_dir_in_user_home(dir),
            directed_graph=self.directed_graph,
            vertex_states=[
                    {VizCyclicTracing.ACTIVATED:
                        {"fillcolor": "red", "style": "filled"}},
                    {VizCyclicTracing.IN_CYCLE:
                        {"fillcolor": "blue", "style": "filled"}}])
        viz_cyclic_tracing.set_status(vertex_5, VizCyclicTracing.IN_CYCLE)
        viz_cyclic_tracing.set_status(vertex_6, VizCyclicTracing.IN_CYCLE)
        for vertex in self.directed_graph.get_vertices():
            if str(vertex_5.get_label()) == str(vertex.get_label()) or \
                    str(vertex_6.get_label()) == str(vertex.get_label()):
                self.assertTrue(vertex.get_attr(VizCyclicTracing.IN_CYCLE))
            else:
                self.assertFalse(vertex.get_attr(VizCyclicTracing.IN_CYCLE))

    def test_VizCyclicTracing_snapshot(self):
        dir = TestVizCyclicTracing.RESOURCES_PATH + "/" + \
            inspect.currentframe().f_code.co_name
        viz_cyclic_tracing: VizCyclicTracing = VizCyclicTracing(
            path=pt.get_dir_in_user_home(dir),
            directed_graph=self.directed_graph)
        viz_cyclic_tracing.snapshot(self.directed_graph)
        self.assertTrue(os.path.exists(path.join(
            pt.get_dir_in_user_home(dir),
            VizCyclicTracing.IMAGE_NAME_PREFIX +
            ("{:04d}".format(viz_cyclic_tracing.snapshot_no - 1)) + "." +
            VizCyclicTracing.IMAGE_TYPE)))
        viz_cyclic_tracing.snapshot(self.directed_graph)
        self.assertTrue(os.path.exists(path.join(
            pt.get_dir_in_user_home(dir),
            VizCyclicTracing.IMAGE_NAME_PREFIX +
            ("{:04d}".format(viz_cyclic_tracing.snapshot_no - 1)) + "." +
            VizCyclicTracing.IMAGE_TYPE)))

    def tearDown(self):
        pt.clean_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH_RECYCLE)
        self.assertFalse(os.path.exists(pt.get_dir_in_user_home(
            TestVizCyclicTracing.RESOURCES_PATH_RECYCLE)))


if __name__ == '__main__':
    unittest.main()
