'''import PIL
from PIL import Image, ImageDraw
import numpy
import random

order = 3

base = "D:\\workspace\\论文\\motion blur\\img\\494\\"

oriname = ["0pgd", "0multi", "0att3", "0att2", "0input", "0normal", "0gaussian"]

for i in range(len(oriname)):
    img = Image.open(base + oriname[i] + ".jpg")
    if oriname[i] == "0pgd" or oriname[i] == "0multi":
        tmp = Image.open(base + "0input.jpg")
        img = numpy.array(img).astype('float')
        tmp = numpy.array(tmp).astype('float')
        pertu = img - tmp
        print(pertu)
        pertu = pertu * 1.8
        img = pertu + tmp
        for ii in range(len(img)):
            for j in range(len(img[0])):
                for k in range(3):
                    if img[ii][j][k] < 0:
                        img[ii][j][k] = 0
                    if img[ii][j][k] > 255:
                        img[ii][j][k] = 255
        img = Image.fromarray(img.astype('uint8'))

    whole = numpy.array(list([[[0]*3]*224]*336))
    rec1 = (40, 120, 60, 140)
    rec2 = (120, 120, 160, 160)
    cut1 = img.crop(rec1).resize((112, 112), PIL.Image.NEAREST)
    cut2 = img.crop(rec2).resize((112, 112), PIL.Image.NEAREST)

    draw = ImageDraw.Draw(img)
    draw.rectangle(rec1, fill=None, outline=(0, 0, 255), width=3)
    draw.rectangle(rec2, fill=None, outline=(255, 0, 0), width=3)
    draw = ImageDraw.Draw(cut1)
    draw.rectangle((0, 0, 111, 111), fill=None, outline=(0, 0, 255), width=3)
    draw = ImageDraw.Draw(cut2)
    draw.rectangle((0, 0, 111, 111), fill=None, outline=(255, 0, 0), width=3)

    cut1 = numpy.array(cut1)
    cut2 = numpy.array(cut2)
    img = numpy.array(img)

    whole[0:112, 0:112] = cut1
    whole[0:112, 112:224] = cut2
    whole[112:336] = img

    whole = Image.fromarray(whole.astype('uint8'))
    whole.save(base + "cut\\" + oriname[i] + ".jpg")'''



'''
for order in range(3, 12):
    if order == 10:
        name = "adv173-34-10"
    elif order == 11:
        name = "input173"
    else:
        name = oriname + str(order)
    img = Image.open(base + name + ".jpg")

    img = img.crop((226*1 + 1, 226*22 + 1, 226*2 - 1, 226*23 - 1))
    # cut.save(base + "cut\\" + name + ".jpg")

    cut = img.crop((60, 70, 85, 95))
    cut = cut.resize((100, 100), PIL.Image.NEAREST)
    img = numpy.array(img)
    cut = numpy.array(cut)
    for i in range(100):
        for j in range(100):
            cut[i][j] = img[70+i//4][60+j//4]
    img[:100, -100:] = cut
    img = Image.fromarray(img)

    draw = ImageDraw.Draw(img)
    draw.rectangle(((60, 70), (85, 95)), fill=None, outline=(255, 0, 0), width=3)
    draw.rectangle(((224-100, 0), (224, 100)), fill=None, outline=(255, 0, 0), width=3)
    img.save(base + "cut\\" + name + ".jpg")
'''
