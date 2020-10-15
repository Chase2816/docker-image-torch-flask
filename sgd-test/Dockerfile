FROM python:3.7

ADD ./sgd /code

WORKDIR /code

RUN pip install opencv-python -i https://mirrors.aliyun.com/pypi/simple/
# RUN pip install matplotlib -i https://mirrors.aliyun.com/pypi/simple/

RUN apt-get install -y libsm6
RUN apt-get install -y libxrender1
RUN apt-get install -y libxext-dev

# RUN apt-get update
# RUN apt install libgl1-mesa-glx -y 

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

RUN pip install torch-1.6.0+cpu-cp37-cp37m-linux_x86_64.whl

RUN pip install torchvision-0.7.0+cpu-cp37-cp37m-linux_x86_64.whl

CMD ["python","test03.py"]

