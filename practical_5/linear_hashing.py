#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementation of linear hashing
"""
from math import log2

class LinearHashing(object):
    def __init__(self, *args, **kwargs):
        self.threshold = kwargs.get('threshold', 0.7)
        self.data_capacity = kwargs.get('data_capacity', 2)  # capacity to store data per bucket
        self.total_data = 0
        self.buffer = {0: [], 1: []}
        self.index_counter = 0
        self.previous_phase = 1

    @property
    def current_phase(self):
        return int(log2(len(self.buffer)))

    @property
    def buffer_capacity(self):
        return self.data_capacity * len(self.buffer)

    @property
    def threshold_outbound(self):
        return (self.total_data / self.buffer_capacity) > self.threshold

    def hash_function(self, value, flag=0):
        if not flag:
            # if no splitting require
            return value % (2**self.current_phase)
        else:
            # if splitting require
            return value % (2**(self.current_phase + 1))

    def set_index_counter_if(self):
        # set index counter from where splitting to be done to 0 when phase changes
        if self.current_phase != self.previous_phase:
            self.index_counter = 0

    def insert(self, value):
        self.set_index_counter_if()

        if self.threshold_outbound:
            # buffer to be extend
            buffer_index = self.hash_function(value, flag=1)
            self.buffer[buffer_index] = self.buffer.setdefault(buffer_index, []) + [value]
            # bucket to be split
            bucket_to_split = self.buffer[self.index_counter]
            self.buffer[self.index_counter] = []
            for data in bucket_to_split:
                buffer_index = self.hash_function(data)
                self.buffer[buffer_index] = self.buffer.setdefault(buffer_index, []) + [data]
            self.index_counter += 1
        else:
            buffer_index = self.hash_function(value)
            # self.buffer[buffer_index].append(value)
            self.buffer[buffer_index] = self.buffer.setdefault(buffer_index, []) + [value]
        self.total_data += 1

    def delete(self):
        return NotImplementedError

    def __repr__(self):
        return "\n".join("{} -> {}".format(k, v) for k, v in self.buffer.items())

    def __str__(self):
        return "\n".join("{} -> {}".format(k, v) for k, v in self.buffer.items())

if __name__ == "__main__":
    l = LinearHashing()
    input_lis = [3, 2, 4, 1, 8, 14, 5, 10, 7, 24, 17, 13, 15]
    for i in input_lis:
        print("inserting: ", i)
        print("STATUS:-------")
        print("INDEX: {}\nCURRENT PHASE: {} \t PREVIOUS PHASE: {}".format(l.index_counter, l.current_phase, l.previous_phase))
        print("-"*40)
        print(">>>>> ", l.buffer)
        l.insert(i)
    print(l)