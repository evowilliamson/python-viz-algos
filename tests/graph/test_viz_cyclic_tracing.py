import unittest
from pythonalgos.graph.directed_graph import DirectedGraph
from pythonvizalgos.graph.viz_cyclic_tracing import VizCyclicTracing
import os
import time
from pythonalgos.util.logging import Logging
import pythonalgos.util.path_tools as pt
from os import path


class TestVizCyclicTracing(unittest.TestCase):

    DIGRAPH_VIZ = "digraph_viz"
    RESOURCES_PATH = "python-test-resources"

    def setUp(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)

    def test_VizCyclicTracing_default(self):
        pt.create_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH)
        VizCyclicTracing.enable(
            pt.get_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH), 
            self.directed_graph)
        VizCyclicTracing.snapshot()
        self.assertTrue(True)

    def test_VizCyclicTracing_vertex_only(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)        
        vertex_1 = self.directed_graph.get_vertex(1)
        vertex_1.set_attr("activated", True)
        vertex_2 = self.directed_graph.get_vertex(2)
        vertex_2.set_attr("in_cycle", True)
        pt.create_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH)
        VizCyclicTracing.enable(pt.get_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH),
            self.directed_graph,
            vertex_states=[
                {VizCyclicTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                {VizCyclicTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}}])
        VizCyclicTracing.snapshot()
        self.assertTrue(True)

    def test_VizCyclicTracing_activate_vertex(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)        
        vertex_1 = self.directed_graph.get_vertex(1)
        pt.create_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH)
        VizCyclicTracing.enable(pt.get_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH), 
            self.directed_graph,
            vertex_states=[
                {VizCyclicTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                {VizCyclicTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}}])        
        VizCyclicTracing.change_activated_vertex(self.directed_graph, vertex_1)
        for label, vertex in self.directed_graph.get_vertices().items():
            if vertex_1.get_label() == label:
                self.assertTrue(vertex.get_attr(VizCyclicTracing.ACTIVATED))
            else:
                self.assertFalse(vertex.get_attr(VizCyclicTracing.ACTIVATED))

    def test_VizCyclicTracing_set_status(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)        
        vertex_5 = self.directed_graph.get_vertex(5)
        vertex_6 = self.directed_graph.get_vertex(6)
        pt.create_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH)        
        VizCyclicTracing.enable(pt.get_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH), 
            self.directed_graph,
            vertex_states=[
                {VizCyclicTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                {VizCyclicTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}}])        
        VizCyclicTracing.set_status(self.directed_graph, vertex_5, VizCyclicTracing.IN_CYCLE)
        VizCyclicTracing.set_status(self.directed_graph, vertex_6, VizCyclicTracing.IN_CYCLE)
        for label, vertex in self.directed_graph.get_vertices().items():
            if vertex_5.get_label() == label or vertex_6.get_label() == label:
                self.assertTrue(vertex.get_attr(VizCyclicTracing.IN_CYCLE))
            else:
                self.assertFalse(vertex.get_attr(VizCyclicTracing.IN_CYCLE))

    def test_VizCyclicTracing_snapshot(self):
        pt.create_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH)
        VizCyclicTracing.enable(pt.get_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH), self.directed_graph)
        VizCyclicTracing.snapshot() 
        self.assertTrue(os.path.exists(path.join(pt.get_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH),
            VizCyclicTracing.IMAGE_NAME_PREFIX + ("{:04d}".format(VizCyclicTracing.snapshot_no - 1)) + "." + 
            VizCyclicTracing.IMAGE_TYPE)))
        VizCyclicTracing.snapshot() 
        self.assertTrue(os.path.exists(path.join(pt.get_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH),
            VizCyclicTracing.IMAGE_NAME_PREFIX + ("{:04d}".format(VizCyclicTracing.snapshot_no - 1)) + "." + 
            VizCyclicTracing.IMAGE_TYPE)))

    def test_VizCyclicTracing_acyclic(self):
        Logging.enable()
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [7, 8],6:[7, 8], 
                         7: [9, 10, 11], 8: [11, 12], 9: [], 
                         10: [11], 11: [12], 12: []}
        self.directed_graph = DirectedGraph(self.vertices)        
        pt.create_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH)
        VizCyclicTracing.enable(
            pt.get_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH), 
            self.directed_graph,
            vertex_states=[
                    {VizCyclicTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                    {VizCyclicTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}},
                    {VizCyclicTracing.VISISTED: {"fillcolor":"gray", "style": "filled"}}])
        self.assertFalse(self.directed_graph.is_cyclic())       

    def test_VizCyclicTracing_cyclic(self):
        Logging.enable()
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [7, 8], 6:[7, 8], 
                         7: [9, 10, 11], 8: [3], 9: [], 
                         10: [11], 11: [12], 12: []}
        self.directed_graph = DirectedGraph(self.vertices)        
        pt.create_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH)
        VizCyclicTracing.enable(
            pt.get_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH), 
            self.directed_graph,
            vertex_states=[
                    {VizCyclicTracing.ACTIVATED: {"fillcolor":"red", "style": "filled"}}, 
                    {VizCyclicTracing.IN_CYCLE: {"fillcolor":"blue", "style": "filled"}},
                    {VizCyclicTracing.VISISTED: {"fillcolor":"gray", "style": "filled"}}])
        self.assertTrue(self.directed_graph.is_cyclic())       
                
    def tearDown(self):
        try:
            pt.clean_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH)
            self.assertFalse(os.path.exists(pt.get_dir_in_user_home(TestVizCyclicTracing.RESOURCES_PATH)))
        except:
            pass


if __name__ == '__main__':
    unittest.main()
