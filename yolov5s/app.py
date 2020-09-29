import io
import json

from torchvision import models
import torchvision.transforms as transforms
from PIL import Image,ImageDraw

from utils.general import non_max_suppression
from models.experimental import attempt_load

from flask import Flask, jsonify, request
app = Flask(__name__)

model = attempt_load("weights/yolov5s.pt")  # load FP32 model
model.eval()

names= ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        'hair drier', 'toothbrush']

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize((512,640)),
                                        transforms.ToTensor(),
                                        ])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image)

def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model(tensor[None])[0]
    print(outputs)
    outputs = non_max_suppression(outputs,0.3,0.5)
    boxs = outputs[0]
    print(boxs[0])
    print(int(boxs[0][-1].item()))
    class_name = names[int(boxs[0][5].item())]
    print(boxs.shape)
    boxes = []
    for i in range(boxs.shape[0]):
        boxes.append([boxs[i][0].item(),boxs[i][1].item(),boxs[i][2].item(),boxs[i][3].item(),boxs[i][4].item(),boxs[i][5].item()])

    return boxes

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        boxes = get_prediction(image_bytes=img_bytes)
        return ({'boxes': boxes})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
