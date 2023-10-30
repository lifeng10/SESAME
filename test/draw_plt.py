import matplotlib.pyplot as plt
import pickle

path = '/Users/carotpa/PaperCode/00_Enron_DataSet/Experiment_Result/BSSE/Final_result/result_prune_final_with_dummy.pkl'
with open(path, "rb") as file:
    dict = pickle.load(file)

time = []
accuracy = []
for key, value in dict.items():
    if "(futur^market^receiv)v(offer^question^energi)" in key:
        print(key)
        # print(value[2][0])
        # print(value[3][0])
        time.append(value[2][0])
        accuracy.append(value[3][0])
print(time)
print(accuracy)

# 输入数据
accuracy_data = accuracy
time_data = time
# 创建画布和轴对象
fig, ax1 = plt.subplots()

# 绘制准确性折线图
ax1.plot(accuracy_data, color='b', marker='o', label='Accuracy')
ax1.set_xlabel('Data Point')
ax1.set_ylabel('Accuracy', color='b')
ax1.tick_params('y', colors='b')

# 创建右侧纵坐标轴对象
ax2 = ax1.twinx()

# 绘制时间折线图
ax2.plot(time_data, color='r', marker='s', label='Time')
ax2.set_ylabel('Time', color='r')
ax2.tick_params('y', colors='r')

# 设置图例
lines = ax1.get_lines() + ax2.get_lines()
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='upper left')

for i in range(len(accuracy_data)):
    if i % 5 == 0:
        ax1.axvline(i, color='gray', linestyle='dashed')

# 设置标题和显示图形
plt.title('Accuracy vs. Time')
plt.show()