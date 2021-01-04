import os
import shutil



test_txt_file = r'E:\data\VOC2007_new\ImageSets\Main\test.txt'
trainval_txt_file = r'E:\data\VOC2007_new\ImageSets\Main\trainval.txt'
img_path = r'E:\data\VOC2007_new\JPEGImages'
copy_path = r'E:\pycharm_project\image_aug_for_detection\myfile\myaugment\images'

shutil.rmtree(copy_path)
os.mkdir(copy_path)

with open(trainval_txt_file) as f:
    strs = f.readlines()
    for path in strs:
        print(path.strip())
        img_id = os.path.join(img_path,path.strip()+'.jpg')
        print(img_id)
        dst_dir = os.path.join(copy_path,path.strip()+'.jpg')
        print(dst_dir)
        shutil.copyfile(img_id,dst_dir)
        # exit()

print(len(os.listdir(copy_path)))