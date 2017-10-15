import pytesseract
from PIL import Image


# 使用tesseract引擎识别图片，返回列表
# (\d+.\d+.\d+.\d+:\d+).*  '\1',
def ocr_ip_http(filename_list):
	ip_list = []
	print('正在调用tesseract引擎...')
	for name in filename_list:
		image = Image.open(name)
		text = pytesseract.image_to_string(image, lang='num')
		proxies = text.replace(' ','')
		# proxies = {'http': 'http://' + text}
		ip_list.append(proxies)
	print('返回一组结果')
	return ip_list