import matplotlib.pyplot as plt

# SESAME+ 数据
sesame_times = [3.135705793125000, 3.112503017700000, 3.093671732333320, 3.079198267599890, 2.980097335999970]
sesame_accuracy = [0.911764705882352, 0.962445835339431, 0.996346728661574, 0.993050384710846, 0.962834585018293]

# TWINSSE 数据
twinsse_times = [25.8437773150071, 28.9104877644931, 30.9745563520045, 55.6266108680065, 56.4180105049963]
twinsse_accuracy = [0.493526670119109, 0.579112928593897, 0.589081058553865, 0.578113320376737, 0.731329961321035]

# 横坐标
x = [1000, 2000, 3000, 4000, 5000]

# 创建一个新的 Figure 对象，用于绘制图形
fig, ax1 = plt.subplots()

# 用ax1绘制搜索时间的折线图
color = 'tab:red'
ax1.set_xlabel('Number of queries')
ax1.set_ylabel('Time (seconds)', color=color)
ax1.plot(x, sesame_times, '-o', label='SESAME+ times', color=color)
ax1.plot(x, twinsse_times, '-o', label='TWINSSE times', color='orange')
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(loc='upper left')

# 创建一个与ax1共享横坐标的新的 Axes 对象，用于绘制搜索准确性的柱状图
ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Accuracy', color=color)
ax2.bar(x, sesame_accuracy, width=150, label='SESAME+ accuracy', color=color, alpha=0.5)
ax2.bar(x, twinsse_accuracy, width=150, label='TWINSSE accuracy', color='green', alpha=0.5)
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc='upper right')

# 添加标题
plt.title('Comparison of SESAME+ and TWINSSE')

# 显示图像
plt.show()
