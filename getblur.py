import PIL
from PIL import Image, ImageDraw
import numpy
import random


base = "D:\\workspace\\论文\\motion blur\\img\\simple\\"

#savepath = "img\\1433\\"
'''
oriname = "img_00091.jpg"
advname = "19.jpg"
ori = numpy.array(Image.open(base+oriname).convert("RGB")).astype('float64')
adv = numpy.array(Image.open(base+advname).convert("RGB")).astype('float64')

pertu = abs(ori - adv)
red = numpy.array([0., 255., 255.])
blue = numpy.array([255., 255., 0.])
tmp = numpy.copy(pertu)
tmp01 = numpy.copy(pertu)
s = numpy.max(tmp)
print(s)
tt = 1
random.seed(123)
for i in range(tt, 224, tt):
    for j in range(tt, 224, tt):
        t = random.uniform(-1, 1)
        bb = [255, 255, 255]
        if t > 1:
            aa = red * tmp[i][j] / s
        elif t < -1:
            aa = blue * tmp[i][j] / s
            bb = blue
        else:
            r = random.uniform(-1, 1)
            if -0.2 < r < 0.2:
                aa = [0, 0, 0]
                bb = red
            elif r > 0:
                aa = tmp[i][j] / 100 * red
                bb = red
            else:
                aa = tmp[i][j] / 100 * blue
                bb = blue

        if tmp[i][j][0] <= 10 and tmp[i][j][1] <= 10 and tmp[i][j][2] <= 10:
            bb = [0, 0, 0]

        for ki in range(tt):
            for kj in range(tt):
                for ch in range(3):
                    tmp[i-ki][j-kj][ch] = aa[ch]
                    tmp01[i-ki][j-kj][ch] = bb[ch]

for i in range(0, 224):
    for j in range(0, 224):
        for k in range(0, 3):
            tmp[i][j][k] = max(0, tmp[i][j][k])
            tmp[i][j][k] = min(255, tmp[i][j][k])
tmp = tmp[25:125, 50:150, :]
tmp01 = tmp01[25:125, 50:150, :]
f = numpy.array(255-tmp).astype('uint8')
f = Image.fromarray(f).convert("RGB")
# f = f.resize((256, 256), PIL.Image.NEAREST)
f.save(base + "grad3" + ".jpg")

f = numpy.array(255-tmp01).astype('uint8')
f = Image.fromarray(f).convert("RGB")
# f = f.resize((256, 256), PIL.Image.NEAREST)
f.save(base + "direction3" + ".jpg")

'''

val = [[0.5, 1., 0.7, 1., 1.],
       [0.6, 0.5, 1., 1., 1.],
       [1., 0.9, 1., 0.3, 1.],
       [0.4, 1., 1., 0.6, 1.],
       [0.4, 1., 1., 0.6, 1.]]
val = numpy.array(val)
random.seed(223)
for i in range(5):
    for j in range(5):
        val[i][j] = random.uniform(-12, 30)
ss = abs(val).sum()
sa = abs(val).max()
si = abs(val).min()
print(ss / 25)
print((sa+si)/2)
print(sa-si)
print(ss / 25 / (sa-si) * 2)
val = (abs(val)-(sa+si)/2) / ((sa-si) / 2) * (ss / 25) / ((sa+si) / 2)  # 除标准化 乘平均值 除期望平均值（最大最小值的期望）
# val * ss / ((sa-si)^2 * 25 / 2)
# 方向相反 越小越需要攻击 权重越大
# (-1,1)或者(0,1)都可以控制平均攻击强度50%
# 不能改变正负性 非对称区间处理后还得是非对称
# one-step 不能学习数据特征 尝试用均值方差等特征来估计分布

# 梯度区间非对称 说明这一帧更加敏感？应该尽量不攻击还是尽量多反向攻击？  粗略说 脆弱就攻击 不管梯度  多攻击区间大头
# 既考虑最大值最小值的非对称 也要考虑均值的非对称
# 均值非对称两种情况（少见 可以采集数据统计）
# 梯度分布以正负数量为主！！不是数值  标准化除(|max|+|min|) / 2 因为后续有截断操作，并不需要一定在(-1,1) 避免差距过大所以不直接用最大值做标准化
# 1.运动模糊方向不对称 梯度相对对称 同向筛选掉之后 运动模糊多的部分对应剩下的梯度少的部分 -> 多攻击 权重越大 进行的反向修改越多 越不利于攻击
#       尤其常见于 背景简单 运动物体内部不复杂且没有完整边界 导致内部外部模糊不对称 难以引入额外信息 某种意义上是运动模糊攻击的短板
#    min(count0, count1) / max(count0, count1)   type1
# 2.梯度方向不对称 运动模糊相对对称 能够帮助模型确认分类（梯度为负较多）或者否定分类（梯度为正较多）的关键帧 或者是过拟合比较严重的帧 -> 多攻击 混淆
#    max(count0, count1) / min(count0, count1)   type2
# (以上是最后权值 如果在1-gw之前操作则要取相反数 很麻烦)
# 上述两者互相中和 视为一个系数

