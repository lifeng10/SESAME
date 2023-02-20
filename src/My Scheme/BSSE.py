import sys
import pickle
import csv
import src.inner_product.single_input_fe.fully_secure_fe.fully_secure_fe_ddh
import mmh3
import numpy as np
import time
from src.helpers.helpers import get_int
from charm.core.math.integer import integer
from charm.toolbox.integergroup import IntegerGroup
import gc


def obj2pkl(obj, path):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)


def pickle_mpk_serialize(mpk, path):
    mpk_serialize = {}
    mpk_serialize['group_p'] = int(mpk['group'].p)
    mpk_serialize['group_q'] = int(mpk['group'].q)
    mpk_serialize['gen1'] = mpk['group'].serialize(mpk['gen1'])
    mpk_serialize['gen2'] = mpk['group'].serialize(mpk['gen2'])
    mpk_serialize['p'] = mpk['p']
    temp_h = []
    for item in mpk['h']:
        temp_h.append(mpk['group'].serialize(item))
    mpk_serialize['h'] = temp_h
    obj2pkl(mpk_serialize, path)


def pickle_mpk_deserialize(path):
    with open(path, "rb") as file:
        mpk_serialize = pickle.load(file)
    mpk_deserialize = {}
    group_deserialize = IntegerGroup()
    group_deserialize.setparam(mpk_serialize['group_p'], mpk_serialize['group_p'])
    mpk_deserialize['group'] = group_deserialize
    mpk_deserialize['gen1'] = group_deserialize.deserialize(mpk_serialize['gen1'])
    mpk_deserialize['gen2'] = group_deserialize.deserialize(mpk_serialize['gen2'])
    mpk_deserialize['p'] = mpk_serialize['p']
    temp_h = []
    for item in mpk_serialize['h']:
        temp_h.append(group_deserialize.deserialize(item))
    mpk_deserialize['h'] = temp_h
    return mpk_deserialize


def pickle_msk_serialize(msk, path):
    msk_serialize = {}
    for key, value in msk.items():
        temp = []
        for item in value:
            temp.append(get_int(item))
        msk_serialize[key] = temp
    obj2pkl(msk_serialize, path)


def pickle_msk_deserialize(path, mpk):
    with open(path, "rb") as file:
        msk_serialize = pickle.load(file)
    msk_deserialize = {}
    for key, value in msk_serialize.items():
        temp = []
        for item in value:
            temp.append(integer(item) % mpk['p'])
        msk_deserialize[key] = temp
    return msk_deserialize


def pickle_EDB_Serialize(EDB, path):
    BF_DB_Serialize = {}
    for key, value in EDB.items():
        value['c'] = get_int(value['c'])
        value['d'] = get_int(value['d'])
        temp_e = []
        for item in value['e']:
            temp_e.append(get_int(item))
        value['e'] = temp_e
        BF_DB_Serialize[key] = value
    obj2pkl(BF_DB_Serialize, path)

def pickle_EDB_Deserialize(path, mpk):
    with open(path, "rb") as file:
        BF_DB_Serialize = pickle.load(file)
    BF_DB_Deserialize = {}
    for key, value in BF_DB_Serialize.items():
        value['c'] = integer(value['c']) % mpk['p']
        value['d'] = integer(value['d']) % mpk['p']
        temp_e = []
        for item in value['e']:
            temp_e.append(integer(item) % mpk['p'])
        value['e'] = temp_e
        BF_DB_Deserialize[key] = value
    return BF_DB_Deserialize


