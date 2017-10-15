from PIL import Image
import os
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from get_useragent import get_useragent


# 使用phantomjs请求页面，并且截图 指定名称 'page_img.png'
def request_web(url):
	phan = dict(DesiredCapabilities.PHANTOMJS)
	phan["phantomjs.page.settings.loadImages"] = False
	phan["phantomjs.page.settings.userAgent"] = (get_useragent())
	driver = webdriver.PhantomJS(r"D:\A\phantomjs-2.1.1-windows\bin\phantomjs.exe",desired_capabilities=phan)
	print('正在访问url...')
	driver.get(url)
	print('正在储存图片...')
	driver.save_screenshot('page_img.png')


# 使用Photoshop分析图片尺寸，并切割为指定大小，名称列表。需要输入储存文件的路径。
def corp_img(filepath):
	im = Image.open('page_img.png')
	w, h = im.size
	area = (0,362,w,h)
	im2 = im.crop(area)
	im2.save('page_img_crop.png')
	filename_list = []
	print('正在切割图片...')
	for i in range(15):
		area = (41,39*i,256,39*(i+1))
		newim = im2.crop(area)
		fileneme = 'part-'+str(i+1)+'.png'
		fileneme = os.path.join(filepath, fileneme)
		newim.save(fileneme)
		filename_list.append(fileneme)
	return filename_list