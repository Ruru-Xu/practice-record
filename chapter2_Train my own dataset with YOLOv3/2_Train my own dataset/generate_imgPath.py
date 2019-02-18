# -*- coding: utf-8 -*-
import os
import os.path

pathh = "D:/workspace/darknet/train_images/"

for filenames in os.walk(pathh):
    filenames = list(filenames)
    filenames = filenames[2]
    for filename in filenames:
        print(filename)
        with open ("t.txt",'a') as f:
            f.write(pathh+filename+'\n')