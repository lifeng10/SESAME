import pickle
import statistics


def compute_avg(test_times):
    # 给定的测试时间列表
    # test_times = [6.095224721000001, 4.689013038999988, 4.7306815420000135, 4.611671166999997, 4.63700309799998, 4.621931726000014, 4.6990773140000215, 4.643902310999977, 4.672528718000024, 4.597599045000038]

    # 计算平均时间
    avg_time = sum(test_times) / len(test_times)
    print("平均时间：", avg_time)

    # 计算差值的标准差
    diffs = [abs(time - avg_time) for time in test_times]
    std_dev = statistics.stdev(diffs)

    # 去掉明显有区别的数值
    filtered_times = [time for time in test_times if abs(time - avg_time) <= std_dev]

    # 计算过滤后的平均时间
    if len(filtered_times) == 0:
        filtered_avg_time = avg_time
    else:
        filtered_avg_time = sum(filtered_times) / len(filtered_times)

    print("去掉明显有区别的数值后的平均时间：", filtered_avg_time)
    return filtered_avg_time

path = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/CNFFilter/experiment_result/result_final.pkl'
with open(path, "rb") as file:
    dict = pickle.load(file)

token_time = []
search_time = []
accuracy = []
for key, value in dict.items():
    # if "bf_size: 2400, bf_hash_count: 2," in key:
    print(key)
    # for item in value:
    #     print(item)
    # break
    print(value[2])
    # print(value[3])
    search_time.append(compute_avg(value[2]))
    # print(value[6])
    # accuracy.append(value[2][0])
    # print(value[1])
    # token_time.append(compute_avg(value[1]))
    # print(value[2])
    # search_time.append(compute_avg(value[2]))
    # print(value[3])
    # accuracy.append(value[3][0])
# print('================================================================================')
# print('token time')
# for item in token_time:
#     print(item)
print('search time')
for item in search_time:
    print(item)
# print('accuracy')
# for item in accuracy:
#     print(item)
