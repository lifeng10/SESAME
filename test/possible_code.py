import matplotlib.pyplot as plt
# 3 V 3
# SESAME+ 数据
# sesame_times = [3.656145698000120, 3.604369720777560, 3.439008261749670, 3.467450416666900, 3.457608349999190]
# sesame_accuracy = [0.805184603299293, 0.963872832369942, 0.902769416014449, 0.959501557632398, 0.977916748094586]

# TWINSSE 数据
# twinsse_times = [36.8941906964035, 40.4710475263321, 42.1995343884991, 63.9908299070011, 69.6873610759939]
# twinsse_accuracy = [0.928769657724329, 0.584115071919949, 0.678373382624769, 0.612061939690301, 0.749202975557917]

# 2 V 2
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

# 创建一个图例，并使用LaTeX语法显示带下标的字符串
legend_label_time = r'$\mathrm{{TWINSSE}}_{\mathrm{{OXT}}}$ times'

# 用ax1绘制搜索时间的折线图
color = 'tab:red'
ax1.set_xlabel('Number of Results', fontsize=16)
ax1.set_ylabel('Time (seconds)', color=color, fontsize=16)
ax1.plot(x, sesame_times, '-o', label='SESAME+ times', color=color)
ax1.plot(x, twinsse_times, '-o', label=legend_label_time, color='orange')
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(loc='upper left', fontsize=12)

# 创建一个与ax1共享横坐标的新的 Axes 对象，用于绘制搜索准确性的柱状图
ax2 = ax1.twinx()

# 创建一个图例，并使用LaTeX语法显示带下标的字符串
legend_label_accuracy = r'$\mathrm{{TWINSSE}}_{\mathrm{{OXT}}}$ accuracy'

color = 'tab:blue'
ax2.set_ylabel('Accuracy', color=color, fontsize=16)
ax2.bar(x, sesame_accuracy, width=250, label='SESAME+ accuracy', color=color, alpha=0.5)
ax2.bar(x, twinsse_accuracy, width=250, label=legend_label_accuracy, color='green', alpha=0.5)
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(loc='upper right', fontsize=12)

# 调整坐标轴字体大小
ax1.tick_params(axis='x', labelsize=15)
ax1.tick_params(axis='y', labelsize=15)
ax2.tick_params(axis='y', labelsize=15)
# 自动调整画布大小
# fig.tight_layout()
# plt.xticks(x)
# fig.set_size_inches(550/80, 400/80)
# plt.subplots_adjust(wspace=10, hspace=10)

# 设置y轴范围
ax1.set_ylim([0, max(max(sesame_times), max(twinsse_times)) + 15])
ax2.set_ylim([0, 1.21])

# 添加标题
plt.title('Comparison of SESAME+ and '+r'$\mathrm{{TWINSSE}}_{\mathrm{{OXT}}}$', fontsize=16)

plt.tight_layout()

plt.savefig("comparison_2.pdf", format='pdf')

# 显示图像
plt.show()
