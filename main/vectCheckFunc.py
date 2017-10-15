'''
	针对标准字体的识别封装
	使用方法
	1. 生成图片训练集
	origin_img_dir = 标注好的素材图片文件夹
	trained_img_dir = 输出的分类父文件夹训练集
	get_img_train_set(origin_img_dir, trained_img_dir)

	2. 已有图片训练集，识别目标图片
	trained_img_dir = 训练集图片文件夹
	sample_name = 目标图片文件
	text = check_sample(sample_name, trained_img_dir)
'''

from PIL import Image
import os
import time
import math


# 二值化，返回im对象，可以指定二值化的临界值，也可以指定二值化为(0,1)或者(0,255)
def get_two_value(im, limit_value=140, col=255):
	im = im.convert('L')
	threshold = limit_value
	table = []
	for i in range(256):
		if i < threshold:
			table.append(0)
		else:
			table.append(col)
	im = im.point(table,'1')
	return im


# 分隔图片的单个字符，返回x方向的分割坐标
def crop_loc(im):
	inletter = False
	foundletter = False
	start = 0
	end = 0
	lettersx = []#用来记录每个数字的起始位置
	# 这两个循环就是遍历每个像素点
	# x,y w,h  x = w, y = h
	for x in range(im.size[0]):
		for y in range(im.size[1]):
			# 获取每个点的值（0，255）
			pix = im.getpixel((x, y))
			# 当遇到黑色的时候，记录一下，说明以及接触到了数字
			if pix != 255:
				inletter = True#如果不是白色，这说明已经开始接触到数字了
		# 如果接触到了数字，就标记这一行为start
		if foundletter == False and inletter == True:
			foundletter = True
			start = x#数字的起始坐标
		# 如果这一行没有接触到数字但是之前有接触到过数字，就记录这上一行的位置
		if foundletter == True and inletter == False:
			foundletter = False
			end = x-1#数字的结束位置
			if start == end:
				start, end = start-1, start+1
			lettersx.append((start, end))
		inletter = False
	return lettersx


# 按照指定坐标x_loc分割图片为多个im对象，返回对象集
def crop_img_list(im, x_loc, string=None):
	i = 0
	imlist = []
	for each in x_loc:
		region = (each[0],0,each[1],im.size[1])
		newim = im.crop(region)
		imlist.append(newim)
		i += 1
	return imlist


# 把一个切割后的im对象集，按照标注好的文件名称，保存到指定训练集。注意filename中不能含有额外的点，可以使用别的字符代替。
def save_crop(imlist, filename, target_dir='new', ex_size=None):
	values = filename.split('.')[0]
	if not os.path.exists(target_dir):
		os.mkdir(target_dir)
	i = 0
	for newim in imlist:
		if ex_size != None:
			newim = get_new_img(newim, ex_size)
			newim = get_two_value(newim)
		dirname = os.path.join(target_dir, values[i])
		if not os.path.exists(dirname):
			os.mkdir(dirname)
		timename = str(time.time()).replace('.','')
		newname = timename + '-' + filename
		newfile = os.path.join(dirname, newname)
		newim.save(newfile)
		i += 1

# 夹角公式
class VectorCompare(object):
	# 计算矢量大小 计算平方和
	def magnitude(self, concordance):
		total = 0
		for word, count in concordance.items():
			total += count ** 2
		return math.sqrt(total)

	# 计算矢量之间的 cos 值
	def relation(self, concordance1, concordance2):
		topvalue = 0
		for word, count in concordance1.items():
			if word in concordance2:
				# 计算相乘的和
				topvalue += count * concordance2[word]
		return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


# 图片转向量
def buildvector(im):
	d1 = {}
	count = 0
	for i in im.getdata():
		d1[count] = i
		count += 1
	return d1


# 生成向量训练集
def Vector_train(BASEDIR):
	train_list = os.listdir(BASEDIR)
	imageset = []
	for d in train_list:
		dir_name = os.path.join(BASEDIR, d)
		file_list = os.listdir(dir_name)
		for f in file_list:
			train_vect = []
			filename = os.path.join(dir_name, f)
			train_vect.append(buildvector(Image.open(BASEDIR+"/%s/%s" % (d, f))))
			imageset.append({d: train_vect})
	# imageset = [{d: train_vect},{d: train_vect},{d: train_vect}...]
	return imageset


# 目标向量拿到训练集里面逐个对比向量夹角
def confirm_im(im, imageset, k):
	guess = []
	v = VectorCompare()
	
	for image in imageset:
		for value, vect in image.items():
			if len(vect) != 0:
				cos = (v.relation(vect[0], buildvector(im)))
				guess.append((cos, value))
				# 夹角值 和 对比的值 放入元组 (cos, value), 然后加入guess列表 [(cos, value),(cos, value),(cos, value)...]
	guess.sort(reverse=True)
	for cos, value in guess[:k]:
		# print('检验对象与值 %s 的cos夹角为 %.3f'%(value, cos))
		pass
	return value


# 根据已经标注好的样本，输出训练集图片
def get_img_train_set(source_dir, output_dir):
	train_list = os.listdir(source_dir)
	for name in train_list:
		file_path = os.path.join(source_dir, name)
		im = Image.open(file_path)
		im = get_two_value(im)
		x_loc = crop_loc(im)
		imlist = crop_img_list(im, x_loc, string=None)
		save_crop(imlist, name, target_dir=output_dir)


# 使用已经有的图片训练集去识别目标
def check_sample(sample_name, train_dir):
	im = Image.open(sample_name)
	im = get_two_value(im)
	x_loc = crop_loc(im)
	imlist = crop_img_list(im, x_loc)
	imageset = Vector_train(train_dir)
	text = ''
	for im in imlist:
		value = confirm_im(im, imageset, 1)
		text += value
	print('识别完成：按照规则图片对应的文本是%s'%text)
	return text


if __name__ == '__main__':
	trained_img_dir = 'trainedImage/'
	sample_name = 'markImage/110x170x150x215p8080.png'
	text = check_sample(sample_name, trained_img_dir)