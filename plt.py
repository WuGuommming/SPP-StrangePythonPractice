import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection
from matplotlib.legend_handler import HandlerPathCollection, HandlerLine2D


name = ['PGD-$L_2$', 'PGD-$L_{\infty}$', 'MultAV-$L_2$', 'MultAV-$L_{\infty}$',
        '${v=0.5,\omega=0.6}$',
        '${v=0.5,\omega=0.8}$',
        '${v=0.3,\omega=0.6}$',
        '${v=0.3,\omega=0.8}$',
        '${v=0.5,\omega=0.6}$',
        '${v=0.5,\omega=0.8}$',
        '${v=0.3,\omega=0.6}$',
        '${v=0.3,\omega=0.8}$']
col = [(161/255, 129/255, 170/255), (161/255, 129/255, 170/255), (65/255, 76/255, 135/255), (65/255, 76/255, 135/255),
       (165/255, 179/255, 120/255), (165/255, 179/255, 120/255), (165/255, 179/255, 120/255), (165/255, 179/255, 120/255),
       (101/255, 136/255, 116/255), (101/255, 136/255, 116/255), (101/255, 136/255, 116/255), (101/255, 136/255, 116/255)]

att = [100, 100, 100, 98.69,
       99.61, 98.36, 98.50, 94.70,
       99.94, 99.08, 99.22, 96.53]
d1 = [88.87, 82.40, 80.56, 57.46,
      89.73, 79.71, 76.37, 63.29,
      90.64, 84.03, 77.09, 68.19]
d5 = [85.28, 78.60, 78.08, 55.83,
      86.45, 76.96, 72.91, 62.30,
      87.63, 79.65, 74.15, 66.30]
edcol = ['white', 'white', 'white', 'white',
         'white', 'white', 'white', 'white',
         'white', 'white', 'white', 'white']

# plt.scatter(d1, d5, s=[(a - 94) * 500 for a in att],
#            label=name, c=col, marker='.', alpha=0.8,
#            edgecolors=edcol)
# plt.legend(prop={'size': 6}, ncol=2)

plt.scatter(d1[0:2], d5[0:2], s=[(a - 94) * 1000 for a in att[0:2]],
            label="PGD", c=col[0:2], marker='.', alpha=0.8,
            edgecolors=edcol[0:2])
plt.scatter(d1[2:4], d5[2:4], s=[(a - 94) * 1000 for a in att[2:4]],
            label="MultAV", c=col[2:4], marker='.', alpha=0.8,
            edgecolors=edcol[2:4])
plt.scatter(d1[4:8], d5[4:8], s=[(a - 94) * 1000 for a in att[4:8]],
            label="DFP-MBA", c=col[4:8], marker='.', alpha=0.8,
            edgecolors=edcol[4:8])
plt.scatter(d1[8:12], d5[8:12], s=[(a - 94) * 1000 for a in att[8:12]],
            label="DFP-MBA+AMBG", c=col[8:12], marker='.', alpha=0.8,
            edgecolors=edcol[8:12])


def update_scatter(handle, orig):
    handle.update_from(orig)
    handle.set_sizes([500])


def updateline(handle, orig):
    handle.update_from(orig)
    handle.set_markersize(8)


plt.legend(handler_map={PathCollection: HandlerPathCollection(update_func=update_scatter),
                        plt.Line2D: HandlerLine2D(update_func=updateline)},
           #bbox_to_anchor=(100, 50)
           loc=2, fontsize=10)

for i in range(2):
    plt.text(d1[i]+4, d5[i]-4.5, name[i], ha='center', va='bottom', fontsize=8, color=col[i])
for i in range(2, 4):
    plt.text(d1[i]+3, d5[i]-5, name[i], ha='center', va='center', fontsize=8, color=col[i])
for i in range(4, 8):
    plt.text(d1[i]-6.8*(att[i]-94)/5, d5[i]+2, name[i], ha='center', va='center', fontsize=8, color=col[i])
for i in range(8, 12):
    plt.text(d1[i]-6.5*(att[i]-94)/6, d5[i]+3, name[i], ha='center', va='center', fontsize=8, color=col[i])
plt.xlabel("FR-1(%) under denoise$_2$")
plt.ylabel("FR-1(%) under denoise$_5$")
'''
for i in range(12):
    plt.scatter(d1[i], d5[i], s=(att[i] - 92) * 1000,
                label=name[i], c=col[i], marker='.', alpha=None,
                edgecolors='white',
                cmap='viridis')
    # 用scatter绘制散点图,可调用marker修改点型, label图例用$$包起来表示使用latex公式编辑显示，写\sum符号效果比较明显，普通的符号带上后就变成了斜体，edgecolors边缘颜色，只有前两个是必备参数
    # plt.legend(prop={'size': 6}, ncol=2)
'''
plt.xlim(50, 100)
plt.ylim(50, 100)

plt.savefig("defense.png", dpi=750, bbox_inches='tight')
plt.show()

# 继续添加
'''
x = np.random.randn(10)
y = np.random.randn(10)
plt.scatter(x, y, s=200, label='$dislike$', c = 'red', marker='.', alpha = None, edgecolors= 'white')
plt.legend()  # 每次都要执行

plt.show()
'''
