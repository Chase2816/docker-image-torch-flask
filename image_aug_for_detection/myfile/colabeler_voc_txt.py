import os
import random
from glob import glob
import shutil

saved_path = r'E:\data\1113-hongyuan\VOC2007/'
# saved_path = r"E:\xunleidownload\VOCdevkit\VOC2007-200/"
# trainval_percent = 0.66
trainval_percent = 1
# train_percent = 0.8
#
train_percent = 1
xmlfilepath = saved_path + 'Annotations/'
txtsavepath = saved_path + 'ImageSets/Main'
total_xml = os.listdir(xmlfilepath)

num=len(total_xml)
list=range(num)
tv=int(num*trainval_percent)
tr=int(tv*train_percent)
trainval= random.sample(list,tv)
train=random.sample(trainval,tr)

ftrainval = open(saved_path + 'ImageSets/Main/trainval.txt', 'w')
ftest = open(saved_path + 'ImageSets/Main/test.txt', 'w')
ftrain = open(saved_path + 'ImageSets/Main/train.txt', 'w')
fval = open(saved_path + 'ImageSets/Main/val.txt', 'w')

for i  in list:
    name=total_xml[i][:-4]+'\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
             ftrain.write(name)
        else:
             fval.write(name)
    else:
         ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest .close()