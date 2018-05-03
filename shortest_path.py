#!/usr/bin/env python3

# CS560 Spring 2018 Group Project
# Minimal-Cost Path through a Hexagonally-Tiled Map
# Group 17 

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

    # define comparison of Node objects, used in the heap.
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
                if m is not None:
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
    # get input from file
    nodeList = get_node_list(path_to_file)
    
    node_map = []
    
    # build array of Node objects (not yet connected)
    for n in nodeList:
        node = Node(n[0], n[1])
        node_map.append(node)

    # set flags for the nodes that are on the edges
    assign_edge_nodes(node_map, map_width)

    # assign adjacent nodes, build the graph
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

    # push all the nodes onto the heap of unvisited nodes.
    for n in node_map:
        heapq.heappush(unvisited, (n, n.position))

    # start at the first node on the heap, the starting node.
    current = unvisited[0][0]
    
    # djikstras algorithm
    while current.is_goal_node is False:
        current = unvisited[0][0]
        for n in current.adjacent_nodes:
            if current.cost_to_get_here + n.cost < n.cost_to_get_here:
                n.cost_to_get_here = current.cost_to_get_here + n.cost
                n.got_here_from = current
        visited.append(heapq.heappop(unvisited))
        heapq.heapify(unvisited)

    # path array will store the path
    path = []
    
    # the last (goal) node
    n = visited[-1][0]
    
    # go backwards from the goal node, building the path.
    while n.is_starting_node is False:
        path.insert(0, n)
        n = n.got_here_from

    # add the first (starting) node
    path.insert(0, visited[0][0])

    return path

# main program:

node_map = create_node_map(sys.argv[1], 8)
shortest_path = djikstras_shortest_path(node_map)
cost = shortest_path[-1].cost_to_get_here

with open("output.txt", mode='w') as f:
    for n in shortest_path:
        f.write(str(n.position)+"\n")
    f.write("MINIMAL-COST PATH COSTS: %d" % cost)
    f.close()
