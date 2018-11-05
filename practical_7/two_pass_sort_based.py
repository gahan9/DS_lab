#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementation of sorting based two pass algorithm
"""
import os
import math

from itertools import islice
from faker import Faker

fak = Faker()


class Iterator(object):
    """
    Iterator class to add tuple in form of table
    attributes -> <attrib1, attrib2, attrib3,...>
    Adding values
    values -> <val1, val2, val3, ....>
    """

    def __init__(self, attribute_tuple, file_path, *args, **kwargs):
        """
        :param attribute_tuple: attribute tuple in form of string containing attributes of file (if to be created)
        :param file_path: location of data file
        :param args:
        :param kwargs:
        """
        self.attributes = attribute_tuple
        self.file_path = file_path
        self.write_back_path = kwargs.get("write_back_path", "temp.write")
        self.separator = "\t"
        self.records_per_block = kwargs.get("records_per_block", 30)
        self.initialize_file()

    @staticmethod
    def read_in_chunks(file_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    @property
    def free_memory(self):
        # calculate how many blocks can be accommodated in memory buffer
        num_lines = sum(1 for line in open(self.file_path))
        no_of_records = num_lines - 2  # remove header line and last new line
        return 101  # for now return available memory statically for basic implementation

    @property
    def total_blocks(self):
        # calculate total number of blocks by record size
        return math.ceil(self.total_records / self.records_per_block)

    @property
    def total_records(self):
        # calculate total number of blocks by record size
        num_lines = sum(1 for line in open(self.file_path))
        no_of_records = num_lines - 2  # remove header line and last empty line
        return no_of_records

    @property
    def can_be_one_pass(self):
        # return False  # for testing
        return True if self.total_blocks < self.free_memory else False

    @property
    def can_be_two_pass(self):
        return True if self.free_memory > math.ceil(math.sqrt(self.total_blocks)) else False

    def initialize_file(self):
        # check if file exits or not
        if os.path.exists(self.file_path):
            pass
        else:
            # create file with header if file not exist
            with open(self.file_path, "w") as f:
                f.write(self.separator.join(self.attributes))
                f.write("\n")
        return True

    def add_dummy_data(self, number_of_record=100):
        """

        :param number_of_record: number of records to be inserted in given file path
        :return:
        """
        with open(self.file_path, "a+") as file:  # open file in append mode
            for _ in range(number_of_record):
                f = fak.profile()
                data_tuple = (
                    f['name'], f['ssn'], f['sex'], f['job'].replace("\n", ""), f['company'].replace("\n", ""), f['address'].replace("\n", "")
                )
                data_string = self.separator.join(data_tuple) + "\n"
                file.write(data_string)

    @staticmethod
    def summary(total_results, total_records):
        print("-"*30)
        print("Total Results: {}".format(total_results))
        print("Total Records: {}".format(total_records))
        return True

    def get_distinct(self, attribute=None, only_summary=True):
        sort_key = attribute if attribute else "ssn"
        _result_set = []
        if self.can_be_one_pass:
            print("Processing One Pass Algorithm")
            with open(self.file_path, "r") as f:
                content = f.read().split("\n")
            for record in content:
                if record not in _result_set:
                    _result_set.append(record)
        elif self.can_be_two_pass:
            # apply 2 pass algorithm to sort and use operation on database
            print("Processing Two Pass Algorithm")
            f = open(self.file_path, "r")
            writer = open(self.write_back_path, "w")
            header = f.readline()
            writer.write(header)
            _idx = header.split(self.separator).index(sort_key)
            while True:
                # read blocks one by one
                block_records = list(islice(f, self.free_memory - 1))
                if not block_records:
                    break
                else:
                    # sort sublist by "ssn" or any other attribute
                    sorted_sublist = sorted(block_records, key=lambda x: x.split(self.separator)[_idx])
                    writer.writelines(sorted_sublist)
                # write sorted block/sublist data back to disk(secondary memory)
            f.close()
            writer.close()
            # read sublist from each block and output desire result
            last_read = ""
            total_results = 0
            # for line in open(self.write_back_path, "r"):
            file = open(self.write_back_path, "r")
            for index, line in enumerate(file.readlines()):
                # TODO: fix pass 2 here...
                # for i in range(self.free_memory - 1):
                #     pass
                current_record = line.split(self.separator)[_idx]
                if current_record and current_record != last_read:
                    if not only_summary:
                        print(current_record)
                    last_read = current_record
                    total_results += 1
            self.summary(total_results-2, self.total_records)
        else:
            # can not proceed all given blocks with memory constraint
            print("Require more than two pass to handle this large data")
        return _result_set


if __name__ == "__main__":
    table = Iterator(attribute_tuple=("name", "ssn", "gender", "job", "company", "address"),
                     file_path="iterator.dbf")
    # table.get_distinct("name", only_summary=True)
    # table.get_distinct("job", only_summary=True)
    # table.get_distinct("ssn", only_summary=True)
    table.get_distinct("name", only_summary=True)
