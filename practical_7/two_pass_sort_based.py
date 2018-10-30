#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524

Implementation of sorting based two pass algorithm
"""
import os

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
        self.separator = "\t"
        self.records_per_block = kwargs.get("records_per_block", 50)
        self.initialize_file()

    @property
    def get_free_memory(self):
        # calculate how many blocks can be accommodated in memory buffer
        num_lines = sum(1 for line in open(self.file_path))
        no_of_records = num_lines - 2  # remove header line and last new line
        return

    @property
    def get_total_blocks(self):
        # calculate total number of blocks by record size
        os.popen("wc")
        return

    def initialize_file(self):
        # check if file exits or not
        if os.path.exists(self.file_path):
            pass
        else:
            # create file with header if file not exist
            with open(self.file_path, "w") as f:
                f.write(self.separator.join(self.attributes))
                f.write("\n")

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
    def _match(value, condition, record_val, case=False):
        """
        dynamic evaluation of matching value
        :param value: value to be match
        :param condition: condition through which values to be compared
        :param record_val: value of record in data file
        :param case: case sensitive? (True or False)
        :return: boolean value if condition satisfies or not
        """
        # exist in...
        if eval("""'{}' {} '{}'""".format(value.lower(), condition, record_val.lower())):
            if case and eval("""'{}' {} '{}'""".format(value, condition, record_val)):
                # match case sensitive
                return True
            elif not case:
                # match case insensitive
                return True
        return False

    def select(self, attributes=None, condition="all", values=None, case_sensitive=False):
        """
        dynamic selection from data file with various operations
        :param attributes: attribute/column name
        :param condition: condition to be compared
        :param values: value to be matched for attribute
        :param case_sensitive: whether match should be case sensitive or not
        :return:
        prints matched data and summary
        """
        query = "{0}\n{0}\nSELECT * from {1}".format("#"*50, self.file_path)
        where_clause = " WHERE {} {} {}".format(attributes[0], condition, values[0])
        query = query + where_clause if condition != "all" else query
        print(query)
        file = open(self.file_path, "r")
        header = file.readline()  # skip header
        print(header)
        total_results = 0
        total_records = 0
        for record in file.read().split("\n"):
            total_records += 1
            if record and condition == "all":
                total_results += 1
                print(record)
            elif record:
                record_lis = record.split("\t")
                attribute, value = attributes[0], values[0]
                record_val = record_lis[header.split("\t").index(attribute)]
                # print(record_val, value, condition)
                if condition.lower() in ("==", "equal", "equals", "equals to"):
                    if self._match(value, "==", record_val, case_sensitive):
                        total_results += 1
                        print(record)
                elif condition.lower() in ("in", "contains", "contain"):
                    if self._match(value, "in", record_val, case_sensitive):
                        total_results += 1
                        print(record)
                elif condition.lower() in ("<", "lt"):
                    if self._match(value, "<", record_val, case_sensitive):
                        total_results += 1
                        print(record)
                elif condition.lower() in (">", "gt"):
                    if self._match(value, ">", record_val, case_sensitive):
                        total_results += 1
                        print(record)
                elif condition.lower() in ("<=", "lte"):
                    if self._match(value, "<=", record_val, case_sensitive):
                        total_results += 1
                        print(record)
                elif condition.lower() in (">=", "gte"):
                    if self._match(value, ">=", record_val, case_sensitive):
                        total_results += 1
                        print(record)
        file.close()
        print("-"*30)
        print("Total Results: {}".format(total_results))
        print("Total Records: {}".format(total_records))


if __name__ == "__main__":
    table = Iterator(attribute_tuple=("name", "ssn", "gender", "job", "company", "address"),
                     file_path="iterator.dbf")
    table.add_dummy_data(1000)
    # table.select(attributes=["name"], values=["William Jensen"], condition="==", case_sensitive=False)
    # table.select(attributes=["gender"], values=["M"], condition="==", case_sensitive=False)
    # table.select(attributes=["name"], values=["William"], condition="in", case_sensitive=True)
    # table.select(attributes=["ssn"], values=["441-31-5305"], condition="==", case_sensitive=False)
    # table.select(attributes=["ssn"], values=["-511"], condition="in", case_sensitive=False)
