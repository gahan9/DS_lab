#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementation of linear hashing
"""


class LinearHashing(object):
    global_bucket = {}
    total_data = 0

    def __init__(self, *args, **kwargs):
        self.threshold = kwargs.get('threshold', 0.7)
        self.bucket_size = kwargs.get('bucket_size', 3)
        self.data_capacity = kwargs.get('data_capacity', 2)

    @property
    def threshold_outbound(self):
        return (self.total_data / self.data_capacity) < self.threshold

    @property
    def (self):
        return (self.total_data / self.data_capacity) < self.threshold

    def insert(self, value):
        return NotImplementedError

    def delete(self):
        return NotImplementedError


if __name__ == "__main__":
    l = LinearHashing()
    l.insert(5)

