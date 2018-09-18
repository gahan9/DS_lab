class InternalNode(object):
    """
    Class : B Tree Node
    """
    def __init__(self, degree=4):
        """
        initialize B tree node
        :param degree: specify degree of btree  # default degree set to 4
        """
        self.degree = degree
        self.max_data = self.degree-1  # number of keys per node
        self.keys = []  # store keys/data values
        self.children = []  # store child nodes (list of instances of BtreeNode); empty list if node is leaf node
        self.parent = None

    def __repr__(self):
        return " | ".join(map(str, self.keys))

    @property
    def is_leaf(self):
        return False

    @property
    def total_keys(self):
        return len(self.keys)

    @property
    def is_balanced(self):
        return self.total_keys <= self.max_data


class Btree(object):
    def __init__(self, degree=4):
        self.degree = degree
        self.root = InternalNode(degree=degree)

    def search_node(self, start_node, value):
        """

        :param start_node: get root or any non leaf node
        :param value: value to be search
        :return: most matching leaf node
        """
        if start_node.is_leaf:
            return start_node
        else:
            for index in range(len(start_node.keys)-1):  # search for next possible node
                if value < start_node.keys[index]:  # key is greater than value to be search
                    return self.search_node(start_node.children[0], value)
                elif start_node.keys[index] <= value < start_node.keys[index+1]:
                    return self.search_node(start_node.children[index], value)
                else:
                    return self.search_node(start_node.children[index+1], value)

    def search(self, value):
        """
        :param value: value to be search
        :return: leaf node containing value else False
        tuple of 3 values (status, msg, node)
        0 - status of success or failure
        1 - message status
        2 - last explored node
        """
        status, msg, node = None, "", None
        if not self.root.keys:
            # initially no keys/data value - initialize root first
            # msg += "No data in tree..!!"
            status, msg, node = False, "No data in tree..!!", self.root
        else:
            node = self.search_node(self.root, value)
            if node:
                # if current node is leaf then check if value exist in current node or not
                try:
                    node.keys.index(value)
                    status, msg, node = True, "Value found in root node", node
                except ValueError:
                    status, msg, node = False, "Value not found", self.root
        return status, msg, node

    def split(self, node):
        center_idx = len(node.keys) // 1  # center node index
        median = node.keys[center_idx - 1]  # key to be shift to upper level
        sibling1_node, sibling2_node = BtreeNode(), BtreeNode()
        if not node.parent:
            # split root node for overflow
            node.keys = [median]
            node.children = [sibling1_node, sibling2_node]
            sibling1_node.parent = node
            sibling2_node.parent = node
            sibling1_node.keys, sibling2_node.keys = node.keys[:center_idx], node.keys[center_idx:]

    def insert(self, value):
        if not self.root.keys:
            # initially no keys/data value - initialize root
            self.root.keys.insert(0, value)
            status, msg, node = True, "LOL!! it was first value!!", self.root
        else:
            status, msg, node = self.search(value)
            for index in range(len(node.keys)):
                if value < node.keys[index]:  # key is greater than value to be search
                    node.keys.insert(index, value)
                elif node.keys[index] <= value < node.keys[index + 1]:
                    node.keys.insert(index, value)
                else:
                    node.keys.insert(index+1, value)
            if node.is_balanced:
                status, msg = True, "Balanced - No Split Require"
            else:
                msg = "splitting require"
                self.split(node)
        print(msg, node.keys)
        return status, msg, node


if __name__ == "__main__":
    b = Btree()
    b.insert(5)
    b.insert(1)
    b.insert(15)
    print(b.root)
    print(b.root)
