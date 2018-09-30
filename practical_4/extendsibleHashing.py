# coding=utf-8
import random
import math

__author__ = "Gahan Saraiya"
__url__ = "https://github.com/gahan9/DS_lab/blob/master/practical_4/extendsibleHashing.py"

DEBUG = False


def print_log(*args):
    if DEBUG:
        print("DEBUG: ", *args, sep=" <|> ")


class Bucket(object):
    def __init__(self, bucket_size=2):
        self.bucket_size = bucket_size
        self.data = {}
        self.total_data = 0

    def is_full(self):
        return len(self.data) >= self.bucket_size

    def add(self, key, val):
        self.data[key] = val

    def get(self, key):
        return self.data.get(key)

    @staticmethod
    def int_to_bin(data, pad_digits):
        return bin(data).split('b')[-1].zfill(pad_digits)

    def show(self):
        if self.data:
            _max = int(math.log(max(self.data), 2)) + 1
            for k, v in self.data.items():
                print(self.int_to_bin(k, _max), v)

    def __repr__(self):
        return "{}".format(self.data) if self.data else ''


class GlobalBucket(object):
    def __init__(self, bucket_size=2):
        self.bucket_size = bucket_size  # max size of each bucket
        self.total_global_data = 0
        bucket = Bucket(self.bucket_size)
        self.buckets = [bucket]  # list of buckets in global buckets

    def get_bucket(self, key):
        return self.buckets[key & ((1 << self.total_global_data) - 1)]

    def add(self, key, val):
        print_log("adding key: {} and value: {}".format(key, val))
        bucket = self.get_bucket(key)
        print_log("bucket status is full?: {}", bucket.is_full())
        if bucket.is_full() and bucket.total_data == self.total_global_data:
            self.total_global_data += 1
            self.buckets *= 2
            print_log("buckets: {}".format(self.buckets))
        if bucket.is_full() and bucket.total_data < self.total_global_data:
            bucket.add(key, val)
            bucket1 = Bucket(self.bucket_size)
            bucket2 = Bucket(self.bucket_size)
            for k, v in bucket.data.items():
                # print_log("key", k, "value", v)
                if ((k & ((1 << self.total_global_data) - 1)) >> bucket.total_data) & 1 == 1:
                    bucket2.add(k, v)
                else:
                    bucket1.add(k, v)
            for idx, value in enumerate(self.buckets):
                # print_log("idx", idx)
                if value == bucket:
                    if (idx >> bucket.total_data) & 1 == 1:
                        self.buckets[idx] = bucket2
                    else:
                        self.buckets[idx] = bucket1
            bucket2.total_data = bucket1.total_data = bucket.total_data + 1
        else:
            bucket.add(key, val)
        # print("bucket after adding", val, "operation: ", bucket.data)

    def get(self, key):
        return self.get_bucket(key).get(key)

    def __repr__(self):
        return ", ".join("{}".format(b) for b in self.buckets if b.__repr__())


def test(input_nums=10):
    """
    test function to test the implementation
    :param input_nums: number of inputs to be added
    :return:
    """
    BUCKET_SIZE = 3  # defining single bucket size
    g = GlobalBucket(BUCKET_SIZE)
    inputs = [random.randint(1, 1000) for i in range(input_nums)]
    print("Bucket Size: ", BUCKET_SIZE)
    print("Total Inputs : ", input_nums)
    print("Input Sequence: ", inputs)
    for i in inputs:
        print_log("*>Adding {} in to bucket".format(i))
        g.add(i, i)
    print("-"*40)
    print("global bucket > ", g)
    for _bucket in g.buckets:
        if _bucket.__repr__():
            print("-----Exploring bucket: {}".format(_bucket))
            _bucket.show()


if __name__ == "__main__":
    TEST_NUM = 25
    test(TEST_NUM)
