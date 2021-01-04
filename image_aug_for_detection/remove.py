import os
import shutil

img_dir = r"E:\pycharm_project\image_aug_for_detection\myfile\myaugment\augment_images"
voc_dir = r"E:\pycharm_project\image_aug_for_detection\myfile\voc_train.txt"
csv_dir = "myfile/myaugment/csv_files/augmented_labels.txt"

shutil.rmtree(img_dir)
os.remove(voc_dir)
os.remove(csv_dir)