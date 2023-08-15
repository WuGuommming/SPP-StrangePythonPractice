import os
tarname = "for_a40"
dataset = "ucf101"

src = "F:\\workspace\\dataset\\" + dataset + "\\"
filename = dataset + "_val_split_1_rawframes - ori.txt"
dstname = dataset + "_val_split_1_rawframes.txt"
deblurname = "val_list\\" + dataset + "_deblur=" + tarname + ".txt"

tar = "/media/hd0/wuguoming/dataset/"
res = "/root/autodl-tmp/"

file = open(src + filename, encoding="utf-8")
lines = file.readlines()
file.close()

file = open(src + dstname, "w")
# deblurfile = open(src + deblurname, "w")

for line in lines:
    print(line)
    line = line.replace(tar, res)
    line = line.replace("\\", "/")
    print(line)

    file.write(line)


'''for i in range(len(lines)):
    line = lines[i]
    print(line)
    linelist = line.split(" ")
    newline = "/media/hd0/wuguoming/att-mb/" + dataset + "/" + tarname + "/" + str(i) + " 40 " + linelist[2]
    deblurline = "/media/hd0/wuguoming/att-mb/" + dataset + "/deblur=" + tarname + "/" + str(i) + " 40 " + linelist[2]
    print(newline)
    print(deblurline)

    file.write(newline)
    deblurfile.write(deblurline)'''

file.close()
