import mmh3
from BSSE import *


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
    q = [["becaus", "busi"], ["contact", "corp", "email"], ["pleas", "note", "time"]]
    path = '/Users/carotpa/PaperCode/00_Enron_DataSet/01_SelectedFiles/999/111/q.pkl'
    obj2pkl(q, path)
