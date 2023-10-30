import matplotlib.pyplot as plt

# 四组输入数据
sesame_times = [3.66, 3.60, 3.44, 3.47, 3.46]
twinsse_ox_tcnf_times = [36.89, 40.47, 42.20, 63.99, 69.69]
twinsse_ox_tdnf_times = [8.90, 12.60, 15.97, 20.61, 23.09]
cnf_filter_times = [0.06, 0.11, 0.20, 0.30, 0.47]

# 横坐标
x = [1000, 2000, 3000, 4000, 5000]

# 创建一个新的Figure对象，用于绘制图形
fig, ax = plt.subplots()

legend_label_CNF = r'$\mathrm{{TWINSSE}}_{\mathrm{{OXT}}}$ CNF'
legend_label_DNF = r'$\mathrm{{TWINSSE}}_{\mathrm{{OXT}}}$ DNF'

# 绘制四组输入的对比图
ax.plot(x, sesame_times, marker='o', label='SESAME+', linewidth=2)
ax.plot(x, twinsse_ox_tcnf_times, marker='s', label=legend_label_CNF, linewidth=2)
ax.plot(x, twinsse_ox_tdnf_times, marker='^', label=legend_label_DNF, linewidth=2)
ax.plot(x, cnf_filter_times, marker='*', label='CNFFilter', linewidth=2)

# 设置图形属性
ax.set_xlabel('Number of Results', fontsize=16)
ax.set_ylabel('Time (seconds)', fontsize=16)
ax.set_title('Performance Comparison', fontsize=16)
ax.legend(fontsize=14)
ax.grid(True)

ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)

# 自动调整画布大小
fig.tight_layout()

plt.savefig("comparison.pdf", format='pdf')

# 显示图像
plt.show()