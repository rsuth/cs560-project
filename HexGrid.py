from searchstrategies import Djikstra

class HexGrid:
    def __init__(self, nodes, position=226, g = Djikstra.g ):
        self.goal_state = 8
        self.nodes = nodes
        self.position = position
        self.initial=226
        self.g = gs

    def goal_test(self, position):
        return position == self.goal_state

    def result(self, action):
        return action

    def actions(self, position):
        actions = []
        if position < 219:
            if self.nodes[position+15] != -1:
                actions.append(position+15)
        if position < 226 and position % 15 != 8:
            if self.nodes[position+8] != -1:
                actions.append(position+8)
        if position < 226 and position % 15 != 1:
            if self.nodes[position+7] != -1:
                actions.append(position+7)
        if position > 15:
            if self.nodes[position-15] != -1:
                actions.append(position-15)
        if position > 8 and position % 15 != 8:
            if self.nodes[position-7] != -1:
                actions.append(position-7)
        if position > 8 and position % 15 != 1:
            if self.nodes[position-8] != -1:
                actions.append(position-8)
        return actions

class Node:

    def __init__(self, problem, position, cost, parent=None):
        "Create a search tree Node, derived from a parent."
        self.problem = problem # Save problem representation
        self.state = position
        self.parent = parent
        self.cost = cost

        self.f = 0

        # find new node's depth and parent and cost from start
        if self.parent:
            self.depth = parent.depth + 1
            self.total_cost = problem.g(self.parent, self)
        else:
            self.depth = 0  # root of search tree
            self.total_cost = self.cost


    def expand(self, problem):
        "List the nodes reachable in one step from this node."
        return [self.child_node(action)
                for action in problem.actions(self.state)]

    def child_node(self, action):
        # derive new state
        new_pos = self.problem.result(action)
        child_cost = self.problem.nodes[new_pos]
        # Create child
        return Node(self.problem, new_pos, child_cost, parent=self)

    def path(self):
        "Return a list of nodes forming the path from the root to this node."
        node, path = self, []
        # Chase parent pointers, appending each node as it is found
        while node:
            path.append(node)
            node = node.parent
        # List is from goal to initial state,
        # reverse to provide initial state to goal
        path.reverse()
        return path

    def get_total_cost(self):
        "get_f estimate of cost from initial node to goal node"
        return self.total_cost

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __lt__(self, node):
        return self.f < node.f

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return str(self.state)
