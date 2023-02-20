from BSSE import *
import gc


def BSSE_DNF_query(path_read, q, bf_size, bf_hash_count, group_prime, pickle_flag, path_dump):
    # path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    with open(path_read, 'r', encoding='utf-8') as f:
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

    if pickle_flag:
        path_dump_mpk = path_dump + '_mpk.pkl'
        path_dump_msk = path_dump + '_msk.pkl'
        path_dump_EDB = path_dump + '_EDB.pkl'
        pickle_mpk_serialize(mpk, path_dump_mpk)
        pickle_msk_serialize(msk, path_dump_msk)
        pickle_EDB_Serialize(BF_DB, path_dump_EDB)

    del bsse, BF_DB, mpk, msk, alpha_list, func_key_list, trap_list, result_list
    gc.collect()

    return T_Setup, T_gentoken, T_Search, accuracy


def BSSE_DNF_query_prune(path_read, q, bf_size, bf_hash_count, group_prime, pickle_flag, path_dump):
    # path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    with open(path_read, 'r', encoding='utf-8') as f:
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
    alpha_list, beta_list, func_key_list, trap_list = bsse.gen_token_client_DNF_prune(q, mpk, msk)
    T2_gentoken = time.perf_counter()
    T_gentoken = T2_gentoken - T1_gentoken

    T1_Search = time.perf_counter()
    result_list = bsse.Search_DNF_prune(alpha_list, beta_list, trap_list, func_key_list, mpk, BF_DB)
    T2_Search = time.perf_counter()
    T_Search = T2_Search - T1_Search

    print("search result list", result_list)
    accuracy = bsse.precision_DNF(result_list, q)

    if pickle_flag:
        path_dump_mpk = path_dump + '_mpk_prune.pkl'
        path_dump_msk = path_dump + '_msk_prune.pkl'
        path_dump_EDB = path_dump + '_EDB_prune.pkl'
        pickle_mpk_serialize(mpk, path_dump_mpk)
        pickle_msk_serialize(msk, path_dump_msk)
        pickle_EDB_Serialize(BF_DB, path_dump_EDB)

    del bsse, BF_DB, mpk, msk, alpha_list, func_key_list, trap_list, result_list
    gc.collect()

    return T_Setup, T_gentoken, T_Search, accuracy


def list2str(q):
    s = ''
    flag = True
    for q_item in q:
        if flag:
            s = '(' + '^'.join(q_item) + ')'
            flag = False
        else:
            s = s + 'v' + '(' + '^'.join(q_item) + ')'
    return s


if __name__ == "__main__":
    data_path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'
    q_list = [[["becaus", "busi"], ["contact", "corp", "email"], ["pleas", "note", "time"]],
              [["becaus", "busi"], ["contact", "corp", "email"], ["pleas", "note", "time"]],
              [["becaus", "busi"], ["contact", "corp", "email"], ["pleas", "note", "time"]]]
    bf_size_list = [2400, 2200, 2000, 1800, 1600, 1400, 1200, 1000]
    bf_hash_count_list = [8, 7, 6, 5, 4, 3, 2]
    group_prime = 512

    # Test for prune
    DNF_query_result_prune = {}
    for bf_size in bf_size_list:
        for bf_hash_count in bf_hash_count_list:
            path_dump = '' + '/' + str(bf_size) + '_' + str(bf_hash_count)
            这里要补全
            pickle_flag = True
            for q in q_list:
                T_Setup_list_prune = []
                T_gentoken_list_prune = []
                T_Search_list_prune = []
                accuracy_prune = []
                for i in range(10):
                    T_Setup, T_gentoken, T_Search, accuracy = BSSE_DNF_query_prune(data_path, q, bf_size, bf_hash_count,
                                                                                   group_prime, pickle_flag, path_dump)
                    T_Setup_list_prune.append(T_Setup)
                    T_gentoken_list_prune.append(T_gentoken)
                    T_Search_list_prune.append(T_Search)
                    accuracy_prune.append(accuracy)
                    pickle_flag = False
                key = "bf_size: " + str(bf_size) + ", bf_hash_count: " + str(bf_hash_count) + ", q: " + list2str(q)
                value = (T_Setup_list_prune, T_gentoken_list_prune, T_Search_list_prune, accuracy_prune)
                DNF_query_result_prune[key] = value
    path_dump_result_prune = '' 这里也要补全
    obj2pkl(DNF_query_result_prune, path_dump_result_prune)

    # Test without prune
    DNF_query_result = {}
    for bf_size in bf_size_list:
        for bf_hash_count in bf_hash_count_list:
            path_dump = '' + '/' + str(bf_size) + '_' + str(bf_hash_count)
            这里要补全
            pickle_flag = True
            for q in q_list:
                T_Setup_list = []
                T_gentoken_list = []
                T_Search_list = []
                accuracy = []
                for i in range(10):
                    T_Setup, T_gentoken, T_Search, accuracy = BSSE_DNF_query(data_path, q, bf_size, bf_hash_count,
                                                                             group_prime, pickle_flag, path_dump)
                    T_Setup_list.append(T_Setup)
                    T_gentoken_list.append(T_gentoken)
                    T_Search_list.append(T_Search)
                    accuracy.append(accuracy)
                    pickle_flag = False
                key = "bf_size: " + str(bf_size) + ", bf_hash_count: " + str(bf_hash_count) + ", q: " + list2str(q)
                value = (T_Setup_list, T_gentoken_list, T_Search_list, accuracy)
                DNF_query_result[key] = value
    path_dump_result = '' 这里也要补全
    obj2pkl(DNF_query_result_prune, path_dump_result)
