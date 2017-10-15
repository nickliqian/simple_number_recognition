from numCheckFunc import *
from catchCropImg import *
from tessCheckFunc import *

def mainTessCheck():
	# 获取要识别的页面
	url = 'http://www.goubanjia.com/free/type/http/index1.shtml'
	request_web(url)

	# 给页面上要识别的数字分区域-切割,并存到unknowImage文件夹
	filename_list = corp_img('unknowImage')

	# 识别每个区域的数字
	ip_list = ocr_ip_http(filename_list)
	print(all_ip)


def mainVectCheck():
	# 获取要识别的页面
	url = 'http://www.goubanjia.com/free/type/http/index1.shtml'
	request_web(url)

	# 给页面上要识别的数字分区域-切割,并存到unknowImage文件夹
	filename_list = corp_img('unknowImage')

	# 指定文件和训练集路径开始识别
	for name in filename_list:
		trained_img_dir = 'trainedImage'
		sample_name = name
		text = check_sample(sample_name, trained_img_dir)
		text = text.replace('x','.').replace('p',':')
		print(text)


def get_trained_dir():
	origin_img_dir = 'markImage/'
	trained_img_dir = 'te'
	get_img_train_set(origin_img_dir, trained_img_dir)


if __name__ == '__main__':
	mainVectCheck()