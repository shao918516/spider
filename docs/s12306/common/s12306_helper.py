#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

__author__ = 'Terry'

import random

def random_int_by_raw(i):
    return str(i + random.randint(-5, 5))

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

def date_format_12306_getQueueCount(date_str):
    """
        转化日期函数
    :param date_str:   类似：2018-10-16
    :return:  类似：Tue Oct 16 2018 00:00:00 GMT+0800 (中国标准时间)
    """
    return time.strftime('%a %b %d %Y', time.strptime(date_str, '%Y-%m-%d')) + ' 00:00:00 GMT+0800 (中国标准时间)'


if __name__ == '__main__':
    print(get_position_simple('13'))