class BSSE_Protocol:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.fe = src.inner_product.single_input_fe.fully_secure_fe.fully_secure_fe_ddh

    def add_list(self, bf, keyword_list):
        for item in keyword_list:
            for i in range(self.hash_count):
                index = mmh3.hash(item, i) % self.size
                bf[index] = 1
        return bf

    def add_item(self, bf, item):
        if isinstance(item, list):
            return self.add_list(bf, item)
        else:
            for i in range(self.hash_count):
                index = mmh3.hash(item, i) % self.size
                bf[index] = 1
            return bf

    def Setup(self, DB, p):
        BF_DB = {}
        mpk, msk = self.fe.set_up(p, self.size)
        for row in DB:
            bf_row = [0] * self.size
            bf_row = self.add_list(bf_row, row[1:])
            encrypted_bf = self.fe.encrypt(mpk, bf_row)
            BF_DB[row[0]] = encrypted_bf
        return BF_DB, mpk, msk

    def gen_token_client_Conj(self, q, mpk, msk, dummy_keyword=''):
        trap = [0] * self.size
        trap = self.add_list(trap, q)
        alpha = np.count_nonzero(trap)
        if len(dummy_keyword) != 0:
            trap = self.add_item(trap, dummy_keyword)
        func_key = self.fe.get_functional_key(mpk, msk, trap)
        return alpha, func_key, trap

    def gen_token_client_Conj_prune(self, q, mpk, msk, dummy_keyword=''):
        trap = [0] * self.size
        trap = self.add_list(trap, q)
        alpha = np.count_nonzero(trap)
        if len(dummy_keyword) != 0:
            trap = self.add_item(trap, dummy_keyword)
        beta = np.nonzero(trap)[0]
        trap_prune = []
        for i in beta:
            trap_prune.append(trap[i])
        func_key = self.fe.get_functional_key_prune(mpk, msk, trap_prune, beta)
        return alpha, beta, func_key, trap_prune

    def gen_token_client_DNF(self, q, mpk, msk, dummy_keyword_list=''):
        trap_list = []
        func_key_list = []
        alpha_list = []
        for i in range(len(q)):
            trap = [0] * self.size
            trap = self.add_list(trap, q[i])
            alpha = np.count_nonzero(trap)
            if len(dummy_keyword_list) != 0:
                trap = self.add_item(trap, dummy_keyword_list[i])
            func_key = self.fe.get_functional_key(mpk, msk, trap)
            trap_list.append(trap)
            func_key_list.append(func_key)
            alpha_list.append(alpha)
        return alpha_list, func_key_list, trap_list

    def gen_token_client_DNF_prune(self, q, mpk, msk, dummy_keyword_list=''):
        trap_list = []
        func_key_list = []
        alpha_list = []
        beta_list = []
        for i in range(len(q)):
            trap = [0] * self.size
            trap = self.add_list(trap, q[i])
            alpha = np.count_nonzero(trap)
            if len(dummy_keyword_list) != 0:
                trap = self.add_item(trap, dummy_keyword_list[i])
            beta = np.nonzero(trap)[0]
            trap_prune = []
            for i in beta:
                trap_prune.append(trap[i])
            func_key = self.fe.get_functional_key_prune(mpk, msk, trap_prune, beta)
            trap_list.append(trap_prune)
            func_key_list.append(func_key)
            alpha_list.append(alpha)
            beta_list.append(beta)
        return alpha_list, beta_list, func_key_list, trap_list

    def Search_Conj(self, alpha, trap, func_key, mpk, BF_DB):
        result_list = []
        for key, value in BF_DB.items():
            ip = self.fe.decrypt(mpk, func_key, value, trap, self.size)
            if ip >= alpha:
                result_list.append(key)
        return result_list

    def Search_Conj_prune(self, alpha, beta, trap, func_key, mpk, BF_DB):
        result_list = []
        for key, value in BF_DB.items():
            ip = self.fe.decrypt_prune(mpk, func_key, value, trap, beta, self.size)
            if ip >= alpha:
                result_list.append(key)
        return result_list

    def Search_DNF(self, alpha_list, func_key_list, mpk, BF_DB, trap_list):
        result_list = []
        for key, value in BF_DB.items():
            for i in range(len(func_key_list)):
                ip = self.fe.decrypt(mpk, func_key_list[i], value, trap_list[i], self.size)
                if ip >= alpha_list[i]:
                    result_list.append(key)
                    break
        return result_list

    def Search_DNF_prune(self, alpha_list, beta_list, trap_list, func_key_list, mpk, BF_DB):
        result_list = []
        for key, value in BF_DB.items():
            for i in range(len(func_key_list)):
                ip = self.fe.decrypt_prune(mpk, func_key_list[i], value, trap_list[i], beta_list[i], self.size)
                if ip >= alpha_list[i]:
                    result_list.append(key)
                    break
        return result_list

    def true_result(self, q):
        path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/keyword100_files100.csv'

        # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            DB = [row for row in reader]
            for i in range(len(DB)):
                if i == 0:
                    continue
                DB[i] = list(filter(None, DB[i]))

        s = set()
        flag = True
        for row in DB[1:]:
            if row[0] in q:
                if flag and len(s) == 0:
                    s = set(row[1:])
                    flag = False
                    continue
                s = s & set(row[1:])

        true_result_list = []
        for item in list(s):
            true_result_list.append(int(float(item)))
        true_result_list.sort()

        return true_result_list

    def precision_Conj(self, result_list, q):
        true_result_list = self.true_result(q)

        search_result_list = []
        for item in list(result_list):
            search_result_list.append(int(float(item)))
        search_result_list.sort()

        print("true list: ", true_result_list)
        flag = True
        for item in true_result_list:
            if item not in search_result_list:
                flag = False
        if flag:
            print("Search result pass!")

        accuracy = float(len(true_result_list)) / float(len(search_result_list))
        print(accuracy)

    def precision_DNF(self, result_list, q):
        true_result_list = []
        for row in q:
            true_result_list = true_result_list + self.true_result(row)
        true_result_list = list(set(true_result_list))

        search_result_list = []
        for item in list(result_list):
            search_result_list.append(int(float(item)))
        search_result_list.sort()

        print("true list: ", true_result_list)
        flag = True
        for item in true_result_list:
            if item not in search_result_list:
                flag = False
        if flag:
            print("Search result pass!")

        accuracy = float(len(true_result_list)) / float(len(search_result_list))
        print(accuracy)

        return accuracy


