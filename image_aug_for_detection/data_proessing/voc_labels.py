import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

# sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

# classes = ["group", "block", "hot","stent"]
classes = ["diode", "shadow", "stain"]
# voc_path = r"F:\data\boat1215/"
# voc_path = r"F:\data\boat1221/"
voc_path = r"F:\data\M300_opt1228/"

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open(voc_path+'outputs/%s.xml'%(image_id),encoding="utf-8")
    out_file = open(voc_path+'labels/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# wd = getcwd()


if not os.path.exists(voc_path+'labels/'):
    os.makedirs(voc_path+'labels/')
image_ids = open('dj1228.txt').read().strip().split()
list_file = open('ss.txt', 'w')
for image_id in image_ids:
    list_file.write(voc_path+'images/%s.jpg\n'%(image_id))
    print(image_id)
    convert_annotation(image_id)
list_file.close()

