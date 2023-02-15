import mmh3


class BloomFilter:
    def __init__(self, size, hash_count):
        self.bf = [0] * size
        self.size = size
        self.hash_count = hash_count

    def add(self, item):
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            self.bf[index] = 1
        return self

    def __contains__(self, item):
        out = True
        for i in range(self.hash_count):
            index = mmh3.hash(item, i) % self.size
            if self.bf[index] == 0:
                out = False
        return out


if __name__ == "__main__":
    for i in range(5):
        print(mmh3.hash("123", i) % 10000000)
