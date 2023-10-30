from test_BSSE import *


if __name__ == "__main__":
    data_path = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/file_keyword500_list.csv'
    path_kf = '/Users/carotpa/PaperCode/00_Enron_DataSet/02_TFIDF_Extracted/10KB/keywords500_files.csv'

    q_list = [[["note", "pleas"], ["mark", "inform"]],
              [["note", "pleas"], ["mark", "inform"], ["need", "make"]],
              [["note", "pleas", "mark"], ["mark", "inform", "mail"]],
              [["note", "pleas", "mark"], ["mark", "inform", "mail"], ["need", "make", "provid"]]
              ]
    bf_size_list = [1200, 1800, 2400]
    bf_hash_count_list = [2, 3, 4, 5]
    group_prime = 256

    # Encrypt database
    for bf_size in bf_size_list:
        for bf_hash_count in bf_hash_count_list:
            print("Start encrypt: bf_size: %d, bf_hash_count: %d" % (bf_size, bf_hash_count))
            with open(data_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                DB = [row for row in reader]
                for i in range(len(DB)):
                    DB[i] = list(filter(None, DB[i]))
            T1_Setup = time.perf_counter()
            bsse = BSSE_Protocol(bf_size, bf_hash_count)
            BF_DB, mpk, msk = bsse.Setup(DB[2:], group_prime)
            T2_Setup = time.perf_counter()
            T_Setup = T2_Setup - T1_Setup
            print("Encrypting DB has done, Encryption time is: %s" % str(T_Setup))

            path_dump = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Encrypted_Database/' + str(
                bf_size) + '_' + str(bf_hash_count)
            path_dump_mpk = path_dump + '_mpk.pkl'
            path_dump_msk = path_dump + '_msk.pkl'
            path_dump_EDB = path_dump + '_EDB.pkl'
            pickle_mpk_serialize(mpk, path_dump_mpk)
            pickle_msk_serialize(msk, path_dump_msk)
            pickle_EDB_Serialize(BF_DB, path_dump_EDB)
            print("Dumping Done!")

            del bsse, BF_DB, mpk, msk
            gc.collect()
