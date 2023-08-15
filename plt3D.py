import numpy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def colmatrix(st, ld, ur, width, height):
    xx = ((ur[0]-st[0])/width, (ur[1]-st[1])/width, (ur[2]-st[2])/width)
    yy = ((ld[0]-st[0])/height, (ld[1]-st[1])/height, (ld[2]-st[2])/height)
    res = np.empty((height, width, 3))
    ans = np.empty((height, width), dtype=object)

    for i in range(height):
        for j in range(width):
            for k in range(3):
                res[i][j][k] = st[k] + i * yy[k] + j * xx[k]
                if res[i][j][k] > 1:
                    res[i][j][k] = 1
            ans[i][j] = tuple(res[i][j])

    return ans.ravel()


omega = np.arange(0.5, 1.0, step=0.1)
v = np.arange(0.5, 0, step=-0.1)

ucf = [[97.86, 97.01, 94.70, 88.43, 65.33],
       [96.90, 95.66, 87.22, 83.85, 56.14],
       [95.47, 93.38, 87.92, 75.00, 45.23],
       [91.95, 87.21, 77.89, 59.51, 32.42],
       [78.55, 67.48, 52.41, 34.43, 20.00]]
ucf = numpy.array(ucf)
ucfA = [[98.31, 97.88, 96.21, 92.03, 73.25],  # omega 0.5
        [97.78, 96.82, 94.73, 88.60, 64.97],
        [96.64, 95.26, 91.71, 82.02, 53.34],
        [94.36, 91.09, 86.32, 68.65, 38.81],
        [84.80, 76.01, 61.71, 42.06, 23.04]]
ucfA = numpy.array(ucfA)

hm = [[99.94, 99.67, 99.15, 97.58, 90.58],
      [99.61, 99.35, 98.50, 96.53, 87.70],
      [99.28, 98.69, 97.32, 94.24, 81.41],
      [98.36, 96.99, 94.70, 88.48, 72.64],
      [94.37, 90.97, 84.23, 75.00, 57.13]]
hm = numpy.array(hm)
hmA = [[99.94, 99.92, 99.88, 98.17, 92.63],
       [99.94, 99.67, 99.22, 97.78, 90.58],
       [99.61, 99.28, 98.36, 96.20, 86.26],
       [99.08, 98.23, 96.53, 91.95, 78.01],
       [96.40, 94.29, 88.58, 82.06, 63.73]]
hmA = numpy.array(hmA)


xx, yy = np.meshgrid(v, omega)  # 网格化坐标
v, omega = xx.ravel(), yy.ravel()  # 矩阵扁平化
bottom = np.zeros_like(v)  # 设置柱状图的底端位值
ucfA = ucfA.ravel()  # 扁平化矩阵
ucf = ucf.ravel()
hm = hm.ravel()
hmA = hmA.ravel()

width = height = 0.08  # 每一个柱子的长和宽

# 绘图设置
fig = plt.figure(dpi=300, figsize=(24, 8))
ax = fig.add_subplot(141, projection='3d')
ax.bar3d(v-width/2, omega-height/2, bottom, width, height, ucf,
         shade=True,
         color=colmatrix((46/255, 47/255, 35/255), (185/255, 199/255, 141/255), (210/255, 191/255, 165/255), 5, 5))
# 坐标轴设置
ax.set_xlim(0.55, 0.05)
ax.set_ylim(0.95, 0.45)
# ax.set_zlim(20, 100)
ax.set_xlabel('$v$')
ax.set_ylabel('$\omega$')
ax.set_zlabel('FR-1(%)', labelpad=0)
ax.set_title("FR-1(%) on UCF-101 dataset", y=1.0)

bx = fig.add_subplot(142, projection='3d')
bx.bar3d(v-width/2, omega-height/2, bottom, width, height, ucfA,
         shade=True,
         color=colmatrix((46/255, 47/255, 35/255), (185/255, 199/255, 141/255), (210/255, 191/255, 165/255), 5, 5))

# 坐标轴设置
bx.set_xlim(0.55, 0.05)
bx.set_ylim(0.95, 0.45)
# bx.set_zlim(20, 100)
bx.set_xlabel('$v$')
bx.set_ylabel('$\omega$')
bx.set_zlabel('FR-1(%)', labelpad=0)
bx.set_title("FR-1(%) with AMBG on UCF-101 dataset", y=1.0)

cx = fig.add_subplot(143, projection='3d')
cx.bar3d(v-width/2, omega-height/2, bottom, width, height, hm,
         shade=True,
         color=colmatrix((34/255, 36/255, 73/255), (156/255, 179/255, 212/255), (175/255, 90/255, 118/255), 5, 5))
# 坐标轴设置
cx.set_xlim(0.55, 0.05)
cx.set_ylim(0.95, 0.45)
# cx.set_zlim(50, 100)
cx.set_xlabel('$v$')
cx.set_ylabel('$\omega$')
cx.set_zlabel('FR-1(%)', labelpad=0)
cx.set_title("FR-1(%) on HMDB-51 dataset", y=1.0)


dx = fig.add_subplot(144, projection='3d')
dx.bar3d(v-width/2, omega-height/2, bottom, width, height, hmA,
         shade=True,
         color=colmatrix((34/255, 36/255, 73/255), (156/255, 179/255, 212/255), (175/255, 90/255, 118/255), 5, 5))
# 坐标轴设置
dx.set_xlim(0.55, 0.05)
dx.set_ylim(0.95, 0.45)
# dx.set_zlim(50, 100)
dx.set_xlabel('$v$')
dx.set_ylabel('$\omega$')
dx.set_zlabel('FR-1(%)', labelpad=0)
dx.set_title("FR-1(%) with AMBG on HMDB-51 dataset", y=1.0)


plt.subplots_adjust(hspace=0, wspace=0.1)
plt.show()
