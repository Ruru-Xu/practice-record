"""
1 划分数据集为训练集和测试集
2 数据增强并转换对应的标签

增强方法：
	直方图 模糊 亮度调整 随机中央裁剪 旋转(90 180 270) 水平翻转 垂直翻转 水平垂直翻转 高斯噪声 高斯模糊 水平翻转_高斯模糊
	垂直翻转_高斯噪声 水平翻转_直方图 水平垂直翻转_直方图
"""
import os
import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import random
from skimage import io
import data_augment
import bbox_convert
import cv2
from tqdm import tqdm


dataset = "train_dataset"			# 数据集
train_images_dir = "train2017"	 # 训练集
train_labels_dir = "train_labels"	# 训练集标签
val_images_dir = "val2017"		 # 验证集
val_labels_dir = "val_labels"		# 验证集标签
train_label_csv = "train_labels.csv" 
class_name = "bar"					# 类名


def save_to_xml(xml_path, image_name, size, class_name, annot, func=None, random_margin=0):
	"""
	把box保存到xml
	Args:
		xml_path(str): xml路径
		image_name(str): 图片名
		size(): (width, height)
		class_name(str): 类名
		annot(numpy): 
		func(str): 转换函数
		random_margin(int): 随机中央裁剪
	"""
	with open(xml_path, "w") as xml_file:
		xml_file.write('<annotation>\n')
		xml_file.write('	<folder>VOC2007</folder>\n')
		xml_file.write('	<filename>' + image_name + '</filename>\n')
		xml_file.write('	<size>\n')
		xml_file.write('		<width>' + str(size[0]) + '</width>\n')
		xml_file.write('		<height>' + str(size[1]) + '</height>\n')
		xml_file.write('		<depth>3</depth>\n')
		xml_file.write('	</size>\n')

		for box in annot:
			box = box.split(' ')
			# if bbox_convert:
				# box = bbox_convert(box, size)
				#box = globals()[bbox_convert](box, size)
			if func == "hor_flip":
				box = bbox_convert.hor_flip_convert(box, size)
			elif func == "ver_flip":
				box = bbox_convert.ver_flip_convert(box, size)
			elif func == "hor_ver_flip":
				box = bbox_convert.hor_ver_flip_convert(box, size)
			elif func == "r_90":
				box = bbox_convert.rotate_convert(box, size, 90)
			elif func == "r_180":
				box = bbox_convert.rotate_convert(box, size, 180)
			elif func == "r_270":
				box = bbox_convert.rotate_convert(box, size, 270)
			elif func == "c_c":
				box = bbox_convert.center_crop_convert(box, random_margin)

			xml_file.write('	<object>\n')
			xml_file.write('		<name>' + class_name + '</name>\n')
			xml_file.write('		<pose>Unspecified</pose>\n')
			xml_file.write('		<truncated>0</truncated>\n')
			xml_file.write('		<difficult>0</difficult>\n')
			xml_file.write('		<bndbox>\n')
			xml_file.write('			<xmin>' + str(box[0]) + '</xmin>\n')
			xml_file.write('			<ymin>' + str(box[1]) + '</ymin>\n')
			xml_file.write('			<xmax>' + str(box[2]) + '</xmax>\n')
			xml_file.write('			<ymax>' + str(box[3]) + '</ymax>\n')
			xml_file.write('		</bndbox>\n')
			xml_file.write('	</object>\n')
		xml_file.write('</annotation>')

