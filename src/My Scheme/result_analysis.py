import pickle
import matplotlib.pyplot as plt
import statistics


def compute_avg(test_times):
    # 给定的测试时间列表
    # test_times = [6.095224721000001, 4.689013038999988, 4.7306815420000135, 4.611671166999997, 4.63700309799998, 4.621931726000014, 4.6990773140000215, 4.643902310999977, 4.672528718000024, 4.597599045000038]

    # 计算平均时间
    avg_time = sum(test_times) / len(test_times)

    # 计算差值的标准差
    diffs = [abs(time - avg_time) for time in test_times]
    std_dev = statistics.stdev(diffs)

    # 去掉明显有区别的数值
    filtered_times = [time for time in test_times if abs(time - avg_time) <= std_dev]

    # 计算过滤后的平均时间
    if len(filtered_times) == 0:
        filtered_avg_time = 0
    else:
        filtered_avg_time = sum(filtered_times) / len(filtered_times)

    print("平均时间：", avg_time)
    print("去掉明显有区别的数值后的平均时间：", filtered_avg_time)
    return filtered_avg_time


path = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Final_result/result_prune_final_with_dummy.pkl'
with open(path, "rb") as file:
    dict = pickle.load(file)

for key, value in dict.items():
    print(key)
    for item in value[1:3]:
        # print(item)
        s = compute_avg(item)

# for key, value in dict.items():
#     print(key)
#     # print(value[2])
#     ypoints = value[2]
#     plt.figure(1)
#     plt.plot(ypoints, linestyle='-.')
#     plt.title(key)
#     plt.draw()
#     plt.pause(2)
#     plt.close(1)
