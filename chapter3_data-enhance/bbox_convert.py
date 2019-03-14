"""
数据增强之后转换对应的标注框
"""
import numpy as np
import cv2

def abbox_to_rebox(box, size):
    """
    把绝对坐标转成yolo的相对坐标
    Args:
        box: [xmin, ymin, xmax, ymax]
        size: (width, height)
    return:
        box: [x_center, y_center, width, height]
    """
    xmin = int(box[0])  # 左上角横坐标
    ymin = int(box[1])  # 左上角纵坐标
    xmax = int(box[2])  # 右下角横坐标
    ymax = int(box[3])  # 右下角纵坐标
    # 转成相对位置和宽高
    x_center = (xmin + xmax) / (2 * size[0])
    y_center = (ymin + ymax) / (2 * size[1])
    width = (xmax - xmin) / size[0]
    height = (ymax - ymin) / size[1]
    return [x_center, y_center, width, height]


def hor_flip_convert(box, size):
    """
    水平翻转
    Args:
        box: [xmin, ymin, xmax, ymax]
        size: (width, height)
    return:
        box: [xmin, ymin, xmax, ymax]
    """
    xmin = size[0] - int(box[2])  # 左上角横坐标
    ymin = int(box[1])  # 左上角纵坐标
    xmax = size[0] - int(box[0])  # 右下角横坐标
    ymax = int(box[3])  # 右下角纵坐标
    return [xmin, ymin, xmax, ymax]

def ver_flip_convert(box, size):
    """
    垂直翻转
    Args:
        box: [xmin, ymin, xmax, ymax]
        size: (width, height)
    return:
        box: [xmin, ymin, xmax, ymax]
    """
    xmin = int(box[0])  # 左上角横坐标
    ymin = size[1] - int(box[3])  # 左上角纵坐标
    xmax = int(box[2])  # 右下角横坐标
    ymax = size[1] - int(box[1])  # 右下角纵坐标
    return [xmin, ymin, xmax, ymax]

def hor_ver_flip_convert(box, size):
    """
    水平垂直翻转
    Args:
        box: [xmin, ymin, xmax, ymax]
        size: (width, height)
    return:
        box: [xmin, ymin, xmax, ymax]
    """
    xmin = size[0] - int(box[2])  # 左上角横坐标
    ymin = size[1] - int(box[3])  # 左上角纵坐标
    xmax = size[0] - int(box[0])  # 右下角横坐标
    ymax = size[1] - int(box[1])  # 右下角纵坐标
    return [xmin, ymin, xmax, ymax]

def rotate_convert(box, size, angle, scale=1.0):
    """
    旋转，目前只支持旋转90，180，270
    Args:
        box: [xmin, ymin, xmax, ymax]
        size: (width, height)
        angle: 度数
    return:
        box: [xmin, ymin, xmax, ymax]
    """
    box = [int(b) for b in box]
    (w, h) = size
    # 角度变弧度 
    rangle = np.deg2rad(angle) # angle in radians 
    # now calculate new image width and height 
    nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale 
    nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale

    # ask OpenCV for the rotation matrix 
    rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale) 
    # calculate the move from the old center to the new center combined with the rotation 
    rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))

    # the move only affects the translation, so update the translation part of the transform 
    rot_mat[0, 2] += rot_move[0] 
    rot_mat[1, 2] += rot_move[1]
    point1 = np.dot(rot_mat, np.array([(box[0]+box[2])/2, box[1], 1])) # 获取原始矩形的四个中点，然后将这四个点转换到旋转后的坐标系下 
    point2 = np.dot(rot_mat, np.array([box[2], (box[1]+box[3])/2, 1])) 
    point3 = np.dot(rot_mat, np.array([(box[0]+box[2])/2, box[3], 1])) 
    point4 = np.dot(rot_mat, np.array([box[0], (box[1]+box[3])/2, 1])) 
    concat = np.vstack((point1, point2, point3, point4)) # 合并np.array # 改变array类型 
    concat = concat.astype(np.int32) 
    xmin, ymin, rw, rh = cv2.boundingRect(concat) 
    xmax = xmin + rw
    ymax = ymin + rh
    return [xmin, ymin, xmax, ymax]


def center_crop_convert(box, margin):
    """
    随机中央裁剪
    Args:
        box:
        margin:
    """
    box = [(int(b)-margin) for b in box]
    return box
