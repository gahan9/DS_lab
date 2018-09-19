#!usr/bin/python3
# coding=utf-8
"""
some terminology of python:
_var => (convention only) underscore prefix is just a hint to programmer that a variable or method starting with a single underscore is intended for internal use
var_ => (convention only) to brake name conflict
__var => “dunders” (name mangling) rewrite the attribute name in order to avoid naming conflicts in subclasses.
            interpreter changes the name of the variable in a way that makes it harder to create collisions when the class is extended later.
"""

import math
import logging
import os
from datetime import datetime
from bisect import bisect_right, bisect_left
from collections import deque

__author__ = "Gahan Saraiya"

LOG_DIR = "."
logger = logging.getLogger('bPlusTree')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(name)-8s - %(levelname)s]: %(message)s',
                    datefmt='[%Y-%d-%m_%H.%M.%S]',
                    filename=os.path.join(LOG_DIR, 'b_plus_tree_{}.log'.format(datetime.now().strftime('%Y-%d-%m_%H.%M.%S'))),
                    filemode='w')
ch = logging.StreamHandler()  # create console handler with a higher log level
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(name)-8s - %(levelname)s]: %(message)s')
# fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)
log = logger.debug
log = print


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

    def __repr__(self):
        return " | ".join(map(str, self.keys))

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

    def search_key(self, node, key):
        if node.is_leaf:
            _index = bisect_left(node.keys, key)
            return _index, node
        else:
            _index = bisect_right(node.keys, key)
            return self.search_key(node.children[_index], key)

    def search(self, start=None, end=None):
        """

        :param start: specify start node to search range for
        :param end: specify end node for range search
        :return:
        """
        _result = []
        node = self.__root
        leaf = self.__leaf

        if start is None:
            while True:
                for val in leaf.keys:
                    if val <= end:
                        _result.append(val)
                    else:
                        return _result
                if leaf.sibling is None:
                    return _result
                else:
                    leaf = leaf.sibling
        elif end is None:
            _index, leaf = self.search_key(node, start)
            _result.extend(leaf.keys[_index:])  # equivalent to _result + leaf
            while True:
                if leaf.sibling is None:
                    return _result
                else:
                    leaf = leaf.sibling
                    _result.extend(leaf.keys)
        else:
            if start == end:
                _index, _node = self.search_key(node, start)
                try:
                    if _node.keys[_index] == start:
                        _result.append(_node.keys[_index])
                        return _result
                    else:
                        return _result
                except IndexError:
                    return _result
            else:
                _index1, _node1 = self.search_key(node, start)
                _index2, _node2 = self.search_key(node, end)
                if _node1 is _node2:
                    if _index1 == _index2:
                        return _result
                    else:
                        _result.extend(_node1.keys[_index1:_index2])
                        return _result
                else:
                    _result.extend(_node1.keys[_index1:])
                    node_ = _node1
                    while True:
                        if _node1.sibling == _node2:
                            _result.extend(_node2.keys[:_index2 + 1])
                            return _result
                        else:
                            _result.extend(node_.sibling.keys)
                            node_ = node_.sibling

    def traverse(self):
        _result, _leaf = [], self.__leaf
        while True:
            _result.extend(_leaf.keys)
            if _leaf.sibling is None:
                return _result
            else:
                _leaf = _leaf.sibling

    def pretty_print(self):
        print("B+ Tree: \n")
        queue = deque()
        height = 0
        queue.append([self.__root, height])
        while True:
            try:
                node, height_ = queue.popleft()
            except IndexError:
                return
            else:
                if not node.is_leaf:
                    print("{} The height is {}".format(node.keys, height_))
                    if height_ == height:
                        height += 1
                    queue.extend([[i, height] for i in node.children])
                else:
                    print("{} leaf is >> {}".format([i for i in node.keys], height_))

    def insert(self, value):
        node = self.__root
        # log("parent:{} leaf:{} node:{}\tkeys:{}\t children:{}".format(node.parent, node.is_leaf, node, node.keys, getattr(node, 'children', '0')))

        def split_leaf_node(node):
            mid = (self.degree + 1) // 2  # integer division in python3
            new_leaf = LeafNode(self.degree)
            new_leaf.keys = node.keys[mid:]
            if node.parent is None:  # None and 0 are to be treated as different value
                parent_node = InternalNode(self.degree)  # create new parent for node
                parent_node.keys, parent_node.kids = [node.keys[mid]], [node, new_leaf]
                node.parent = new_leaf.parent = parent_node
                self.__root = parent_node
            else:
                i = node.parent.children.index(node)
                node.parent.keys.insert(i, node.keys[mid])
                node.parent.children.insert(i + 1, new_leaf)
                new_leaf.parent = node.parent
            node.keys = node.keys[:mid]
            node.sibling = new_leaf
            print(node, node.sibling, self.__root.children, sep=" --- ")

        def split_internal_node(node_):
            mid = self.degree // 2  # integer division in python3
            new_node = InternalNode(self.degree)
            new_node.keys = node_.keys[mid:]
            new_node.children = node_.children[mid:]
            new_node.parent = node_.parent
            for child in new_node.children:
                child.parent = new_node  # assign parent to every new child of current node
            if node_.parent is None:  # again Note that None and 0 are not same but both treated as False in boolean
                # need to make new root if we are to split root node
                new_root = InternalNode(self.degree)
                new_root.keys = [node_.keys[mid - 1]]
                new_root.children = [node_, new_node]
                node_.parent = new_node.parent = new_root  # set parent of newly created node
                self.__root = new_root  # set new ROOT node
            else:
                # if node is not root internal node
                _index = node_.parent.children.index(node_)
                node_.parent.keys.insert(_index, node_.keys[mid - 1])
                node_.parent.children.insert(_index + 1, new_node)
            node_.keys = node_.keys[:mid - 1]
            node_.children = node_.children[:mid]
            return node_.parent

        def insert_node(node):
            if node.is_leaf:  # logic for leaf node
                _index = bisect_right(node.keys, value)  # bisect and get index value of where to insert value in node.keys
                node.keys.insert(_index, value)
                if not node.is_balanced:
                    split_leaf_node(node)
                else:
                    return
            else:  # logic for internal node
                if not node.is_balanced:
                    self.insert(split_internal_node(node))
                else:
                    _index = bisect_right(node.keys, value)
                    print(node.keys, node.children, _index)
                    insert_node(node.children[_index])

        insert_node(node)

    def merge(self, node, index):
        if node.children[index].is_leaf:
            node.children[index].keys = node.children[index].keys + node.children[index + 1].keys
            node.children[index].sibling = node.children[index + 1].sibling
        else:
            node.children[index].keys = node.children[index].keys + [node.keys[index]] + node.children[index + 1].keys
            node.children[index].children = node.children[index].children + node.children[index + 1].children
        node.children.remove(node.children[index + 1])
        node.keys.remove(node.children[index])
        if node.keys:
            return node
        else:
            node.children[0].parent = None
            self.__root = node.children[0]
            del node
            return self.__root

    @staticmethod
    def traverse_left_to_right(node, index):
        if node.children[index].is_leaf:
            node.children[index + 1].keys.insert(0, node.children[index].keys[-1])
            node.children[index].keys.pop()
            node.keys[index] = node.children[index + 1].keys[0]
        else:
            node.children[index + 1].children.insert(0, node.children[index].children[-1])
            node.children[index].children[-1].parent = node.children[index + 1]
            node.children[index + 1].keys.insert(0, node.keys[index])
            node.children[index].children.pop()
            node.children[index].keys.pop()

    @staticmethod
    def traverse_right_to_left(node, index):
        if node.children[index].is_leaf:
            node.children[index].keys.append(node.children[index + 1].keys[0])
            node.children[index + 1].keys.remove(node.children[index + 1].keys[0])
            node.keys[index] = node.children[index + 1].keys[0]
        else:
            node.children[index].children.append(node.children[index + 1].children[0])
            node.children[index + 1].children[0].parent = node.children[index]
            node.children[index].keys.append(node.keys[index])
            node.keys[index] = node.children[index + 1].children[0]
            node.children[index + 1].children.remove(node.children[index + 1].children[0])
            node.children[index + 1].keys.remove(node.children[index + 1].keys[0])

    def delete(self, value, node=None):
        node = self.__root if not node else node
        if node.is_leaf:
            _index = bisect_left(node.keys, value)
            try:
                node_ = node.keys[_index]
            except IndexError:
                return -1
            else:
                if node_ != value:
                    return -1
                else:
                    node.keys.remove(value)
                    return 0
        else:
            _index = bisect_right(node.keys, value)
            if _index == len(node.keys):
                if not node.children[_index].is_empty:
                    return self.delete(node.children[_index], value)
                elif not node.children[_index - 1].is_empty:
                    self.traverse_left_to_right(node, _index - 1)
                    return self.delete(node.children[_index], value)
                else:
                    return self.delete(self.merge(node, _index), value)


if __name__ == "__main__":
    # test_lis = [0, 1, 11, 1, 2]
    # test_lis = [i for i in range(1, 4 + 1)]
    b = BPlusTree(degree=4)
    for val in range(1, 6):
        b.insert(val)
    # b.pretty_print()
