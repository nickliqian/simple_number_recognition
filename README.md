# simple_number_recognition
使用PIL和几种分类算法对标准数字图片进行识别。

## 背景
在采集某个免费代理网站的时候，遇到比较复杂的html代码。
考虑到我需要采集的是 数字+点号+冒号，并且都是同一种标准字体。
就试着使用ocr来识别。

## 如何实现
1. 使用selenium+phantomjs采集web页面，并且截图储存到本地。
2. 使用Photoshop分析页面尺寸，用PIL裁剪需要识别的位置为若干张小图到本地。
3. 使用tesseract或者空间向量算法识别图像。

## 识别方法详解
##### Tesseract
1. 安装Tesseract-OCR--图像识别引擎
2. 安装jTessBoxEditorFX--训练图像识别数据的工具
3. `pip install pytesseract`--python与交互Tesseract-OCR的包
4. 使用`image_to_string`识别图片，`lang='num'`是自己根据目标图片训练的数据名称
```
import pytesseract  
from PIL import Image
im = Image.open(image_name)
text = pytesseract.image_to_string(im, lang='num')
```

##### 空间向量算法
1. 原理：首先有一组单个字符图片集，并已标注数值
2. 将此图片集转换为空间向量集形式
3. 对于需要识别的图片，先进行图片分割，分割成若干个单个字符图片
4. 把未知图片转为空间向量形式
5. 计算未知图片向量与训练集中每个图片向量的cos夹角，cos值越大说明图片重合度越高。

## 使用此项目
######1. catchCropImg 
是从某个网站采集web页面，并且分割为标准大小的例子
######2. get_useragent
每次访问使用随机浏览器代理
######3. tessCheckFunc
调用tesseract识别图片 `ip_list = ocr_ip_http(filename_list)`
######4. vectCheckFunc
生成训练集，设置训练集的目标图片开始识别图片
```
1. 生成图片训练集
origin_img_dir = 标注好的素材图片文件夹 'markImage'
trained_img_dir = 输出的分类父文件夹训练集 'trainedImage'
get_img_train_set(origin_img_dir, trained_img_dir)

2. 已有图片训练集，识别目标图片
trained_img_dir = 训练集图片文件夹 'trainedImage'
sample_name = 目标图片文件名称
text = check_sample(sample_name, trained_img_dir)
```

######5. main —— 使用以上函数的例子


## 注意
1. 图片分割算法目前较为简陋，对于有粘黏和有干扰的字符暂不可用。
2. 如果字体变化多样，则需要扩展更大的训练集。
