import os
import argparse
import xml.etree.ElementTree as ET

def convert_voc_annotation(data_path, data_type, anno_path, use_difficult_bbox=True):

    # classes = ['diode', 'shadow', 'stain']
    classes = ['group string','break']
    img_inds_file = os.path.join(data_path, 'ImageSets', 'Main', data_type + '.txt')
    with open(img_inds_file, 'r') as f:
        txt = f.readlines()
        image_inds = [line.strip() for line in txt]

    with open(anno_path, 'a') as f:
        for image_ind in image_inds:
            image_path = os.path.join(data_path, 'JPEGImages', image_ind + '.jpg')
            # image_path = data_path + 'JPEGImages' +'/' + image_ind + '.jpg'
            annotation = image_path
            label_path = os.path.join(data_path, 'Annotations', image_ind + '.xml')
            root = ET.parse(label_path).getroot()
            objects = root.findall('object')
            for obj in objects:
                difficult = obj.find('difficult').text.strip()
                if (not use_difficult_bbox) and(int(difficult) == 1):
                    continue
                bbox = obj.find('bndbox')
                class_name = obj.find('name').text.strip()
                class_ind = classes.index(obj.find('name').text.lower().strip())
                xmin = bbox.find('xmin').text.strip()
                xmax = bbox.find('xmax').text.strip()
                ymin = bbox.find('ymin').text.strip()
                ymax = bbox.find('ymax').text.strip()
                annotation += '+' + ','.join([xmin, ymin, xmax, ymax, class_name])
            print(annotation)
            # f.write(annotation + "\n")


            print(annotation)
            label = annotation.split('+')
            # print(label)
            # exit()
            label_ = label[1:]
            for i in range(len(label_)):
                xml = label[0] + ',' + label_[i]
                f.write(xml + "\n")
    return len(image_inds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="E:\data\group_string\VOC2007/")
    parser.add_argument("--train_annotation", default="E:/pycharm_project/image_aug_for_detection/myfile/voc_train.txt")
    parser.add_argument("--test_annotation",  default="E:/pycharm_project/image_aug_for_detection/myfile/voc_test.txt")
    flags = parser.parse_args()

    if os.path.exists(flags.train_annotation):os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation):os.remove(flags.test_annotation)

    num1 = convert_voc_annotation(os.path.join(flags.data_path), 'trainval', flags.train_annotation, False)
    # num1 = convert_voc_annotation(os.path.join(flags.data_path),  'test', flags.test_annotation, False)
    print('=> The number of image for train is: %d' %(num1))


