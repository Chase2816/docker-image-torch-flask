import cv2
import numpy as np
import os
from utils.general import non_max_suppression
from models.experimental import attempt_load
from torchvision import transforms
import torch
from PIL import Image, ImageDraw
import shutil


# 轮廓面积计算函数
def areaCal(contour):
    area = 0
    for i in range(len(contour)):
        area += cv2.contourArea(contour[i])
    return area

# 轮廓检测 计算面积
def findrect(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    # cv2.imshow("b", binary)
    # cv2.imshow("gray", gray)
    # ret,binary = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
    d = cv2.dilate(binary, (3, 3))
    kernel = np.ones((3, 3), dtype=np.uint8)
    erosion = cv2.erode(binary, kernel, iterations=1)
    # ss = np.hstack((binary, erosion))
    g = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 99

    img_open = cv2.morphologyEx(binary, cv2.MORPH_OPEN, g)
    # cv2.imshow("xx", img_open)
    img_close = cv2.morphologyEx(img_open, cv2.MORPH_CLOSE, g)
    # cv2.imshow("xc", img_close)

    _, contours, hierarchy = cv2.findContours(img_close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print('cts_' + str(len(contours)))
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    # cv2.imshow("mm",img)
    print(path, " | ", areaCal(contours), " | ", areaCal(contours) / (640 * 480))
    # cv2.waitKey(50)
    return areaCal(contours), areaCal(contours) / (640 * 480)

def box_detect(img):
    tf = transforms.Compose([
        transforms.Resize((512, 640)),
        transforms.ToTensor(),
    ])
    model = attempt_load(r"D:\GoogleEarthProPortable\yolov5-master\runs\yolov5s\weights\last.pt")  # load FP32 model
    model.eval()

    img_tensor = tf(img)
    pred = model(img_tensor[None])[0]
    pred = non_max_suppression(pred, 0.4, 0.5)
    # print(pred)
    # print(pred[0].shape)

    b1 = pred[0][0].cpu().detach().long().numpy()
    cx1, cy1, w = (b1[2] - b1[0]) / 2, (b1[3] - b1[1]) / 2, b1[2] - b1[0]
    # print(cx1, cy1)
    return cx1 + b1[0], cy1 + b1[1], w

import time

start = time.time()

im_path = r"E:\pycharm_project\Data-proessing\boat\data/"
# im_path = r"D:\GoogleEarthProPortable\data/"

im_files = os.listdir(im_path)
im_files.sort(key=lambda x: int(x[:-4]))
print(im_files)

l = []
for i in im_files:
    area, s = findrect(im_path + "/" + i)
    if s <= 0.8:
        l.append(i)
print(l)

s = []
for j in range(len(l)):
    if j == 0:
        s.append(l[j])
    if j < len(l) - 1:
        if int(l[j + 1].split(".")[0]) - int(l[j].split(".")[0]) == 3:
            continue
        s.append(l[j + 1])
print(s)

s = [int(a.split(".")[0]) for a in s]
print(s)
# ['672', '843', '1020']
d = []
c = []
for k in range(1, len(s)):
    print(f"k:{k}")
    if k == 1:
        a = []
        # a.append(str(s[0]) + ".jpg")
        a.append("n")
        for idx in range(len(im_files)):
            if int(im_files[idx].split(".")[0]) <= s[k]:
                print(im_files[idx])
                img1 = Image.open(im_path + im_files[idx])
                img2 = Image.open(im_path + im_files[idx + 1])

                cx1, cy1,w1 = box_detect(img1)
                cx2, cy2,w2 = box_detect(img2)

                im1 = cv2.imread(im_path + im_files[idx])
                im2 = cv2.imread(im_path + im_files[idx + 1])
                cv2.circle(im1, (int(cx1), int(cy1)), 20, (0, 255, 0))
                cv2.circle(im2, (int(cx2), int(cy2)), 20, (255, 0, 0))
                cv2.imshow("im1", im1)
                cv2.imshow("im2", im2)
                cv2.waitKey(50)

                # if cx2 < cx1 and (w1/w2)>0.9:
                if cx2 < cx1 and (w2 / w1) > 0.95:

                    # a.append(im_files[idx+1])
                    a.append("n")
        print(a)
        print(len(a))
        c.append(a)

    elif k < len(s):
        b = []
        # b.append(str(s[k - 1] + 3) + ".jpg")
        b.append("n")
        for idx in range(len(im_files)):
            # print(f"sssssssssssss:{im_files[idx]}")
            if int(im_files[idx].split(".")[0]) > s[k - 1] + 3 and int(im_files[idx].split(".")[0]) <= s[k]:
                print(im_files[idx])
                img1 = Image.open(im_path + im_files[idx])
                img2 = Image.open(im_path + im_files[idx + 1])

                cx1, cy1,w1 = box_detect(img1)
                cx2, cy2,w2 = box_detect(img2)
                # print("cx1:cx2",cx1,cx2)
                im1 = cv2.imread(im_path + im_files[idx])
                im2 = cv2.imread(im_path + im_files[idx + 1])
                cv2.circle(im1, (int(cx1), int(cy1)), 20, (0, 255, 0))
                cv2.circle(im2, (int(cx2), int(cy2)), 20, (255, 0, 0))
                cv2.imshow("im1", im1)
                cv2.imshow("im2", im2)
                cv2.waitKey(50)

                if cx2 < cx1 and (w2/w1)>0.95:

                    # b.append(im_files[idx+1])
                    b.append("n")

        print(b)
        print(len(b))
        c.append(b)

print(c)
c[2][-1] = "y"
print(c)

print(c[0], len(c[0]))
print(c[1], len(c[1]))
print(c[2], len(c[2]))
print(time.time() - start)
cv2.waitKey(0)
