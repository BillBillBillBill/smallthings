#!/usr/bin/env python
#coding: utf-8
import Image
import ImageDraw
import ImageFont
import ImageFilter
import string
import random


imgList = []
fontPath = "/usr/share/fonts/truetype/ttf-devanagari-fonts/"


# 获得随机四个字母
def getRandomChar():
    return [random.choice(string.letters) for _ in range(4)]


# 获得颜色
def getRandomColor():
    return (random.randint(30, 100), random.randint(30, 100), random.randint(30, 100))


# 获得验证码图片
def getCaptchaImage():
    global imgList
    width = 240
    height = 60
    # 创建画布
    image = Image.new('RGB', (width, height), (180, 180, 180))
    font = ImageFont.truetype(fontPath + 'kalimati.ttf', 40)
    draw = ImageDraw.Draw(image)
    # 创建验证码对象
    Captcha = getRandomChar()
    # 把验证码放到画布上
    for t in range(4):
        draw.text((60 * t + 10, 0), Captcha[t], font=font, fill=getRandomColor())
    # 填充噪点
    for _ in range(random.randint(1500, 3000)):
        draw.point((random.randint(0, width), random.randint(0, height)), fill=getRandomColor())
    # 填充线条
    for _ in range(5):
        draw.line([(random.randint(0, width), random.randint(0, height)), (random.randint(0, width), random.randint(0, height))], fill=getRandomColor(), width=random.randint(1,3))
    # 模糊处理
    image = image.filter(ImageFilter.BLUR)
    # 扭曲图像
    # 新图片
    newImage = Image.new('RGB', (width, height), (180, 180, 180))
    # load像素
    newPix = newImage.load()
    pix = image.load()
    offset = 0
    for y in range(0, height):
        offset = random.randint(-1,1)
        for x in range(0, width):
            # 新的x坐标点
            newx = x + offset
            if 0 < newx < width:
                # 把源像素通过偏移到新的像素点
                newPix[newx, y] = pix[x, y]
    # 保存名字为验证码的值图片
    CaptchaValue = "".join(Captcha).lower()
    CaptchaImgName = CaptchaValue + '.jpg'
    imgList.append(CaptchaImgName)
    newImage.save(CaptchaImgName, 'jpeg')

if __name__ == '__main__':
    # 生成十张验证码图片
    for _ in xrange(10):
        getCaptchaImage()
    print imgList
