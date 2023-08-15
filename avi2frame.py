import os
import numpy as np
import cv2

db_src = "F:\\workspace\\dataset\\hmdb51\\"
label = os.listdir(db_src + "video\\")
'''
print(label)
labelfile = open("F:\\workspace\\dataset\\hmdb51_label.txt", "w")
for s in label:
    labelfile.write(s+"\n")
labelfile.close()
'''

for label_name in label:
    video_src = db_src + "video\\" + label_name + "\\" + label_name + "\\"
    videos = os.listdir(video_src)

    for v in videos:
        cap = cv2.VideoCapture(video_src + v)
        v = v.split('.')[0]
        cnt = 0
        'img_{:05d}.jpg'
        flag = True
        while flag:
            flag, frame = cap.read()
            if flag:
                tar = db_src + "rawframes\\" + label_name + "\\" + v + "\\"
                if not os.path.exists(tar):
                    os.makedirs(tar)
                cv2.imwrite(tar + "img_%05d.jpg" % cnt, frame)
                cnt += 1
        cap.release()
