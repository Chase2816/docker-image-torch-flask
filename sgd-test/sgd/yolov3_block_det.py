import cv2
import numpy as np
import os
# from utils.general import non_max_suppression
# from models.experimental import attempt_load
# from torchvision import transforms
import torch
from PIL import Image, ImageDraw
import time

#轮廓面积计算函数
def areaCal(contour):
    area = 0
    for i in range(len(contour)):
        area += cv2.contourArea(contour[i])
    return area

#轮廓检测 计算面积
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
    g = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) #99

    img_open = cv2.morphologyEx(binary, cv2.MORPH_OPEN, g)
    # cv2.imshow("xx", img_open)
    img_close = cv2.morphologyEx(img_open, cv2.MORPH_CLOSE, g)
    # cv2.imshow("xc", img_close)

    _,contours,hierarchy = cv2.findContours(img_close,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print('cts_' + str(len(contours)))
    cv2.drawContours(img,contours,-1,(0,0,255),3)
    # cv2.imshow("mm",img)
    print(path," | ",areaCal(contours)," | ",areaCal(contours)/(640*480))
    # cv2.waitKey(50)
    return areaCal(contours),areaCal(contours)/(640*480)

# def box_detect(img):
#     tf = transforms.Compose([
#         transforms.Resize((512, 640)),
#         transforms.ToTensor(),
#     ])
#     model = attempt_load(r"D:\GoogleEarthProPortable\yolov5-master\runs\yolov5s\weights\last.pt")  # load FP32 model
#     model.eval()
#
#     img_tensor = tf(img)
#     pred = model(img_tensor[None])[0]
#     pred = non_max_suppression(pred, 0.4, 0.5)
#     # print(pred)
#     # print(pred[0].shape)
#
#     b1 = pred[0][0].cpu().detach().long().numpy()
#     cx1, cy1 = (b1[2] - b1[0]) / 2, (b1[3] - b1[1]) / 2
#     # print(cx1, cy1)
#     return cx1+b1[0],cy1

def yolov3_pred(img):
    confThreshold = 0.25  # 0.3
    nmsThreshold = 0.45  # 0.45  0.5
    net_input_width = 416
    net_input_height = 416

    classesFile = "boat.names"
    modelConfiguration = "yolov3.cfg"
    modelWeights = "yolov3_10000.weights"

    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (net_input_width, net_input_height), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    layersNames = net.getLayerNames()
    outs = net.forward([layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()])
    runtime, _ = net.getPerfProfile()

    frameHeight = img.shape[0]
    frameWidth = img.shape[1]

    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    box = boxes[indices[0][0]]
    x1,y1,x2,y2 = box[0],box[1],box[2]+box[0],box[3]+box[1]
    cx,cy = int((x2-x1)/2)+x1,int((y2-y1)/2)+y1
    # cx,cy = (x2-x1)/2,(y2-y1)/2
    # print(x1,y1,x2,y2,cx,cy)

    return cx,cy

start = time.time()

im_path = r"E:\pycharm_project\Data-proessing\boat\data/"

im_files = os.listdir(im_path)
im_files.sort(key=lambda x:int(x[:-4]))
print(im_files)

l = []
for i in im_files:
    area,s = findrect(im_path+"/"+i)
    if s <=0.8:
      l.append(i)
print(l)

s = []
for j in range(len(l)):
    if j == 0:
        s.append(l[j])
    if j<len(l)-1:
        if int(l[j+1].split(".")[0])-int(l[j].split(".")[0]) == 3:
            continue
        s.append(l[j+1])
print(s)

s = [int(a.split(".")[0]) for a in s]
print(s)


c = []
for k in range(1,len(s)):
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

                # cx1, cy1 = box_detect(img1)
                # cx2, cy2 = box_detect(img2)


                # draw1 = ImageDraw.Draw(img1)
                # draw2 = ImageDraw.Draw(img2)
                # draw1.rectangle((cx1,cy1,cx1+10,cy1+10),fill=(0,255,0),width=20)
                # draw2.rectangle((cx2,cy2,cx2+10,cy2+10),fill=(0,0,255),width=20)
                # img1.show()
                # img2.show()

                im1 = cv2.imread(im_path + im_files[idx])
                im2 = cv2.imread(im_path + im_files[idx + 1])
                cx1, cy1 = yolov3_pred(im1)
                cx2, cy2 = yolov3_pred(im2)
                cv2.circle(im1,(int(cx1),int(cy1)),20,(0,255,0))
                cv2.circle(im2,(int(cx2),int(cy2)),20,(255,0,0))
                cv2.imshow("im1",im1)
                cv2.imshow("im2",im2)
                cv2.waitKey(50)

                if cx2<cx1:
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
            print(f"sssssssssssss:{im_files[idx]}")
            print(s[k-1],s[k])
            if int(im_files[idx].split(".")[0]) > s[k-1]+3 and int(im_files[idx].split(".")[0]) < s[k]:
                print(im_files[idx])
                # one
                # img1 = Image.open(im_path + im_files[idx])
                # img2 = Image.open(im_path + im_files[idx +1])
                # cx1, cy1 = box_detect(img1)
                # cx2, cy2 = box_detect(img2)
                # print("cx1:cx2",cx1,cx2)

                # two
                img1 = cv2.imread(im_path + im_files[idx])
                img2 = cv2.imread(im_path + im_files[idx+1])

                cx1, cy1 = yolov3_pred(img1)
                cx2, cy2 = yolov3_pred(img2)

                cv2.circle(im1, (int(cx1), int(cy1)), 20, (0, 255, 0))
                cv2.circle(im2, (int(cx2), int(cy2)), 20, (255, 0, 0))
                cv2.imshow("im1", im1)
                cv2.imshow("im2", im2)
                cv2.waitKey(50)


                if cx2 < cx1:
                    # b.append(im_files[idx+1])
                    b.append("n")
                    # c += 1
        print(b)
        print(len(b))
        c.append(b)


print(c)
c[2][-1] = "y"
print(c)
print(c[0],len(c[0]))
print(c[1],len(c[1]))
print(c[2],len(c[2]))
print(time.time()-start)

# image_path = "data/data1/669.jpg"
# im = cv2.imread(image_path)
# x1,y1,x2,y2,cx,cy = yolov3_pred(im)
# cv2.rectangle(im,(x1,y1),(x2,y2),(255,0,0))
# cv2.circle(im,(cx,cy),1,(255,0,0),4)
# cv2.imshow("s",im)
# cv2.waitKey(0)
# print(yolov3_pred(im))