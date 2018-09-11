class BtreeNode(object):
    def __init__(self, order=4):
        self.order = order
        self.keys = []
        self.children = []
        self.parent = None

    @property
    def enum_child(self):
        return enumerate(self.children)

    @property
    def enum_keys(self):
        return enumerate(self.keys)

    @property
    def is_root(self):
        return not self.parent

    @property
    def is_leaf(self):
        return False if self.children else True

    @property
    def total_keys(self):
        return len(self.children)

    @property
    def is_balanced(self):
        # check if node is balanced or not
        if self.is_root:
            return True if self.total_keys < self.order else False
        else:
            pass

    @staticmethod
    def insert(node):
        # TODO: implementation
        if node.is_balanced:
            pass

    def search(self):
        # TODO: searching
        pass


if __name__ == "__main__":
    b = BtreeNode()
