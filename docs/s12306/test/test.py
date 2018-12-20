#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

import random

def random_int_by_raw(i):
    return str(i + random.randint(-5, 5))

def get_position_simple(index_str):
    """
        最简单的方式实现：
        把 8张图片的中心点，按顺序点击，然后进行提交，得到
        38,44,108,42,184,40,257,41,41,113,108,115,182,112,256,115

        根据输入的 字符串 类似 '63'， 需要得到对应的坐标串， 类似：'115,113,180,44'
    :param index_str:  下标的序号字符串
    :return:   坐标串
    """

    position_li = [[38,44],[108,42],[184,40],[257,41],[41,113],[108,115],[182,112],[256,115]]

    re_postion_li = []

    for s in index_str:
        # 下标需要减一
        index = int(s) - 1
        position = position_li[index]
        x = random_int_by_raw(position[0])
        y = random_int_by_raw(position[1])

        re_postion_li.append(x)
        re_postion_li.append(y)

    return ','.join(re_postion_li)


if __name__ == '__main__':
    # s = '12'
    # 得到 115,113,180,44
    # result = get_position_simple(s)
    # print(result)

    # print(str(random.random()))

    # seat_type = '无'
    # if seat_type != '' or seat_type != '无' or seat_type != '0':
    #     print('true')
    # else:
    #     print('false')

    from itertools import product, combinations

    li = ['a', 'b', 'c', 'd']
    r = product(li, repeat=3)
    print(list(r))

    r1 = combinations(li, 3)
    print(list(r1))
