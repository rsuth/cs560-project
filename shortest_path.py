import re
import sys
import heapq
import time

INFINITY = sys.maxsize

# Node class used to store properties of each node
class Node():
    def __init__(self, position, cost):
        self.position = position
        self.cost = cost
        self.adjacent_nodes = []
        self.is_left_edge = False
        self.is_right_edge = False
        self.is_top_edge = False
        self.is_bottom_edge = False
        self.is_goal_node = False
        self.is_starting_node = False
        self.cost_to_get_here = INFINITY
        self.visited = False
        self.got_here_from = None

    def __lt__(self, other):
        return self.cost_to_get_here < other.cost_to_get_here

    def __le__(self, other):
        return self.cost_to_get_here <= other.cost_to_get_here

    def __gt__(self, other):
        return self.cost_to_get_here > other.cost_to_get_here

    def __ge__(self, other):
        return self.cost_to_get_here >= other.cost_to_get_here

# takes path to the file representing the nodes in the hexagonal grid
# returns a list of tuples (num, cost)
def get_node_list(path_to_file):
    nodes = []
    with open(path_to_file) as f:
        try:
            for line in f:
                m = re.match(re.compile(r'(\d+)\s+(-?\d+)'), line)
                pos = int(m.group(1))
                cost = int(m.group(2))
                nodes.append((pos, cost))
        except AttributeError as e:
            print("invalid line in input file:\n%s" % line)
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
# and has the form (position, cost). returns a list of Node objects
# where each Node stores a list of every node that is adjacent
def create_node_map(path_to_file, map_width):
    nodeList = get_node_list(path_to_file)
    node_map = []
    for n in nodeList:
        node = Node(n[0], n[1])
        node_map.append(node)

    assign_edge_nodes(node_map, map_width)

    for node in node_map:
        candidate_nodes = []
        top_center = (node.position - 1) - (2*map_width - 1)
        bottom_center = (node.position - 1) + (2*map_width - 1)
        top_right = (node.position - 1) - (map_width - 1)
        bottom_left = (node.position - 1) + (map_width - 1)
        bottom_right = (node.position - 1) + map_width
        top_left = (node.position - 1) - map_width

        # top left corner
        if node.is_left_edge and node.is_top_edge:
            candidate_nodes.append(node_map[bottom_right])
            candidate_nodes.append(node_map[bottom_center])

        # bottom left corner
        if node.is_left_edge and node.is_bottom_edge:
            candidate_nodes.append(node_map[top_right])
            candidate_nodes.append(node_map[top_center])
            node.is_starting_node = True
            node.cost_to_get_here = node.cost

        # top right corner
        if node.is_right_edge and node.is_top_edge:
            candidate_nodes.append(node_map[bottom_center])
            candidate_nodes.append(node_map[bottom_left])
            node.is_goal_node = True

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
            if c.cost >= 0:
                node.adjacent_nodes.append(c)

    return node_map

# takes a list of Node objects and returns an in order list of
# Node objects on the shortest path
def djikstras_shortest_path(node_map):
    visited = []
    unvisited = []

    for n in node_map:
        heapq.heappush(unvisited, (n, n.position))

    current = unvisited[0][0]
    while current.is_goal_node is False:
        current = unvisited[0][0]
        for n in current.adjacent_nodes:
            if current.cost_to_get_here + n.cost < n.cost_to_get_here:
                n.cost_to_get_here = current.cost_to_get_here + n.cost
                n.got_here_from = current
        visited.append(heapq.heappop(unvisited))
        heapq.heapify(unvisited)

    n = visited[-1][0]
    path = []

    while n.is_starting_node is False:
        path.insert(0, n)
        n = n.got_here_from

    path.insert(0, visited[0][0])  # add the last (starting) node

    return path


start = time.time()

node_map = create_node_map('INPUT.TXT', 8)
shortest_path = djikstras_shortest_path(node_map)
cost = shortest_path[-1].cost_to_get_here


for n in shortest_path:
    print(n.position)
print("MINIMAL-COST PATH COSTS: %d" % cost)

end = time.time()
print("completed in %f seconds" % (end-start))