def Conjunctive_query():
    path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        DB = [row for row in reader]
        for i in range(len(DB)):
            DB[i] = list(filter(None, DB[i]))
        # for row in DB[2:]:
        #     print(row)

    bsse = BSSE_Protocol(200, 3)
    BF_DB, mpk, msk = bsse.Setup(DB[2:], 256)
    q = ["becaus", "busi"]
    alpha, func_key, trap = bsse.gen_token_client_Conj(q, mpk, msk)
    result_list = bsse.Search_Conj(alpha, trap, func_key, mpk, BF_DB)
    print("search result list", result_list)
    bsse.precision_Conj(result_list, q)

def Conjunctive_query_prune():
    path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        DB = [row for row in reader]
        for i in range(len(DB)):
            DB[i] = list(filter(None, DB[i]))
        # for row in DB[2:]:
        #     print(row)

    bsse = BSSE_Protocol(200, 3)
    BF_DB, mpk, msk = bsse.Setup(DB[2:], 256)
    q = ["becaus", "busi"]
    alpha, beta, func_key, trap_prune = bsse.gen_token_client_Conj_prune(q, mpk, msk)
    result_list = bsse.Search_Conj_prune(alpha, beta, trap_prune, func_key, mpk, BF_DB)
    print("search result list", result_list)
    bsse.precision_Conj(result_list, q)

def DNF_query():
    path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        DB = [row for row in reader]
        for i in range(len(DB)):
            DB[i] = list(filter(None, DB[i]))
        # for row in DB[2:]:
        #     print(row)

    bsse = BSSE_Protocol(200, 3)
    BF_DB, mpk, msk = bsse.Setup(DB[2:], 256)
    q = [["becaus", "busi"], ["contact", "corp", "email"], ["pleas", "note", "time"]]
    alpha_list, func_key_list, trap_list = bsse.gen_token_client_DNF(q, mpk, msk)
    result_list = bsse.Search_DNF(alpha_list, func_key_list, mpk, BF_DB, trap_list)
    print("search result list", result_list)
    bsse.precision_DNF(result_list, q)

def DNF_query_prune():
    path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        DB = [row for row in reader]
        for i in range(len(DB)):
            DB[i] = list(filter(None, DB[i]))
        # for row in DB[2:]:
        #     print(row)

    bsse = BSSE_Protocol(300, 5)
    BF_DB, mpk, msk = bsse.Setup(DB[2:], 256)
    q = [["becaus", "busi"], ["contact", "corp", "email"], ["pleas", "note", "time"]]
    alpha_list, beta_list, func_key_list, trap_list = bsse.gen_token_client_DNF_prune(q, mpk, msk)
    result_list = bsse.Search_DNF_prune(alpha_list, beta_list, trap_list, func_key_list, mpk, BF_DB)
    print("search result list", result_list)
    bsse.precision_DNF(result_list, q)


def test_Code(q, bf_size, bf_hash_count, group_prime):
    path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        DB = [row for row in reader]
        for i in range(len(DB)):
            DB[i] = list(filter(None, DB[i]))
        # for row in DB[2:]:
        #     print(row)

    T1_Setup = time.perf_counter()
    bsse = BSSE_Protocol(bf_size, bf_hash_count)
    BF_DB, mpk, msk = bsse.Setup(DB[2:], group_prime)
    T2_Setup = time.perf_counter()
    T_Setup = T2_Setup - T1_Setup

    T1_gentoken = time.perf_counter()
    alpha_list, func_key_list, trap_list = bsse.gen_token_client_DNF(q, mpk, msk)
    T2_gentoken = time.perf_counter()
    T_gentoken = T2_gentoken - T1_gentoken

    T1_Search = time.perf_counter()
    result_list = bsse.Search_DNF(alpha_list, func_key_list, mpk, BF_DB, trap_list)
    T2_Search = time.perf_counter()
    T_Search = T2_Search - T1_Search

    print("search result list", result_list)
    accuracy = bsse.precision_DNF(result_list, q)

    return T_Setup, T_gentoken, T_Search, accuracy


