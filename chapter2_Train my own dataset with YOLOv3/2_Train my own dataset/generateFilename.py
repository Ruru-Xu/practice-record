
# -*- coding:utf-8 -*-
# 将一个文件夹下图片保存在txt文本
import sys
sys.path.append('/home/imc/XR/darknet/myTest/trainImage') 
import os
import random
img_dir = '/home/imc/XR/darknet/myTest/trainImage'
file_list = []
write_dir_name = '/home/imc/XR/darknet/myTest/trainImg_list.txt'  
write_file = open(write_dir_name, "w")
for file in os.listdir(img_dir):
  if file.endswith(".jpg"):
    write_name2 = file
    #write_name1 = write_name.split('.')
    #print(write_name1)
    #write_name2 = write_name1[0]
    #print(write_name2)
    file_list.append(write_name2)
    sorted(file_list)
num = len(file_list)
path = '/home/imc/XR/darknet/myTest/trainImage/'
for current_line in range(num):
    write_file.write(path + file_list[current_line] + '\n')

