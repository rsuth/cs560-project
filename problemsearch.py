from HexGrid import Node
from queues import PriorityQueue
from explored import Explored
import time

def graph_search(problem):
    """graph_search(problem) - Given a problem representation
    attempt to solve the problem.
    Returns a tuple (path, path_cost) where:
    path - list of actions to solve the problem or None if no solution was found
    path_cost - Cost to execute the given path
    """

    initial_node = Node(problem, problem.initial, problem.nodes[problem.initial])

    frontier_nodes = PriorityQueue(min, Node.get_total_cost)
    frontier_nodes.append(initial_node)

    explored_nodes = Explored()
    nodes_explored = 0

    while len(frontier_nodes)>0:
        # Pop the next node from the frontier, add it to the explored set,
        # and increment the nodes_explored counter
        current_node = frontier_nodes.pop()
        explored_nodes.add(current_node.state)
        nodes_explored += 1

        #Check to see if the current node is a goal state
        if current_node.problem.goal_test(current_node.state):
            return (current_node.path(), current_node.total_cost)

        #Generate the possible actions from the current_node
        successor_nodes = current_node.expand(problem)

        #For each successor_node, if it hasn't been explored, add it to the frontier set
        for node in successor_nodes:
            if explored_nodes.exists(node.state) is False:
                frontier_nodes.append(node)

    print("No solution found.")
    return(None,nodes_explored)
