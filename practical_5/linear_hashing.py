#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementation of linear hashing
"""
from collections import OrderedDict
from math import log2, log


class LinearHashing(object):
    def __init__(self, *args, **kwargs):
        self.threshold = kwargs.get('threshold', 0.7)
        self.data_capacity_per_bucket = kwargs.get('data_capacity_per_bucket', 2)  # capacity to store data per bucket
        self.total_data = 0  # keep count of total inserted record
        self.buffer = {key: [] for key in range(2)}  # initial buffer
        self.index_counter = 0  # keep index counter from where we are supposed to start split in phase
        self.previous_phase = 1  # keeping phase number to reset index counter
        self.has_title = None

    @property
    def current_phase(self):
        return int(log2(len(self.buffer)))

    @property
    def buffer_capacity(self):
        return self.data_capacity_per_bucket * len(self.buffer)

    @property
    def threshold_outbound(self):
        return ((self.total_data + 1) / self.buffer_capacity) > self.threshold

    def hash_function(self, value, flag=0):
        """

        :param value: value on which hash function to be applied
        :param flag: set flag to 1 if splitting the bucket
        :return:
        """
        if not flag:
            # if no splitting require
            return value % (2 ** self.previous_phase)
        else:
            # if splitting require
            return value % (2 ** (self.current_phase + 1))

    def set_index_counter_if(self):
        """
        set index counter from where splitting to be done to 0 when phase changes
        :return: None
        """
        if self.current_phase != self.previous_phase:
            self.index_counter = 0
            self.previous_phase = self.current_phase

    def insert(self, value, print_status=0):
        """

        :param value: value to be inserted
        :param print_status: set to 1 if
        :return:
        """
        self.set_index_counter_if()
        buffer_capacity_beefore_insert = self.buffer_capacity
        if self.threshold_outbound:
            # buffer to be extend
            self.buffer[len(self.buffer)] = []
            buffer_index = self.hash_function(value)
            self.buffer[buffer_index] = self.buffer.setdefault(buffer_index, []) + [value]
            # bucket to be split
            bucket_to_split = self.buffer[self.index_counter]
            self.buffer[self.index_counter] = []
            for data in bucket_to_split:
                buffer_idx = self.hash_function(data, flag=1)
                self.buffer[buffer_idx] = self.buffer.setdefault(buffer_idx, []) + [data]
            self.index_counter += 1
        else:
            buffer_index = self.hash_function(value)
            # self.buffer[buffer_index].append(value)
            self.buffer[buffer_index] = self.buffer.setdefault(buffer_index, []) + [value]
        self.total_data += 1

        if print_status:
            data_dict = OrderedDict()
            data_dict["Sr No."] = self.total_data
            data_dict["Element"] = value
            data_dict["SplitIndex"] = self.index_counter
            data_dict["Phase"] = self.current_phase
            data_dict["Ratio"] = round(self.total_data / buffer_capacity_beefore_insert, 2)
            data_dict["Threshold"] = self.threshold
            # data_dict["Previous Phase"] = self.previous_phase
            if not self.has_title:
                print("\t".join(data_dict.keys()) + "\t" + "RESULT")
                self.has_title = True
            print("\t".join("{:^{}s}".format(str(v), len(k)) for k, v in data_dict.items()), end="\t")
            print(self.buffer)

        return True

    def delete(self):
        return NotImplementedError

    def __repr__(self):
        return "\n".join("{} -> {}".format(k, v) for k, v in self.buffer.items())

    def __str__(self):
        return "\n".join("{} -> {}".format(k, v) for k, v in self.buffer.items())


if __name__ == "__main__":
    capacity = 3
    print("Capacity per bucket (without chaining): {}".format(capacity))
    hash_bucket = LinearHashing(data_capacity_per_bucket=capacity, threshold=0.7)
    input_lis = [3, 2, 4, 1, 8, 14, 5, 10, 7, 24, 17, 13, 15]
    for i in input_lis:
        # print("STATUS:-------")
        # print(">>>>> ", l.buffer)
        # print("\n{2}\n{3} Inserting: {0:-3d} (Iteration :{1}) {3}".format(i, hash_bucket.total_data + 1, "#"*50, "#"*5))
        result = hash_bucket.insert(i, print_status=1)
        # if result:
        #     print("Value {} inserted successfully.\n{}".format(i, "#"*50))
    print(hash_bucket)
