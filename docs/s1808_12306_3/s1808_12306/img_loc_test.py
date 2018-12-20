#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

__author__ = 'Terry'

def get_x_y_by_index_simple(index):
    """ 根据图片坐标，得到 x和y 的坐标值

    :param index:  图片的下标位置， 从 1到8
    :return:   图片对应的 x,y  坐标
    """
    x_y_li = [[40,37],[110,34],[186,35],[266,37],[41,115],[113,113],[192,112],[266,114]]

    # 对坐标进行随机变化
    x_y = x_y_li[index-1]
    x_y = [i+random.randint(-5, 5) for i in x_y]

    return x_y

def get_x_y_by_index(index):
    # 每个小图片的像素大小是 67*67的
    pix = 67
    # 2个图片之间的 间隔是 5
    blank = 5
    # 第一行图片距离顶部的位置
    top = 10

    # 转成整型，并且从 1到8 转为 0-7
    index = int(index) - 1

    x = (blank + pix//2) + (blank + pix)*(index % 4) + random.randint(-7, 7)
    y = (top + pix//2) + (blank + pix)*(index // 4) + random.randint(-7, 7)

    return x, y

def get_loc_by_vcode(vcode):
    """ 根据验证码的坐标位置，得到 坐标字符串

    :param vcode:  坐标位置字符串，譬如：'572'
    :return:  x、y坐标字符串，譬如： '41,115,192,112,110,34'
    """
    loc_li = []
    # 对字符串进行遍历
    for code in vcode:
        x, y = get_x_y_by_index(int(code))
        loc_li.append(str(x))
        loc_li.append(str(y))

    return ','.join(loc_li)

if __name__ == '__main__':
    # 40,111,189,109,118,39
    print(get_loc_by_vcode('572'))
    print(get_loc_by_vcode('572'))
    print(get_loc_by_vcode('572'))
    # print(random.randint(-5, 5))