def test():
# if __name__ == "__main__":
    path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        DB = [row for row in reader]
        for i in range(len(DB)):
            DB[i] = list(filter(None, DB[i]))

    print("Before Serialize!")
    bsse = BSSE_Protocol(300, 4)
    BF_DB, mpk, msk = bsse.Setup(DB[2:], 256)
    q = [["becaus", "busi"], ["contact", "corp", "email"], ["pleas", "note", "time"]]
    alpha_list, func_key_list, trap_list = bsse.gen_token_client_DNF(q, mpk, msk)
    result_list = bsse.Search_DNF(alpha_list, func_key_list, mpk, BF_DB, trap_list)
    print("search result list", result_list)
    bsse.precision_DNF(result_list, q)
    print()

    print("After Deserialize!")
    pickle_EDB_Serialize(BF_DB, "/Users/carotpa/PaperCode/00_Enron_DataSet/EDB.pkl")
    pickle_mpk_serialize(mpk, "/Users/carotpa/PaperCode/00_Enron_DataSet/mpk.pkl")
    pickle_msk_serialize(msk, "/Users/carotpa/PaperCode/00_Enron_DataSet/msk.pkl")

    del bsse, BF_DB, mpk, msk, alpha_list, func_key_list, trap_list, result_list
    gc.collect()

    mpk_Deser = pickle_mpk_deserialize("/Users/carotpa/PaperCode/00_Enron_DataSet/mpk.pkl")
    msk_Deser = pickle_msk_deserialize("/Users/carotpa/PaperCode/00_Enron_DataSet/msk.pkl", mpk_Deser)
    EDB_Deser = pickle_EDB_Deserialize("/Users/carotpa/PaperCode/00_Enron_DataSet/EDB.pkl", mpk_Deser)

    bsse = BSSE_Protocol(300, 4)
    alpha_list, func_key_list, trap_list = bsse.gen_token_client_DNF(q, mpk_Deser, msk_Deser)
    result_list = bsse.Search_DNF(alpha_list, func_key_list, mpk_Deser, EDB_Deser, trap_list)
    print("search result list", result_list)
    bsse.precision_DNF(result_list, q)


#========================Test Code for Serialize=============================
    # bsse = BSSE_Protocol(500, 3)
    # BF_DB, mpk, msk = bsse.Setup(DB[2:], 512)
    # q = [["becaus", "busi"], ["contact", "corp", "email"], ["pleas", "note", "time"]]
    # alpha_list, func_key_list, trap_list = bsse.gen_token_client_DNF(q, mpk, msk)
    # result_list = bsse.Search_DNF(alpha_list, func_key_list, mpk, BF_DB, trap_list)
    # print("search result list", result_list)
    # bsse.precision_DNF(result_list, q)

    # print("Serialize and Deserialize:")
    # pickle_EDB_Serialize(BF_DB, "/Users/carotpa/PaperCode/00_Enron_DataSet/serialize.pkl")
    # BF_DB_Deserialize = pickle_EDB_Deserialize('/Users/carotpa/PaperCode/00_Enron_DataSet/serialize.pkl', mpk)
    # alpha_list, func_key_list, trap_list = bsse.gen_token_client_DNF(q, mpk, msk)
    # result_list = bsse.Search_DNF(alpha_list, func_key_list, mpk, BF_DB_Deserialize, trap_list)
    # print("search result list", result_list)
    # bsse.precision_DNF(result_list, q)


#========================Test Code=============================
    # print("Conjunctive_query()")
    # T1 = time.perf_counter()
    # Conjunctive_query()
    # T2 = time.perf_counter()
    # print("Conjunctive_query():" + str(T2 - T1) + "ms")
    #
    # T1 = time.perf_counter()
    # print("Conjunctive_query_prune()")
    # Conjunctive_query_prune()
    # T2 = time.perf_counter()
    # print("Conjunctive_query_prune():" + str(T2 - T1) + "ms")
    #
    # T1 = time.perf_counter()
    # print("DNF_query()")
    # DNF_query()
    # T2 = time.perf_counter()
    # print("DNF_query():" + str(T2 - T1) + "ms")
    #
    # T1 = time.perf_counter()
    # print("DNF_query_prune()")
    # DNF_query_prune()
    # T2 = time.perf_counter()
    # print("DNF_query_prune():" + str(T2 - T1) + "ms")
