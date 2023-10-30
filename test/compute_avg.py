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
    filtered_avg_time = sum(filtered_times) / len(filtered_times)

    print("平均时间：", avg_time)
    print("去掉明显有区别的数值后的平均时间：", filtered_avg_time)
    return filtered_avg_time


if __name__ == '__main__':
    test_times = [4.347913690000496, 4.343033095999999, 4.407196828000451, 4.408172920999277, 4.355305499999304, 4.3548561690004135, 4.349492807999923, 4.400253275998693, 4.393933134999315, 4.349624946999029, 4.347913690000496, 4.343033095999999, 4.407196828000451, 4.408172920999277, 4.355305499999304, 4.3548561690004135, 4.349492807999923, 4.400253275998693, 4.393933134999315, 4.349624946999029]

    compute_avg(test_times)
