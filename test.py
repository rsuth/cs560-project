import unittest
import shortest_path

class BuildNodeMap(unittest.TestCase):
    valid_file = 'valid_file'
    bad_file_path = 'asdf'
    file_lines = 13
    expected_result = [
        (1, -1),
        (2, -1),
        (3, -1),
        (4, 8),
        (5, -1),
        (6, 9),
        (7, -1),
        (8, 13),
        (9, -1),
        (10, -1),
        (11, 7),
        (12, 8),
        (13, 8),
    ]
    
    def testBadFile(self):
        self.assertRaises(FileNotFoundError, shortest_path.get_node_list, self.bad_file_path)
    
    def testCorrectNumberOfNodes(self):
        self.assertEqual(len(shortest_path.get_node_list(self.valid_file)),self.file_lines)
    
    def testCorrectResult(self):
        self.assertListEqual(shortest_path.get_node_list(self.valid_file),self.expected_result)
    
    def testCreateNodeMap(self):
        node_map = shortest_path.create_map_of_nodes(self.expected_result, 3)
        
        i = 0
        for n in node_map:
            self.assertEqual(n.position, self.expected_result[i][0])
            self.assertEqual(n.cost, self.expected_result[i][1])
            i += 1
    
    def testNegativesExcluded(self):
        node_map = shortest_path.create_map_of_nodes(self.expected_result, 3)
        for n in node_map:
            for adj in n.adjacent_nodes:
                self.assertTrue(adj.cost > 0)
    
    def testConnected(self):
        node_map = shortest_path.create_map_of_nodes(self.expected_result, 3)
        self.assertTrue(node_map[3] in node_map[5].adjacent_nodes)
        self.assertTrue(node_map[5] in node_map[3].adjacent_nodes)
        self.assertTrue(node_map[7] in node_map[12].adjacent_nodes)
        self.assertTrue(node_map[12] in node_map[7].adjacent_nodes)
        self.assertFalse(node_map[3] in node_map[7].adjacent_nodes)
        self.assertFalse(node_map[7] in node_map[3].adjacent_nodes)
        self.assertFalse(node_map[0] in node_map[12].adjacent_nodes)
        self.assertFalse(node_map[12] in node_map[0].adjacent_nodes)
        self.assertFalse(node_map[8] in node_map[9].adjacent_nodes)
    
    


