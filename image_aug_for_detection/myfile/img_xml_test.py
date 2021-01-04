import os
import random


img_path= r"E:\pycharm_project\image_aug_for_detection\myfile\myaugment\images"
xml_path = r"E:\pycharm_project\image_aug_for_detection\myfile\myaugment\xml"

ftest = open('test.txt', 'w')
ftrain = open('trainval.txt', 'w')

# ftest = open('E:\pycharm_project\image_aug_for_detection\myfile\myaugment\VOCdevkit\VOC2007-200\ImageSets/test.txt', 'w')
# ftrain = open('E:\pycharm_project\image_aug_for_detection\myfile\myaugment\VOCdevkit\VOC2007-200\ImageSets/train.txt', 'w')

# img_path = r"E:\data\group_string\VOC2007-200\JPEGImages"
# xml_path = r"E:\data\group_string\VOC2007-200\Annotations"
# ftest = open('E:\data\group_string\VOC2007-200\ImageSets\Main/test.txt', 'w')
# ftrain = open('E:\data\group_string\VOC2007-200\ImageSets\Main/trainval.txt', 'w')
train_percent = 0.8

total_xml = os.listdir(xml_path)

num = len(total_xml)
print(num)

list = range(num)
tr = int(num*train_percent)
train = random.sample(list,tr)

print(len(train))
for i in list:
    name = total_xml[i][:-4]+'\n'
    if i in train:
        ftrain.write(name)
    else:
        ftest.write(name)

ftrain.close()
ftest .close()