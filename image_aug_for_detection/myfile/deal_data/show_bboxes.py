import cv2
import numpy as np
from PIL import Image

# ID = 10
count = 100
for ID in range(count):
    label_txt = r"E:\pycharm_project\image_aug_for_detection\myfile\myaugment\csv_files\augmented_labels.txt"
    image_info = open(label_txt).readlines()[ID].split(',')
    print(image_info)
    print(image_info[0])
    image_path = image_info[0]
    image = cv2.imread(image_path)
    print(image.shape)
    print(image_info[1:])
    print(image_info[4])
    image = cv2.rectangle(image,(int(float(image_info[1])),
                                 int(float(image_info[2]))),
                                (int(float(image_info[3])),
                                 int(float(image_info[4]))),(255,0,0),2)
    # cv2.imshow('im',image)
    # cv2.waitKey(0)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    image = Image.fromarray(np.uint8(image))
    image.show()

