import xml.etree.ElementTree as ET
import xml.dom.minidom as DOC
import os

def parse_xml(xml_path):
    '''
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 格式为[[x_min, y_min, x_max, y_max, name]]
    '''
    tree = ET.parse(xml_path)
    root = tree.getroot()
    objs = root.findall('object')
    coords = list()
    for ix, obj in enumerate(objs):
        name = obj.find('name').text
        box = obj.find('bndbox')
        x_min = int(box[0].text)
        y_min = int(box[1].text)
        x_max = int(box[2].text)
        y_max = int(box[3].text)
        coords.append([x_min, y_min, x_max, y_max, name])
    return coords

# voc_path = r"F:\data\boat1215/"
voc_path = r"F:\data\M300_opt_0104/"
image_ids = os.listdir(voc_path+"outputs")

a = []
for i in image_ids:
    print(voc_path+i)
    coords = parse_xml(voc_path+"outputs/"+i)
    print(coords,len(coords))

    if len(coords) == 0:
        a.append(i)

print(a)
print(len(a))
#
for j in a:
    print(j)
    s = j.split(".")[0]
    print(s)
    os.remove(voc_path+"outputs/"+j)
    os.remove(voc_path+"images/"+s+".jpg")

