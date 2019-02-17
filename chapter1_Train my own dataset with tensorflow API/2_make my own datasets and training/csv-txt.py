import csv
import os, sys
from glob import glob
from PIL import Image

src_img_dir = r'JPEJmages'
src_txt_dir = r'ImageSets'
src_xml_dir = r'Annotations'

img_lists = glob(src_img_dir + '/*jpg')
img_basenames = []
for item in img_lists:
    img_basenames.append(os.path.basename(item))

img_names = []
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    img_names.append(temp1)

c = []
filename = r'/home/imc/XR/anaconda3/lib/python3.6/site-packages/tensorflow/models/research/object_detection/my_game/dollar-game/data_dollar/train_labels.csv'
with open(filename) as f:
    reader = csv.reader(f)
    head_now = next(reader)
    l = []
    b = []
    for cow in reader:
        label = cow[0]
        l.append(label)
        bbox = cow[1]
        b.append(bbox)
label = []
for item in l:
    temp1, temp2 = os.path.splitext(item)
    label.append(temp1)

for img in img_names:
    img_file = src_txt_dir + os.sep + img + '.txt'
    fp = open(img_file, 'w')
    for i in range(len(label)):
        if label[i] == img:
            fp.write(str(b[i]))
            fp.write('\n')
