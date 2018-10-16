#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Gahan Saraiya
GiT: https://github.com/gahan9
StackOverflow: https://stackoverflow.com/users/story/7664524
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

        :param attribute_tuple: attribute tuple in form of string
        :param args:
        :param kwargs:
        """
        self.attributes = attribute_tuple
        self.file_path = file_path
        self.separator = "\t"
        self.attribute_map = {
            "name": 0, "ssn": 1, "gender": 2, "job": 3, "company": 4, "address": 5
        }
        self.initialize_file()

    def initialize_file(self):
        if os.path.exists(self.file_path):
            pass
        else:
            with open(self.file_path, "w") as f:
                f.write(self.separator.join(self.attributes))
                f.write("\n")

    def add_dummy_data(self, number_of_record=100):
        file = open(self.file_path, "a+")
        for _ in range(number_of_record):
            f = fak.profile()
            data_tuple = (
                f['name'],
                f['ssn'],
                f['sex'],
                f['job'].replace("\n", ""),
                f['company'].replace("\n", ""),
                f['address'].replace("\n", "")
            )
            data_string = self.separator.join(data_tuple) + "\n"
            file.write(data_string)

    def select(self, attributes=None, values=None, condition="all"):
        file = open(self.file_path, "r")
        header = file.readline()  # skip header
        print("SELECT * from {} where {} {} {}".format(self.file_path, attributes[0], condition, values[0]))
        print(header)
        if condition == "all":
            for record in file.read().split("\n"):
                print(record)
            file.close()
        else:
            for record in file.read().split("\n"):
                record_lis = record.split("\t")
                attribute = attributes[0]
                value = values[0]
                idx = self.attribute_map[attribute]
                # print(record_lis[idx])
                if condition == "==" or condition.lower().startswith("equals"):
                    if record_lis[idx] == value:
                        print(record)
                elif condition == "contains":
                    if value.lower() in record_lis[idx].lower():
                        print(record)


if __name__ == "__main__":
    table = Iterator(attribute_tuple=("name", "ssn", "gender", "job", "company", "address"),
                     file_path="iterator.dbf")
    # table.add_dummy_data(1000)
    table.select(attributes=["name"], values=["Tanner Erickson"], condition="==")