def train_time_augment(dataset, images_dir, images_list, labels_dir, train_label_csv, class_name):
	"""
	数据增强并对标注框进行转换
	Args:
		dataset:			数据集
		images_dir:			保存的图片目录
		images_dir:			需处理图片列表
		labels_dir:			保存的xml目录
		train_label_csv:	数据集对应的csv文件
		class_name:			类名
	"""
	if not os.path.exists(images_dir):
		os.makedirs(images_dir)
	if not os.path.exists(labels_dir):
		os.makedirs(labels_dir)
	annots = pd.read_csv(train_label_csv)
	for image_name in tqdm(images_list):
		image_path = os.path.join(dataset, image_name)
		# 读取图片
		image_np = cv2.imread(image_path)
		# 图片的宽 高
		size = (image_np.shape[1], image_np.shape[0])
		# 图片名称为1234.jpg	  图片的前缀为1234
		image_prefix = image_name.split('.')[0]
		annot = annots[annots["ID"] == image_name]["Detection"].values

		# 原始的图片
		image_ori_path = os.path.join(images_dir, "{}.jpg".format(image_prefix))
		cv2.imwrite(image_ori_path, image_np)
		ori_xml_path = os.path.join(labels_dir, "{}.xml".format(image_prefix))
		save_to_xml(ori_xml_path, image_name, size, class_name, annot, None)

		# 直方图
		image_eh = data_augment.equalize_hist(image_np)
		image_eh_path = os.path.join(images_dir, "{}_eh.jpg".format(image_prefix))
		cv2.imwrite(image_eh_path, image_eh)
		eh_xml_path = os.path.join(labels_dir, "{}_eh.xml".format(image_prefix))
		save_to_xml(eh_xml_path, image_name, size, class_name, annot, None)

		# 模糊
		image_sf = data_augment.smooth_filter(image_np)
		image_sf_path = os.path.join(images_dir, "{}_sf.jpg".format(image_prefix))
		cv2.imwrite(image_sf_path, image_sf)
		sf_xml_path = os.path.join(labels_dir, "{}_sf.xml".format(image_prefix))
		save_to_xml(sf_xml_path, image_name, size, class_name, annot, None)

		# 亮度调整
		image_lb = data_augment.lower_brightness(image_np)
		image_lb_path = os.path.join(images_dir, "{}_lb.jpg".format(image_prefix))
		cv2.imwrite(image_lb_path, image_lb)
		lb_xml_path = os.path.join(labels_dir, "{}_lb.xml".format(image_prefix))
		save_to_xml(lb_xml_path, image_name, size, class_name, annot, None)

		# 随机中央裁剪
		
		random_margin = random.randint(5, 20)
		box_out_of_range = False
		for box in annot: # 遍历检查坐标是否小于0
			box = box.split(" ")
			box = [int(x) for x in box]
			box_cc = bbox_convert.center_crop_convert(box, random_margin)
			if box_cc[0] < 0 or box_cc[1] < 0:
				box_out_of_range = True
				break
		if not box_out_of_range: #坐标不小于0才进行下面的操作
			image_cc = data_augment.center_crop(image_np, random_margin)
			image_cc_path = os.path.join(images_dir, "{}_cc.jpg".format(image_prefix))
			cv2.imwrite(image_cc_path, image_cc)
			cc_xml_path = os.path.join(labels_dir, "{}_cc.xml".format(image_prefix))
			save_to_xml(cc_xml_path, image_name, size, class_name, annot, "c_c", random_margin)

		# 旋转 90 180 270
		image_r_90 = data_augment.rotate(image_np, 90)
		image_r_90_path = os.path.join(images_dir, "{}_r_90.jpg".format(image_prefix))
		cv2.imwrite(image_r_90_path, image_r_90)
		r_90_xml_path = os.path.join(labels_dir, "{}_r_90.xml".format(image_prefix))
		save_to_xml(r_90_xml_path, image_name, size, class_name, annot, "r_90")

		image_r_180 = data_augment.rotate(image_np, 180)
		image_r_180_path = os.path.join(images_dir, "{}_r_180.jpg".format(image_prefix))
		cv2.imwrite(image_r_180_path, image_r_180)
		r_180_xml_path = os.path.join(labels_dir, "{}_r_180.xml".format(image_prefix))
		save_to_xml(r_180_xml_path, image_name, size, class_name, annot, "r_180")

		image_r_270 = data_augment.rotate(image_np, 270)
		image_r_270_path = os.path.join(images_dir, "{}_r_270.jpg".format(image_prefix))
		cv2.imwrite(image_r_270_path, image_r_270)
		r_270_xml_path = os.path.join(labels_dir, "{}_r_270.xml".format(image_prefix))
		save_to_xml(r_270_xml_path, image_name, size, class_name, annot, "r_270")

		# 水平翻转
		image_h = data_augment.flip(image_np, 'h')
		image_h_path = os.path.join(images_dir, "{}_h.jpg".format(image_prefix))
		cv2.imwrite(image_h_path, image_h)
		h_xml_path = os.path.join(labels_dir, "{}_h.xml".format(image_prefix))
		save_to_xml(h_xml_path, image_name, size, class_name, annot, "hor_flip")
		# 垂直翻转
		image_v = data_augment.flip(image_np, 'v')
		image_v_path = os.path.join(images_dir, "{}_v.jpg".format(image_prefix))
		cv2.imwrite(image_v_path, image_v)
		v_xml_path = os.path.join(labels_dir, "{}_v.xml".format(image_prefix))
		save_to_xml(v_xml_path, image_name, size, class_name, annot, "ver_flip")

		# 水平垂直翻转
		image_hv = data_augment.flip(image_np, 'h_v')
		image_hv_path = os.path.join(images_dir, "{}_hv.jpg".format(image_prefix))
		cv2.imwrite(image_hv_path, image_hv)
		hv_xml_path = os.path.join(labels_dir, "{}_hv.xml".format(image_prefix))
		save_to_xml(hv_xml_path, image_name, size, class_name, annot, "hor_ver_flip")

		# 高斯噪声
		image_gn = data_augment.add_Gaussian_noise(image_np)
		image_gn_path = os.path.join(images_dir, "{}_gn.jpg".format(image_prefix))
		io.imsave(image_gn_path, image_gn)
		gn_xml_path = os.path.join(labels_dir, "{}_gn.xml".format(image_prefix))
		save_to_xml(gn_xml_path, image_name, size, class_name, annot, None)
		# 高斯模糊
		image_gb = data_augment.Gaussian_blur(image_np)
		image_gb_path = os.path.join(images_dir, "{}_gb.jpg".format(image_prefix))
		cv2.imwrite(image_gb_path, image_gb)
		gb_xml_path = os.path.join(labels_dir, "{}_gb.xml".format(image_prefix))
		save_to_xml(gb_xml_path, image_name, size, class_name, annot, None)

		# 水平翻转 高斯模糊
		image_h_gb = data_augment.Gaussian_blur(image_h)
		image_h_gb_path = os.path.join(images_dir, "{}_h_gb.jpg".format(image_prefix))
		cv2.imwrite(image_h_gb_path, image_h_gb)
		h_gb_xml_path = os.path.join(labels_dir, "{}_h_gb.xml".format(image_prefix))
		save_to_xml(h_gb_xml_path, image_name, size, class_name, annot, "hor_flip")

		# 垂直翻转 高斯噪声
		image_v_gn = data_augment.add_Gaussian_noise(image_v)
		image_v_gn_path = os.path.join(images_dir, "{}_v_gn.jpg".format(image_prefix))
		io.imsave(image_v_gn_path, image_v_gn)
		v_gn_xml_path = os.path.join(labels_dir, "{}_v_gn.xml".format(image_prefix))
		save_to_xml(v_gn_xml_path, image_name, size, class_name, annot, "ver_flip")

		# 水平翻转 直方图
		image_h_eh = data_augment.equalize_hist(image_h)
		image_h_eh_path = os.path.join(images_dir, "{}_h_eh.jpg".format(image_prefix))
		cv2.imwrite(image_h_eh_path, image_h_eh)
		h_eh_xml_path = os.path.join(labels_dir, "{}_h_eh.xml".format(image_prefix))
		save_to_xml(h_eh_xml_path, image_name, size, class_name, annot, "hor_flip")

		# 水平垂直翻转 直方图
		image_hv_eh = data_augment.equalize_hist(image_hv)
		image_hv_eh_path = os.path.join(images_dir, "{}_hv_eh.jpg".format(image_prefix))
		cv2.imwrite(image_hv_eh_path, image_hv_eh)
		hv_eh_xml_path = os.path.join(labels_dir, "{}_hv_eh.xml".format(image_prefix))
		save_to_xml(hv_eh_xml_path, image_name, size, class_name, annot, "hor_ver_flip")


def main():
	annots = pd.read_csv(train_label_csv)
	images_list = annots['ID'].drop_duplicates().values
	# 划分训练集、验证集
	random_stat = 123
	np.random.seed(random_stat)
	train_list, val_list = train_test_split(images_list, test_size=0.1, random_state=random_stat)

	# 训练集
	train_time_augment(dataset, train_images_dir, train_list, train_labels_dir, train_label_csv, class_name)
	# 验证集
	train_time_augment(dataset, val_images_dir, val_list, val_labels_dir, train_label_csv, class_name)

main()



