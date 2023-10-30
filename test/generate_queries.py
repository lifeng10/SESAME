import csv

def sortKeywords(DB):
    length = len(DB)
    for i in range(length - 1):
        for j in range(length - 1 - i):
            if len(DB[j]) > len(DB[j+1]):
                temp = DB[j+1]
                DB[j+1] = DB[j]
                DB[j] = temp
    sorted_keywords = []
    for row in DB:
        sorted_keywords.append(row[0])
    return DB, sorted_keywords

def generate_union(k1, k2, k3, DB, sorted_keywords):
    # if DB[sorted_keywords.index(k1)][0] == k1:
    s1 = set(DB[sorted_keywords.index(k1)][1:])
    # else:
    #     print("error")
    # if DB[sorted_keywords.index(k2)][0:] == k2:
    s2 = set(DB[sorted_keywords.index(k2)][1:])
    # else:
    #     print("error")
    # if DB[sorted_keywords.index(k3)][0] == k3:
    s3 = set(DB[sorted_keywords.index(k3)][1:])
    # else:
    #     print("error")
    return s1 | s2 | s3

def verify(k1, k2, k3, k4, k5, k6, DB):
    s1 = set()
    s2 = set()
    s3 = set()
    s4 = set()
    s5 = set()
    s6 = set()
    for row in DB:
        if row[0] == k1:
            s1 = set(row[1:])
        if row[0] == k2:
            s2 = set(row[1:])
        if row[0] == k3:
            s3 = set(row[1:])
        if row[0] == k4:
            s4 = set(row[1:])
        if row[0] == k5:
            s5 = set(row[1:])
        if row[0] == k6:
            s6 = set(row[1:])
    print(len((s1 | s2 | s3) & (s4 | s5 | s6)))

path_kf = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/keywords500_files.csv'

with open(path_kf, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    DB = [row for row in reader]
    for i in range(len(DB)):
        DB[i] = list(filter(None, DB[i]))

DB, sorted_keywords = sortKeywords(DB[1:])

# ss1 = set()
# ss2 = set()
k1 = 'class'
k2 = 'build'
k3 = 'elink'
k4 = 'summer'
k5 = 'black'
# ss1 = generate_union(k1, k2, k3, DB, sorted_keywords)
# for key in sorted_keywords:
#     ss2 = generate_union(k4, k5, key, DB, sorted_keywords)
#     print(key)
#     print(len(ss1 & ss2))
#     if len(ss1 & ss2) < 3005 and len(ss1 & ss2) > 2995:
#         print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#         print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# verify(k1, k2, k3, k4, k5, 'exchang', DB)

s1 = set()
s2 = set()
s3 = set()
s4 = set()
s5 = set()
s6 = set()
for row in DB:
    if row[0] in ["employ"]:
        s1 = set(row[1:])
    if row[0] in ["legal"]:
        s2 = set(row[1:])
    if row[0] in ["build"]:
        s3 = set(row[1:])
    if row[0] in ["billion"]:
        s4 = set(row[1:])
    if row[0] in ["begin"]:
        s5 = set(row[1:])
    if row[0] in ["contract"]:
        s6 = set(row[1:])
s = (s1 & s2 & s3) | (s4 & s5 & s6)
print(len(s))

# for key in sorted_keywords:
#     print(key)
#     s1 = set()
#     s2 = set()
#     s3 = set()
#     s4 = set()
#     s5 = set()
#     s6 = set()
#     for row in DB:
#         if row[0] in ["employ"]:
#             s1 = set(row[1:])
#         if row[0] in ["legal"]:
#             s2 = set(row[1:])
#         if row[0] in ["build"]:
#             s3 = set(row[1:])
#         if row[0] in ["billion"]:
#             s4 = set(row[1:])
#         if row[0] in ["begin"]:
#             s5 = set(row[1:])
#         if row[0] in [key]:
#             s6 = set(row[1:])
#     s = (s1 & s2 & s3) | (s4 & s5 & s6)
#     print(len(s))
#     if len(s) < 2005 and len(s) > 1995:
#         print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#         print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")


