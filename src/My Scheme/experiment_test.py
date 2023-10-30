from BSSE import *
import gc


def BSSE_DNF_query(bsse, BF_DB, mpk, msk, path_kf, q, pickle_flag, path_dump, T_Setup, dummy_keyword_list=''):
    # path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    # with open(path_read, 'r', encoding='utf-8') as f:
    #     reader = csv.reader(f)
    #     DB = [row for row in reader]
    #     for i in range(len(DB)):
    #         DB[i] = list(filter(None, DB[i]))
        # for row in DB[2:]:
        #     print(row)

    # T1_Setup = time.perf_counter()
    # bsse = BSSE_Protocol(bf_size, bf_hash_count)
    # BF_DB, mpk, msk = bsse.Setup(DB[2:], group_prime)
    # T2_Setup = time.perf_counter()
    # T_Setup = T2_Setup - T1_Setup

    T1_gentoken = time.perf_counter()
    alpha_list, func_key_list, trap_list = bsse.gen_token_client_DNF(q, mpk, msk, dummy_keyword_list)
    T2_gentoken = time.perf_counter()
    T_gentoken = T2_gentoken - T1_gentoken

    T1_Search = time.perf_counter()
    result_list = bsse.Search_DNF(alpha_list, func_key_list, mpk, BF_DB, trap_list)
    T2_Search = time.perf_counter()
    T_Search = T2_Search - T1_Search

    # print("search result list", result_list)
    accuracy = bsse.precision_DNF(result_list, q, path_kf)

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


def BSSE_DNF_query_prune(bsse, BF_DB, mpk, msk, path_kf, q, pickle_flag, path_dump, T_Setup, dummy_keyword_list=''):
    # path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/file100_keyword100_list.csv'

    # 只是读取DB和过滤空字符串，没有对DB进行剪枝，即坐标轴还在DB中
    # with open(path_read, 'r', encoding='utf-8') as f:
    #     reader = csv.reader(f)
    #     DB = [row for row in reader]
    #     for i in range(len(DB)):
    #         DB[i] = list(filter(None, DB[i]))
        # for row in DB[2:]:
        #     print(row)

    # T1_Setup = time.perf_counter()
    # bsse = BSSE_Protocol(bf_size, bf_hash_count)
    # BF_DB, mpk, msk = bsse.Setup(DB[2:], group_prime)
    # T2_Setup = time.perf_counter()
    # T_Setup = T2_Setup - T1_Setup

    T1_gentoken = time.perf_counter()
    alpha_list, beta_list, func_key_list, trap_list = bsse.gen_token_client_DNF_prune(q, mpk, msk, dummy_keyword_list)
    T2_gentoken = time.perf_counter()
    T_gentoken = T2_gentoken - T1_gentoken

    T1_Search = time.perf_counter()
    result_list = bsse.Search_DNF_prune(alpha_list, beta_list, trap_list, func_key_list, mpk, BF_DB)
    T2_Search = time.perf_counter()
    T_Search = T2_Search - T1_Search

    # print("search result list", result_list)
    accuracy = bsse.precision_DNF(result_list, q, path_kf)

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


