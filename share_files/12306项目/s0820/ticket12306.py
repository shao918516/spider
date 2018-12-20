#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import random

def get_loc_by_seq(index):
    """
        根据若快返回的12306的验证码结果，生成对应 12306提交的坐标
    :param index:
    :return:
    """
    px = 67
    border = 4
    blank = 20

    y_seq, x_seq = divmod(index, 4)

    x = x_seq * (border + px) + random.randint(blank, px-blank)
    y = y_seq * (border + px) + random.randint(blank, px-blank)

    return x, y

def get_pos_by_img():
    im_li = [[37, 42], [109, 43], [181, 44], [257, 40], [35, 113], [110, 112], [183, 113], [262, 112]]
