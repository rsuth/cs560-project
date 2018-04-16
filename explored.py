class Explored(object):
    "Maintain an explored set.  Assumes that states are hashable"

    def __init__(self):
        "__init__() - Create an empty explored set"
        self.explored_states = {}

    def exists(self, state):
        """exists(state) - Has this state already been explored?
        Returns True or False, state must be hashable
        """
        if hash(state) in self.explored_states:
            if state in self.explored_states[hash(state)]:
                return True
        return False

    def add(self, state):
        """add(state) - add given state to the explored set.
        state must be hashable and we asssume that it is not already in set
        """
        if hash(state) in self.explored_states:
            self.explored_states[hash(state)].append(state)
        else:
            self.explored_states[hash(state)] = [state]
