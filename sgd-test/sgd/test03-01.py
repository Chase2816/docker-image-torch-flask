import requests
import os
import cv2,io
import time


start = time.time()
area_url = "http://172.20.112.102:5001/predict"
det_url = "http://172.20.112.102:5001/detect"
# area_url = "http://localhost:9000/predict"
# det_url = "http://localhost:9000/detect"

im_path = r"E:\pycharm_project\Data-proessing\boat\data/"
# im_path = r"D:\GoogleEarthProPortable\data/"

im_files = os.listdir(im_path)
im_files.sort(key=lambda x: int(x[:-4]))
print(im_files)

l = []
for i in im_files:
    s = requests.session()
    s.keep_alive = False
    # s.post(url, data=data)
    # headers = {'Connection':'close'}
    img = open(im_path+i,"rb").read()
    payload = {'file':img}
    # payload1 = {'file':img}
    # r = requests.post(area_url,files=payload,headers=headers).json()
    r = requests.post(area_url,files=payload).json()
    # r = s.post(area_url, files=payload).json()

    # r1 = requests.post(det_url, files=payload1).json()
    # print(r1)
    print(r)
    print(r['s'])

    if r['s'] <= 0.8:
        l.append(i)
print(l)

s = []
for j in range(len(l)):
    if j == 0:
        s.append(l[j])
    if j < len(l) - 1:
        if int(l[j + 1].split(".")[0]) - int(l[j].split(".")[0]) == 3:
            continue
        s.append(l[j + 1])
print(s)

s = [int(a.split(".")[0]) for a in s]
print(s)
# ['672', '843', '1020']
d = []
c = []
for k in range(1, len(s)):
    print(f"k:{k}")
    if k == 1:
        a = []
        # a.append(str(s[0]) + ".jpg")
        a.append("n")
        for idx in range(len(im_files)):
            if int(im_files[idx].split(".")[0]) <= s[k]:
                print(im_files[idx])

                img1 = open(im_path + im_files[idx], "rb").read()
                img2 = open(im_path + im_files[idx+1], "rb").read()
                payload1 = {'file': img1}
                payload2 = {'file': img2}

                s2 = requests.session()
                s2.keep_alive = False
                # s.post(url, data=data)
                # r1 = s2.post(det_url,files=payload1).json()
                # r2 = s2.post(det_url,files=payload2).json()

                # headers = {'Connection': 'close'}
                r1 = requests.post(det_url, files=payload1).json()
                r2 = requests.post(det_url, files=payload2).json()
                print(r1)
                print(r2)

                im1 = cv2.imread(im_path + im_files[idx])
                im2 = cv2.imread(im_path + im_files[idx + 1])
                cv2.circle(im1, (int(r1['cx']), int(r1['cy'])), 20, (0, 255, 0))
                cv2.circle(im2, (int(r2['cx']), int(r2['cy'])), 20, (255, 0, 0))
                cv2.imshow("im1", im1)
                cv2.imshow("im2", im2)
                cv2.waitKey(50)

                if r2['cx'] < r1['cx'] and (r2['w']/r1['w'])>0.95:
                    # a.append(im_files[idx+1])
                    a.append("n")
        print(a)
        print(len(a))
        c.append(a)

    elif k < len(s):
        b = []
        # b.append(str(s[k - 1] + 3) + ".jpg")
        b.append("n")
        for idx in range(len(im_files)):
            # print(f"sssssssssssss:{im_files[idx]}")
            if int(im_files[idx].split(".")[0]) > s[k - 1] + 3 and int(im_files[idx].split(".")[0]) <= s[k]:
                print(im_files[idx])
                img1 = open(im_path + im_files[idx], "rb").read()
                img2 = open(im_path + im_files[idx + 1], "rb").read()
                payload1 = {'file': img1}
                payload2 = {'file': img2}
                s3 = requests.session()
                s3.keep_alive = False
                # s.post(url, data=data)
                # r1 = s3.post(det_url, files=payload1).json()
                # r2 = s3.post(det_url, files=payload2).json()

                # headers = {'Connection': 'close'}
                # r1 = requests.post(det_url, files=payload1, headers=headers).json()
                # r2 = requests.post(det_url, files=payload2, headers=headers).json()
                r1 = requests.post(det_url, files=payload1).json()
                r2 = requests.post(det_url, files=payload2).json()
                print(r1)
                print(r2)

                im1 = cv2.imread(im_path + im_files[idx])
                im2 = cv2.imread(im_path + im_files[idx + 1])
                cv2.circle(im1, (int(r1['cx']), int(r1['cy'])), 20, (0, 255, 0))
                cv2.circle(im2, (int(r2['cx']), int(r2['cy'])), 20, (255, 0, 0))
                cv2.imshow("im1", im1)
                cv2.imshow("im2", im2)
                cv2.waitKey(50)

                if r2['cx'] < r1['cx'] and (r2['w']/r1['w'])>0.95:
                    # b.append(im_files[idx+1])
                    b.append("n")

        print(b)
        print(len(b))
        c.append(b)

print(c)
c[2][-1] = "y"
print(c)

print(c[0], len(c[0]))
print(c[1], len(c[1]))
print(c[2], len(c[2]))
print(time.time() - start)