import math

class Djikstra:
    "Lowest cost first"
    @classmethod
    def g(cls, parentnode, childnode):
        return parentnode.total_cost + childnode.cost


    @classmethod
    def h(cls, state):
        return 0

class aStar:
    "Lowest cost first + heuristic"
    @classmethod
    def g(cls, parentnode, childnode):
        return parentnode.total_cost + childnode.cost


    @classmethod
    def h(cls, state):
        raise NotImplementedError
