import subprocess

import mmh3
from BSSE import *
import os, time, random
from multiprocessing import Pool, Queue


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


def long_time_task(a, b):
    c = a + b
    return c


if __name__ == "__main__":
    data_path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/file_keyword500_list.csv'
    path_kf = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/keywords500_files.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    with open(path_kf, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        DB = [row for row in reader]
        for i in range(len(DB)):
            DB[i] = list(filter(None, DB[i]))

    keyword_len = []
    for row in DB[1:]:
        keyword_len.append((row[0], len(row[1:])))
        print((row[0], len(row[1:])))
    print("====================")
    print("====================")
    result = sorted(keyword_len, key=lambda t: t[1])
    for i in result:
        print(i)
