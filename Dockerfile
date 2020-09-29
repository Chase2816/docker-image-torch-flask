# 基础镜像
FROM python:3.7

# 代码添加到code文件夹
ADD ./yolov5s /code

# 设置code文件夹为工作目录
WORKDIR /code

# 安装依赖支持
RUN apt-get update ##[edited]
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y

# pip freeze > requirements.txt
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

RUN pip install torch-1.6.0+cpu-cp37-cp37m-linux_x86_64.whl

RUN pip install torchvision-0.7.0+cpu-cp37-cp37m-linux_x86_64.whl

CMD ["python","app.py"]

