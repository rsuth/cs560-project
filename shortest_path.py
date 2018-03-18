import re


# Node class used to store properties of each node
class Node():
    def __init__(self, _position, _cost):
        self.position = _position
        self.cost = _cost
        self.adjacent_nodes = []
        self.is_left_edge = False
        self.is_right_edge = False
        self.is_top_edge = False
        self.is_bottom_edge = False
        self.isGoalNode = False
        self.isStartingNode = False

# takes path to the file representing the nodes in the hexagonal grid
# returns a list of tuples (num, cost)
def get_node_list(path_to_file):
    nodes = []
    with open(path_to_file) as f:
        for line in f:
            m = re.match(re.compile(r'(\d+) (-?\d+)'), line)
            pos = int(m.group(1))
            cost = int(m.group(2))
            nodes.append((pos, cost))
        f.close()
    return nodes

# sets flags for each node that is on an edge
def assign_edge_nodes(node_map, width):
    for i in range(0, len(node_map)-width+1, 2*width-1): 
        node_map[i].is_left_edge = True
    for i in range(width-1, len(node_map), 2*width-1): 
        node_map[i].is_right_edge = True
    for i in range(0, width): 
        node_map[i].is_top_edge = True
    for i in range(len(node_map)-width, len(node_map)): 
        node_map[i].is_bottom_edge = True

# takes a list of tuples where each tuple represents a hexagon
# and has the form (position, cost). builds an array of Node objects
# where each Node stores an array of every node that is adjacent
def create_map_of_nodes(nodeList, map_width):
    node_map = []
    for n in nodeList:
        node = Node(n[0], n[1])
        node_map.append(node)

    assign_edge_nodes(node_map, map_width)

    for node in node_map:
        candidate_nodes = []
        top_center =    (node.position - 1) - (2*map_width - 1)
        bottom_center = (node.position - 1) + (2*map_width - 1)
        top_right =     (node.position - 1) - (map_width - 1)
        bottom_left =   (node.position - 1) + (map_width - 1)
        bottom_right =  (node.position - 1) + map_width
        top_left =      (node.position - 1) - map_width
        
        # top left corner
        if node.is_left_edge and node.is_top_edge:
            candidate_nodes.append(node_map[bottom_right])
            candidate_nodes.append(node_map[bottom_center])
        
        # bottom left corner
        if node.is_left_edge and node.is_bottom_edge:
            candidate_nodes.append(node_map[top_right])
            candidate_nodes.append(node_map[top_center])

        # top right corner
        if node.is_right_edge and node.is_top_edge:
            candidate_nodes.append(node_map[bottom_center])
            candidate_nodes.append(node_map[bottom_left])
        
        # bottom right corner
        if node.is_right_edge and node.is_bottom_edge:
            candidate_nodes.append(node_map[top_center])
            candidate_nodes.append(node_map[top_left])
        
        # left edge
        if node.is_left_edge and not node.is_top_edge and not node.is_bottom_edge:
            candidate_nodes.append(node_map[top_center])
            candidate_nodes.append(node_map[top_right])
            candidate_nodes.append(node_map[bottom_right])
            candidate_nodes.append(node_map[bottom_center])
        
        # right edge
        if node.is_right_edge and not node.is_top_edge and not node.is_bottom_edge:
            candidate_nodes.append(node_map[top_center])
            candidate_nodes.append(node_map[top_left])
            candidate_nodes.append(node_map[bottom_left])
            candidate_nodes.append(node_map[bottom_center])
        
        # bottom, not corner
        if node.is_bottom_edge and not node.is_left_edge and not node.is_right_edge:    
            candidate_nodes.append(node_map[top_right])
            candidate_nodes.append(node_map[top_center])
            candidate_nodes.append(node_map[top_left])
        
        # top, not corner
        if node.is_top_edge and not node.is_left_edge and not node.is_right_edge:       
            candidate_nodes.append(node_map[bottom_right])
            candidate_nodes.append(node_map[bottom_center])
            candidate_nodes.append(node_map[bottom_left])

        # middle
        if not node.is_right_edge and not node.is_left_edge and not node.is_bottom_edge and not node.is_top_edge:
            candidate_nodes.append(node_map[top_right])
            if 0 <= top_center < len(node_map):
                candidate_nodes.append(node_map[top_center])
            candidate_nodes.append(node_map[top_left])
            candidate_nodes.append(node_map[bottom_right])
            if 0 <= bottom_center < len(node_map):
                candidate_nodes.append(node_map[bottom_center])
            candidate_nodes.append(node_map[bottom_left])

        # dont add nodes that have a cost of -1
        # since those nodes are off limits for the pathfinding algorithm
        for c in candidate_nodes: 
            if c.cost > 0: 
                node.adjacent_nodes.append(c)
    
    return node_map

nodes = get_node_list('inputfile')
node_map = create_map_of_nodes(nodes,3)

for n in node_map: 
    print('node: %2d | cost: %2d | connected to %d nodes' % (n.position, n.cost, len(n.adjacent_nodes)))


