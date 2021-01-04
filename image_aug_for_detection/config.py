class DefaultConfigs(object):
    raw_images = "./data/raw/images/"                                       # 原始图片路径
    raw_csv_files = "./data/raw/csv_files/train_labels.csv"                 # 原始csv格式标签
    augmented_images = "./data/augmented/images/"                           # 增强后的图片保存路径
    augmented_csv_file = "./data/augmented/csv_files/augmented_labels.csv"  # 增强后的csv格式的标注文件
    image_format = "jpg"                                                    # 默认图片格式
# config = DefaultConfigs()




class MyDefaultConfigs(object):
    raw_images = r"F:\data\M300_opt1228\images/"
    raw_csv_files = r"E:\pycharm_project\image_aug_for_detection\myfile\voc_train.txt"
    augmented_images = r"E:\pycharm_project\image_aug_for_detection\myfile\myaugment\augment_images/"
    augmented_csv_file = r"E:\pycharm_project\image_aug_for_detection\myfile\myaugment\csv_files/"
    image_format = "jpg"
config = MyDefaultConfigs()