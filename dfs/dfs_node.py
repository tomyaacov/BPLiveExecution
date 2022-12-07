class DFSNode:
    def __init__(self, prefix, _id):
        self.id = _id
        self.prefix = prefix
        self.transitions = {}
        self.must_finish = None
        self.rewards = {}

    def __key(self):
        return self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

