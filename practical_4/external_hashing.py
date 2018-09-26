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
        _result = self.data.get(key, None)
        return _result if _result else "Key does not exist"


class GlobalBucket(object):
    def __init__(self):
        self.total_data = 0
        b = Bucket()
        self.buckets = [b]

    def get_bucket(self, key):
        p = self.buckets[key & ((1 << self.total_data) - 1)]
        return p

    def add(self, key):
        pass


if __name__ == "__main__":
    # inputs = [1, 11, 5, 59, 54, 12, 9, 67]
    # binary_inputs = [bin(i).split('b')[-1] for i in [1, 11, 5, 59, 54, 12, 9, 67]]
    inputs = ['1', '1011', '101', '111011', '110110', '1100', '1001', '1000011']
    g = GlobalBucket()
    for i in inputs:
        g.add(i)
