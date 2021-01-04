import os
import shutil

# 合并内容添加到txt
# b1 = r"F:\data\boat1221\labels/"
# b2 = r"F:\data\boat1215\labels/"
#
# b1_files = os.listdir(b1)
# b2_files = os.listdir(b2)
# print(b1_files)
# print(b2_files)
# for i in b1_files:
#     print(i)
#     fp = open(b1+i, 'r')
#     for line in fp:
#         fq = open(b2+i, 'a')
#         fq.write(line)
#     fp.close()
#     fq.close()

b1 = r"F:\data\M300_opt_0104\images/"
b2 = r"F:\data\M300_opt_0104\outputs/"

c = 0
b1_files = os.listdir(b1)
b2_files = os.listdir(b2)
print(b1_files)
print(b2_files)
for i in b1_files:
    print(i)
    im_src = b1+i
    im_dst = b1+"0104_"+str(c)+".jpg"
    ann_src = b2+i.split(".")[0]+".xml"
    ann_dst = b2+"0104_"+str(c)+".xml"
    print(im_src,im_dst)
    print(ann_src,ann_dst)
    # exit()
    os.rename(im_src,im_dst)
    os.rename(ann_src,ann_dst)
    c +=1
    # shutil.copyfile(im_src,im_dst)
    # shutil.copyfile(ann_src,ann_dst)


