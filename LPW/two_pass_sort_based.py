#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementation of sorting based two pass algorithm
for difference operator
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

    def __init__(self, attribute_tuple, data_one_path, data_two_path, *args, **kwargs):
        """
        :param attribute_tuple: attribute tuple in form of string containing attributes of file (if to be created)
        :param data_one_path: path to first data file
        :param data_two_path: path to second data file
        :param args:
        :param kwargs:
        """
        self.attributes = attribute_tuple
        self.data_one_path = data_one_path
        self.data_two_path = data_two_path
        self.write_back_folder = kwargs.get("write_back_path", "phase_one_write_back")
        self.separator = "\t"
        self.records_per_block = kwargs.get("records_per_block", 30)
        self.initialize_file()
        # print("{0}\n{1}Consideration{1}\n"
        #       "Records per block: {2}\n"
        #       "Total Records: {3}\n{0}\n".format("#"*50, "-"*10, self.records_per_block, self.total_records)
        #       )

    @property
    def free_memory(self):
        # calculate how many blocks can be accommodated in memory buffer
        num_lines = sum(1 for line in open(self.data_one_path))
        no_of_records = num_lines - 2  # remove header line and last new line
        return 101  # for now return available memory statically for basic implementation

    @property
    def total_blocks(self):
        # calculate total number of blocks by record size
        return math.ceil(self.total_records / self.records_per_block)

    @property
    def total_records(self):
        # calculate total number of blocks by record size
        num_lines = sum(1 for line in open(self.data_one_path))
        no_of_records = num_lines - 2  # remove header line and last empty line
        return no_of_records

    @property
    def can_be_one_pass(self):
        return False  # for testing
        # return True if self.total_blocks < self.free_memory else False

    @property
    def can_be_two_pass(self):
        return True  # for testing
        # return True if self.free_memory > math.ceil(math.sqrt(self.total_blocks)) else False

    def initialize_file(self):
        # create write back directory for phase 1
        os.makedirs(self.write_back_folder, exist_ok=True)
        # check if file exits or not
        for file_path in [self.data_one_path, self.data_two_path]:
            if os.path.exists(file_path):
                pass
            else:
                # create file with header if file not exist
                with open(file_path, "w") as f:
                    f.write(self.separator.join(self.attributes))
                    f.write("\n")
        return True

    @staticmethod
    def summary(total_results, total_records):
        print("-"*30)
        print("Total Results: {}".format(total_results))
        print("Total Records: {}".format(total_records))
        return True

    @staticmethod
    def split_file_in_blocks(file_obj, split_size):
        blocks = []
        while True:
            block_records = list(islice(file_obj, split_size))
            if not block_records:
                break
            else:
                blocks.append(block_records)
        return blocks

    @staticmethod
    def create_file_obj(attribute):
        file_name = "output_distinct_on_{}.tsv".format(attribute)
        return open(file_name, "w")

    def difference_of(self, on_attribute, only_summary=True, output_write=False):
        output_obj = self.create_file_obj(on_attribute) if output_write else None
        sort_key = on_attribute
        print("{0}\n DIFFERENCE ON ATTRIBUTE {1}\n{0}".format('#'*50, sort_key))
        _result_set = []
        if self.can_be_one_pass:
            print("Processing One Pass Algorithm")
            print("Exiting as the program meant to be use two-pass sort based algorithm")
            raise NotImplementedError
        elif self.can_be_two_pass:
            # apply 2 pass algorithm to sort and use operation on database
            print("Processing Two Pass Algorithm")

            # PHASE 1 -----------------------------------------------------------------------------------------------
            file_pointer_one = open(self.data_one_path, "r")
            file_pointer_two = open(self.data_two_path, "r")
            header_one = file_pointer_one.readline()
            header_two = file_pointer_two.readline()
            # writer = open(self.write_back_path, "w")
            # writer.write(header)
            _idx = header_one.split(self.separator).index(sort_key)
            file_order_one = 0  # finally a number contains total number of split/sublist file
            file_order_two = 0  # finally a number contains total number of split/sublist file
            for i, f in enumerate([file_pointer_one, file_pointer_two]):
                file_order = 0
                while True:
                    block_records = list(islice(f, self.free_memory - 1))
                    # read blocks one by one
                    if not block_records:
                        break
                    else:
                        file_order += 1
                        # sort sublist by "ssn" or any other attribute
                        writer = open(os.path.join(self.write_back_folder, "temp{}_00{}".format(i+1, file_order)), "w")
                        # writer.write(header)
                        sorted_sublist = sorted(block_records, key=lambda x: x.split(self.separator)[_idx])
                        # write sorted block/sublist data back to disk(secondary memory)
                        writer.writelines(sorted_sublist)
                        writer.close()
                f.close()
                if i == 0:
                    file_order_one = file_order
                else:
                    file_order_two = file_order


            # PHASE 2 -----------------------------------------------------------------------------------------------
            # Performing difference of first - second
            partition_ptr_lis_one = [open(os.path.join(self.write_back_folder, "temp1_00{}".format(i)), "r")
                                     for i in range(1, file_order_one+1)]
            partition_ptr_lis_two = [open(os.path.join(self.write_back_folder, "temp2_00{}".format(i)), "r")
                                     for i in range(1, file_order_two+1)]
            phase2_data_one = [i.readline().split(self.separator)[_idx] for i in partition_ptr_lis_one]  # get first element from each sublist
            phase2_data_two = [i.readline().split(self.separator)[_idx] for i in partition_ptr_lis_two]  # get first element from each sublist
            # read sublist from each block and output desire result
            total_results = 0
            total_ignored = 0
            # for line in open(self.write_back_path, "r"):
            while any(phase2_data_one):  # loop over data from whose you will perform minus operator
                temp_lis_one = list(filter(None, phase2_data_one)) if None in phase2_data_one else phase2_data_one
                temp_lis_two = list(filter(None, phase2_data_two)) if None in phase2_data_two else phase2_data_two
                min_one = min(temp_lis_one)
                chunk_no_one = phase2_data_one.index(min_one)
                next_record_one = partition_ptr_lis_one[chunk_no_one].readline()
                if temp_lis_two:
                    min_two = min(temp_lis_two)
                    chunk_no_two = phase2_data_two.index(min_two)
                    next_record_two = partition_ptr_lis_two[chunk_no_two].readline()
                    if min_one < min_two:
                        if next_record_one:
                            phase2_data_one[chunk_no_one] = next_record_one.split(self.separator)[_idx]
                        else:
                            # file/sublist has nothing to load/read
                            del partition_ptr_lis_one[chunk_no_one]
                            del phase2_data_one[chunk_no_one]
                    elif min_one > min_two:
                        if next_record_two:
                            phase2_data_two[chunk_no_two] = next_record_one.split(self.separator)[_idx]
                        else:
                            # file/sublist has nothing to load/read
                            del partition_ptr_lis_two[chunk_no_two]
                            del phase2_data_two[chunk_no_two]
                    elif min_one == min_two:
                        for i, next_record in enumerate([next_record_one, next_record_two]):
                            if i == 0:
                                phase2_data, chunk_no, partition_ptr_lis = phase2_data_one, chunk_no_one, partition_ptr_lis_one
                            else:
                                phase2_data, chunk_no, partition_ptr_lis = phase2_data_two, chunk_no_two, partition_ptr_lis_two
                            if next_record:
                                phase2_data[chunk_no] = next_record_one.split(self.separator)[_idx]
                            else:
                                # file/sublist has nothing to load/read
                                del partition_ptr_lis[chunk_no]
                                del phase2_data[chunk_no]
                        if min_one != min_two:
                            if not only_summary:
                                print(min_one)
                            if output_write:
                                output_obj.write(min_one + "\n")
                            total_ignored += 1
                else:
                    # if there is data in first data table but no data in second data table
                    if min_one:
                        if not only_summary:
                            print(min_one)
                        if output_write:
                            output_obj.write(min_one + "\n")
                    if next_record_one:
                        phase2_data_one[chunk_no_one] = next_record_one.split(self.separator)[_idx]
                    else:
                        # file/sublist has nothing to load/read
                        del partition_ptr_lis_one[chunk_no_one]
                        del phase2_data_one[chunk_no_one]
            self.summary(self.total_records - total_ignored, self.total_records)
        else:
            # can not proceed all given blocks with memory constraint
            print("Require more than two pass to handle this large data")
            raise NotImplementedError
        return _result_set


if __name__ == "__main__":
    table = Iterator(attribute_tuple=("name", "ssn", "gender", "job", "company", "address"),
                     data_one_path="data_two.dbf",
                     data_two_path="data_one.dbf")
    table.difference_of(on_attribute="name", only_summary=False, output_write=True)
