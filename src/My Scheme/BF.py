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


def true_result(q, path_kf):
    with open(path_kf, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        DB = [row for row in reader]
        for i in range(len(DB)):
            if i == 0:
                continue
            DB[i] = list(filter(None, DB[i]))

    s = set()
    flag = True
    count = 0
    for row in DB[1:]:
        if row[0] in q:
            if flag and len(s) == 0:
                s = set(row[1:])
                count = count + 1
                flag = False
                continue
            s = s & set(row[1:])
            count = count + 1

    true_result_list = []
    for item in list(s):
        true_result_list.append(int(float(item)))
    true_result_list.sort()

    print(count)

    return true_result_list


def or_result(q, path_kf):
    with open(path_kf, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        DB = [row for row in reader]
        for i in range(len(DB)):
            if i == 0:
                continue
            DB[i] = list(filter(None, DB[i]))

    s = set()
    count = 0
    for row in DB[1:]:
        if row[0] in q:
            s = s | set(row[1:])
            count = count + 1

    true_result_list = []
    for item in list(s):
        true_result_list.append(int(float(item)))
    true_result_list.sort()
    print(count)

    return true_result_list


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
    print("====================")
    print("====================")
    result = sorted(keyword_len, key=lambda t: t[1])

    q1 = [['random', 'commission'], ['yesterday', 'payment']]
    q2 = [['height', 'commission'], ['yesterday', 'sign']]
    q3 = [['style', 'section'], ['revenu', 'offer']]
    q4 = [['travel', 'black'], ['summer', 'michael']]
    q5 = [['class', 'build'], ['process', 'mani']]
    q6 = [['random', 'commission', 'script'], ['script', 'yard', 'sportslin']]
    q7 = [['height', 'commission', 'script'], ['yesterday', 'hotel', 'practic']]
    q8 = [['style', 'section', 'span'], ['bank', 'protect', 'style']]
    q9 = [['travel', 'black', 'elink'], ['summer', 'michael', 'width']]
    q10 = [['class', 'build', 'elink'], ['summer', 'black', 'exchang']]

    Q1 = [['color', 'border'], ['commission', 'softwar']]
    Q2 = [['round', 'board'], ['protect', 'georg']]
    Q3 = [['court', 'agenc'], ['produc', 'onlin']]
    Q4 = [['march', 'technolog'], ['control', 'recent']]
    Q5 = [['demand', 'account'], ['respons', 'long']]
    Q6 = [['sunday', 'practic', 'night'], ['attempt', 'retail', 'dasovich']]
    Q7 = [['employe', 'legal', 'build'], ['summer', 'billion', 'begin']]
    Q8 = [['link', 'account', 'develop'], ['perform', 'present', 'time']]
    Q9 = [['copyright', 'sell', 'right'], ['document', 'know', 'receiv']]
    Q10 = [['contact', 'custom', 'inform'], ['sent', 'want', 'make']]

    # s1 = set(true_result(Q1[0], path_kf))
    # s2 = set(true_result(Q1[1], path_kf))
    # print("length: ", len(s1 | s2))
    print(len(or_result(['travel', 'click'], path_kf)))

    for keyword, frequency in result[350:]:
        q = [['travel', 'click'], ['wednesday']]
        q[1].append(keyword)
        s1 = set(or_result(q[0], path_kf))
        s2 = set(or_result(q[1], path_kf))
        true_result_list = list(s1 & s2)
        print(q)
        print("count: " + str(len(true_result_list)))
        if len(true_result_list) > 3950 and len(true_result_list) < 4050:
            print("=============================================================================")
            print("=============================================================================")
            print("=============================================================================")

    # for keyword, frequency in result[0:]:
    #     q = ['class', 'build']
    #     q.append(keyword)
    #     true_result_list = or_result(q, path_kf)
    #     true_result_list = list(set(true_result_list))
    #     print(q)
    #     print("count: " + str(len(true_result_list)))

    # q = [["height", "calpin"], ["travel", "water"]]
    # true_result_list = []
    # for row in q:
    #     true_result_list = true_result_list + true_result(row, path_kf)
    # true_result_list = list(set(true_result_list))
    # print(true_result_list)
    # print(len(true_result_list))
