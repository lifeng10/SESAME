# -*- coding: utf-8 -*-
"""
Read_file: 读取目录中的所有文件
end_num:
Preprocess: 得到每个文档中对应字典中的关键字的词频
    即，得到一个矩阵和一个字典，每一行代表一个文档，一行中每个数字代表对应字典中的关键字在文档中的词频
"""

import os
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


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

    path = "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/dictionary100.pkl"
    with open(path, 'rb') as file:
        dictionary100 = pickle.load(file)

    path = "/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/p100.pkl"
    with open(path, 'rb') as file:
        p100 = pickle.load(file)

    # name_dic = [i for i in range(100)]
    # dictionary = pd.DataFrame(columns=name_dic, data=dictionary100)
    #
    # name_p = dictionary100
    # p =

    print(dictionary100)
    print(p100)

    name = ['file id']
    # for file in p100:

