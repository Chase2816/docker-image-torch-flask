FROM python:3.7

ADD ./yolov5s /code

WORKDIR /code

RUN apt-get update
RUN apt install libgl1-mesa-glx -y 

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

RUN pip install torch-1.6.0+cpu-cp37-cp37m-linux_x86_64.whl

RUN pip install torchvision-0.7.0+cpu-cp37-cp37m-linux_x86_64.whl

CMD ["python","app.py"]