def test_for_prune_with_dummy_keyword():
    data_path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/file_keyword500_list.csv'
    path_kf = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/keywords500_files.csv'

    q_list = [[["futur", "market"], ["offer", "question"]],
              [["futur", "market", "receiv"], ["offer", "question", "energi"]]
              ]
    dummy_keyword_list = ["234dfsf", "734dfh"]
    # Here, add some extra parameters
    bf_size_list = [900, 1200, 1500, 1800, 2100, 2400]
    bf_hash_count_list = [6, 5, 4, 3, 2]
    group_prime = 256

    # Test for prune with dummy keyword
    DNF_query_result_prune = {}
    for bf_size in bf_size_list:
        for bf_hash_count in bf_hash_count_list:
            for q in q_list:
                print("Start query: %s" % list2str(q))
                T_Setup_list_prune = []
                T_gentoken_list_prune = []
                T_Search_list_prune = []
                accuracy_list_prune = []
                # Here, change 1 to 10
                for i in range(10):
                    print("Start test (prune, dummy): bf_size: %d, bf_hash_count: %d" % (bf_size, bf_hash_count))
                    # Setup Phase
                    path_dump = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Encrypted_Database/' + str(
                        bf_size) + '_' + str(bf_hash_count)
                    path_dump_mpk = path_dump + '_mpk.pkl'
                    path_dump_msk = path_dump + '_msk.pkl'
                    path_dump_EDB = path_dump + '_EDB.pkl'
                    mpk = pickle_mpk_deserialize(path_dump_mpk)
                    msk = pickle_msk_deserialize(path_dump_msk, mpk)
                    BF_DB = pickle_EDB_Deserialize(path_dump_EDB, mpk)
                    bsse = BSSE_Protocol(bf_size, bf_hash_count)
                    print("Loading DB has done!")
                    T_Setup, T_gentoken, T_Search, accuracy = BSSE_DNF_query_prune(bsse, BF_DB, mpk, msk, path_kf, q,
                                                                                   False, path_dump, 0,
                                                                                   dummy_keyword_list)
                    print("T_gentoken: ", T_gentoken)
                    print("T_Search: ", T_Search)
                    T_Setup_list_prune.append(T_Setup)
                    T_gentoken_list_prune.append(T_gentoken)
                    T_Search_list_prune.append(T_Search)
                    accuracy_list_prune.append(accuracy)

                    del bsse, BF_DB, mpk, msk
                    gc.collect()
                key = "bf_size: " + str(bf_size) + ", bf_hash_count: " + str(bf_hash_count) + ", q: " + list2str(q)
                value = (T_Setup_list_prune, T_gentoken_list_prune, T_Search_list_prune, accuracy_list_prune)
                DNF_query_result_prune[key] = value
                path_dump_result_prune_partial = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/with_prune/dummy/size_count_q/result_prune_partial_' + str(
                    bf_size) + '_' + str(bf_hash_count) + '.pkl'
                obj2pkl(DNF_query_result_prune, path_dump_result_prune_partial)
            path_dump_result_prune_size_count = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/with_prune/dummy/size_count/result_prune_size_count_' + str(
                bf_size) + '_' + str(bf_hash_count) + '.pkl'
            obj2pkl(DNF_query_result_prune, path_dump_result_prune_size_count)
    path_dump_result_prune = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/with_prune/dummy/result_prune_final_with_dummy.pkl'
    obj2pkl(DNF_query_result_prune, path_dump_result_prune)


