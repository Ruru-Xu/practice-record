'''
清除单身的xml或者jpg
在Windows运行
'''
import os
import os.path

h = 0
a = ''
b = ''
dele = []
pathh = "D://workspace//darknet//train_images//"
#dele.remove(1)
for filenames in os.walk(pathh):
    filenames = list(filenames)
    filenames = filenames[2]
    for filename in filenames:

        print(filename)
        if h==0:
            a = filename
            h = 1
        elif h==1:
            #print(filename)
            b = filename
            if a[0:a.rfind('.', 1)]==b[0:b.rfind('.', 1)]:
                h = 0
                #print(filename)
            else:
                h = 1
                dele.append(a)
                a = b
        else:
            print("wa1")
print(dele)
for file in dele:
    os.remove(pathh+file)
    print("remove"+file+" is OK!")

#再循环一次看看有没有遗漏的单身文件
for filenames in os.walk(pathh):
    filenames = list(filenames)
    filenames = filenames[2]
    for filename in filenames:

        print(filename)
        if h==0:
            a = filename
            h = 1
        elif h==1:
            #print(filename)
            b = filename
            if a[0:a.rfind('.', 1)]==b[0:b.rfind('.', 1)]:
                h = 0
                #print(filename)
            else:
                h = 1
                dele.append(a)
                a = b
        else:
            print("wa1")
print (dele)