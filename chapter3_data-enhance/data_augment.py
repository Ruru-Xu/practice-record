"""
数据增强
数据增强方法：
	直方图、水平翻转 垂直翻转 水平垂直翻转、高斯噪声、高斯模糊、旋转
"""

import os
import random
import cv2
import math
import numpy as np
from skimage import io
import skimage
from skimage.util import random_noise


def equalize_hist(image):
	"""
	直方图
	"""
	(b, g, r) = cv2.split(image)
	bH = cv2.equalizeHist(b)
	gH = cv2.equalizeHist(g)
	rH = cv2.equalizeHist(r)
	dealt_image = cv2.merge([bH,gH,rH])
	return dealt_image

def flip(image, f_t):
	"""
	水平翻转 垂直翻转 水平垂直翻转
	Args:
		image:
		f_t: h 、v or h_v
	return:
		dealt_image
	"""
	flip_type = {"h":1, "v":0, "h_v":-1}
	if f_t in flip_type:
		dealt_image = cv2.flip(image, flip_type[f_t])
	else:
		raise Exception("error type")
	return dealt_image


def add_Gaussian_noise(image, mode="localvar"):
	"""
	高斯噪声
	"""
	dealt_image = random_noise(image, mode, seed=None, clip=True)
	return dealt_image

def Gaussian_blur(image):
	"""
	高斯模糊
	"""
	kernel_size = (29,29)
	sigma = 5	
	dealt_image = cv2.GaussianBlur(image, kernel_size, sigma)
	return dealt_image

def rotate(image, angle, scale=1.0):
	"""
	旋转
	Args:
		image:
		angle: 旋转的角度
	return:
		dealt_image	
	"""
	(h, w) = image.shape[:2]
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

	dealt_image = cv2.warpAffine(image, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)
	return dealt_image

def smooth_filter(image):
	"""
	dst = cv.filter2D(src, ddepth, kernel[, dst[, anchor[, delta[, borderType]]]])
	src：输入图像
	ddepth：输出图像深度，-1为与原图相同
	kernel：卷积核
	anchor：锚点，默认为(-1, -1)，指卷积核的中心点
	delta：输出结果时的附加值，默认为0
	borderType：边界模式，默认为BORDER_DEFAULT

	"""
	fileter = random.choice([13, 15, 17])
	kernel=np.ones((fileter, fileter),np.float32)/(fileter*fileter) #29*29的均值滤波，值越大模糊效果越强
	return cv2.filter2D(image,-1,kernel)


def lower_brightness(image):
	"""
	亮度要随机变化
	"""
	kernel=np.ones((3,3),np.float32)/(5*5)  #相当于3*3做卷积，然后乘9/25可达到降低亮度的效果
	return cv2.filter2D(image,-1,kernel)

def center_crop(image, margin):
	"""
	随机中央裁剪
	Args:
		image:
		margin:
	return:
		dealt_image
	"""
	(h, w) = image.shape[:2]
	dealt_image = image[margin:h-margin, margin:w-margin, :]
	return dealt_image


# image_path = os.path.join("train_dataset", "000C7C0E.jpg")
# image = cv2.imread(image_path)

# image_sf = smooth_filter(image)
# cv2.imwrite("sf_29.jpg", image_sf)