def comparison_test():
    Bq_list_DNF = [
        [['color', 'border'], ['commission', 'softwar']],
        [['round', 'board'], ['protect', 'georg']],
        [['court', 'agenc'], ['produc', 'onlin']],
        [['march', 'technolog'], ['control', 'recent']],
        [['demand', 'account'], ['respons', 'long']],
        [['sunday', 'practic', 'night'], ['attempt', 'retail', 'dasovich']],
        [['employe', 'legal', 'build'], ['summer', 'billion', 'begin']],
        [['link', 'account', 'develop'], ['perform', 'present', 'time']],
        [['copyright', 'sell', 'right'], ['document', 'know', 'receiv']],
        [['contact', 'custom', 'inform'], ['sent', 'want', 'make']]
    ]

    data_path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/file_keyword500_list.csv'
    path_kf = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/keywords500_files.csv'

    dummy_keyword_list = ["234dfsf", "734dfh"]
    # Here, add some extra parameters
    bf_size_list = [2400]
    bf_hash_count_list = [2]
    group_prime = 256

    # Test for prune with dummy keyword
    DNF_query_result_prune = {}
    for bf_size in bf_size_list:
        for bf_hash_count in bf_hash_count_list:
            for q in Bq_list_DNF:
                print("Start query: %s" % list2str(q))
                T_Setup_list_prune = []
                T_gentoken_list_prune = []
                T_Search_list_prune = []
                accuracy_list_prune = []
                # Here, change 1 to 10
                for i in range(10):
                    print("Start test (prune, dummy): bf_size: %d, bf_hash_count: %d" % (bf_size, bf_hash_count))
                    # Setup Phase
                    path_dump = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Encrypted_Database/' + str(
                        bf_size) + '_' + str(bf_hash_count)
                    path_dump_mpk = path_dump + '_mpk.pkl'
                    path_dump_msk = path_dump + '_msk.pkl'
                    path_dump_EDB = path_dump + '_EDB.pkl'
                    mpk = pickle_mpk_deserialize(path_dump_mpk)
                    msk = pickle_msk_deserialize(path_dump_msk, mpk)
                    BF_DB = pickle_EDB_Deserialize(path_dump_EDB, mpk)
                    bsse = BSSE_Protocol(bf_size, bf_hash_count)
                    print("Loading DB has done!")
                    T_Setup, T_gentoken, T_Search, accuracy = BSSE_DNF_query_prune(bsse, BF_DB, mpk, msk, path_kf, q,
                                                                                   False, path_dump, 0,
                                                                                   dummy_keyword_list)
                    print("T_gentoken: ", T_gentoken)
                    print("T_Search: ", T_Search)
                    T_Setup_list_prune.append(T_Setup)
                    T_gentoken_list_prune.append(T_gentoken)
                    T_Search_list_prune.append(T_Search)
                    accuracy_list_prune.append(accuracy)

                    del bsse, BF_DB, mpk, msk
                    gc.collect()
                key = "bf_size: " + str(bf_size) + ", bf_hash_count: " + str(bf_hash_count) + ", q: " + list2str(q)
                value = (T_Setup_list_prune, T_gentoken_list_prune, T_Search_list_prune, accuracy_list_prune)
                DNF_query_result_prune[key] = value
                path_dump_result_prune_partial = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Comparison_result/dummy/size_count_q/result_prune_partial_' + str(
                    bf_size) + '_' + str(bf_hash_count) + '.pkl'
                obj2pkl(DNF_query_result_prune, path_dump_result_prune_partial)
            path_dump_result_prune_size_count = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Comparison_result/dummy/size_count/result_prune_size_count_' + str(
                bf_size) + '_' + str(bf_hash_count) + '.pkl'
            obj2pkl(DNF_query_result_prune, path_dump_result_prune_size_count)
    path_dump_result_prune = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Comparison_result/dummy/result_prune_final_with_dummy.pkl'
    obj2pkl(DNF_query_result_prune, path_dump_result_prune)


