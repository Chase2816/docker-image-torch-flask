import os
import argparse
import xml.etree.ElementTree as ET


def convert_voc_annotation(data_path, data_type, anno_path, use_difficult_bbox=True):

    classes = ['diaper', 'lifepaper', 'paomian_tong', 'umbrella', 'book', 'knife', 'teddy bear', 'toothbrush', 'glass',
               'metal',
               'plastic', 'paper', 'apple', 'banana', 'orange', 'broccoli', 'carrot', 'battery', 'lamp', 'paint_bucket']
    img_inds_file = os.path.join(data_path, 'ImageSets', 'Main', data_type + '.txt')
    with open(img_inds_file, 'r') as f:
        txt = f.readlines()
        image_inds = [line.strip() for line in txt]
        print(img_inds_file)

    with open(anno_path, 'a') as f:
        for image_ind in image_inds:
            print("========================", image_ind)
            image_path = os.path.join(data_path, 'JPEGImages', image_ind + '.jpg')
            annotation = image_path
            bbox = {}
            label_path = os.path.join(data_path, 'Annotations', image_ind + '.xml')
            root = ET.parse(label_path).getroot()
            objects = root.findall('object')
            for obj in objects:
                difficult = obj.find('difficult').text.strip()
                # if (not use_difficult_bbox) and(int(difficult) == 1):
                #     continue
                bbox = obj.find('bndbox')
                class_ind = classes.index(obj.find('name').text.lower().strip())
                # print(class_ind)

                class_name = obj.find('name').text.lower().strip()
                # print(class_name)
                # exit()
                xmin = bbox.find('xmin').text.strip()
                xmax = bbox.find('xmax').text.strip()
                ymin = bbox.find('ymin').text.strip()
                ymax = bbox.find('ymax').text.strip()

                # annotation += ',' + ','.join([xmin,ymin,xmax,ymax,str(class_name)])
                # print(','.join([xmin,ymin,xmax,ymax,str(class_name)]))
                # bbox[annotation] = [int(xmin),int(ymin),int(xmax),int(ymax),str(class_name)]
                annotation += ' ' + ','.join([xmin, ymin, xmax, ymax, class_name])
                # print(class_name)
                # print(annotation)
                # f.write(annotation + "\n")
                # exit()
            # print(bbox)
            # exit()
            print(annotation)
            label = annotation.split(' ')
            label_ = label[1:]
            for i in range(len(label_)):
                xml = label[0] + ',' + label_[i]
                f.write(xml + "\n")

            # exit()
            # f.write(annotation + "\n")
    return len(image_inds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default=r"G:\cai_op\image_aug_for_detection\data")
    parser.add_argument("--trainval_annotation",
                        default=r"G:\cai_op\image_aug_for_detection\test_file/litter20_trainval.txt")
    parser.add_argument("--train_annotation", default=r"G:\cai_op\image_aug_for_detection\test_file/litter10_train.txt")
    parser.add_argument("--test_annotation", default=r"G:\cai_op\image_aug_for_detection\test_file/litter10_test.txt")
    parser.add_argument("--val_annotation", default=r"G:\cai_op\image_aug_for_detection\test_file/litter10_val.txt")
    flags = parser.parse_args()

    if os.path.exists(flags.trainval_annotation): os.remove(flags.trainval_annotation)
    if os.path.exists(flags.train_annotation): os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation): os.remove(flags.test_annotation)
    if os.path.exists(flags.val_annotation): os.remove(flags.val_annotation)

    num_train = convert_voc_annotation(os.path.join(flags.data_path, 'VOC2007-200'), 'train', flags.train_annotation, False)
    num_val = convert_voc_annotation(os.path.join(flags.data_path, 'VOC2007-200'), 'val', flags.val_annotation, False)
    num_trainval = convert_voc_annotation(os.path.join(flags.data_path, 'VOC2007-200'), 'trainval',
                                          flags.trainval_annotation, False)
    # num2 = convert_voc_annotation(os.path.join(flags.data_path, 'train/VOCdevkit/VOC2012'), 'trainval', flags.train_annotation, False)
    num_test = convert_voc_annotation(os.path.join(flags.data_path, 'VOC2007-200'), 'test', flags.test_annotation, False)
    # print('=> The number of image for train is: %d\tThe number of image for test is:%d' %(num1 + num2, num3))
    print(
        '=> The number of image for trainval is: %d\tThe number of image for test is:%d\n=> The number of image for train is: %d\tThe number of image for val is:%d' % (
        num_trainval, num_test, num_train, num_val))