# 另外考虑 即使比较对称 但仍然利用梯度（剩下的）区分重要帧和不重要帧
# 某帧在某个位置出现了集中的梯度（实际均值和理论均值不同 越远越重要） 说明视频帧?重要? 越不攻击

# (-2, 2) -> 0 假设均值为1.2 区间压缩
# 取值(-1, 1) 没有1.2  压缩系数1-1.2/4 后1.2变为1.2*0.7 -> 0.84
# (-0.8, 1) -> 0.1 均值为-0.2 区间压缩
# 两种均值之差占总长度的比例 1 + abs(理论均值-实际均值)/(max-min)


print(val)
for i in range(5):
    for j in range(5):
        val[i][j] = min(val[i][j], 1.)
        val[i][j] = max(val[i][j], -1.)
print(val)

white = [238, 229, 242]
green = [122, 125, 92]
frame = [[[[0]*3]*8]*5] * 5
frame = numpy.array(frame).astype('float64')

for i in range(5):
    for j in range(5):
        frame[i][0][j] = green
    for j in range(1, 5):
        for k in range(0, i+1):
            frame[i][j][k] = white
        for k in range(i+1, 5):
            frame[i][j][k] = green
frame = frame[:, :, :5, :]
for i in range(5):
    f = numpy.array(frame[i]).astype('uint8')
    f = Image.fromarray(f).convert("RGB")
    f = f.resize((150, 150), PIL.Image.NEAREST)
    f.save(base + "frame" + str(i) + ".jpg")

mb = frame[0] * 0.6
for i in range(1, 5):
    mb += frame[i] * 0.1
f = numpy.array(mb).astype('uint8')
f = Image.fromarray(f).convert("RGB")
f = f.resize((150, 150), PIL.Image.NEAREST)
f.save(base + "mb.jpg")

pertu = mb - frame[0]
f = numpy.array(255-pertu).astype('uint8')
f = Image.fromarray(f).convert("RGB")
f = f.resize((150, 150), PIL.Image.NEAREST)
f.save(base + "oripertu.jpg")

for i in range(0, 5):
    f = numpy.array(255 - pertu*(0.6+i*0.16)).astype('uint8')
    f = Image.fromarray(f).convert("RGB")
    f = f.resize((150, 150), PIL.Image.NEAREST)
    f.save(base + "step" + str(i) + ".jpg")

newpertu = numpy.copy(pertu)
fv = val
for i in range(5):
    for j in range(5):
        t = random.random()
        if pertu[i][j][0] == 0:
            fv[i][j] = [0, 0, 0]
        elif t > 0.5:
            fv[i][j] = 1
        else:
            fv[i][j] = abs(val[i][j])
        pertu[i][j] = pertu[i][j] * fv[i][j]

print(fv)
f = numpy.array(255-pertu).astype('uint8')
f = Image.fromarray(f).convert("RGB")
f = f.resize((150, 150), PIL.Image.NEAREST)
f.save(base + "finalpertu.jpg")

f = numpy.array(pertu+frame[0]).astype('uint8')
f = Image.fromarray(f).convert("RGB")
f = f.resize((150, 150), PIL.Image.NEAREST)
f.save(base + "grad-ad.jpg")

for i in range(5):
    for j in range(5):
        if not (fv[i][j] == 1 or fv[i][j] == 0):
            fv[i][j] = int(fv[i][j] / (1. / 5.)) * 0.16 + 0.6
            newpertu[i][j] = newpertu[i][j] * fv[i][j]
print(fv)

f = numpy.array(255-newpertu).astype('uint8')
f = Image.fromarray(f).convert("RGB")
f = f.resize((150, 150), PIL.Image.NEAREST)
f.save(base + "T-pertu.jpg")

f = numpy.array(newpertu+frame[0]).astype('uint8')
f = Image.fromarray(f).convert("RGB")
f = f.resize((150, 150), PIL.Image.NEAREST)
f.save(base + "T-adv.jpg")
