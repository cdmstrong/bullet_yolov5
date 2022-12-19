import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil
#VOC生成txt的文件

sets = ['trainval', 'test'] #数据集，最后会生成以这三个数据集命名的txt文件

classes = ['bullet'] #标签名，注意一定不要出错


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open('./VOC2007/annotations/%s.xml' % (image_id), 'r', encoding="UTF-8")
    out_file = open('./VOC2007/labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


for image_set in sets:
    if not os.path.exists('./VOC2007/labels/'): #创建label文件夹
        os.makedirs('./VOC2007/labels/')
    image_ids = open('./VOC2007/ImageSets/Main/%s.txt' % (image_set)).read().strip().split()
    list_file = open('./VOC2007/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write('F:\python\yolov5\VOC2007/images/%s.JPG\n' % (image_id)) #这里最好用全局路径
        convert_annotation(image_id)
    list_file.close()