def test():
    data_path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/file_keyword500_list.csv'
    path_kf = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/keywords500_files.csv'

    q_list = [
              [["futur", "market", "receiv"], ["offer", "question", "energi"]]
              ]
    dummy_keyword_list = ["234dfsf", "734dfh"]
    # Here, add some extra parameters
    bf_size_list = [1200, 1800, 2400]
    bf_hash_count_list = [5, 4, 3, 2]
    group_prime = 256

    # Test for prune with dummy keyword
    DNF_query_result_prune = {}
    for bf_size in bf_size_list:
        for bf_hash_count in bf_hash_count_list:
            for q in q_list:
                print("Start query: %s" % list2str(q))
                T_Setup_list_prune = []
                T_gentoken_list_prune = []
                T_Search_list_prune = []
                accuracy_list_prune = []
                # Here, change 1 to 10
                for i in range(10):
                    print("Start test (prune, dummy): bf_size: %d, bf_hash_count: %d" % (bf_size, bf_hash_count))
                    # Setup Phase
                    path_dump = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Encrypted_Database/' + str(
                        bf_size) + '_' + str(bf_hash_count)
                    path_dump_mpk = path_dump + '_mpk.pkl'
                    path_dump_msk = path_dump + '_msk.pkl'
                    path_dump_EDB = path_dump + '_EDB.pkl'
                    mpk = pickle_mpk_deserialize(path_dump_mpk)
                    msk = pickle_msk_deserialize(path_dump_msk, mpk)
                    BF_DB = pickle_EDB_Deserialize(path_dump_EDB, mpk)
                    bsse = BSSE_Protocol(bf_size, bf_hash_count)
                    print("Loading DB has done!")
                    T_Setup, T_gentoken, T_Search, accuracy = BSSE_DNF_query_prune(bsse, BF_DB, mpk, msk, path_kf, q,
                                                                                   False, path_dump, 0, dummy_keyword_list)
                    print("T_gentoken: ", T_gentoken)
                    print("T_Search: ", T_Search)
                    T_Setup_list_prune.append(T_Setup)
                    T_gentoken_list_prune.append(T_gentoken)
                    T_Search_list_prune.append(T_Search)
                    accuracy_list_prune.append(accuracy)

                    del bsse, BF_DB, mpk, msk
                    gc.collect()
                key = "bf_size: " + str(bf_size) + ", bf_hash_count: " + str(bf_hash_count) + ", q: " + list2str(q)
                value = (T_Setup_list_prune, T_gentoken_list_prune, T_Search_list_prune, accuracy_list_prune)
                DNF_query_result_prune[key] = value
                path_dump_result_prune_partial = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/with_prune/dummy/size_count_q/result_prune_partial_' + str(
                    bf_size) + '_' + str(bf_hash_count) + '.pkl'
                obj2pkl(DNF_query_result_prune, path_dump_result_prune_partial)
            path_dump_result_prune_size_count = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/with_prune/dummy/size_count/result_prune_size_count_' + str(
                bf_size) + '_' + str(bf_hash_count) + '.pkl'
            obj2pkl(DNF_query_result_prune, path_dump_result_prune_size_count)
    path_dump_result_prune = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/with_prune/dummy/result_prune_final_with_dummy.pkl'
    obj2pkl(DNF_query_result_prune, path_dump_result_prune)

    # Test without prune without dummy keyword
    # DNF_query_result = {}
    # for bf_size in bf_size_list:
    #     for bf_hash_count in bf_hash_count_list:
    #         for q in q_list:
    #             print("Start query: %s" % list2str(q))
    #             T_Setup_list = []
    #             T_gentoken_list = []
    #             T_Search_list = []
    #             accuracy_list = []
    #             # Here, change 1 to 10
    #             for i in range(10):
    #                 print("Start test (without prune): bf_size: %d, bf_hash_count: %d" % (bf_size, bf_hash_count))
    #                 # Setup Phase
    #                 path_dump = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Encrypted_Database/' + str(
    #                     bf_size) + '_' + str(bf_hash_count)
    #                 path_dump_mpk = path_dump + '_mpk.pkl'
    #                 path_dump_msk = path_dump + '_msk.pkl'
    #                 path_dump_EDB = path_dump + '_EDB.pkl'
    #                 mpk = pickle_mpk_deserialize(path_dump_mpk)
    #                 msk = pickle_msk_deserialize(path_dump_msk, mpk)
    #                 BF_DB = pickle_EDB_Deserialize(path_dump_EDB, mpk)
    #                 bsse = BSSE_Protocol(bf_size, bf_hash_count)
    #                 print("Loading DB has done!")
    #                 T_Setup, T_gentoken, T_Search, accuracy = BSSE_DNF_query(bsse, BF_DB, mpk, msk, path_kf, q,
    #                                                                          False, path_dump, 0)
    #                 print("T_gentoken: ", T_gentoken)
    #                 print("T_Search: ", T_Search)
    #                 T_Setup_list.append(T_Setup)
    #                 T_gentoken_list.append(T_gentoken)
    #                 T_Search_list.append(T_Search)
    #                 accuracy_list.append(accuracy)
    #             key = "bf_size: " + str(bf_size) + ", bf_hash_count: " + str(bf_hash_count) + ", q: " + list2str(q)
    #             value = (T_Setup_list, T_gentoken_list, T_Search_list, accuracy_list)
    #             DNF_query_result[key] = value
    #             path_dump_result_partial = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/without_prune/size_count_q/result_partial_' + str(
    #             bf_size) + '_' + str(bf_hash_count) + '.pkl'
    #             obj2pkl(DNF_query_result, path_dump_result_partial)
    #         path_dump_result_size_count = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/without_prune/size_count/result_partial_' + str(
    #             bf_size) + '_' + str(bf_hash_count) + '.pkl'
    #         obj2pkl(DNF_query_result, path_dump_result_size_count)
    # path_dump_result = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/without_prune/result_final_without_dummy.pkl'
    # obj2pkl(DNF_query_result, path_dump_result)

    # Test without prune with dummy keyword
    # del DNF_query_result
    # gc.collect()
    DNF_query_result = {}
    for bf_size in bf_size_list:
        for bf_hash_count in bf_hash_count_list:
            for q in q_list:
                print("Start query: %s" % list2str(q))
                T_Setup_list = []
                T_gentoken_list = []
                T_Search_list = []
                accuracy_list = []
                # Here, change 1 to 10
                for i in range(10):
                    print("Start test (without prune, with dummy): bf_size: %d, bf_hash_count: %d" % (bf_size, bf_hash_count))
                    # Setup Phase
                    path_dump = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Encrypted_Database/' + str(
                        bf_size) + '_' + str(bf_hash_count)
                    path_dump_mpk = path_dump + '_mpk.pkl'
                    path_dump_msk = path_dump + '_msk.pkl'
                    path_dump_EDB = path_dump + '_EDB.pkl'
                    mpk = pickle_mpk_deserialize(path_dump_mpk)
                    msk = pickle_msk_deserialize(path_dump_msk, mpk)
                    BF_DB = pickle_EDB_Deserialize(path_dump_EDB, mpk)
                    bsse = BSSE_Protocol(bf_size, bf_hash_count)
                    print("Loading DB has done!")
                    T_Setup, T_gentoken, T_Search, accuracy = BSSE_DNF_query(bsse, BF_DB, mpk, msk, path_kf, q,
                                                                             False, path_dump, 0, dummy_keyword_list)
                    print("T_gentoken: ", T_gentoken)
                    print("T_Search: ", T_Search)
                    T_Setup_list.append(T_Setup)
                    T_gentoken_list.append(T_gentoken)
                    T_Search_list.append(T_Search)
                    accuracy_list.append(accuracy)
                key = "bf_size: " + str(bf_size) + ", bf_hash_count: " + str(bf_hash_count) + ", q: " + list2str(q)
                value = (T_Setup_list, T_gentoken_list, T_Search_list, accuracy_list)
                DNF_query_result[key] = value
                path_dump_result_partial = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/without_prune/dummy/size_count_q/result_partial_' + str(
                    bf_size) + '_' + str(bf_hash_count) + '.pkl'
                obj2pkl(DNF_query_result, path_dump_result_partial)
            path_dump_result_size_count = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/without_prune/dummy/size_count/result_partial_' + str(
                bf_size) + '_' + str(bf_hash_count) + '.pkl'
            obj2pkl(DNF_query_result, path_dump_result_size_count)
    path_dump_result = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/without_prune/dummy/result_final_with_dummy.pkl'
    obj2pkl(DNF_query_result, path_dump_result)


if __name__ == "__main__":
    # comparison_test()
    data_path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/file_keyword500_list.csv'
    with open(data_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        DB = [row for row in reader]
        for row in DB:
            print(row[0])
