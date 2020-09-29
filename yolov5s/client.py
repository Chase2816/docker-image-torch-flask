import requests
import os

# image = open(r"E:\pycharm_project\Data-proessing\model_flask\timg.jpg", 'rb').read()
# payload = {'file': image}
#
# r = requests.post("http://localhost:9060/predict", files=payload).json()
# print(r)

for i in os.listdir("inference/images"):
    print(i)
    image = open("inference/images/"+i,'rb')
    payload = {'file':image}
    r = requests.post(" http://172.20.112.102:8080/predict", files=payload).json()
    print(r)
