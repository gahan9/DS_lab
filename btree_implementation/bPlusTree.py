"""
some terminology of python:
_var => (convention only) underscore prefix is just a hint to programmer that a variable or method starting with a single underscore is intended for internal use
var_ => (convention only) to brake name conflict
__var => “dunders” (name mangling) rewrite the attribute name in order to avoid naming conflicts in subclasses.
            interpreter changes the name of the variable in a way that makes it harder to create collisions when the class is extended later.
"""

import math
from bisect import bisect_right, bisect_left
from collections import deque

__author__ = "Gahan Saraiya"


class InternalNode(object):
    """
    Class : B+ Tree Internal Node
    represents internal (non-leaf) node in B+ tree
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
        # return False if total keys exceeds max accommodated keys (degree - 1)
        return self.total_keys <= self.max_data

    def is_empty(self):
        return self.total_keys <= math.floor(self.degree / 2)


class LeafNode(object):
    """
    Class : B+ Tree Leaf Node
    represents leaf node in B+ tree
    """
    def __init__(self, degree=4):
        self.degree = degree
        self.keys = []  # data values
        self.sibling = None  # sibling node to point
        self.parent = None  # parent node - None for root node

    @property
    def is_leaf(self):
        return True

    @property
    def total_keys(self):
        return len(self.keys)

    @property
    def is_balanced(self):
        # return False if total keys exceeds max accommodated data (degree - 1)
        return self.total_keys <= self.degree - 1

    def is_empty(self):
        return self.total_keys <= math.ceil(self.degree / 2)


class BPlusTree(object):
    def __init__(self, degree=4):
        self.degree = degree
        self.__root = LeafNode(degree=degree)
        self.__leaf = self.__root

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

    def split_leaf(self, node):
        mid = (self.degree + 1) // 2
        new_leaf = LeafNode(self.degree)
        new_leaf.keys = node.keys[mid:]
        if node.parent is None:  # None and 0 are to be treated as different value
            parent_node = InternalNode(self.degree)  # create new parent for node
            parent_node.keys, parent_node.kids = [node.keys[mid].key], [node, new_leaf]
            node.par = new_leaf.par = parent_node
            self.__root = parent_node
        else:
            i = node.parent.children.index(node)
            node.parent.keys.insert(i, node.keys[mid].key)
            node.parent.children.insert(i + 1, new_leaf)
            new_leaf.parent = node.parent
        node.keys = node.keys[:mid]
        node.sibling = new_leaf

    def insert(self, value):
        node = self.__root

        if node.is_leaf:
            idx = bisect_right(node.keys, value)  # bisect and get index value of where to insert value in node.keys
            node.keys.insert(idx, value)
            if not node.is_balanced:
                self.split_leaf(node)
            else:
                return
        else:
            if not node.is_balanced:
                self.insert(self.split(node))
            else:
                _index = bisect_right(node.keys, value)
                self.insert(node.children[_index])

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
    b = BPlusTree()
    b.insert(5)
    b.insert(1)
    b.insert(15)
    print(b)
    print(b)
