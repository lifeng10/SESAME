import matplotlib.pyplot as plt
import numpy as np

# 数据
twinsse_time = [25.8437773150071, 28.9104877644931, 30.9745563520045, 55.6266108680065, 56.4180105049963]
sesame_time = [3.135705793125000, 3.112503017700000, 3.093671732333320, 3.079198267599890, 2.980097335999970]
twinsse_accuracy = [0.493526670119109, 0.579112928593897, 0.589081058553865, 0.578113320376737, 0.731329961321035]
sesame_accuracy = [0.911764705882352, 0.962445835339431, 0.996346728661574, 0.993050384710846, 0.962834585018293]
x = [1000, 2000, 3000, 4000, 5000]

# 创建画布
fig, ax1 = plt.subplots()

# 设置第一个y轴
color = 'tab:red'
ax1.set_xlabel('Number of Results')
ax1.set_ylabel('Time (s)', color=color)
ax1.plot(x, twinsse_time, color=color, marker='o', label='TWINSSE')
ax1.plot(x, sesame_time, color='blue', marker='s', label='SESAME+')
ax1.tick_params(axis='y', labelcolor=color)

# 设置第二个y轴
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Accuracy', color=color)
ax2.bar(np.array(x) - 200, twinsse_accuracy, width=200, align='edge', label='TWINSSE', alpha=0.7, color=color)
ax2.bar(np.array(x), sesame_accuracy, width=200, align='edge', label='SESAME+', alpha=0.7, color='orange')
ax2.tick_params(axis='y', labelcolor=color)

# 添加图例
handles, labels = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(handles + handles2, labels + labels2, loc='lower right')

# 显示图形
plt.title('Comparison of TWINSSE and SESAME+')
plt.show()
