import numpy as np
import time


x = np.reciprocal(np.array([4, 4, 7, 5], dtype=float))
y = np.array([5, 2, 7, 2])
z = np.array([1, 2, 3, 4])
print(x)
print(np.multiply(x, y).astype(int))

M = np.array([[2, 0, 1, 0, 0, 0, 0], [3, 3, 2, 2, 3, 4, 1], [4, 4, 3, 3, 0, 9, 9]])
alpha = [2, 3, 4]
T1 = time.perf_counter()
for j in range(M.shape[1]):
    for i in range(M.shape[0]):
        if M[i, j] >= alpha[i]:
            print(j)
T2 = time.perf_counter()
print("traditional comparisons time:" + str(T2 - T1) + "ms")

T1 = time.perf_counter()
S = set()
for i in range(M.shape[0]):
    y = np.where(M[i, :] >= alpha[i])[0].tolist()
    S.update(y)
print(S)
T2 = time.perf_counter()
print("traditional comparisons time:" + str(T2 - T1) + "ms")
