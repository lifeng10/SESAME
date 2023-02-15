# -*- coding: utf-8 -*-
"""
Read_file: 读取目录中的所有文件
end_num:
Preprocess: 得到每个文档中对应字典中的关键字的词频
    即，得到一个矩阵和一个字典，每一行代表一个文档，一行中每个数字代表对应字典中的关键字在文档中的词频
"""

import os

import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import pandas as pd


# 提取文档中的关键字，并计算对应关键字的tfidf
def Read_file(file_dir):
    # 文档集存于列表中,处理文档集
    file_list = []
    for root, dirs, files in os.walk(file_dir):  # file_dir：文档集
        if len(files) > 0:
            for file in files:
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    file_list.append(file.read())
    return file_list


# 判断字符串是否以数字结尾
def end_num(string):
    text = re.compile(r".*[0-9]$")
    if text.match(string):
        return True
    else:
        return False


#  对文件进行预处理，得到只有单词组成的文档
def Preprocess(file_list):
    Flist = []
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    for i in range(len(file_list)):
        Words = []
        input_str = (file_list[i])
        input_str = input_str.translate(table)
        input_str = input_str.split()
        for word in input_str:
            word = lemmatizer.lemmatize(word)   # 还原词性
            stem = stemmer.stem(word)   # 提取词干
            if end_num(stem):   # 以数字结尾的单词，不要
                continue
            if len(stem) > 10 or len(stem) < 4:  # 单词长度大于10，小于4的，不要
                continue
            Words.append(stem)  # 提取词干
        file = ' '.join(Words)  # file:处理过后的文档
        file = re.sub(r"\d+", "", file)  # 去除文档中的数字
        Flist.append(file)
    return Flist

# 得到每个文档中所有关键字的tfidf
# P是一个矩阵，每行对应每个文档，每列对应字典中的每个单词的词频
def Vect_files(file_list):
    tfidf = TfidfVectorizer(max_df=0.85, min_df=0.05, max_features=500, encoding='latin-1', stop_words="english")
    X_tfidf = tfidf.fit_transform(file_list)
    dictionary = tfidf.get_feature_names()
    P = X_tfidf.toarray()
    return dictionary, P


# 写成二进制文件
def obj2csv(obj, path):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)

# 读取文件
# with open(path, 'rb') as file:
#     obj = pickle.load(file)


if __name__ == '__main__':
    # filelist = Read_file("/Users/carotpa/PaperCode/00_Enron_DataSet/01_SelectedFiles")
    # Flist = Preprocess(filelist)
    # dictionary, P = Vect_files(Flist)
    # obj2csv(dictionary, "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/dictionary500_189513.pkl")
    # obj2csv(P, "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/p500_189513.pkl")

    # ================================Visualization====================================
    # path = "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/dictionary100.pkl"
    # with open(path, 'rb') as file:
    #     dictionary100 = pickle.load(file)
    #
    # path = "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/p100.pkl"
    # with open(path, 'rb') as file:
    #     p100 = pickle.load(file)
    #
    # dictionary = pd.DataFrame(data=dictionary100)
    # dictionary.to_csv('/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/dictionary100_1.csv', encoding='gbk')
    #
    # column_name = dictionary100
    # p = pd.DataFrame(columns=column_name, data=p100)
    # p.to_csv('/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/p100.csv', encoding='gbk')

    # ==========Sort keywords in each file according to TFIDF===============
    # path = "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/dictionary100.pkl"
    # with open(path, 'rb') as file:
    #     dictionary100 = pickle.load(file)
    #
    # path = "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/p100.pkl"
    # with open(path, 'rb') as file:
    #     p100 = pickle.load(file)

    # p100_sorted = np.argsort(-p100, axis=1)
    # p100_sroted_element = np.sort(-p100, axis=1)
    # print(p100_sorted)
    # print(p100_sroted_element)
    #
    # file_keyword_list = [[] for i in range(len(p100_sorted))]
    # for file_i in range(len(p100_sorted)):
    #     for list_j in range(len(p100_sorted[file_i])):
    #         if p100_sroted_element[file_i, list_j] > -0.00005:
    #             break
    #         else:
    #             file_keyword_list[file_i].append(dictionary100[p100_sorted[file_i, list_j]])
    # file_keyword_list = pd.DataFrame(data=file_keyword_list)
    # file_keyword_list.to_csv('/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv', encoding='gbk')

    # ==========replace float in p100 with 1===============
    # path = "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/p100.pkl"
    # with open(path, 'rb') as file:
    #     p100 = pickle.load(file)

    # [rows, cols] = p100.shape
    # p100_int = np.empty([rows, cols], dtype=int)
    # for row in range(rows):
    #     for column in range(cols):
    #         if p100[row, column] > 0.0005:
    #             p100_int[row, column] = 1
    #         else:
    #             p100_int[row, column] = 0
    #
    # path = "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/dictionary100.pkl"
    # with open(path, 'rb') as file:
    #     dictionary100 = pickle.load(file)
    #
    # column_name = dictionary100
    # p100_int = pd.DataFrame(columns=column_name, data=p100_int)
    # p100_int.to_csv('/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/p100_int.csv', encoding='gbk')

    # ==========list keyword files table===============
    # dict = {}
    # for keyword in dictionary100:
    #     dict[keyword] = []
    #
    # [rows, cols] = p100.shape
    # for i in range(rows):
    #     for j in range(cols):
    #         if p100[i, j] >= 0.0005:
    #             dict[dictionary100[j]].append(int(i))
    #
    # print(dict)
    #
    # keyword_num = len(dictionary100)
    # keyword_files = [[] for i in range(keyword_num)]
    # for i in range(keyword_num):
    #     keyword_files[i] = dict[dictionary100[i]]
    # keyword_files = pd.DataFrame(index=dictionary100, data=keyword_files, dtype=int)
    # keyword_files.to_csv('/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/keyword100_files100.csv', encoding='gbk')

    # ==========Test===============
    path = "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/dictionary100.pkl"
    with open(path, 'rb') as file:
        dictionary100 = pickle.load(file)

    path = "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/p100.pkl"
    with open(path, 'rb') as file:
        p100 = pickle.load(file)

    print(dictionary100)
    print(p100)
