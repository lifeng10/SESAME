# -*- coding: utf-8 -*-
import pickle
import operator


# 按照tfidf，降序排列每个文档中的关键字
# 结果存放到afterSortedP.pkl中
class Keyword:
    def __init__(self, keyword_num, tfidf):
        self.keyword_num = keyword_num
        self.tfidf = tfidf


# 获取每个文档中排序前num个关键字
def extractKeywords(num):
    with open("/Users/carotpa/PaperCode/20200928VBSFB/ExperimentData/p1500.pkl", "rb") as file:
        P = pickle.load(file)
    files = []
    for i in range(len(P)):  # 遍历每一个文件
        file = []
        for j in range(len(P[i])):
            keyword = Keyword(j, P[i][j])
            file.append(keyword)
        cmpfun = operator.attrgetter("tfidf", "keyword_num")
        file.sort(key=cmpfun, reverse=True)
        file = file[:num]  # 获取每个文档中tfidf前num个关键字
        files.append(file)
    return files


if __name__ == '__main__':
    # with open("afterSortedP.pkl", 'rb') as file:
    #     P = pickle.load(file)

    with open("/Users/carotpa/PaperCode/20200928VBSFB/ExperimentData/dictionary1500.pkl", 'rb') as file:
        dictionary = pickle.load(file)

    files = extractKeywords(60)

    fileObject = open("/Users/carotpa/PaperCode/20200928VBSFB/ExperimentData/File_Keywords_10000files.txt", 'w')
    i = 0
    for p in files:
        fileObject.write(str(i) + " ")
        for Keyword in p:
            fileObject.write(dictionary[Keyword.keyword_num]
                             + "," + str(Keyword.keyword_num) + " ")
        fileObject.write('\n')
        i += 1
        if i == 10000:
            break
    fileObject.close()

    # fileObject = open("/Users/carotpa/PaperCode/20200928VBSFB/ExperimentData/Dictionary1500.txt", 'w')
    # for keyword in dictionary:
    #     fileObject.write(keyword + " ")
    # fileObject.close()

    # with open("/Users/carotpa/PaperCode/20200928VBSFB/ExperimentData/p1500.pkl", "rb") as file:
    #     P = pickle.load(file)
    # print(P.shape)
