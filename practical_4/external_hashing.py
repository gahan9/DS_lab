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
        bucket = self.buckets[key & ((1 << self.total_data) - 1)]
        return bucket

    def add(self, key, val):
        bucket = self.get_bucket(key)
        if bucket.is_full():
            if bucket.total_data == self.total_data:
                self.total_data += 1
                self.buckets = self.buckets * 2
            elif bucket.total_data < self.total_data:
                bucket.add(key, val)
                bucket1 = Bucket()
                bucket2 = Bucket()
                for k, v in bucket.data.items():
                    if ((k & ((1 << self.total_data) - 1)) >> bucket.total_data) & 1 == 1:
                        bucket2.add(key, val)
                    else:
                        bucket1.add(key, val)
                for idx, value in enumerate(self.buckets):
                    if value == bucket:
                        if (idx >> bucket.total_data) & 1 == 1:
                            self.buckets[i] = bucket2
                        else:
                            self.buckets[i] = bucket1
                bucket2.total_data = bucket1.total_data = bucket.total_data + 1
        else:
            bucket.add(key, val)

    def get(self, key):
        p = self.get_bucket(key)
        return p.get(key)


if __name__ == "__main__":
    inputs = [1, 11, 5, 59, 54, 12, 9, 67]
    # binary_inputs = [bin(i).split('b')[-1] for i in [1, 11, 5, 59, 54, 12, 9, 67]]
    # inputs = ['1', '1011', '101', '111011', '110110', '1100', '1001', '1000011']
    g = GlobalBucket()
    for i in inputs:
        g.add(i, i)
    print(inputs)
    for i in range(len(inputs)):
        print(g.get(i))
