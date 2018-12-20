#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

__author__ = 'Terry'

from PIL import Image as image
import re
import io
from urllib.request import urlopen


def get_merge_image(file, location_list):
    """
    根据位置对图片进行合并还原
    :file:图片
    :location_list:图片位置
    """

    # 用image加载图片
    im = image.open(file)

    im_list_upper=[]
    im_list_down=[]

    # 根据52个div的x和y坐标，进行循环，把打乱了的图切割成52个小图片
    for location in location_list:
        if location['y'] == -58:
            # 宽度必须为10，  修改为12的话，会有干扰空隙，可以保存图片查看区别
            im_list_upper.append(im.crop((abs(location['x']), 58, abs(location['x']) + 10, 116)))
        elif location['y'] == 0:
            im_list_down.append(im.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))

    # 建立一个新的图片
    new_im = image.new('RGB', (260, 116))

    x_offset = 0
    # 根据下图片列表，把小图片按照 x和y坐标，粘贴到 new_im
    for im in im_list_upper:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    x_offset = 0
    # 根据下图片列表，把小图片按照 x和y坐标，粘贴到 new_im
    for im in im_list_down:
        new_im.paste(im, (x_offset, 58))
        x_offset += im.size[0]

    # new_im.save(str(time.time())+".jpg")
    return new_im


def get_image(driver, div_xpath):
    """
    下载并还原图片
    :driver:webdriver
    :div:图片的div
    """

    background_image_divs = []
    #找到图片所在的div
    for _ in range(5):
        # 使用的 find_elements_by_xpath , elements是有 s的，复数的div
        background_image_divs = driver.find_elements_by_xpath(div_xpath)

        if background_image_divs:
            break
        else:
            time.sleep(.5)

    # 正则匹配 打乱了的图片的 url
    mathes = re.findall("background-image: url\(\"(.*)\"\);", background_image_divs[0].get_attribute('style'))
    imageurl = mathes[0]
    # 替换图片的后缀, ca58e81a.webp 变为 ca58e81a.jpg
    # imageurl = imageurl.replace("webp", "jpg")

    location_list = []
    # 遍历52个DIV，获取它们的 position
    for background_image in background_image_divs:
        location={}

        #得出每个div的 x 和 y 坐标
        mathes = re.findall(r"background-position: (.*)px (.*)px;", background_image.get_attribute('style'))
        location['x']=int(mathes[0][0])
        location['y']=int(mathes[0][1])

        location_list.append(location)

    # 访问网络，得到图片
    jpg_file = io.BytesIO(urlopen(imageurl).read())

    #重新合并图片
    image = restore_img(jpg_file, location_list)

    return image


def is_similar(image1, image2, x, y):
    """
        对比RGB值
    """

    # 获得图片指定x和y的像素的 (r,g,b)
    pixel1 = image1.getpixel((x, y))
    pixel2 = image2.getpixel((x, y))

    for i in range(0, 3):
        if abs(pixel1[i] - pixel2[i]) >= 30:
            return False

    return True

def get_diff_location(image1, image2):
    """
    计算缺口的位置
    """
    for x in range(80, 260):
        for y in range(20, 116):
            if not is_similar(image1, image2, x, y):
                return x

def test_get_img():
    url = 'https://static.geetest.com/pictures/gt/0f340b2ba/0f340b2ba.webp'
    file = io.BytesIO(urlopen(url).read())
    im = image.open(file)

    return im

def restore_img(im_file, position_li):
    """
            x = -157

            x_index = (x + 1) /12 = 13
            第一张图片是：
            (0, 0, 12, 58)
            第 13 张图片的 2个 x是什么？
            (156, 0, 168, 58)

        """
    old_im = image.open(im_file)
    new_im = image.new('RGB', (260, 116))

    for i, position in enumerate(position_li):
        index = i % 26

        x = abs(position['x'])
        y = abs(position['y'])
        cut_im = old_im.crop((x - 1, y, x + 11, y + 58))

        new_im.paste(cut_im, (index * 10, abs(y - 58)))

    # new_im.save('new_test2.jpg')
    return new_im

if __name__ == '__main__':
    """
        x = -157
        
        x_index = (x + 1) /12 = 13 
        第一张图片是：
        (0, 0, 12, 58)
        第 13 张图片的 2个 x是什么？
        (156, 0, 168, 58)
        
    """

    im = test_get_img()
    im.save('old_full.jpg')
    new_im = image.new('RGB', (260, 116))
    # new_im = image.new('RGB', (312, 116))
    position_li = [{'x': -157, 'y': -58}, {'x': -145, 'y': -58}, {'x': -265, 'y': -58}, {'x': -277, 'y': -58},
                   {'x': -181, 'y': -58}, {'x': -169, 'y': -58}, {'x': -241, 'y': -58}, {'x': -253, 'y': -58},
                   {'x': -109, 'y': -58}, {'x': -97, 'y': -58}, {'x': -289, 'y': -58}, {'x': -301, 'y': -58},
                   {'x': -85, 'y': -58}, {'x': -73, 'y': -58}, {'x': -25, 'y': -58}, {'x': -37, 'y': -58},
                   {'x': -13, 'y': -58}, {'x': -1, 'y': -58}, {'x': -121, 'y': -58}, {'x': -133, 'y': -58},
                   {'x': -61, 'y': -58}, {'x': -49, 'y': -58}, {'x': -217, 'y': -58}, {'x': -229, 'y': -58},
                   {'x': -205, 'y': -58}, {'x': -193, 'y': -58}, {'x': -145, 'y': 0}, {'x': -157, 'y': 0},
                   {'x': -277, 'y': 0}, {'x': -265, 'y': 0}, {'x': -169, 'y': 0}, {'x': -181, 'y': 0},
                   {'x': -253, 'y': 0}, {'x': -241, 'y': 0}, {'x': -97, 'y': 0}, {'x': -109, 'y': 0},
                   {'x': -301, 'y': 0}, {'x': -289, 'y': 0}, {'x': -73, 'y': 0}, {'x': -85, 'y': 0}, {'x': -37, 'y': 0},
                   {'x': -25, 'y': 0}, {'x': -1, 'y': 0}, {'x': -13, 'y': 0}, {'x': -133, 'y': 0}, {'x': -121, 'y': 0},
                   {'x': -49, 'y': 0}, {'x': -61, 'y': 0}, {'x': -229, 'y': 0}, {'x': -217, 'y': 0},
                   {'x': -193, 'y': 0}, {'x': -205, 'y': 0}]

    for i, position in enumerate(position_li):
        index = i % 26

        x = abs(position['x'])
        y = abs(position['y'])
        # 从错乱的图片中截取指定坐标的图片
        cut_im = im.crop((x-1, y, x+11, y + 58))
        # cut_im.save(f'{i}.jpg')
        # 将截取的图片  粘贴到 新的图片对象上
        new_im.paste(cut_im, (index * 10, abs(y-58)))

    new_im.save('new_full.jpg')